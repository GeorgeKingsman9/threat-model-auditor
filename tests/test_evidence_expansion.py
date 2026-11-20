"""Offline checks of generic, bounded evidence closure and legacy replay."""
import copy
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest
from unittest.mock import patch

import evidence_expansion
import source_bundle

SHA = 'a' * 40


class EvidenceExpansionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def put(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def test_only_imported_vendor_helpers_and_their_closure_are_read(self):
        self.put('main.py', 'from third_party.Engine import helper\n')
        self.put('third_party/Engine/__init__.py', '')
        self.put('third_party/Engine/helper.py', 'from .formatting import serialize\n')
        self.put('third_party/Engine/formatting.py', 'def serialize(x):\n    return str(x)\n')
        self.put('third_party/Engine/unrelated.py', 'UNRELATED = True\n')
        self.put('vendor/unused.py', 'UNRELATED_VENDOR = True\n')
        snapshot = source_bundle.load_repository(str(self.root))
        paths = {s['path'] for s in snapshot['segments']}
        self.assertEqual(paths, {'main.py', 'third_party/Engine/__init__.py',
                                 'third_party/Engine/helper.py', 'third_party/Engine/formatting.py'})
        self.assertEqual(snapshot['eligibility_policy'], evidence_expansion.POLICY)
        self.assertNotIn('UNRELATED', str(snapshot))
        source_bundle.validate_repository(snapshot)

    def test_config_template_then_finite_task_index_preserves_raw_bytes(self):
        self.put('runner.py', 'config = open_config(f"configs/tasks/{args.task}_config.json")\n')
        raw = b'{"source": "data/task_index.json"}\r\n'
        p = self.root / 'configs/tasks/task_config.json'; p.parent.mkdir(parents=True)
        p.write_bytes(raw)
        self.put('data/task_index.json', '{"task": "an original task", "record_index": 3}\n')
        self.put('data/unreferenced.json', 'DO_NOT_READ_UNREFERENCED\n')
        snapshot = source_bundle.load_repository(str(self.root))
        segments = {s['path']: s for s in snapshot['segments']}
        self.assertEqual(segments['configs/tasks/task_config.json']['text'].encode(), raw)
        self.assertEqual(segments['configs/tasks/task_config.json']['sha256'], hashlib.sha256(raw).hexdigest())
        self.assertIn('data/task_index.json', segments)
        self.assertNotIn('DO_NOT_READ_UNREFERENCED', str(snapshot))
        self.assertTrue(any(e.get('target') == 'data/task_index.json' and e['line'] == 1 for e in snapshot['evidence_expansion']['needed']))
        source_bundle.validate_repository(snapshot)

    def test_hard_exclusions_cannot_be_overridden_and_oversized_data_remains_unresolved(self):
        self.put('main.py', 'paths = ["cases/manual.json", "data/gold.json", "credentials.json", "data/huge.json", "data/table"]\n')
        for name in ('cases/manual.json', 'data/gold.json', 'credentials.json'):
            self.put(name, 'MUST_NOT_BE_READ')
        self.put('data/huge.json', 'x' * (evidence_expansion.LIMITS['max_data_bytes'] + 1))
        self.put('data/table/one.json', '{}')
        original = source_bundle.os.open
        touched = []
        def tracked(path, *args, **kwargs):
            touched.append(str(path)); return original(path, *args, **kwargs)
        with patch.object(source_bundle.os, 'open', side_effect=tracked):
            snapshot = source_bundle.load_repository(str(self.root))
        self.assertEqual([s['path'] for s in snapshot['segments']], ['main.py'])
        self.assertFalse(any('huge' in p or 'gold' in p or 'manual' in p or 'credentials' in p for p in touched))
        reasons = {e['reason'] for e in snapshot['evidence_expansion']['unresolved']}
        self.assertIn('referenced_file_byte_limit', reasons)
        self.assertIn('directory_reference_no_bulk_read', reasons)
        self.assertNotIn('MUST_NOT_BE_READ', str(snapshot))

    def test_expansion_budget_and_credential_omission_replay(self):
        self.put('main.py', 'x = "cfg.json"\n')
        fake = 'ghp_' + 'A' * 36
        self.put('cfg.json', json.dumps({'token': fake}))
        snapshot = source_bundle.load_repository(str(self.root))
        self.assertNotIn(fake, str(snapshot))
        self.assertEqual(snapshot['omitted'][0]['reason'], 'credential_like_content')
        source_bundle.validate_repository(snapshot)
        small = source_bundle.load_repository(str(self.root), max_chars=20)
        self.assertEqual(small['evidence_expansion']['over_limit'][0]['reason'], 'expansion_character_budget')
        source_bundle.validate_repository(small)

    def test_templates_never_bulk_expand_dataset_and_many_configs_are_bounded(self):
        self.put('main.py', 'x = open_config(f"configs/{args.name}.json")\n')
        for n in range(evidence_expansion.LIMITS['max_template_matches'] + 1):
            self.put(f'configs/{n}.json', '{}')
        snapshot = source_bundle.load_repository(str(self.root))
        self.assertEqual(snapshot['evidence_expansion']['added_files'], 0)
        self.assertTrue(any(e['reason'] == 'template_match_limit' for e in snapshot['evidence_expansion']['over_limit']))

    def test_snapshot_replay_uses_same_selector_and_rejects_tampered_reference_metadata(self):
        self.put('main.py', 'x = "config.json"\n')
        self.put('config.json', '{"a": 1}')
        snapshot = source_bundle.load_repository(str(self.root))
        for alter in (
            lambda x: x['evidence_expansion']['needed'][0].update(line=99),
            lambda x: x['inventory'][0].update(evidence_kind='invented'),
            lambda x: x.update(eligibility_policy='future-unknown'),
        ):
            bad = copy.deepcopy(snapshot); alter(bad)
            with self.assertRaises(source_bundle.RepositoryError): source_bundle.validate_repository(bad)
        legacy = source_bundle.load_repository(str(self.root), expand_evidence=False)
        self.assertNotIn('eligibility_policy', legacy)
        self.assertEqual([s['path'] for s in legacy['segments']], ['main.py'])
        source_bundle.validate_repository(legacy)

    def git(self, *args):
        return subprocess.run(['git', '-c', 'commit.gpgsign=false', '-C', str(self.root), *args],
                              capture_output=True, check=True).stdout.decode().strip()

    def test_gitlink_uses_pinned_public_gitmodules_binding_in_separate_snapshot(self):
        self.git('init', '-q'); self.git('config', 'user.name', 'Fixture'); self.git('config', 'user.email', 'fixture@example.test')
        self.put('main.py', 'import os\nx = os.path.join(os.path.dirname(__file__), "third_party/Engine")\n')
        self.put('.gitmodules', '[submodule "engine"]\n path = third_party/Engine\n url = git@github.com:example/engine.git\n')
        self.git('add', '.'); self.git('update-index', '--add', '--cacheinfo', '160000,' + SHA + ',third_party/Engine')
        self.git('commit', '-qm', 'fixture')
        # Independently valid child identity, raw Git object hashes and inventory.
        child_root = self.root / 'child'; child_root.mkdir(); (child_root / 'common.py').write_text('def serialize(x):\n    return x\n')
        child = source_bundle.load_repository(str(child_root), expand_evidence=False)
        child.update(source='https://github.com/example/engine', source_binding=source_bundle._digest(b'https://github.com/example/engine'),
                     revision_kind='git_commit', revision=SHA, commit=SHA, tree_sha=None,
                     commit_binding='github_codeload_full_commit_url', archive_sha256='0' * 64)
        actual_loader = source_bundle.load_repository
        calls = []
        def loader(source, **kwargs):
            calls.append((source, kwargs)); return copy.deepcopy(child)
        with patch.object(source_bundle, 'load_repository', side_effect=loader):
            snapshot = actual_loader(str(self.root))
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][1]['revision'], SHA)
        self.assertFalse(calls[0][1]['expand_evidence'])
        self.assertEqual(snapshot['dependency_snapshots'][0]['mount_path'], 'third_party/Engine')
        self.assertEqual(snapshot['dependency_acquisition'][0]['status'], 'resolved')
        self.assertNotIn('third_party/Engine/common.py', {s['path'] for s in snapshot['segments']})
        self.assertEqual(snapshot['dependency_metadata']['text'], (self.root / '.gitmodules').read_text())
        source_bundle.validate_repository(snapshot)
        bad = copy.deepcopy(snapshot); bad['dependency_snapshots'][0]['revision'] = 'b' * 40
        with self.assertRaises(source_bundle.RepositoryError): source_bundle.validate_repository(bad)

    def test_remote_tree_fetches_only_referenced_config_and_retains_blob_binding(self):
        from test_source_only import SourceOnlyTests, COMMIT, REPOSITORY
        fixture = SourceOnlyTests()
        files = {'main.py': b'x = "configs/runtime.json"\n',
                 'configs/runtime.json': b'{"task": "data/index.json"}\n',
                 'data/index.json': b'{"record": 4}\n',
                 'configs/unrelated.json': b'NEVER_FETCH',
                 'data/full.json': b'NEVER_FETCH_DATA'}
        mock, requested = fixture.fixture(files)
        with mock:
            snapshot = source_bundle.load_repository(REPOSITORY, revision=COMMIT, fetch_mode='files')
        self.assertEqual({s['path'] for s in snapshot['segments']}, {'main.py', 'configs/runtime.json', 'data/index.json'})
        self.assertFalse(any('unrelated' in url or 'full.json' in url for url in requested))
        for item in snapshot['files']:
            self.assertEqual(item['object_id'], hashlib.sha1(f"blob {len(files[item['path']])}\0".encode() + files[item['path']]).hexdigest())
        source_bundle.validate_repository(snapshot)

    def test_archive_extension_uses_identical_policy(self):
        raw = io.BytesIO()
        files = {'main.py': b'x = "configs/runtime.json"\n', 'configs/runtime.json': b'{"n": 3}',
                 'data/unrelated.json': b'NEVER_READ'}
        with tarfile.open(fileobj=raw, mode='w:gz') as archive:
            for path, data in files.items():
                info = tarfile.TarInfo('repo-' + SHA + '/' + path)
                info.size = len(data); archive.addfile(info, io.BytesIO(data))
        with patch.object(source_bundle, '_download_archive', return_value=raw.getvalue()):
            snapshot = source_bundle.load_repository('https://github.com/example/repo', revision=SHA)
        self.assertEqual({s['path'] for s in snapshot['segments']}, {'main.py', 'configs/runtime.json'})
        source_bundle.validate_repository(snapshot)

    def test_dynamic_import_has_no_package_install_or_external_resolution(self):
        self.put('main.py', 'import importlib\nmod = importlib.import_module("external.helpers")\n')
        with patch.object(source_bundle, '_download_archive') as download:
            snapshot = source_bundle.load_repository(str(self.root))
        download.assert_not_called()
        self.assertTrue(any(e['reference'] == 'external.helpers' and e['reason'] == 'module_not_in_pinned_repository' for e in snapshot['evidence_expansion']['unresolved']))


if __name__ == '__main__': unittest.main()
