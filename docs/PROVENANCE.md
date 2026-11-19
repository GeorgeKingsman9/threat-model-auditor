# Evidence provenance and release boundary

The included records were manually curated before this release. The CLI replays
their normalization and verdicts. It does not fetch sources, authenticate claims,
or reproduce historical attack experiments. Publication of these metadata does
not turn the records into independently verified findings.

The original `reference` strings are retained to preserve the existing pilot.
Paths beginning `papers/`, `repository/`, `analysis/`, or `results/` refer to the
research archive used during annotation, **not files bundled in this repository**.
The upstream mappings below were checked against local vendored revisions. They
identify public sources for further review, not public copies of local run logs.

## Records with public references already in the JSON

AdapTools, MUZZLE, FHA, AGENTCON, Overcoming the Retrieval Barrier, LIAR, and
ICoA include paper URLs and, for ICoA, pinned source URLs. A paper's description
of its own procedure is distinct from an independently observed execution.
The normalized `present` value does not erase this evidence-type distinction;
read `source_group`, the reference and the fixed scope together.

## Records that also depend on local archive references

| Paper | Public source mapping | Material not included here |
| --- | --- | --- |
| ASPI | Pinned paper and source links below | Historical audit reports and local reconstruction notes |
| ObliInjection | Pinned paper and source links below | Local matched-run report and historical Table XI generator inputs |
| WebTrap | Pinned paper and source links below | Saved local requests and local context-effect experiments |
| Blind Spots in the Guard | [Paper version](https://arxiv.org/html/2605.22001v1) | Local audit/source archive and experiment provenance; no public source mapping established for this release |

### ASPI

Paper: [arXiv:2605.17324v1](https://arxiv.org/html/2605.17324v1).
Source revision: `e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d`.

- [Stage 1 designer input](https://github.com/scaleapi/aspi/blob/e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d/src/aspi/dataset/pipeline.py#L106-L122)
- [Stage 2 direct-user input](https://github.com/scaleapi/aspi/blob/e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d/src/aspi/dataset/pipeline.py#L125-L139)
- [Slot-deleted partial-query construction](https://github.com/scaleapi/aspi/blob/e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d/src/aspi/prompts/dataset.py#L89-L99)

The normalized finding concerns the direct-user `clarif_user` baseline and the
specified knowledge boundary. It must not be generalized to `clarif_ask_user`
or treated as evidence about all experimental arms.

### ObliInjection

Paper: [arXiv:2512.09321v3](https://arxiv.org/html/2512.09321v3).
Source revision: `b1f6a3f48c0cf121534374cbcef453832594867b`.

- [HotpotQA configuration](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/configs/task_configs/hotpotqa_config.json#L14-L26)
- [Target-task data handling](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L246-L307)
- [Released optimizer](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/obliinjection.py#L25-L93)
- [Attacker input construction](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/attacker/attacker.py#L106-L123)

The released full-question path and the historical Table XI procedure are
different questions. Public optimizer code does not establish the historical
generator's inputs; that internal check remains unresolved.

### WebTrap

Paper: [arXiv:2605.08310v1, §4.1](https://arxiv.org/html/2605.08310v1#S4.SS1).
Source revision: `f8255c83d4a569fc374198b67717fcbee17af1fb`.

- [File-case construction](https://github.com/liuyaojialiuyaojia/WebTrap/blob/f8255c83d4a569fc374198b67717fcbee17af1fb/file/exp/exp1/build_cases_top20.py#L326-L343)
- [Injection input handling](https://github.com/liuyaojialiuyaojia/WebTrap/blob/f8255c83d4a569fc374198b67717fcbee17af1fb/file/exp/attack/psaa/inject.py#L193-L215)
- [Prompt construction](https://github.com/liuyaojialiuyaojia/WebTrap/blob/f8255c83d4a569fc374198b67717fcbee17af1fb/file/exp/attack/psaa/inject.py#L421-L440)
- [Associated configuration](https://github.com/liuyaojialiuyaojia/WebTrap/blob/f8255c83d4a569fc374198b67717fcbee17af1fb/file/exp/attack/psaa/file_psaa_v1.yaml#L124-L134)

These sources expose the released construction path. The separate assertion
about saved local execution requests relies on archive records not shipped here.

## Interpreting agreement

The gold labels are the authors' expected judgments for these curated scopes.
They were used during development. Agreement measures regression stability on
these records, not independent validation of the evidence, generalization to
unseen papers, or automatic extraction accuracy.

No upstream paper PDFs, original attack payloads, credentials, model outputs or
complete experiment logs are bundled. Upstream licenses remain applicable.
