"""Synthetic code-only channel discovery; no gold cases, providers or network."""

import copy
import hashlib
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from input_channels import candidate_citations_match, discover_channels


def document(**files):
    parts = [{"id": "paper:p1", "source_kind": "paper",
              "text": "An attacker sees all questions. optimize(secret_document)"}]
    for path, text in files.items():
        parts.append({"id": "repo:" + path + ":L1-L" + str(len(text.splitlines())),
                      "path": path, "text": text, "line_start": 1,
                      "line_end": len(text.splitlines()), "source_kind": "code",
                      "sha256": hashlib.sha256(text.encode()).hexdigest()})
    return {"segments": parts, "sha256": "synthetic-input-binding"}


class InputChannelTests(unittest.TestCase):
    def test_question_and_documents_in_one_request_remain_distinct_candidates(self):
        source = document(**{"constructor.py": (
            "def construct(question, documents, backend):\n"
            "    prompt = f'{question} / {documents}'\n"
            "    return backend.generate(prompt)\n")})
        before = copy.deepcopy(source)
        result = discover_channels(source)
        rows = result["candidates"]
        self.assertEqual({row["channel_kind"] for row in rows}, {"question", "documents"})
        self.assertEqual(len(rows), 2)
        self.assertEqual(len({row["id"] for row in rows}), 2)
        self.assertFalse(result["truncated"])
        for row in rows:
            self.assertEqual(row["status"], "candidate")
            self.assertNotIn("permission", row)
            self.assertNotIn("observation", row)
            self.assertEqual(row["call"], "backend.generate")
            part = next(part for part in source["segments"] if part["id"] == row["citation"]["segment_id"])
            self.assertIn(row["citation"]["quote"], part["text"])
        self.assertEqual(source, before)

    def test_opaque_optimization_in_attack_context_has_question_and_document_channels(self):
        source = document(**{"runner.py": (
            "def attack(record, receiver):\n"
            "    question_lst = record['question']\n"
            "    document_content = record['documents']\n"
            "    return receiver(question_lst, document_content)\n")})
        result = discover_channels(source)
        self.assertEqual({row["channel_kind"] for row in result["candidates"]}, {"question", "documents"})
        self.assertTrue(all(row["phase_hint"] == "construction_or_optimization_candidate"
                            for row in result["candidates"]))

    def test_evaluator_input_does_not_become_attacker_receipt(self):
        source = document(**{"evaluation.py": (
            "def evaluate(question, model):\n"
            "    return model.generate(question)\n")})
        rows = discover_channels(source)["candidates"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["role_hint"], "evaluator_candidate")
        self.assertEqual(rows[0]["status"], "candidate")
        self.assertNotIn("attacker_delivery", rows[0])

    def test_imported_wrapper_aliases_bind_to_actual_model_boundary(self):
        source = document(**{
            "main.py": (
                "from wrapper import send as deliver\n"
                "def attack(case):\n"
                "    alias = case['question']\n"
                "    return deliver(alias)\n"),
            "wrapper.py": (
                "def send(value):\n"
                "    return backend.generate(value)\n"),
        })
        result = discover_channels(source)
        rows = result["candidates"]
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["channel_kind"], "question")
        self.assertEqual(row["path"], "wrapper.py")
        self.assertEqual(row["call"], "backend.generate")
        self.assertEqual(row["symbol"], "case['question']")
        quotes = "\n".join(cite["quote"] for cite in row["bindings"])
        self.assertIn("from wrapper import send as deliver", quotes)
        self.assertIn("deliver(alias)", quotes)

    def test_mapping_get_and_named_input_arguments_remain_code_derived(self):
        source = document(**{"runner.py": (
            "def run(record, receiver, opaque):\n"
            "    alias = record.get('question')\n"
            "    return receiver.optimize(alias, feedback=opaque)\n")})
        rows = discover_channels(source)["candidates"]
        self.assertEqual({row["channel_kind"] for row in rows}, {"question", "feedback"})
        query = next(row for row in rows if row["channel_kind"] == "question")
        self.assertEqual(query["symbol"], "record.get('question')")

    def test_same_class_wrapper_binds_self_separately_from_message(self):
        source = document(**{"worker.py": (
            "class Worker:\n"
            "    def build(self, question):\n"
            "        return self.send(question)\n"
            "    def send(self, opaque):\n"
            "        return self.client.chat.completions.create(messages=opaque)\n")})
        rows = discover_channels(source)["candidates"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["channel_kind"], "question")
        self.assertEqual(rows[0]["call"], "self.client.chat.completions.create")
        self.assertTrue(any("self.send(question)" in c["quote"] for c in rows[0]["bindings"]))

    def test_wrapper_return_transform_can_preserve_separate_inputs(self):
        source = document(**{"runner.py": (
            "def package(value):\n"
            "    return {'task': value}\n"
            "def run(question, backend):\n"
            "    request = package(question)\n"
            "    return backend.generate(request)\n")})
        rows = discover_channels(source, max_trace_depth=8)["candidates"]
        self.assertEqual({row["channel_kind"] for row in rows}, {"question"})
        self.assertEqual(len(rows), 1)

    def test_source_labels_and_feedback_are_separate(self):
        source = document(**{"optimizer.py": (
            "def run(task, labels, feedback, receiver):\n"
            "    return receiver.optimize(task=task, labels=labels, feedback=feedback)\n")})
        rows = discover_channels(source)["candidates"]
        self.assertEqual({row["channel_kind"] for row in rows}, {"task", "labels", "feedback"})

    def test_comments_literal_prose_baseline_and_paper_do_not_create_proof(self):
        source = document(**{"baseline.py": (
            "# optimize(question, documents)\n"
            "description = 'attacker query documents'\n"
            "question = dataset['question']\n"
            "print(question)\n"
            "length = len(question)\n"
            "return_value = baseline_metric(question)\n")})
        self.assertEqual(discover_channels(source)["candidates"], [])
        source["segments"].append({"id": "paper:p2", "source_kind": "paper",
                                   "text": "backend.generate(secret_question)"})
        self.assertEqual(discover_channels(source)["candidates"], [])

    def test_builtins_logging_and_constructor_metadata_cannot_saturate_inventory(self):
        source = document(**{"attack.py": (
            "def attack(question, docs, model, logger):\n"
            "    check = any(question for question in docs)\n"
            "    check2 = all([question, docs])\n"
            "    logger.log(question=question, documents=docs)\n"
            "    log = WandBLogger(question, docs)\n"
            "    config = TargetLM(model_name=args.target_model, max_n_tokens=128)\n"
            "    prepared = model.tokenizer.apply_chat_template(question)\n"
            "    return model.generate(question, documents=docs, model_name=args.target_model)\n")})
        rows = discover_channels(source)["candidates"]
        self.assertEqual(len(rows), 2)
        self.assertEqual({row["channel_kind"] for row in rows}, {"question", "documents"})
        self.assertTrue(all(row["call"] == "model.generate" for row in rows))

    def test_question_alias_survives_index_selector_and_named_forwarding(self):
        source = document(**{"runner.py": (
            "def attack(optimizer, rows, args):\n"
            "    question_lst = rows[args.target_data_indices]\n"
            "    target_train_question = question_lst[args.target_data_indices]\n"
            "    return optimizer.run(question_lst=target_train_question)\n")})
        rows = discover_channels(source)["candidates"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["channel_kind"], "question")
        self.assertEqual(rows[0]["symbol"], "target_train_question")
        self.assertIn("target_train_question =", rows[0]["source_citation"]["quote"])

    def test_candidate_bound_ranks_attack_input_before_evaluator_calls(self):
        source = document(**{"a_eval.py": (
            "def evaluate(question, backend):\n"
            "    return backend.generate(question)\n"),
            "z_attack.py": "def attack(question, backend):\n    return backend.generate(question)\n"})
        result = discover_channels(source, max_candidates=1)
        self.assertTrue(result["truncated"])
        self.assertEqual(result["candidates"][0]["path"], "z_attack.py")
        self.assertEqual(result["statistics"]["total_candidates"], 2)

    def test_one_boundary_argument_and_kind_aggregates_multiple_origins(self):
        source = document(**{"runner.py": (
            "def attack(question, other_question, backend):\n"
            "    return backend.generate([question, other_question])\n")})
        rows = discover_channels(source)["candidates"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["channel_kind"], "question")

    def test_model_create_message_wrapper_keeps_task_channel(self):
        source = document(**{"worker.py": (
            "def run(message, model):\n"
            "    return model.create(messages=[UserMessage(content=message.task_spec, source='worker')])\n")})
        rows = discover_channels(source)["candidates"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["channel_kind"], "task")
        self.assertEqual(rows[0]["call"], "model.create")

    def test_same_named_variables_in_different_files_have_distinct_ids(self):
        code = "def run(question, backend):\n    return backend.generate(question)\n"
        rows = discover_channels(document(**{"a.py": code, "b.py": code}))["candidates"]
        self.assertEqual(len(rows), 2)
        self.assertEqual(len({row["id"] for row in rows}), 2)
        self.assertEqual({row["path"] for row in rows}, {"a.py", "b.py"})

    def test_candidate_file_character_node_and_trace_bounds_are_explicit(self):
        source = document(**{"a.py": "backend.generate(question, documents)\n",
                             "b.py": "backend.generate(task)\n"})
        cases = [({"max_candidates": 1}, "candidate_limit"),
                 ({"max_files": 1}, "file_or_character_limit"),
                 ({"max_chars": 1}, "file_or_character_limit"),
                 ({"max_ast_nodes": 1}, "ast_node_limit")]
        for limits, reason in cases:
            with self.subTest(limits=limits):
                result = discover_channels(source, **limits)
                self.assertTrue(result["truncated"])
                self.assertIn(reason, result["limitations"])
        chained = document(**{"a.py": "a = question\nb = a\nc = b\nbackend.generate(c)\n"})
        result = discover_channels(chained, max_trace_depth=1)
        self.assertTrue(result["truncated"])
        self.assertIn("trace_depth_limit", result["limitations"])
        for invalid in (0, -1, True, "2"):
            with self.assertRaises(ValueError):
                discover_channels(source, max_candidates=invalid)

    def test_parse_failures_and_non_python_coverage_are_explicit(self):
        result = discover_channels(document(**{"a.py": "def broken(\n", "b.js": "generate(question)"}))
        self.assertFalse(result["truncated"])
        self.assertFalse(result["discovery_complete"])
        self.assertIn("python_parse_failure", result["limitations"])
        self.assertIn("non_python_segments_not_traced", result["limitations"])
        self.assertEqual(result["candidates"], [])

    def test_declarative_witnesses_do_not_count_as_untraced_programs(self):
        source = document(**{"a.py": "backend.generate(question)\n", "config.json": '{"question": "example"}',
                             "config.yaml": "question: example\n", "config.toml": 'question = "example"',
                             "records.jsonl": '{"question": "sample"}\n', "README.md": "# Experiment\n"})
        result = discover_channels(source)
        self.assertTrue(result["discovery_complete"])
        self.assertEqual(len(result["candidates"]), 1)
        self.assertNotIn("non_python_segments_not_traced", result["limitations"])

    def test_exact_boundary_and_channel_origin_required_for_citation_gate(self):
        source = document(**{"a.py": (
            "question = record['question']\n"
            "documents = record['documents']\n"
            "backend.generate(question, documents)\n")})
        rows = discover_channels(source)["candidates"]
        question = next(row for row in rows if row["channel_kind"] == "question")
        documents = next(row for row in rows if row["channel_kind"] == "documents")
        self.assertFalse(candidate_citations_match(question, [documents["source_citation"], documents["citation"]], source))
        self.assertTrue(candidate_citations_match(question, [question["source_citation"], question["citation"]], source))
        self.assertFalse(candidate_citations_match(question, [question["source_citation"]], source))
        self.assertFalse(candidate_citations_match(question, [{"segment_id": "paper:p1", "quote": "all questions"}], source))

    def test_other_file_and_candidate_id_cannot_replace_source_citations(self):
        code = "question = record['question']\nbackend.generate(question)\n"
        source = document(**{"a.py": code, "b.py": code})
        rows = discover_channels(source)["candidates"]
        a, b = rows
        self.assertFalse(candidate_citations_match(a, [b["source_citation"], b["citation"]], source))
        self.assertFalse(candidate_citations_match(a, [{"segment_id": "paper:p1", "quote": a["id"]}], source))


if __name__ == "__main__":
    unittest.main()
