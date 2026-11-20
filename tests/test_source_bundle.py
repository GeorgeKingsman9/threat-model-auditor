"""Offline checks for provenance-bound, nonexecuting source ingestion."""

import hashlib
import copy
import io
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest
from http.client import IncompleteRead
from unittest.mock import patch
from urllib.error import HTTPError, URLError

import source_bundle


SHA = "a" * 40


class SourceBundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="source-reader-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)

    def put(self, path, text):
        result = self.directory / path
        result.parent.mkdir(parents=True, exist_ok=True)
        result.write_text(text, encoding="utf-8")
        return result

    def git(self, *args):
        result = subprocess.run(["git", "-c", "commit.gpgsign=false", "-C", str(self.directory), *args],
                                capture_output=True, check=True)
        return result.stdout.decode().strip()

    def archive(self, files, prefix=None):
        output = io.BytesIO()
        root = prefix or "repo-" + SHA
        with tarfile.open(fileobj=output, mode="w:gz") as archive:
            for path, data in files:
                name = root + "/" + path
                info = tarfile.TarInfo(name)
                if isinstance(data, tuple):
                    info.type, info.linkname = data
                    archive.addfile(info)
                else:
                    info.size = len(data)
                    archive.addfile(info, io.BytesIO(data))
        return output.getvalue()

    def test_git_commit_reads_objects_not_dirty_worktree_or_untracked_labels(self):
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.test")
        content = "def construct(query):\n    return query\n"
        self.put("src/pipeline.py", content)
        self.put("tests/gold.py", "verdict = 'manually-labeled'\n")
        self.git("add", ".")
        self.git("commit", "-qm", "fixed source")
        first = self.git("rev-parse", "HEAD")
        self.put("src/pipeline.py", "raise Exception('DIRTY TREE MUST NOT BE READ')\n")
        self.put("adjudication/reviewed.py", "old_label = 'inconsistent'\n")
        result = source_bundle.load_repository(str(self.directory), revision=first)
        self.assertEqual(result["commit"], first)
        self.assertEqual(result["revision_kind"], "git_commit")
        self.assertEqual(result["segments"][0]["text"], content)
        self.assertEqual(result["segments"][0]["sha256"], hashlib.sha256(content.encode()).hexdigest())
        self.assertNotIn("DIRTY TREE", str(result))
        self.assertNotIn("manually-labeled", str(result))
        self.assertNotIn("old_label", str(result))
        self.assertNotIn(str(self.directory.parent), str(result))
        self.assertTrue(result["tree_sha"])

    def test_git_ref_resolves_once_and_does_not_run_hooks_or_source(self):
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.test")
        marker = self.directory / "DO_NOT_CREATE"
        self.put("runner.py", "from pathlib import Path\nPath('DO_NOT_CREATE').touch()\n")
        self.git("add", ".")
        self.git("commit", "-qm", "fixed")
        hook = self.put(".git/hooks/post-checkout", "#!/bin/sh\ntouch DO_NOT_CREATE\n")
        hook.chmod(0o755)
        result = source_bundle.load_repository(str(self.directory))
        self.assertEqual(result["revision"], self.git("rev-parse", "HEAD"))
        self.assertFalse(marker.exists())
        self.assertEqual(result["execution"], "none")

    def test_plain_directory_has_manifest_revision_and_rejects_invented_git_identity(self):
        self.put("src/pipeline.py", "x = 1\n")
        result = source_bundle.load_repository(str(self.directory))
        self.assertEqual(result["revision_kind"], "content_manifest")
        self.assertEqual(result["revision"], "content-manifest:" + result["manifest_sha256"])
        self.assertIsNone(result["commit"])
        with self.assertRaisesRegex(source_bundle.RepositoryError, "non-Git"):
            source_bundle.load_repository(str(self.directory), revision=SHA)

    def test_omission_is_explicit_and_does_not_truncate_the_other_whole_file(self):
        self.put("src/pipeline.py", "first = 1\nsecond = 2\n")
        self.put("src/runner.py", "".join(f"item{i} = {i}\n" for i in range(10)))
        result = source_bundle.load_repository(str(self.directory), max_chars=30)
        self.assertEqual([item["path"] for item in result["segments"]], ["src/pipeline.py"])
        self.assertEqual(result["segments"][0]["text"], "first = 1\nsecond = 2\n")
        self.assertEqual(result["segments"][0]["id"], "repo:src/pipeline.py:L1-L2")
        self.assertFalse(result["coverage"]["complete"])
        self.assertTrue(result["coverage"]["inventory_complete"])
        self.assertEqual(result["omitted"][0]["reason"], "character_budget")
        self.assertTrue(result["omitted"][0]["sha256"])
        again = source_bundle.load_repository(str(self.directory), max_chars=500)
        self.assertEqual(again["manifest_sha256"], result["manifest_sha256"])
        self.assertTrue(again["coverage"]["complete"])

    def test_sensitive_labels_data_dependencies_and_local_symlinks_are_not_sent(self):
        self.put("src/pipeline.py", "pass\n")
        for name in [".env", "credentials.py", "secrets.py", "gold.py", "labels.py", "pilot_results.py",
                     "research/findings.py", "adjudication/record.py", "data/sample.py", "tests/assertions.py",
                     "node_modules/pkg/index.js", "vendor/pkg.py", "docs/report.py", "results/report.py",
                     "credentials/login.py", "secrets/service.py", "labels/curation.py"]:
            self.put(name, "DO_NOT_SEND_THIS\n")
        outside = self.put("private.txt", "OUTSIDE_CONTENT\n")
        (self.directory / "link.py").symlink_to(outside)
        (self.directory / "linked_dir").symlink_to(self.directory / "data", target_is_directory=True)
        result = source_bundle.load_repository(str(self.directory))
        self.assertNotIn("DO_NOT_SEND_THIS", str(result))
        self.assertNotIn("OUTSIDE_CONTENT", str(result))
        self.assertEqual([item["path"] for item in result["segments"]], ["src/pipeline.py"])
        reasons = {item["path"]: item["reason"] for item in result["excluded"]}
        self.assertEqual(reasons["link.py"], "symlink")
        self.assertIn("linked_dir/", reasons)

    def test_embedded_credential_pattern_is_omitted_with_hash_not_printed(self):
        self.put("pipeline.py", "pass\n")
        fake = "ghp_" + "A" * 36
        self.put("client.py", f"token = '{fake}'\n")
        result = source_bundle.load_repository(str(self.directory))
        self.assertNotIn(fake, str(result))
        self.assertFalse(result["coverage"]["complete"])
        self.assertEqual(result["omitted"][0]["reason"], "credential_like_content")

    def test_binary_source_and_large_files_do_not_claim_full_coverage(self):
        self.put("pipeline.py", "pass\n")
        (self.directory / "binary.py").write_bytes(b"\x00\xff")
        self.put("huge.py", "x" * 30)
        with patch.object(source_bundle, "MAX_FILE_BYTES", 20):
            result = source_bundle.load_repository(str(self.directory))
        self.assertFalse(result["coverage"]["complete"])
        self.assertEqual({item["reason"] for item in result["omitted"]}, {"not_utf8_source", "file_byte_limit"})

    def test_github_requires_https_without_credentials_and_full_pinned_commit(self):
        for source, revision in [("http://github.com/owner/repo", SHA),
                                 ("https://user:secret@github.com/owner/repo", SHA),
                                 ("https://github.com/owner/repo/tree/main", SHA),
                                 ("https://localhost/owner/repo", SHA),
                                 ("https://github.com/owner/repo", "main"),
                                 ("https://github.com/owner/repo", None)]:
            with self.subTest(source=source, revision=revision), patch.object(source_bundle, "_download_archive") as download:
                with self.assertRaises(source_bundle.RepositoryError):
                    source_bundle.load_repository(source, revision=revision)
                download.assert_not_called()

    def test_pinned_archive_uses_line_ranges_hashes_and_expected_commit_root(self):
        archive = self.archive([("src/pipeline.py", b"def f(x):\n    return x\n"),
                                ("data/private.py", b"NOT_SENT")])
        with patch.object(source_bundle, "_download_archive", return_value=archive) as download:
            result = source_bundle.load_repository("https://github.com/owner/repo.git", revision=SHA)
        self.assertEqual(download.call_args.args, (f"https://codeload.github.com/owner/repo/tar.gz/{SHA}",))
        self.assertEqual(result["commit"], SHA)
        self.assertEqual(result["segments"][0]["line_end"], 2)
        self.assertNotIn("NOT_SENT", str(result))
        self.assertEqual(result["archive_sha256"], hashlib.sha256(archive).hexdigest())
        wrong = self.archive([("src/main.py", b"pass\n")], prefix="repo-" + "b" * 40)
        with patch.object(source_bundle, "_download_archive", return_value=wrong), self.assertRaisesRegex(source_bundle.RepositoryError, "commit"):
            source_bundle.load_repository("https://github.com/owner/repo", revision=SHA)

    def test_archive_traversal_and_duplicate_paths_are_rejected_without_extracting(self):
        for files in [[("../outside.py", b"bad")], [("src/main.py", b"one"), ("src/main.py", b"two")],
                      [("src/../../bad.py", b"bad")], [("src\\escape.py", b"bad")]]:
            archive = self.archive(files)
            with self.subTest(files=files), patch.object(source_bundle, "_download_archive", return_value=archive):
                with self.assertRaises(source_bundle.RepositoryError):
                    source_bundle.load_repository("https://github.com/owner/repo", revision=SHA)
        self.assertFalse((self.directory / "outside.py").exists())

    def test_archive_links_are_never_followed_and_expansion_is_bounded(self):
        archive = self.archive([("src/main.py", b"pass\n"),
                                ("src/alias.py", (tarfile.SYMTYPE, "/private/secret.py")),
                                ("src/hard.py", (tarfile.LNKTYPE, "../outside.py"))])
        with patch.object(source_bundle, "_download_archive", return_value=archive):
            result = source_bundle.load_repository("https://github.com/owner/repo", revision=SHA)
        self.assertEqual(len(result["segments"]), 1)
        self.assertEqual(len(result["excluded"]), 2)
        with patch.object(source_bundle, "_download_archive", return_value=archive), patch.object(source_bundle, "MAX_EXPANDED_BYTES", 1):
            with self.assertRaisesRegex(source_bundle.RepositoryError, "expanded"):
                source_bundle.load_repository("https://github.com/owner/repo", revision=SHA)

    def test_invalid_local_revision_and_empty_budget_fail_closed(self):
        self.git("init", "-q")
        for revision in ["--help", "HEAD..main", "HEAD\n", "HEAD^{tree}"]:
            with self.subTest(revision=revision), self.assertRaisesRegex(source_bundle.RepositoryError, "revision"):
                source_bundle.load_repository(str(self.directory), revision=revision)
        for budget in [0, -1, True, "100"]:
            with self.subTest(budget=budget), self.assertRaisesRegex(source_bundle.RepositoryError, "max_chars"):
                source_bundle.load_repository(str(self.directory), max_chars=budget)

    def test_replay_validation_rejects_changed_text_inventory_lines_and_revision(self):
        self.put("pipeline.py", "def f(x):\n    return x\n")
        snapshot = source_bundle.load_repository(str(self.directory))
        source_bundle.validate_repository(snapshot)

        changes = [
            lambda d: d["segments"][0].update(text="def f(x):\n    return 'changed'\n"),
            lambda d: d["segments"][0].update(line_end=999),
            lambda d: d["segments"][0].update(id="other-id"),
            lambda d: d["inventory"][0].update(sha256="0" * 64),
            lambda d: d.update(revision=SHA),
            lambda d: d["coverage"].update(characters=0),
        ]
        for index, change in enumerate(changes):
            with self.subTest(index=index):
                tampered = copy.deepcopy(snapshot)
                change(tampered)
                with self.assertRaises(source_bundle.RepositoryError):
                    source_bundle.validate_repository(tampered)

    def test_unreadable_inventory_is_not_silently_certified_complete(self):
        def broken_walk(*args, **kwargs):
            kwargs["onerror"](PermissionError("fixture"))
            return iter(())

        with patch.object(source_bundle.os, "walk", side_effect=broken_walk):
            with self.assertRaisesRegex(source_bundle.RepositoryError, "inventory"):
                source_bundle.load_repository(str(self.directory))

    def test_original_utf8_bytes_including_crlf_are_preserved_for_hash_validation(self):
        raw = b"\xef\xbb\xbfdef f(x):\r\n    return x\r\n"
        (self.directory / "pipeline.py").write_bytes(raw)
        snapshot = source_bundle.load_repository(str(self.directory))
        self.assertEqual(snapshot["segments"][0]["text"].encode("utf-8"), raw)
        self.assertEqual(snapshot["segments"][0]["sha256"], hashlib.sha256(raw).hexdigest())
        source_bundle.validate_repository(snapshot)

    def response(self, data=b"archive", headers=None, read_error=None):
        class Response(io.BytesIO):
            status = 200

            def geturl(self):
                return "https://codeload.github.com/owner/repo/tar.gz/" + SHA

            def read(self, amount):
                if read_error:
                    raise read_error
                return super().read(amount)

        response = Response(data)
        response.headers = headers or {}
        return response

    def test_archive_retries_timeout_then_succeeds_with_both_attempts_preserved(self):
        ledger = {}
        with patch.object(source_bundle, "build_opener") as opener:
            opener.return_value.open.side_effect = [URLError(TimeoutError("private transport detail")), self.response()]
            data = source_bundle._download_archive("https://codeload.github.com/owner/repo/tar.gz/" + SHA, acquisition=ledger)
        self.assertEqual(data, b"archive")
        self.assertEqual(len(ledger["attempts"]), 2)
        self.assertEqual(ledger["attempts"][0]["failure_kind"], "timeout")
        self.assertEqual(ledger["attempts"][1]["status"], "succeeded")
        self.assertEqual(ledger["attempts"][1]["bytes_received"], 7)
        self.assertNotIn("private transport detail", str(ledger))

    def test_archive_retry_exhaustion_preserves_distinct_transport_failures(self):
        url = "https://codeload.github.com/owner/repo/tar.gz/" + SHA
        with patch.object(source_bundle, "build_opener") as opener:
            opener.return_value.open.side_effect = [TimeoutError(), self.response(read_error=IncompleteRead(b"partial", 100))]
            with self.assertRaises(source_bundle.RepositoryError) as caught:
                source_bundle._download_archive(url)
        attempts = caught.exception.acquisition["attempts"]
        self.assertEqual(len(attempts), source_bundle.DOWNLOAD_ATTEMPTS)
        self.assertEqual([a["failure_kind"] for a in attempts], ["timeout", "truncated_response"])
        self.assertEqual(attempts[-1]["bytes_received"], 7)
        self.assertNotIn("partial", str(caught.exception.acquisition))

    def test_archive_limits_redirect_and_http_not_found_are_not_retried(self):
        url = "https://codeload.github.com/owner/repo/tar.gz/" + SHA
        cases = [
            (self.response(headers={"Content-Length": str(source_bundle.MAX_DOWNLOAD_BYTES + 1)}), "download_limit"),
            (self.response(b"more than cap"), "download_limit"),
            (HTTPError(url, 404, "private detail", {}, None), "http_error"),
        ]
        for response, expected in cases:
            with self.subTest(expected=expected), patch.object(source_bundle, "build_opener") as opener:
                opener.return_value.open.side_effect = [response]
                with patch.object(source_bundle, "MAX_DOWNLOAD_BYTES", 10 if expected == "download_limit" else source_bundle.MAX_DOWNLOAD_BYTES):
                    with self.assertRaises(source_bundle.RepositoryError) as caught:
                        source_bundle._download_archive(url)
                self.assertEqual(opener.return_value.open.call_count, 1)
                self.assertEqual(caught.exception.acquisition["attempts"][0]["failure_kind"], expected)

    def test_declared_truncation_discards_first_body_and_does_not_join_attempts(self):
        url = "https://codeload.github.com/owner/repo/tar.gz/" + SHA
        with patch.object(source_bundle, "build_opener") as opener:
            opener.return_value.open.side_effect = [self.response(b"partial", {"Content-Length": "20"}), self.response(b"complete")]
            ledger = {}
            data = source_bundle._download_archive(url, acquisition=ledger)
        self.assertEqual(data, b"complete")
        self.assertEqual(ledger["attempts"][0]["failure_kind"], "truncated_response")

    def test_real_download_path_carries_attempt_ledger_into_validated_snapshot(self):
        raw = self.archive([("pipeline.py", b"pass\n")])
        with patch.object(source_bundle, "build_opener") as opener:
            opener.return_value.open.return_value = self.response(raw)
            snapshot = source_bundle.load_repository("https://github.com/owner/repo", revision=SHA)
        self.assertEqual(snapshot["source_acquisition"]["attempts"][0]["sha256"], snapshot["archive_sha256"])
        source_bundle.validate_repository(snapshot)


if __name__ == "__main__":
    unittest.main()
