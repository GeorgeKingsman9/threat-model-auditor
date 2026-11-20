"""Offline role/instance binding tests on synthetic paper and source snapshots.

The review votes exercise deterministic gates, not independent model accuracy.
No model, network, curated cases or expected-label files are used.
"""

import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import extraction_v4 as v4
import extraction_v5 as v5
import test_extraction_v4 as toy


def cite(part, quote):
    return {"segment_id": part, "quote": quote}


class ExtractionV5Tests(unittest.TestCase):
    def fixtures(self):
        paper, repository, document, extraction, review = toy.ExtractionV4Tests().fixtures()
        extraction["schema_version"] = review["schema_version"] = 5
        flow = extraction["flows"][0]
        flow["edge"]["role"] = "attacker_constructor"
        request = copy.deepcopy(flow["code_path"][2]["citation"])
        # The named flow terminates at construction input. Evaluation record
        # alignment is shown separately by the artifact's saved/loaded case ID.
        flow["code_path"] = flow["code_path"][:2] + [
            {"kind": "request", "input_symbol": "build.prompt", "output_symbol": "backend.request",
             "citation": request, "explanation": "Bind the prompt in this construction request."},
            {"kind": "delivery", "input_symbol": "backend.request", "output_symbol": "constructor.input",
             "citation": request, "explanation": "The named constructor receives that argument."},
        ]
        flow["delivery"]["citation"] = copy.deepcopy(request)
        flow["binding"] = {
            "recipient_role": "attacker_constructor", "attacker_delivery": "confirmed",
            "instance_requirement": "same_evaluated_instance", "instance_relation": "same",
            "recipient_citation": copy.deepcopy(request),
            "instance_citations": [
                cite("repo:generator.py:L1-L6", 'save_artifact(case["id"], reply)'),
                cite("repo:evaluator.py:L1-L4", 'reply = read_artifact(case["id"])'),
            ],
            "instance_mapping": {
                "identity_basis": "stable_id_transform",
                "source_identity": {"configuration": "", "path": "generator.py", "record": 'case["id"]'},
                "evaluation_identity": {"configuration": "", "path": "evaluator.py", "record": 'case["id"]'},
                "transformation_reason": "The constructor saves by stable case ID and evaluation loads the same artifact by that ID.",
            },
            "exclusion_citation": None,
            "reason": "The shared rule concerns this evaluated request and the constructor receives it.",
        }
        review["flow_reviews"][0].update(binding_supported=True, instance_alignment_supported=True,
                                          exclusion_supported=False)
        return paper, repository, document, extraction, review

    def decide(self, extraction, review, document):
        return v5.decide_extraction(extraction, review, document, "toy_v5")

    def assert_unresolved(self, result):
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertFalse(result["has_confirmed_inconsistency"])
        self.assertEqual(result["evidence"][0]["claim_result"], "unresolved")

    def add_source(self, paper, repository, extraction, review, part):
        repository = toy.source_bundle(repository["segments"] + [part])
        document = v5.combine_inputs(paper, repository)
        extraction["input_binding"] = review["input_binding"] = document["sha256"]
        return document

    def set_non_model_boundary(self, flow, part, role):
        source = cite(part["id"], 'request = case["user_request"]')
        receipt = cite(part["id"], "return receiver.accept(request)")
        flow["edge"]["role"] = role
        flow["implementation"] = copy.deepcopy(receipt)
        flow["delivery"]["citation"] = copy.deepcopy(receipt)
        flow["binding"]["recipient_role"] = role
        flow["binding"]["recipient_citation"] = copy.deepcopy(receipt)
        flow["binding"]["attacker_delivery"] = "confirmed" if role == "attacker_optimizer" else "unresolved"
        flow["code_path"] = [
            {"kind": "source", "input_symbol": "case.user_request", "output_symbol": "receiver.request",
             "citation": source, "explanation": "Read the task record for the named input."},
            {"kind": "delivery", "input_symbol": "receiver.request", "output_symbol": role + ".input",
             "citation": receipt, "explanation": "Deliver to the actual named receiver."},
        ]

    def test_same_normalized_edge_has_reviewed_role_and_instance_binding(self):
        _, _, document, extraction, review = self.fixtures()
        before = copy.deepcopy((extraction, review, document))
        result = self.decide(extraction, review, document)
        self.assertEqual(result["schema_version"], 5)
        self.assertEqual(result["verdict"], "inconsistent")
        row = result["evidence"][0]
        self.assertEqual(row["validation_mode"], "flow_binding_v1")
        self.assertEqual(row["target"]["role"], "attacker_constructor")
        self.assertEqual(row["flow_binding"], {
            "semantics_version": 1, "observation_target": "matched_edge",
            "recipient_role": "attacker_constructor", "attacker_delivery": "confirmed",
            "instance_requirement": "same_evaluated_instance", "instance_relation": "same",
            "alignment_verified": True, "exclusion_verified": False,
        })
        self.assertEqual(len(row["binding_validation"]["locators"]["instances"]), 2)
        self.assertEqual((extraction, review, document), before)

    def test_v4_raw_source_contract_and_input_hash_are_preserved(self):
        _, _, document, extraction, review = self.fixtures()
        self.assertEqual(v5.model_content(document), v4.model_content(document))
        changed = copy.deepcopy(document)
        changed["segments"][0]["text"] += " changed after preparation"
        with self.assertRaisesRegex(ValueError, "input binding"):
            self.decide(extraction, review, changed)
        for output in (extraction, review):
            output["input_binding"] = "wrong-input"
            with self.assertRaisesRegex(ValueError, "input binding"):
                self.decide(extraction, review, document)
            output["input_binding"] = document["sha256"]
        self.assertNotEqual(v5.prompt_hash(), v4.prompt_hash())
        self.assertEqual(len(v5.prompt_hash()), 64)

    def test_missing_instance_obligation_survives_uncertain_policy_and_empty_path_hints(self):
        _, _, document, extraction, review = self.fixtures()
        flow = extraction["flows"][0]
        flow["scope_resolution"]["basis"] = "unresolved"
        flow["policy_application"]["status"] = "uncertain"
        flow["binding"]["instance_relation"] = "unknown"
        flow["binding"]["instance_citations"] = []
        flow["binding"]["instance_mapping"] = {
            "identity_basis": "unresolved", "source_identity": {"configuration": "", "path": "", "record": ""},
            "evaluation_identity": {"configuration": "", "path": "", "record": ""},
            "transformation_reason": "The necessary mapping has not been supplied."}
        review["flow_reviews"][0].update(policy_application="uncertain", scope_resolution_supported=False,
                                        instance_alignment_supported=False)
        result = self.decide(extraction, review, document)
        self.assert_unresolved(result)
        row = result["evidence"][0]
        self.assertEqual(row["missing_evidence"], [])
        self.assertEqual(row["missing_obligations"][0]["kind"], "same_instance_mapping")
        self.assertTrue(row["missing_obligations"][0]["conditional_on_policy_scope"])

    def test_python_multiline_call_span_and_separate_nearby_calls(self):
        paper, repository, _, extraction, review = self.fixtures()
        part = toy.code_segment("call_spans.py", (
            "def optimize(case, receiver):\n"
            '    request = case["user_request"]\n'
            "    return receiver.accept(\n"
            "        first=1,\n"
            "        second=2,\n"
            "        third=3,\n"
            "        request=request\n"
            "    )\n"
            "receiver.other()\n"
            "receiver.separate()\n"))
        document = self.add_source(paper, repository, extraction, review, part)
        locate = lambda quote: v4._locate(cite(part["id"], quote), document, "code")
        self.assertTrue(v5._same_input_boundary(locate("return receiver.accept("), locate("request=request"), document))
        self.assertFalse(v5._same_input_boundary(locate("receiver.other()"), locate("receiver.separate()"), document))
        self.assertFalse(v5._same_input_boundary(locate("def optimize(case, receiver):"), locate("request=request"), document))

    def test_missing_role_binding_does_not_destroy_independent_policy(self):
        for damage in ("missing_citation", "paper_citation", "review", "role_conflict"):
            with self.subTest(damage=damage):
                _, _, document, extraction, review = self.fixtures()
                flow = extraction["flows"][0]
                if damage == "missing_citation":
                    flow["binding"]["recipient_citation"] = None
                elif damage == "paper_citation":
                    flow["binding"]["recipient_citation"] = copy.deepcopy(flow["declaration"])
                elif damage == "review":
                    review["flow_reviews"][0]["binding_supported"] = False
                else:
                    flow["binding"]["recipient_role"] = "evaluator"
                result = self.decide(extraction, review, document)
                self.assert_unresolved(result)
                row = result["evidence"][0]
                self.assertTrue(row["source_validation"]["policy_supported"])
                self.assertFalse(row["flow_binding"]["alignment_verified"])
                self.assertEqual(row["flow_binding"]["attacker_delivery"], "unresolved")

    def test_instance_failure_preserves_observed_constructor_receipt(self):
        for damage in ("one_locator", "duplicate_locator", "paper_locator", "missing_mapping", "review"):
            with self.subTest(damage=damage):
                _, _, document, extraction, review = self.fixtures()
                binding = extraction["flows"][0]["binding"]
                if damage == "one_locator":
                    binding["instance_citations"] = binding["instance_citations"][:1]
                elif damage == "duplicate_locator":
                    binding["instance_citations"][1] = copy.deepcopy(binding["instance_citations"][0])
                elif damage == "paper_locator":
                    binding["instance_citations"][1] = copy.deepcopy(extraction["flows"][0]["declaration"])
                elif damage == "missing_mapping":
                    binding["instance_mapping"]["identity_basis"] = "unresolved"
                else:
                    review["flow_reviews"][0]["instance_alignment_supported"] = False
                result = self.decide(extraction, review, document)
                self.assert_unresolved(result)
                row = result["evidence"][0]
                self.assertEqual(row["flow_binding"]["instance_relation"], "unknown")
                self.assertEqual(row["flow_binding"]["attacker_delivery"], "confirmed")
                self.assertEqual({observation["status"] for observation in row["matching_observations"]}, {"present"})
                self.assertTrue(row["source_validation"]["delivery_supported"])

    def test_path_or_binding_review_failure_cannot_confirm_attacker_delivery(self):
        for axis in ("implementation_supported", "code_path_supported", "binding_supported"):
            with self.subTest(axis=axis):
                _, _, document, extraction, review = self.fixtures()
                review["flow_reviews"][0][axis] = False
                result = self.decide(extraction, review, document)
                self.assert_unresolved(result)
                self.assertEqual(result["evidence"][0]["flow_binding"]["attacker_delivery"], "unresolved")

    def test_policy_dispute_does_not_erase_independent_receiver_delivery(self):
        _, _, document, extraction, review = self.fixtures()
        review["flow_reviews"][0].update(supported=False, scope_resolution_supported=False)
        result = self.decide(extraction, review, document)
        self.assert_unresolved(result)
        row = result["evidence"][0]
        self.assertEqual(row["assessment"]["policy_application"]["status"], "uncertain")
        self.assertEqual(row["assessment"]["delivery"]["status"], "confirmed")
        self.assertEqual(row["flow_binding"]["instance_requirement"], "unspecified")
        self.assertEqual({observation["status"] for observation in row["matching_observations"]}, {"present"})

    def test_restricted_optimizer_input_is_terminal_without_llm_or_victim_call(self):
        paper, repository, _, extraction, review = self.fixtures()
        part = toy.code_segment("optimization.py", (
            "def optimize(case, receiver):\n"
            "    request = case[\"user_request\"]\n"
            "    return receiver.accept(request)\n"
        ))
        document = self.add_source(paper, repository, extraction, review, part)
        flow = extraction["flows"][0]
        self.set_non_model_boundary(flow, part, "attacker_optimizer")
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "inconsistent")
        self.assertEqual(result["evidence"][0]["flow_binding"]["recipient_role"], "attacker_optimizer")
        self.assertTrue(result["evidence"][0]["source_validation"]["delivery_supported"])
        self.assertNotIn("request", {step["kind"] for step in flow["code_path"]})

    def test_constructor_still_requires_the_generation_request_boundary(self):
        _, _, document, extraction, review = self.fixtures()
        extraction["flows"][0]["code_path"].pop(2)
        extraction["flows"][0]["code_path"][-1]["input_symbol"] = "build.prompt"
        result = self.decide(extraction, review, document)
        self.assert_unresolved(result)
        self.assertIn("source_path_requires_request_and_delivery", result["evidence"][0]["source_validation"]["validation_errors"])

    def test_delivery_endpoint_must_match_the_named_receiver(self):
        _, _, document, extraction, review = self.fixtures()
        flow = extraction["flows"][0]
        victim = cite("repo:evaluator.py:L1-L4", 'return victim.inject(reply)')
        flow["code_path"][-1]["citation"] = victim
        flow["delivery"]["citation"] = victim
        result = self.decide(extraction, review, document)
        self.assert_unresolved(result)
        self.assertIn("source_path_recipient_delivery_boundary_not_aligned", result["evidence"][0]["source_validation"]["validation_errors"])

    def test_adjacent_argument_and_receiver_citations_share_a_reviewed_boundary(self):
        paper, repository, _, extraction, review = self.fixtures()
        part = toy.code_segment("multiline_optimizer.py", (
            "def optimize(case, receiver):\n"
            '    request = case["user_request"]\n'
            "    return receiver.accept(\n"
            "        request\n"
            "    )\n"
        ))
        document = self.add_source(paper, repository, extraction, review, part)
        flow = extraction["flows"][0]
        source = cite(part["id"], 'request = case["user_request"]')
        receiver = cite(part["id"], "return receiver.accept(")
        argument = cite(part["id"], "request\n    )")
        flow["edge"]["role"] = "attacker_optimizer"
        flow["implementation"] = copy.deepcopy(receiver)
        flow["delivery"]["citation"] = copy.deepcopy(argument)
        flow["binding"].update(recipient_role="attacker_optimizer", recipient_citation=copy.deepcopy(receiver))
        flow["code_path"] = [
            {"kind": "source", "input_symbol": "case.user_request", "output_symbol": "optimizer.request",
             "citation": source, "explanation": "Read the task record."},
            {"kind": "delivery", "input_symbol": "optimizer.request", "output_symbol": "optimizer.input",
             "citation": argument, "explanation": "Bind the argument on the adjacent call line."},
        ]
        self.assertEqual(self.decide(extraction, review, document)["verdict"], "inconsistent")

    def test_evaluator_present_does_not_automatically_exclude_attacker_access(self):
        for proposed_delivery in ("unresolved", "excluded", "confirmed"):
            with self.subTest(proposed_delivery=proposed_delivery):
                paper, repository, _, extraction, review = self.fixtures()
                part = toy.code_segment("scoring.py", (
                    "def score(case, receiver):\n"
                    "    request = case[\"user_request\"]\n"
                    "    return receiver.accept(request)\n"
                ))
                document = self.add_source(paper, repository, extraction, review, part)
                flow = extraction["flows"][0]
                self.set_non_model_boundary(flow, part, "evaluator")
                flow["binding"]["attacker_delivery"] = proposed_delivery
                result = self.decide(extraction, review, document)
                self.assert_unresolved(result)
                row = result["evidence"][0]
                self.assertEqual(row["flow_binding"]["attacker_delivery"], "unresolved")
                self.assertFalse(row["flow_binding"]["exclusion_verified"])
                self.assertEqual({observation["status"] for observation in row["matching_observations"]}, {"present"})
                self.assertEqual(row["assessment"]["delivery"]["status"], "confirmed")

    def test_evaluator_scope_refutes_only_the_named_evaluator_edge(self):
        paper, repository, _, extraction, review = self.fixtures()
        part = toy.code_segment("scoring.py", (
            "def score(case, receiver):\n"
            "    request = case[\"user_request\"]\n"
            "    return receiver.accept(request)\n"
        ))
        document = self.add_source(paper, repository, extraction, review, part)
        flow = extraction["flows"][0]
        self.set_non_model_boundary(flow, part, "evaluator")
        flow["policy_application"]["status"] = "not_applicable"
        review["flow_reviews"][0]["policy_application"] = "not_applicable"
        result = self.decide(extraction, review, document)
        row = result["evidence"][0]
        self.assertEqual(row["claim_result"], "refuted")
        self.assertEqual(row["reason"], "bound_claim_refuted_evaluator_policy_inapplicable")
        self.assertEqual(row["flow_binding"]["attacker_delivery"], "unresolved")
        self.assertFalse(row["flow_binding"]["exclusion_verified"])

    def test_unknown_instance_does_not_defeat_a_reviewed_category_wide_ban(self):
        paper, repository, _, extraction, review = self.fixtures()
        rule = "The attacker constructor must not receive any task request from any instance."
        paper["segments"].append({"id": "p3", "text": rule})
        paper["text"] += "\n" + rule
        paper["sha256"] = toy.digest(paper["text"])
        document = v5.combine_inputs(paper, repository)
        extraction["input_binding"] = review["input_binding"] = document["sha256"]
        flow = extraction["flows"][0]
        declaration = cite("paper:p3", rule)
        flow["declaration"] = copy.deepcopy(declaration)
        flow["policy_application"]["citation"] = copy.deepcopy(declaration)
        flow["scope_resolution"].update(basis="specific_rule", common_rule=None,
                                          specific_rule=copy.deepcopy(declaration))
        flow["binding"].update(instance_requirement="any_instance", instance_relation="unknown",
                               instance_citations=[])
        flow["binding"]["instance_mapping"]["identity_basis"] = "unresolved"
        review["flow_reviews"][0]["instance_alignment_supported"] = False
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "inconsistent")
        self.assertEqual(result["evidence"][0]["flow_binding"]["instance_relation"], "unknown")
        review["flow_reviews"][0]["scope_resolution_supported"] = False
        self.assert_unresolved(self.decide(extraction, review, document))

    def test_different_instance_mapping_can_refute_instance_only_restriction(self):
        paper, repository, _, extraction, review = self.fixtures()
        part = toy.code_segment("disjoint_config.py", (
            'train_case = load_records("train.json")[17]\n'
            'eval_case = load_records("evaluation.json")[44]\n'
            'build(train_case, backend)\n'
            'evaluate(eval_case, "direct")\n'
        ))
        document = self.add_source(paper, repository, extraction, review, part)
        flow = extraction["flows"][0]
        binding = flow["binding"]
        binding["instance_citations"] = [
            cite(part["id"], 'train_case = load_records("train.json")[17]'),
            cite(part["id"], 'eval_case = load_records("evaluation.json")[44]'),
        ]
        binding["instance_mapping"] = {
            "identity_basis": "config_path_index",
            "source_identity": {"configuration": "disjoint_config.py", "path": "train.json", "record": "17"},
            "evaluation_identity": {"configuration": "disjoint_config.py", "path": "evaluation.json", "record": "44"},
            "transformation_reason": "The explicit caller selects training record 17 and a separate evaluation record 44; no shared-record remapping is claimed.",
        }
        flow["binding"]["instance_relation"] = "different"
        flow["policy_application"]["status"] = "not_applicable"
        flow["refutation"] = {"basis": "different_instance", "citation": copy.deepcopy(flow["binding"]["instance_citations"][1]),
                               "reason": "The reviewed map establishes another information instance."}
        review["flow_reviews"][0].update(policy_application="not_applicable", refutation="different_instance")
        result = self.decide(extraction, review, document)
        self.assertEqual(result["evidence"][0]["claim_result"], "refuted")
        self.assertEqual(result["evidence"][0]["reason"], "bound_claim_refuted_different_instance")
        flow["binding"]["instance_requirement"] = "any_instance"
        result = self.decide(extraction, review, document)
        self.assert_unresolved(result)

    def test_configuration_path_index_requires_all_identity_components(self):
        _, _, document, extraction, review = self.fixtures()
        mapping = extraction["flows"][0]["binding"]["instance_mapping"]
        mapping["identity_basis"] = "config_path_index"
        result = self.decide(extraction, review, document)
        self.assert_unresolved(result)
        errors = result["evidence"][0]["binding_validation"]["validation_errors"]
        self.assertIn("instance_mapping_source_identity_configuration_missing", errors)
        self.assertIn("instance_mapping_evaluation_identity_configuration_missing", errors)

    def test_filenames_or_equal_text_without_record_mapping_are_unknown(self):
        paper, repository, _, extraction, review = self.fixtures()
        part = toy.code_segment("split_config.py", 'train = "train.json"\ntest = "test.json"\n')
        document = self.add_source(paper, repository, extraction, review, part)
        binding = extraction["flows"][0]["binding"]
        binding["instance_citations"] = [cite(part["id"], 'train = "train.json"'),
                                         cite(part["id"], 'test = "test.json"')]
        mapping = binding["instance_mapping"]
        mapping["identity_basis"] = "config_path_index"
        mapping["source_identity"] = {"configuration": "train", "path": "train.json", "record": ""}
        mapping["evaluation_identity"] = {"configuration": "test", "path": "test.json", "record": ""}
        mapping["transformation_reason"] = "The files share a benchmark name and may share text."
        for relation in ("same", "different"):
            binding["instance_relation"] = relation
            result = self.decide(extraction, review, document)
            self.assert_unresolved(result)
            self.assertEqual(result["evidence"][0]["flow_binding"]["instance_relation"], "unknown")

    def test_config_and_path_can_be_proved_by_source_locator_metadata(self):
        _, _, document, extraction, review = self.fixtures()
        mapping = extraction["flows"][0]["binding"]["instance_mapping"]
        mapping["source_identity"]["configuration"] = "generator.py"
        mapping["evaluation_identity"]["configuration"] = "evaluator.py"
        mapping["identity_basis"] = "config_path_index"
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "inconsistent")

    def test_exclusion_needs_positive_citation_and_its_own_review_axis(self):
        _, _, document, extraction, review = self.fixtures()
        flow = extraction["flows"][0]
        flow["observation"] = "absent"
        flow["delivery"]["status"] = "excluded"
        flow["binding"]["attacker_delivery"] = "excluded"
        flow["refutation"] = {"basis": "excluded_delivery", "citation": copy.deepcopy(flow["delivery"]["citation"]),
                               "reason": "A proposed exclusion without a positive input-boundary argument."}
        review["flow_reviews"][0].update(delivery="excluded", refutation="excluded_delivery", exclusion_supported=True)
        result = self.decide(extraction, review, document)
        self.assert_unresolved(result)
        self.assertFalse(result["evidence"][0]["flow_binding"]["exclusion_verified"])
        self.assertEqual(result["evidence"][0]["flow_binding"]["attacker_delivery"], "unresolved")
        flow["binding"]["exclusion_citation"] = copy.deepcopy(flow["declaration"])
        self.assert_unresolved(self.decide(extraction, review, document))

    def test_positive_boundary_exclusion_has_independent_review(self):
        paper, repository, _, extraction, review = self.fixtures()
        part = toy.code_segment("public_only.py", (
            "def public_only(case, backend):\n"
            '    prompt = {"topic": case["topic"]}\n'
            '    assert "user_request" not in prompt\n'
            "    return backend.generate(prompt)\n"
        ))
        document = self.add_source(paper, repository, extraction, review, part)
        flow = extraction["flows"][0]
        source = cite(part["id"], 'prompt = {"topic": case["topic"]}')
        guard = cite(part["id"], 'assert "user_request" not in prompt')
        receipt = cite(part["id"], "return backend.generate(prompt)")
        flow["implementation"] = guard
        flow["observation"] = "absent"
        flow["delivery"].update(status="excluded", citation=copy.deepcopy(receipt))
        flow["binding"].update(attacker_delivery="excluded", recipient_citation=copy.deepcopy(receipt),
                               exclusion_citation=copy.deepcopy(guard))
        flow["code_path"] = [
            {"kind": "source", "input_symbol": "case.topic", "output_symbol": "public.prompt",
             "citation": source, "explanation": "Build only public topic context."},
            {"kind": "request", "input_symbol": "public.prompt", "output_symbol": "public.request",
             "citation": receipt, "explanation": "The checked public input is the construction request."},
            {"kind": "delivery", "input_symbol": "public.request", "output_symbol": "constructor.input",
             "citation": receipt, "explanation": "The constructor receives this guarded input."},
        ]
        flow["refutation"] = {"basis": "excluded_delivery", "citation": copy.deepcopy(guard),
                               "reason": "The public-only argument and guard exclude the forbidden request field at this boundary."}
        review["flow_reviews"][0].update(delivery="excluded", refutation="excluded_delivery", exclusion_supported=True)
        result = self.decide(extraction, review, document)
        self.assertEqual(result["evidence"][0]["claim_result"], "refuted")
        self.assertTrue(result["evidence"][0]["flow_binding"]["exclusion_verified"])
        review["flow_reviews"][0]["exclusion_supported"] = False
        self.assert_unresolved(self.decide(extraction, review, document))
        review["flow_reviews"][0]["exclusion_supported"] = True
        review["flow_reviews"][0]["code_path_supported"] = False
        result = self.decide(extraction, review, document)
        self.assert_unresolved(result)
        self.assertFalse(result["evidence"][0]["flow_binding"]["exclusion_verified"])

    def test_excess_instance_citations_cannot_replace_a_bounded_mapping(self):
        _, _, document, extraction, review = self.fixtures()
        binding = extraction["flows"][0]["binding"]
        binding["instance_citations"] = binding["instance_citations"] * 5
        result = self.decide(extraction, review, document)
        self.assert_unresolved(result)
        self.assertIn("instance_binding_exceeds_eight_citations", result["evidence"][0]["binding_validation"]["validation_errors"])

    def test_explicit_permission_refutes_permission_suspicion_without_proving_use(self):
        _, _, document, extraction, review = self.fixtures()
        flow = extraction["flows"][0]
        grant = cite("paper:p2", "Only the diagnostic oracle constructor is expressly allowed to receive the target request text")
        flow["declaration"] = copy.deepcopy(grant)
        flow["permission"] = "allow"
        flow["policy_application"]["citation"] = copy.deepcopy(grant)
        flow["scope_resolution"].update(basis="specific_rule", common_rule=None, specific_rule=copy.deepcopy(grant),
                                          override_dimension="diagnostic")
        flow["refutation"] = {"basis": "explicit_permission", "citation": copy.deepcopy(grant),
                               "reason": "The specific diagnostic arm expressly permits this knowledge."}
        flow["delivery"]["status"] = "unresolved"
        flow["binding"]["attacker_delivery"] = "unresolved"
        flow["observation"] = "possible"
        review["flow_reviews"][0].update(delivery="unresolved", refutation="explicit_permission", code_path_supported=False)
        result = self.decide(extraction, review, document)
        self.assertEqual(result["evidence"][0]["claim_result"], "refuted")
        self.assertEqual(result["evidence"][0]["reason"], "bound_claim_refuted_explicit_permission")
        self.assertEqual(result["evidence"][0]["flow_binding"]["attacker_delivery"], "unresolved")
        self.assertEqual(result["verdict"], "consistent_within_scope")
        # A permission proof does not depend on an unrelated omitted file.
        partial = copy.deepcopy(document)
        partial["coverage"]["complete"] = False
        partial["sha256"] = v4._hash_json(v4._binding_material(partial))
        extraction["input_binding"] = review["input_binding"] = partial["sha256"]
        scoped = self.decide(extraction, review, partial)
        self.assertEqual(scoped["verdict"], "consistent_within_scope")
        self.assertFalse(scoped["artifact_coverage"]["complete"])
        extraction["unresolved_questions"] = ["A further named branch still needs its policy resolved."]
        self.assertEqual(self.decide(extraction, review, partial)["verdict"], "insufficient_evidence")

    def test_review_order_is_by_explicit_index(self):
        _, _, document, extraction, review = self.fixtures()
        second = copy.deepcopy(extraction["flows"][0])
        second["claim"] = "A second independent named edge lacks instance mapping."
        second["binding"]["instance_citations"] = []
        extraction["flows"].append(second)
        second_review = copy.deepcopy(review["flow_reviews"][0])
        second_review.update(index=1, instance_alignment_supported=False)
        review["flow_reviews"] = [second_review, review["flow_reviews"][0]]
        result = self.decide(extraction, review, document)
        self.assertEqual([row["flow_binding"]["instance_relation"] for row in result["evidence"]], ["same", "unknown"])
        self.assertEqual([row["semantic_review"]["index"] for row in result["evidence"]], [0, 1])

    def test_invalid_schema_or_incomplete_review_is_rejected(self):
        _, _, document, extraction, review = self.fixtures()
        for mutate in (lambda e, r: e.update(schema_version=4),
                       lambda e, r: e["flows"][0]["binding"].update(recipient_role="offline_designer"),
                       lambda e, r: r["flow_reviews"].clear()):
            ext, rev = copy.deepcopy((extraction, review))
            mutate(ext, rev)
            with self.assertRaises(ValueError):
                self.decide(ext, rev, document)


if __name__ == "__main__":
    unittest.main()
