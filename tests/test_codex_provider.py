"""Mock-only checks: these tests do not start Codex inference or use account quota."""

import json
import os
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

from codex_provider import CodexClient, clean_environment


SCHEMA = {
    "type": "object", "properties": {"ok": {"type": "boolean"}},
    "required": ["ok"], "additionalProperties": False,
}


class CodexProviderTests(unittest.TestCase):
    def setUp(self):
        self.lookup = patch("codex_provider.shutil.which", return_value="/test/bin/codex")
        self.lookup.start()
        self.addCleanup(self.lookup.stop)
        self.proxy_lookup = patch("codex_provider.urllib.request.getproxies", return_value={})
        self.proxy_mock = self.proxy_lookup.start()
        self.addCleanup(self.proxy_lookup.stop)
        self.commands = []

    def test_existing_system_proxy_is_used_by_child_without_global_changes(self):
        self.proxy_mock.return_value = {"https": "http://127.0.0.1:1234", "http": "http://127.0.0.1:1234"}
        with patch.dict(os.environ, {"PATH": "/test/bin"}, clear=True):
            child = clean_environment()
            self.assertEqual(child["HTTPS_PROXY"], "http://127.0.0.1:1234")
            self.assertNotIn("HTTPS_PROXY", os.environ)

    def test_explicit_proxy_environment_takes_precedence(self):
        self.proxy_mock.return_value = {"https": "http://system.invalid:1234"}
        with patch.dict(os.environ, {"https_proxy": "http://explicit.invalid:1234"}, clear=True):
            child = clean_environment()
            self.assertEqual(child["https_proxy"], "http://explicit.invalid:1234")
            self.assertNotIn("HTTPS_PROXY", child)

    def fake_run(self, command, **kwargs):
        self.commands.append((command, kwargs))
        self.assertTrue(Path(kwargs["cwd"]).is_dir())
        if "login" in command:
            self.assertEqual(list(Path(kwargs["cwd"]).iterdir()), [])
            return subprocess.CompletedProcess(command, 0, "", "Logged in using ChatGPT\n")
        answer_path = Path(command[command.index("--output-last-message") + 1])
        answer_path.write_text('{"ok":true}', encoding="utf-8")
        events = [
            {"type": "thread.started", "model": "reported-model"},
            {"type": "turn.started"},
            {"type": "item.completed", "item": {"type": "agent_message", "text": '{"ok":true}'}},
            {"type": "turn.completed", "usage": {"input_tokens": 120, "output_tokens": 8,
                                                       "cached_input_tokens": 20}},
        ]
        return subprocess.CompletedProcess(command, 0, "\n".join(map(json.dumps, events)), "")

    def test_successful_structured_output_and_safe_invocation(self):
        client = CodexClient(model="requested-model", timeout=30)
        with patch("codex_provider.subprocess.run", side_effect=self.fake_run):
            self.assertEqual(client.generate("Extract fields", {"text": "document"}, SCHEMA), {"ok": True})
        command, kwargs = self.commands[-1]
        for flag in ("--ignore-user-config", "--ephemeral", "--skip-git-repo-check", "--json", "--strict-config"):
            self.assertIn(flag, command)
        self.assertEqual(command[command.index("--sandbox") + 1], "read-only")
        self.assertIn('forced_login_method="chatgpt"', command)
        self.assertIn('web_search="disabled"', command)
        self.assertIn("shell_tool", command)
        self.assertIn("plugins", command)
        self.assertEqual(command[-1], "-")
        self.assertEqual(kwargs["timeout"], 30)
        self.assertNotIn("document", command)
        self.assertIn("UNTRUSTED DOCUMENT DATA", kwargs["input"])
        self.assertFalse(Path(kwargs["cwd"]).exists())
        ledger = client.ledger()
        self.assertEqual(len(ledger["calls"]), 1)
        self.assertEqual(ledger["calls"][0]["requested_model"], "requested-model")
        self.assertEqual(ledger["calls"][0]["actual_model"], "reported-model")
        self.assertEqual(ledger["usage"]["input_tokens"], 120)

    def test_default_model_is_not_guessed_or_substituted(self):
        def without_reported_model(command, **kwargs):
            result = self.fake_run(command, **kwargs)
            if "login" not in command:
                rows = [json.loads(line) for line in result.stdout.splitlines()]
                rows[0].pop("model", None)
                result.stdout = "\n".join(map(json.dumps, rows))
            return result
        client = CodexClient()
        with patch("codex_provider.subprocess.run", side_effect=without_reported_model):
            client.generate("Extract fields", {}, SCHEMA)
        self.assertNotIn("--model", self.commands[-1][0])
        self.assertIsNone(client.ledger()["calls"][0]["actual_model"])

    def test_environment_drops_api_credentials_without_copying_auth(self):
        example = {
            "PATH": "/test/bin", "HOME": "/home/example", "CODEX_HOME": "/custom/codex",
            "OPENAI_API_KEY": "not-a-real-key", "ANTHROPIC_API_KEY": "not-a-real-key",
            "OPENAI_BASE_URL": "https://example.invalid", "CODEX_API_KEY": "not-a-real-key",
            "OTHER_APIKEY": "not-a-real-key", "AZURE_OPENAI_API_KEY": "not-a-real-key",
            "CODEX_ACCESS_TOKEN": "not-a-real-key", "AWS_SECRET_ACCESS_KEY": "not-a-real-key",
        }
        with patch.dict(os.environ, example, clear=True):
            cleaned = clean_environment()
            self.assertEqual(cleaned, {key: example[key] for key in ("PATH", "HOME", "CODEX_HOME")})
            client = CodexClient()
            with patch("codex_provider.subprocess.run", side_effect=self.fake_run):
                client.generate("Extract fields", {}, SCHEMA)
            for _, kwargs in self.commands:
                self.assertEqual(kwargs["env"], cleaned)
        self.assertNotIn("not-a-real-key", json.dumps(client.ledger()))

    def test_api_login_is_rejected_before_inference(self):
        with patch("codex_provider.subprocess.run", return_value=subprocess.CompletedProcess(
            [], 0, "Logged in using an API key", ""
        )) as run:
            client = CodexClient()
            with self.assertRaisesRegex(ValueError, "requires an existing ChatGPT login"):
                client.generate("Extract fields", {}, SCHEMA)
        self.assertEqual(run.call_count, 1)
        self.assertEqual(client.ledger()["calls"], [])

    def test_no_cli_does_not_fall_back(self):
        with patch("codex_provider.shutil.which", return_value=None), patch("codex_provider.subprocess.run") as run:
            with self.assertRaisesRegex(ValueError, "not installed"):
                CodexClient().generate("Extract fields", {}, SCHEMA)
            run.assert_not_called()

    def test_tool_events_reject_output_even_if_cli_succeeds(self):
        for kind in ("command_execution", "mcp_tool_call", "function_call", "web_search", "file_change"):
            with self.subTest(kind=kind):
                def with_tool(command, **kwargs):
                    result = self.fake_run(command, **kwargs)
                    if "login" not in command:
                        result.stdout += "\n" + json.dumps({"type": "item.started", "item": {"type": kind}})
                    return result
                client = CodexClient()
                with patch("codex_provider.subprocess.run", side_effect=with_tool):
                    with self.assertRaisesRegex(ValueError, "tool/command event"):
                        client.generate("Extract fields", {}, SCHEMA)
                self.assertEqual(client.ledger()["calls"][0]["status"], "tool_use_rejected")

    def test_prose_about_tools_is_not_a_tool_event(self):
        def prose(command, **kwargs):
            result = self.fake_run(command, **kwargs)
            if "login" not in command:
                result.stdout += "\n" + json.dumps({
                    "type": "item.completed", "item": {"type": "agent_message", "text": "A paper mentions mcp_tool_call."}
                })
            return result
        with patch("codex_provider.subprocess.run", side_effect=prose):
            self.assertEqual(CodexClient().generate("Extract fields", {}, SCHEMA), {"ok": True})

    def test_timeout_does_not_retry_or_echo_raw_error(self):
        def timeout(command, **kwargs):
            if "login" in command:
                return self.fake_run(command, **kwargs)
            raise subprocess.TimeoutExpired(command, 1, output="PRIVATE_CONTENT", stderr="SECRET_KEY")
        client = CodexClient()
        with patch("codex_provider.subprocess.run", side_effect=timeout) as run:
            with self.assertRaisesRegex(ValueError, "timed out") as error:
                client.generate("Extract fields", {}, SCHEMA)
        self.assertEqual(run.call_count, 2)
        self.assertNotIn("SECRET_KEY", str(error.exception))
        self.assertEqual(client.ledger()["calls"][0]["status"], "timeout")

    def test_failure_is_classified_without_exposing_stderr(self):
        def quota(command, **kwargs):
            result = self.fake_run(command, **kwargs)
            if "login" not in command:
                result.returncode = 1
                result.stderr = "quota exceeded; SECRET_KEY"
            return result
        client = CodexClient()
        with patch("codex_provider.subprocess.run", side_effect=quota):
            with self.assertRaisesRegex(ValueError, "account_limit_or_quota") as error:
                client.generate("Extract fields", {}, SCHEMA)
        self.assertNotIn("SECRET_KEY", str(error.exception))
        self.assertNotIn("SECRET_KEY", json.dumps(client.ledger()))

    def test_call_limit_prevents_another_login_or_inference(self):
        client = CodexClient(max_calls=1)
        with patch("codex_provider.subprocess.run", side_effect=self.fake_run) as run:
            client.generate("Extract fields", {}, SCHEMA)
            with self.assertRaisesRegex(ValueError, "call limit reached"):
                client.generate("Extract fields", {}, SCHEMA)
        self.assertEqual(run.call_count, 2)

    def test_missing_or_invalid_final_json_is_not_a_verdict(self):
        for answer in (None, "[]", "not json"):
            with self.subTest(answer=answer):
                def invalid_answer(command, **kwargs):
                    result = self.fake_run(command, **kwargs)
                    if "login" not in command:
                        path = Path(command[command.index("--output-last-message") + 1])
                        if answer is None:
                            path.unlink()
                        else:
                            path.write_text(answer)
                    return result
                with patch("codex_provider.subprocess.run", side_effect=invalid_answer):
                    with self.assertRaisesRegex(ValueError, "final JSON object"):
                        CodexClient().generate("Extract fields", {}, SCHEMA)

    def test_invalid_jsonl_and_missing_turn_completion_are_rejected(self):
        for output, message in (("bad json", "invalid JSON event stream"), ("{}", "completion was not confirmed")):
            def invalid_stream(command, **kwargs):
                result = self.fake_run(command, **kwargs)
                if "login" not in command:
                    result.stdout = output
                return result
            with self.subTest(output=output), patch("codex_provider.subprocess.run", side_effect=invalid_stream):
                with self.assertRaisesRegex(ValueError, message):
                    CodexClient().generate("Extract fields", {}, SCHEMA)

    def event_run(self, extra_events, *, after_completion=False, returncode=0, agent_text=None):
        def run(command, **kwargs):
            result = self.fake_run(command, **kwargs)
            if "login" not in command:
                rows = [json.loads(line) for line in result.stdout.splitlines()]
                if agent_text:
                    rows[2]["item"]["text"] = agent_text
                if after_completion:
                    rows.extend(extra_events)
                else:
                    rows[2:2] = extra_events
                result.stdout = "\n".join(map(json.dumps, rows))
                result.returncode = returncode
            return result
        return run

    def test_reconnect_notifications_before_success_remain_visible_as_warnings(self):
        warnings = [{"type": "error", "message": "Reconnecting 2/5: stream disconnected before completion: Connection reset by peer (os error 54) SECRET_KEY"}]
        client = CodexClient()
        with patch("codex_provider.subprocess.run", side_effect=self.event_run(warnings)):
            self.assertEqual(client.generate("Extract fields", {}, SCHEMA), {"ok": True})
        call = client.ledger()["calls"][0]
        self.assertEqual(call["status"], "completed_with_warnings")
        self.assertEqual(call["diagnostics"][0]["category"], "transport_error")
        self.assertFalse(call["diagnostics"][0]["fatal"])
        self.assertNotIn("SECRET_KEY", json.dumps(client.ledger()))

    def test_item_error_remains_fatal_even_with_final_message_and_turn_completed(self):
        events = [
            {"type": "error", "message": "Reconnecting 5/5: stream disconnected before completion: Connection reset by peer"},
            {"type": "item.completed", "item": {"type": "error", "message": "stream disconnected before completion"}},
        ]
        client = CodexClient()
        with patch("codex_provider.subprocess.run", side_effect=self.event_run(
            events, agent_text="This paper discusses authentication, login and includes number 401."
        )):
            with self.assertRaisesRegex(ValueError, "transport_error"):
                client.generate("Extract fields", {}, SCHEMA)
        call = client.ledger()["calls"][0]
        self.assertEqual(call["execution"]["fatal_error_count"], 1)
        self.assertEqual(call["diagnostics"][-1]["event_type"], "item.error")
        self.assertEqual(call["status"], "transport_error")

    def test_turn_failed_is_not_hidden_by_later_turn_completed(self):
        client = CodexClient()
        events = [{"type": "turn.failed", "error": {"code": "authentication_error", "message": "Authentication failed SECRET_KEY"}}]
        with patch("codex_provider.subprocess.run", side_effect=self.event_run(events)):
            with self.assertRaisesRegex(ValueError, "authentication_error"):
                client.generate("Extract fields", {}, SCHEMA)
        call = client.ledger()["calls"][0]
        self.assertEqual(call["diagnostics"][0]["codes"], ["authentication_error"])
        self.assertEqual(call["execution"]["fatal_error_count"], 1)
        self.assertNotIn("SECRET_KEY", json.dumps(call))

    def test_arbitrary_error_codes_are_not_persisted(self):
        client = CodexClient()
        events = [{"type": "error", "fatal": True, "code": "PRIVATE_TOKEN", "message": "Operation not permitted; PRIVATE_TOKEN"}]
        with patch("codex_provider.subprocess.run", side_effect=self.event_run(events)):
            with self.assertRaisesRegex(ValueError, "cli_environment_error"):
                client.generate("Extract fields", {}, SCHEMA)
        call = client.ledger()["calls"][0]
        self.assertEqual(call["diagnostics"][0]["codes"], [])
        self.assertNotIn("PRIVATE_TOKEN", json.dumps(call))

    def test_error_after_last_completed_turn_is_not_assumed_nonfatal(self):
        events = [{"type": "error", "message": "stream disconnected before completion"}]
        with patch("codex_provider.subprocess.run", side_effect=self.event_run(events, after_completion=True)):
            with self.assertRaisesRegex(ValueError, "transport_error"):
                CodexClient().generate("Extract fields", {}, SCHEMA)

    def test_readonly_doctor_never_invokes_model_or_prints_raw_status(self):
        def inspect(command, **kwargs):
            self.assertNotIn("input", kwargs)
            self.assertNotIn("--output-schema", command)
            if "--version" in command:
                return subprocess.CompletedProcess(command, 0, "codex-cli 0.167.0-alpha.3.2\n", "SECRET_KEY")
            if "login" in command:
                return subprocess.CompletedProcess(command, 0, "", "Logged in using ChatGPT\nSECRET_KEY")
            self.assertEqual(command[-2:], ["exec", "--help"])
            flags = "--ignore-user-config --ephemeral --sandbox --output-schema --output-last-message --json --strict-config"
            return subprocess.CompletedProcess(command, 0, flags, "SECRET_KEY")
        client = CodexClient()
        with patch("codex_provider.subprocess.run", side_effect=inspect) as run:
            report = client.doctor()
        self.assertTrue(report["ready_for_attempt"])
        self.assertEqual(report["runtime_probe"], "not_run")
        self.assertFalse(report["inference_started"])
        self.assertEqual(run.call_count, 3)
        self.assertEqual(client.ledger()["calls"], [])
        self.assertNotIn("SECRET_KEY", json.dumps(report))


if __name__ == "__main__":
    unittest.main()
