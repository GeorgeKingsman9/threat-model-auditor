"""Exercise inference guards and response parsing with a mocked network only."""

import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import urllib.error


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from providers import BudgetExceeded, ModelClient


SCHEMA = {"type": "object", "properties": {}, "required": [], "additionalProperties": False}


class ProviderTests(unittest.TestCase):
    def setUp(self):
        # Even an accidental generate() in a test cannot reach a real provider.
        self.network = patch("providers.urllib.request.urlopen")
        self.urlopen = self.network.start()
        self.addCleanup(self.network.stop)
        environment = patch.dict("os.environ", {
            "OPENAI_API_KEY": "fixture-openai-key-never-real",
            "ANTHROPIC_API_KEY": "fixture-anthropic-key-never-real",
        }, clear=True)
        environment.start()
        self.addCleanup(environment.stop)

    def client(self, **overrides):
        options = dict(provider="openai", model="fixture-model", max_cost_usd=1.0,
                       input_price=1.0, output_price=2.0, max_output_tokens=100,
                       max_calls=2, allow_api=True)
        options.update(overrides)
        return ModelClient(**options)

    def response(self, **overrides):
        response = {
            "id": "fixture-response", "status": "completed",
            "usage": {"input_tokens": 50, "output_tokens": 10},
            "output": [{"type": "message", "content": [{"type": "output_text", "text": "{}"}]}],
        }
        response.update(overrides)
        self.urlopen.return_value = io.BytesIO(json.dumps(response).encode())

    def test_explicit_api_authorization_is_required(self):
        with self.assertRaisesRegex(ValueError, "requires --allow-api"):
            self.client(allow_api=False)
        self.urlopen.assert_not_called()

    def test_budget_and_prices_must_be_positive_finite_numbers(self):
        for field in ("max_cost_usd", "input_price", "output_price"):
            for invalid in (0, -1, float("nan"), float("inf"), -float("inf"), True, None):
                with self.subTest(field=field, invalid=invalid):
                    with self.assertRaises(ValueError):
                        self.client(**{field: invalid})
        self.urlopen.assert_not_called()

    def test_call_and_output_limits_must_be_positive_integers(self):
        for field in ("max_calls", "max_output_tokens"):
            for invalid in (0, -1, 1.5, True, None):
                with self.subTest(field=field, invalid=invalid):
                    with self.assertRaises(ValueError):
                        self.client(**{field: invalid})
        self.urlopen.assert_not_called()

    def test_missing_key_does_not_dispatch_or_charge(self):
        client = self.client()
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(ValueError, "not configured"):
                client.generate("instruction", {"text": "fixture"}, SCHEMA)
        self.assertEqual(client.ledger()["calls"], [])
        self.assertEqual(client.ledger()["charged_or_reserved_usd"], 0)
        self.urlopen.assert_not_called()

    def test_reservation_is_checked_before_dispatch(self):
        client = self.client(max_cost_usd=0.000001)
        with self.assertRaises(BudgetExceeded):
            client.generate("instruction", {"text": "fixture"}, SCHEMA)
        self.assertEqual(client.ledger()["calls"], [])
        self.urlopen.assert_not_called()

    def test_openai_parsing_records_usage_and_never_records_credentials(self):
        client = self.client()
        self.response()
        self.assertEqual(client.generate("instruction", {"text": "fixture"}, SCHEMA), {})
        self.urlopen.assert_called_once()
        ledger = client.ledger()
        self.assertEqual(len(ledger["calls"]), 1)
        self.assertEqual(ledger["calls"][0]["status"], "received")
        self.assertAlmostEqual(ledger["charged_or_reserved_usd"], 0.00007)
        self.assertNotIn("fixture-openai-key-never-real", json.dumps(ledger))
        request = self.urlopen.call_args.args[0]
        payload = json.loads(request.data)
        self.assertEqual(payload["model"], "fixture-model")
        self.assertIs(payload["store"], False)

    def test_anthropic_forced_tool_output_is_parsed(self):
        self.urlopen.return_value = io.BytesIO(json.dumps({
            "id": "fixture-anthropic-response", "stop_reason": "tool_use",
            "usage": {"input_tokens": 50, "output_tokens": 10},
            "content": [{"type": "tool_use", "name": "emit_audit", "input": {}}],
        }).encode())
        client = self.client(provider="anthropic")
        self.assertEqual(client.generate("instruction", {"text": "fixture"}, SCHEMA), {})
        payload = json.loads(self.urlopen.call_args.args[0].data)
        self.assertEqual(payload["tool_choice"], {"type": "tool", "name": "emit_audit"})
        self.assertEqual(len(client.ledger()["calls"]), 1)

    def test_call_limit_blocks_a_second_request(self):
        client = self.client(max_calls=1)
        self.response()
        client.generate("instruction", {"text": "fixture"}, SCHEMA)
        with self.assertRaises(BudgetExceeded):
            client.generate("instruction", {"text": "fixture"}, SCHEMA)
        self.urlopen.assert_called_once()

    def test_transport_failure_retains_reservation_and_does_not_retry(self):
        client = self.client()
        self.urlopen.side_effect = OSError("fixture transport failure")
        with self.assertRaisesRegex(ValueError, "no retry attempted"):
            client.generate("instruction", {"text": "fixture"}, SCHEMA)
        self.urlopen.assert_called_once()
        ledger = client.ledger()
        self.assertEqual(ledger["calls"][0]["status"], "transport_or_response_error")
        self.assertGreater(ledger["charged_or_reserved_usd"], 0)

    def test_http_error_does_not_expose_provider_body_or_credentials(self):
        client = self.client()
        self.urlopen.side_effect = urllib.error.HTTPError(
            "https://example.org", 401, "fixture", {}, io.BytesIO(b"private-provider-body"),
        )
        with self.assertRaises(ValueError) as raised:
            client.generate("instruction", {"text": "fixture"}, SCHEMA)
        self.assertIn("HTTP 401", str(raised.exception))
        self.assertNotIn("private-provider-body", str(raised.exception))
        self.assertNotIn("fixture-openai-key", str(raised.exception))
        self.urlopen.assert_called_once()
        self.assertEqual(client.ledger()["calls"][0]["status"], "http_error")

    def test_incomplete_output_is_not_a_verdict_and_is_not_retried(self):
        client = self.client()
        self.response(status="incomplete")
        with self.assertRaisesRegex(ValueError, "incomplete or refused"):
            client.generate("instruction", {"text": "fixture"}, SCHEMA)
        self.urlopen.assert_called_once()
        self.assertEqual(len(client.ledger()["calls"]), 1)
        self.assertGreater(client.ledger()["charged_or_reserved_usd"], 0)

    def test_multiple_structured_outputs_are_rejected(self):
        client = self.client()
        self.response(output=[{"content": [
            {"type": "output_text", "text": "{}"},
            {"type": "output_text", "text": "{}"},
        ]}])
        with self.assertRaisesRegex(ValueError, "exactly one"):
            client.generate("instruction", {"text": "fixture"}, SCHEMA)
        self.urlopen.assert_called_once()


if __name__ == "__main__":
    unittest.main()
