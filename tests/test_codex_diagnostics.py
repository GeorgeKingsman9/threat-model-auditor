"""Safe diagnosis keeps failure identity without copying arbitrary CLI prose."""

import hashlib
import json
import subprocess
import unittest
from unittest.mock import patch

from codex_provider import CodexClient, diagnostic_summary
import test_codex_provider as original


class CodexDiagnosticTests(unittest.TestCase):
    setUp = original.CodexProviderTests.setUp
    fake_run = original.CodexProviderTests.fake_run
    event_run = original.CodexProviderTests.event_run

    def test_structured_status_and_message_hash_survive_without_raw_message(self):
        message = "HTTP/1.1 429 rate limit: Authorization Bearer PRIVATE_SECRET"
        event = {"type": "turn.failed", "error": {"code": "rate_limit_exceeded", "status_code": 429,
                                                    "message": message}}
        result = diagnostic_summary(event)
        self.assertEqual(result["http_statuses"], [429])
        self.assertEqual(result["category"], "account_limit_or_quota")
        self.assertEqual(result["message_sha256"], hashlib.sha256(message.encode()).hexdigest())
        self.assertEqual(result["message_characters"], len(message))
        self.assertTrue(result["structure"]["has_error_object"])
        self.assertNotIn("PRIVATE_SECRET", json.dumps(result))
        self.assertNotIn("Bearer", json.dumps(result))

    def test_structured_service_status_without_message_still_classifies(self):
        result = diagnostic_summary({"type": "turn.failed", "error": {"http_status": 503}})
        self.assertEqual(result["category"], "service_error")
        self.assertEqual(result["http_statuses"], [503])
        self.assertEqual(result["message_characters"], 0)

    def test_safe_context_and_schema_codes_do_not_fall_through_generic_failure(self):
        for code, expected in (("invalid_json_schema", "structured_output_schema_error"),
                               ("context_length_exceeded", "context_or_request_limit")):
            client = CodexClient()
            events = [{"type": "turn.failed", "error": {"code": code, "message": "SECRET_MESSAGE"}}]
            with self.subTest(code=code), patch("codex_provider.subprocess.run", side_effect=self.event_run(events, returncode=1)):
                with self.assertRaisesRegex(ValueError, expected):
                    client.generate("Extract", {}, original.SCHEMA)
            self.assertEqual(client.calls[0]["status"], expected)
            self.assertNotIn("SECRET_MESSAGE", json.dumps(client.ledger()))

    def test_success_records_elapsed_and_schema_owned_event_shape_only(self):
        client = CodexClient()
        def events(command, **kwargs):
            result = self.fake_run(command, **kwargs)
            if "login" not in command:
                result.stdout += "\n" + json.dumps({"type": "PRIVATE_SECRET", "message": "PRIVATE_TEXT"})
            return result
        with patch("codex_provider.subprocess.run", side_effect=events):
            client.generate("Extract", {}, original.SCHEMA)
        call = client.calls[0]
        self.assertGreaterEqual(call["elapsed_seconds"], 0)
        self.assertEqual(call["event_shapes"]["turn.completed"], 1)
        self.assertEqual(call["event_shapes"]["other"], 1)
        self.assertIsNone(call["cli_version"])
        self.assertNotIn("PRIVATE_SECRET", json.dumps(call))
        self.assertNotIn("PRIVATE_TEXT", json.dumps(call))

    def test_timeout_keeps_only_stream_lengths_and_hashes_and_does_not_retry(self):
        client = CodexClient(timeout=30)
        def timeout(command, **kwargs):
            if "login" in command:
                return self.fake_run(command, **kwargs)
            raise subprocess.TimeoutExpired(command, 30, output=b"PRIVATE_INPUT", stderr="PRIVATE_STDERR")
        with patch("codex_provider.subprocess.run", side_effect=timeout) as run:
            with self.assertRaisesRegex(ValueError, "timed out"):
                client.generate("Extract", {}, original.SCHEMA)
        self.assertEqual(run.call_count, 2)
        details = client.calls[0]["transport_diagnostics"]
        self.assertEqual(details["timeout_seconds"], 30)
        self.assertEqual(details["stdout"]["sha256"], hashlib.sha256(b"PRIVATE_INPUT").hexdigest())
        self.assertEqual(details["stderr"]["bytes"], len("PRIVATE_STDERR"))
        self.assertNotIn("PRIVATE", json.dumps(client.ledger()))

    def test_invalid_stream_opaque_digest_and_stderr_digest_do_not_leak(self):
        client = CodexClient()
        def invalid(command, **kwargs):
            result = self.fake_run(command, **kwargs)
            if "login" not in command:
                result.stdout, result.stderr = "PRIVATE_INVALID_JSON", "PRIVATE_STDERR"
            return result
        with patch("codex_provider.subprocess.run", side_effect=invalid):
            with self.assertRaisesRegex(ValueError, "invalid JSON event stream"):
                client.generate("Extract", {}, original.SCHEMA)
        self.assertEqual(client.calls[0]["stdout_summary"]["bytes"], len("PRIVATE_INVALID_JSON"))
        self.assertNotIn("PRIVATE", json.dumps(client.ledger()))


if __name__ == "__main__":
    unittest.main()
