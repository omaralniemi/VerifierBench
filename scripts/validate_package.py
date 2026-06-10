#!/usr/bin/env python
from pathlib import Path
import sys, json
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.verifier import validate_verification_report, audit_run_evidence
from src.metrics import recompute_metrics_from_report, recompute_taxonomy_counts, compare_metric_summaries

RUNS=['baseline','inject_E2','inject_E3']
validation={'runs':{}, 'expected_checks':[], 'table_outputs':{}}
for run in RUNS:
    report=Path(f'runs/{run}/verification_report.csv')
    metrics=Path(f'runs/{run}/metrics_summary.csv')
    tax=Path(f'runs/{run}/taxonomy_counts.csv')
    validation['runs'][run]=audit_run_evidence(Path('runs')/run)
    recomputed=recompute_metrics_from_report(report)
    checks=compare_metric_summaries(recomputed, metrics)
    validation['runs'][run]['metric_recompute_pass']=bool(checks['pass'].all())
    recomputed.to_csv(f'results/validation/{run}_recomputed_step_metrics.csv', index=False)
    checks.to_csv(f'results/validation/{run}_metric_recompute_checks.csv', index=False)
    recompute_taxonomy_counts(report).to_csv(f'results/validation/{run}_recomputed_taxonomy_counts.csv', index=False)

# Headline manuscript checks.
def get_metric(run, agent, metric):
    df=pd.read_csv(f'runs/{run}/metrics_summary.csv')
    return float(df.loc[df.agent==agent, metric].iloc[0])
def get_tax(run, agent, tax):
    df=pd.read_csv(f'runs/{run}/taxonomy_counts.csv')
    x=df[(df.agent==agent)&(df.taxonomy==tax)]
    return int(x['count'].iloc[0]) if len(x) else 0
expected=[
 ('baseline AgentCorrect ETR', get_metric('baseline','AgentCorrect','ETR'), 1.0),
 ('baseline AgentSkip ETR', get_metric('baseline','AgentSkip','ETR'), 0.742819),
 ('baseline AgentSkip E2E', get_metric('baseline','AgentSkip','E2E'), 0.143333),
 ('inject_E2 AgentWrongTool ETR', get_metric('inject_E2','AgentWrongTool','ETR'), 0.939880),
 ('inject_E2 AgentWrongTool E2E', get_metric('inject_E2','AgentWrongTool','E2E'), 0.700000),
 ('inject_E3 AgentWrongTool ETR', get_metric('inject_E3','AgentWrongTool','ETR'), 0.682699),
 ('inject_E3 AgentWrongTool E2E', get_metric('inject_E3','AgentWrongTool','E2E'), 0.103333),
 ('baseline AgentSkip E1', get_tax('baseline','AgentSkip','E1'), 385),
 ('inject_E2 AgentWrongTool E2', get_tax('inject_E2','AgentWrongTool','E2'), 90),
 ('inject_E3 AgentWrongTool E3', get_tax('inject_E3','AgentWrongTool','E3'), 475),
]
for name, got, exp in expected:
    ok=abs(float(got)-float(exp)) <= 1e-6
    validation['expected_checks'].append({'name':name,'got':got,'expected':exp,'pass':ok})

# Manuscript-aligned table output names.
expected_tables=[
    'results/tables/table4_baseline_metrics.csv',
    'results/tables/table5_perturbation_metrics.csv',
    'results/tables/table6_diagnostic_breakdown.csv',
    'results/tables/table7_evaluator_comparison.csv',
]
for rel in expected_tables:
    validation['table_outputs'][rel]=Path(rel).exists()

out=Path('results/validation/package_validation_report.json')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(validation, indent=2), encoding='utf-8')
print(json.dumps(validation, indent=2))
if not all(c['pass'] for c in validation['expected_checks']) or not all(validation['runs'][r]['metric_recompute_pass'] for r in RUNS):
    raise SystemExit('Validation failed')
if not all(validation['table_outputs'].values()):
    raise SystemExit('Missing manuscript-aligned table output')
