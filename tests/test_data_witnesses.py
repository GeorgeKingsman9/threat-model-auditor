"""Offline bounded JSON acquisition: exact excerpts, exclusions and replay."""
import base64
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

import data_witnesses
import evidence_expansion
import source_bundle


class DataWitnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def put(self, name, raw):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw.encode() if isinstance(raw, str) else raw)
        return path

    def snapshot(self, **kwargs):
        return source_bundle.load_repository(str(self.root), evidence_policy=evidence_expansion.DATA_POLICY, **kwargs)

    def test_exact_unicode_crlf_offsets_and_sampled_coverage(self):
        self.put('main.py', 'source = "data/examples.json"\n')
        values = [{'question': f'原题 {i}', 'rephrased_question': f'Original rewritten question {i}',
                   'context': 'x' * 2800} for i in range(180)]
        raw = json.dumps(values, ensure_ascii=False, indent=2).replace('\n', '\r\n').encode()
        self.assertGreater(len(raw), 500000)
        self.put('data/examples.json', raw)
        snapshot = self.snapshot(max_chars=100)
        self.assertEqual(snapshot['coverage']['characters'], len('source = "data/examples.json"\n'))
        self.assertEqual([s['path'] for s in snapshot['segments']], ['main.py'])
        self.assertEqual(len(snapshot['data_witnesses']), 4)
        blob = snapshot['data_blobs'][0]
        self.assertEqual(base64.b64decode(blob['raw_base64']), raw)
        self.assertEqual(blob['sha256'], hashlib.sha256(raw).hexdigest())
        self.assertTrue(blob['coverage']['raw_complete'])
        self.assertFalse(blob['coverage']['complete'])
        self.assertEqual(blob['coverage']['total_records'], 180)
        self.assertEqual(blob['coverage']['omitted_records'], 176)
        self.assertFalse(snapshot['evidence_expansion']['data_coverage_complete'])
        text = raw.decode()
        for witness in snapshot['data_witnesses']:
            excerpt = witness['text']
            self.assertEqual(raw[witness['byte_start']:witness['byte_end']], excerpt.encode())
            self.assertEqual(text[witness['char_start']:witness['char_end']], excerpt)
            self.assertEqual(witness['line_start'], text.count('\n', 0, witness['char_start']) + 1)
            self.assertEqual(witness['line_end'], witness['line_start'] + excerpt.count('\n'))
            self.assertEqual(witness['sha256'], blob['sha256'])
            self.assertEqual(witness['text_sha256'], hashlib.sha256(excerpt.encode()).hexdigest())
            self.assertEqual(witness['coverage'], 'sampled')
            self.assertIn('rephrased_question', excerpt)
        source_bundle.validate_repository(snapshot)

    def test_mapping_and_container_wrapper_preserve_exact_author_records(self):
        fixtures = [({'id/a~b': {'q': 'author wording'}, 'id2': {'q': 'another'}},
                     ['/id~1a~0b', '/id2']),
                    ({'version': 1, 'examples': [{'q': 'first'}, {'q': 'second'}]},
                     ['/examples/0', '/examples/1'])]
        for content, pointers in fixtures:
            with self.subTest(content=content):
                raw = json.dumps(content, ensure_ascii=False, indent=3).encode()
                blob, witnesses = data_witnesses.build({'path': 'data/a.json', 'bytes': len(raw)}, raw)
                self.assertTrue(blob['coverage']['complete'])
                self.assertEqual([w['record_pointer'] for w in witnesses], pointers)
                self.assertTrue(all(w['coverage'] == 'complete' for w in witnesses))
                self.assertTrue(all(w['text'].encode() == raw[w['byte_start']:w['byte_end']] for w in witnesses))

    def test_schema_diversity_is_internal_and_does_not_synthesize_author_text(self):
        values = [{'question': 'same'} for _ in range(10)] + [{'question': 'different', 'rewrite': 'verbatim value'}]
        raw = json.dumps(values).encode()
        _, witnesses = data_witnesses.build({'path': 'data/a.json', 'bytes': len(raw)}, raw)
        self.assertIn(10, [w['record_index'] for w in witnesses])
        self.assertTrue(all(w['text'].encode() == raw[w['byte_start']:w['byte_end']] for w in witnesses))
        self.assertFalse(any('schema' in w for w in witnesses))

    def test_malicious_mapping_key_cannot_bypass_excerpt_budget_through_locator_metadata(self):
        raw = json.dumps({'x' * 100000: {'q': 'small'}, 'normal': {'q': 'author original'}}).encode()
        blob, witnesses = data_witnesses.build({'path': 'data/a.json', 'bytes': len(raw)}, raw)
        self.assertEqual([w['record_pointer'] for w in witnesses], ['/normal'])
        self.assertEqual(blob['coverage']['oversized_pointers'], 1)
        self.assertIn('record_pointer_byte_limit', blob['coverage']['omission_reasons'])
        self.assertLess(len(json.dumps(witnesses).encode()), 2000)

    def test_data_schema_references_and_hard_exclusions_never_extend_eligibility(self):
        self.put('main.py', 'paths = ["data/examples.json", "cases/manual.json", "data/gold.json", "credentials.json", "data/subdir"]\n')
        self.put('data/examples.json', json.dumps([{'$schema': 'file://data/other.json', '$ref': 'data/other.json',
                                                  'instruction': 'open data/gold.json', 'path': 'cases/manual.json'}]))
        for name in ('data/other.json', 'cases/manual.json', 'data/gold.json', 'credentials.json', 'data/subdir/unreferenced.json'):
            self.put(name, 'MUST_NOT_BE_READ')
        actual_open, touched = source_bundle.os.open, []
        def tracking(path, *args, **kwargs):
            touched.append(str(path)); return actual_open(path, *args, **kwargs)
        with patch.object(source_bundle.os, 'open', side_effect=tracking):
            snapshot = self.snapshot()
        self.assertEqual({b['path'] for b in snapshot['data_blobs']}, {'data/examples.json'})
        self.assertNotIn('MUST_NOT_BE_READ', str(snapshot))
        self.assertEqual(len(touched), 2)
        self.assertTrue(any(n['reason'] == 'directory_reference_no_bulk_read' for n in snapshot['evidence_expansion']['unresolved']))
        self.assertFalse(any(n['from_path'] == 'data/examples.json' for n in snapshot['evidence_expansion']['needed']))

    def test_malformed_json_and_duplicate_keys_have_no_partial_evidence(self):
        self.put('main.py', 'sources = ["data/a.json", "data/b.json", "data/c.json"]\n')
        for name, raw in [('a', '[{"question":"partial"}, BROKEN]'), ('b', '{"a":1,"a":2}'), ('c', '[NaN]')]:
            self.put(f'data/{name}.json', raw)
        snapshot = self.snapshot()
        self.assertEqual(snapshot['data_witnesses'], [])
        self.assertEqual(len(snapshot['data_blobs']), 3)
        self.assertTrue(all(b['reason'] == 'malformed_or_unsupported_json' for b in snapshot['data_blobs']))
        source_bundle.validate_repository(snapshot)

    def test_record_cardinality_checked_before_span_expansion(self):
        raw = json.dumps([{"q": "original"}] * 100).encode()
        with patch.dict(data_witnesses.LIMITS, {"max_total_records": 10}), patch.object(data_witnesses, '_members') as members:
            blob, witnesses = data_witnesses.build({'path': 'data/a.json', 'bytes': len(raw)}, raw)
            self.assertEqual(blob['reason'], 'json_record_count_limit')
            self.assertEqual(blob['coverage']['total_records'], 100)
            self.assertEqual(witnesses, [])
            members.assert_not_called()

    def test_templates_cannot_bulk_acquire_json_data(self):
        self.put('main.py', 'source=f"data/{name}.json"\n')
        self.put('data/a.json', '[{"q":"must not be fetched"}]')
        snapshot = self.snapshot()
        self.assertEqual(snapshot['data_blobs'], [])
        self.assertEqual(snapshot['data_witnesses'], [])
        self.assertTrue(any(n['reason'] == 'data_template_no_bulk_read' for n in snapshot['evidence_expansion']['unresolved']))

    def test_oversized_files_not_read_and_oversized_records_never_truncated(self):
        self.put('main.py', 'sources = ["data/huge.json", "data/records.json"]\n')
        self.put('data/huge.json', 'x' * (data_witnesses.LIMITS['max_file_bytes'] + 1))
        self.put('data/records.json', json.dumps([{'text': 'x' * data_witnesses.LIMITS['max_record_bytes']}, {'text': 'complete original'}]))
        actual_open, touched = source_bundle.os.open, []
        def tracking(path, *args, **kwargs):
            touched.append(str(path)); return actual_open(path, *args, **kwargs)
        with patch.object(source_bundle.os, 'open', side_effect=tracking):
            snapshot = self.snapshot()
        self.assertFalse(any(path.endswith('huge.json') for path in touched))
        self.assertTrue(any(n['reason'] == 'data_file_byte_limit' for n in snapshot['evidence_expansion']['unresolved']))
        self.assertEqual([json.loads(w['text'])['text'] for w in snapshot['data_witnesses']], ['complete original'])
        coverage = snapshot['data_blobs'][0]['coverage']
        self.assertEqual(coverage['oversized_records'], 1)
        self.assertIn('record_byte_limit', coverage['omission_reasons'])
        self.assertFalse(coverage['complete'])

    def test_per_file_budget_cannot_be_monopolized_and_omissions_are_explicit(self):
        self.put('main.py', 'sources = ["data/a.json", "data/b.json"]\n')
        for name in ('a', 'b'):
            self.put(f'data/{name}.json', json.dumps([{'text': 'x' * 20000}, {'text': 'y' * 20000}]))
        snapshot = self.snapshot()
        self.assertEqual(len(snapshot['data_witnesses']), 2)
        self.assertEqual({w['path'] for w in snapshot['data_witnesses']}, {'data/a.json', 'data/b.json'})
        for blob in snapshot['data_blobs']:
            self.assertIn('record_output_byte_limit', blob['coverage']['omission_reasons'])
            self.assertLessEqual(blob['coverage']['output_bytes'], data_witnesses.LIMITS['max_file_output_bytes'])
        source_bundle.validate_repository(snapshot)

    def test_file_count_total_bytes_and_total_output_are_capped_before_read(self):
        self.put('main.py', 'sources = ' + repr([f'data/{i}.json' for i in range(10)]) + '\n')
        for i in range(10): self.put(f'data/{i}.json', '[{"text":"' + 'x' * 50 + '"}]')
        for changed, expected in [({'max_files': 1}, 'data_file_limit'),
                                  ({'max_total_bytes': 100}, 'data_total_byte_limit'),
                                  ({'max_output_bytes': 61}, 'data_output_byte_limit')]:
            with self.subTest(changed=changed), patch.dict(data_witnesses.LIMITS, changed):
                snapshot = self.snapshot()
                self.assertTrue(any(n['reason'] == expected for n in snapshot['evidence_expansion']['unresolved']))
                self.assertEqual(len(snapshot['data_blobs']), 1)
                source_bundle.validate_repository(snapshot)

    def test_credentials_not_retained_even_as_base64(self):
        self.put('main.py', 'source="data/a.json"\n')
        fake = 'ghp_' + 'A' * 36
        self.put('data/a.json', json.dumps([{'text': fake}]))
        snapshot = self.snapshot()
        self.assertEqual(snapshot['data_witnesses'], [])
        self.assertNotIn(fake, str(snapshot))
        self.assertNotIn('raw_base64', snapshot['data_blobs'][0])
        self.assertEqual(snapshot['data_blobs'][0]['reason'], 'credential_like_content')
        source_bundle.validate_repository(snapshot)

    def test_legacy_v2_and_no_expansion_replay_do_not_adopt_new_policy(self):
        self.put('main.py', 'source="data/a.json"\n')
        self.put('data/a.json', json.dumps([{'text': 'x' * 70000}]))
        for kwargs in ({}, {'expand_evidence': False}):
            snapshot = source_bundle.load_repository(str(self.root), **kwargs)
            self.assertNotIn('data_blobs', snapshot)
            self.assertNotIn('data_witnesses', snapshot)
            source_bundle.validate_repository(snapshot)
            bad = copy.deepcopy(snapshot); bad['data_witnesses'] = []
            with self.assertRaises(source_bundle.RepositoryError): source_bundle.validate_repository(bad)
        self.assertEqual(source_bundle.load_repository(str(self.root))['eligibility_policy'], 'directed-evidence-v2')

    def test_tampering_original_text_offsets_sampling_raw_and_hashes_is_rejected(self):
        self.put('main.py', 'source="data/a.json"\n')
        self.put('data/a.json', json.dumps([{'question': f'original {i}'} for i in range(8)]))
        snapshot = self.snapshot()
        edits = [lambda x: x['data_witnesses'][0].update(text='forged'),
                 lambda x: x['data_witnesses'][0].update(byte_start=0),
                 lambda x: x['data_witnesses'][0].update(line_start=99),
                 lambda x: x['data_witnesses'][0].update(sha256='0' * 64),
                 lambda x: x['data_witnesses'][0].update(coverage='complete'),
                 lambda x: x['data_blobs'][0]['coverage'].update(complete=True),
                 lambda x: x['data_blobs'][0].update(raw_base64=base64.b64encode(b'[]').decode()),
                 lambda x: x['data_blobs'].clear(),
                 lambda x: x['evidence_expansion'].update(data_coverage_complete=True)]
        for edit in edits:
            bad = copy.deepcopy(snapshot); edit(bad)
            with self.assertRaises(source_bundle.RepositoryError): source_bundle.validate_repository(bad)

    def test_metadata_only_validator_rebuilds_witnesses_without_file_segments(self):
        self.put('main.py', 'source="data/a.json"\n')
        self.put('data/a.json', json.dumps([{'question': f'original {i}'} for i in range(8)]))
        snapshot = self.snapshot()
        metadata = {key: value for key, value in snapshot.items() if key not in {'files', 'segments'}}
        source_bundle.validate_data_evidence(metadata)
        edits = [lambda x: x['data_witnesses'][0].update(text='forged'),
                 lambda x: x['data_witnesses'][0].update(byte_start=0),
                 lambda x: x['data_witnesses'][0].update(coverage='complete'),
                 lambda x: x['data_blobs'][0]['coverage'].update(complete=True),
                 lambda x: x['data_blobs'][0].update(output_budget=1)]
        for edit in edits:
            bad = copy.deepcopy(metadata); edit(bad)
            with self.assertRaises(source_bundle.RepositoryError): source_bundle.validate_data_evidence(bad)

    def git(self, *args):
        return subprocess.run(['git', '-c', 'commit.gpgsign=false', '-C', str(self.root), *args], capture_output=True, check=True).stdout.decode().strip()

    def test_local_git_raw_and_witness_hashes_bind_to_committed_blob(self):
        self.git('init', '-q'); self.git('config', 'user.name', 'Fixture'); self.git('config', 'user.email', 'fixture@example.test')
        self.put('main.py', 'source="data/a.json"\n')
        raw = b'[{"question":"committed original"}]\r\n'
        self.put('data/a.json', raw)
        self.git('add', '.'); self.git('commit', '-qm', 'fixture')
        self.put('data/a.json', 'WORKTREE CHANGE MUST NOT BE READ')
        snapshot = self.snapshot()
        oid = hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
        self.assertEqual(snapshot['data_blobs'][0]['object_id'], oid)
        self.assertEqual(snapshot['data_witnesses'][0]['object_id'], oid)
        self.assertEqual(base64.b64decode(snapshot['data_blobs'][0]['raw_base64']), raw)
        with self.assertRaises(ValueError):
            data_witnesses.build({'path': 'data/a.json', 'bytes': len(raw), 'object_id': 'b' * 40}, raw)
        source_bundle.validate_repository(snapshot)

    def test_metadata_raw_reslicing_cannot_change_pinned_blob_or_git_tree(self):
        self.git('init', '-q'); self.git('config', 'user.name', 'Fixture'); self.git('config', 'user.email', 'fixture@example.test')
        self.put('main.py', 'source="data/a.json"\n')
        self.put('data/a.json', '[{"question":"original"}]')
        self.git('add', '.'); self.git('commit', '-qm', 'fixture')
        snapshot = self.snapshot()
        metadata = {key: value for key, value in snapshot.items() if key not in {'files', 'segments'}}
        source_bundle.validate_data_evidence(metadata)
        raw = b'[{"question":"forgery!"}]'  # Same original length, entirely rehashed.
        entry = next(e for e in metadata['evidence_manifest'] if e['path'] == 'data/a.json')
        forged_entry = {**entry, 'object_id': data_witnesses.git_blob(raw, entry['object_id'])}
        blob, witnesses = data_witnesses.build(forged_entry, raw)
        bad = copy.deepcopy(metadata)
        # Raw+SHA256+excerpt metadata changed, Git blob identity retained.
        blob['object_id'] = entry['object_id']
        bad.update(data_blobs=[blob], data_witnesses=witnesses)
        with self.assertRaisesRegex(source_bundle.RepositoryError, 'Git blob'):
            source_bundle.validate_data_evidence(bad)
        # Even changing the saved leaf ID cannot retain the original Git tree.
        blob['object_id'] = forged_entry['object_id']
        next(e for e in bad['evidence_manifest'] if e['path'] == entry['path']).update(object_id=forged_entry['object_id'])
        with self.assertRaisesRegex(source_bundle.RepositoryError, 'pinned Git tree'):
            source_bundle.validate_data_evidence(bad)

    def test_remote_bytes_larger_than_old_source_cap_are_bounded_and_blob_checked(self):
        from test_source_only import SourceOnlyTests, COMMIT, REPOSITORY
        raw = json.dumps([{'text': 'x' * 20000} for _ in range(115)]).encode()
        self.assertGreater(len(raw), source_bundle.MAX_FILE_BYTES)
        mock, requested = SourceOnlyTests().fixture({'main.py': b'source="data/a.json"\n', 'data/a.json': raw,
                                                    'data/unrelated.json': b'NEVER_FETCH'})
        with mock:
            snapshot = source_bundle.load_repository(REPOSITORY, revision=COMMIT, fetch_mode='files', evidence_policy=evidence_expansion.DATA_POLICY)
        self.assertEqual(base64.b64decode(snapshot['data_blobs'][0]['raw_base64']), raw)
        self.assertFalse(any('unrelated' in url for url in requested))
        self.assertEqual(snapshot['data_blobs'][0]['object_id'], hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest())
        source_bundle.validate_repository(snapshot)

    def test_archive_uses_same_exact_data_policy(self):
        commit = 'a' * 40
        raw = io.BytesIO()
        with tarfile.open(fileobj=raw, mode='w:gz') as archive:
            for path, content in {'main.py': b'source="data/a.json"\n', 'data/a.json': b'[{"q":"author original"}]'}.items():
                info = tarfile.TarInfo('repo-' + commit + '/' + path)
                info.size = len(content); archive.addfile(info, io.BytesIO(content))
        with patch.object(source_bundle, '_download_archive', return_value=raw.getvalue()):
            snapshot = source_bundle.load_repository('https://github.com/example/repo', revision=commit, evidence_policy=evidence_expansion.DATA_POLICY)
        self.assertEqual(snapshot['data_witnesses'][0]['text'], '{"q":"author original"}')
        source_bundle.validate_repository(snapshot)


if __name__ == '__main__': unittest.main()
