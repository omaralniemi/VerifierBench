# VerifierBench package

Purpose: reproduce the released numerical checks for VerifierBench.

## Run

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/reproduce_all.py
```

Outputs are written under:

```text
results/tables/
results/figures/
results/validation/
```

## Folder map

```text
data/tasks/                 MicroBench-300 JSON
<data>/corpus/              corpus manifest
<data>/schemas/             JSON schemas
runs/baseline/              control run files
runs/inject_E2/             E2 perturbation files
runs/inject_E3/             E3 perturbation files
runs/sensitivity/           sensitivity outputs
runs/per_tool_cost/         per-tool/cost outputs
src/                        reusable Python modules
scripts/                    reproduction commands
```

## Main commands

```bash
python scripts/generate_microbench.py
python scripts/verify_hashes.py
python scripts/validate_package.py
python scripts/reproduce_tables.py
python scripts/reproduce_figures.py
python scripts/audit_package.py
```

`reproduce_all.py` runs the same sequence.

## Generated table CSVs

```text
results/tables/table4_baseline_metrics.csv
results/tables/table5_perturbation_metrics.csv
results/tables/table6_diagnostic_breakdown.csv
results/tables/table7_evaluator_comparison.csv
```

Tables 1-3 are prepared in the article text; the files above correspond to the computed result tables.

## Locked checks

```text
MicroBench-300 tasks = 300
expected steps       = 1497
baseline controls    = ETR 1.000 / E2E 1.000
AgentSkip            = ETR 0.742819 / E2E 0.143333 / E1 385
inject_E2            = ETR 0.939880 / E2E 0.700000 / E2 90
inject_E3            = ETR 0.682699 / E2E 0.103333 / E3 475
```

## Evidence notes

```text
baseline     : reports + claims + traces + artifacts + SHA-256 manifest
inject_E2    : reports + claims + traces + artifacts + SHA-256 manifest
inject_E3    : compact normalized evaluation bundle; see runs/inject_E3/EVIDENCE_NOTE.md
```

## Availability text

Use a public URL only after the repository is made public.

```text
The implementation code and reproducibility package will be made publicly available at: https://github.com/omaralniemi/VerifierBench upon publication.```

For review-stage private release, use supplementary upload plus the wording requested by the journal/editor.

## License

See `LICENSE`.
