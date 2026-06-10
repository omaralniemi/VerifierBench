"""VerifierBench trace-evidence validation utilities.

The package contains two levels of reproducibility support:

1. `verification_report.csv` files are the locked step-level outputs of the
   VerifierBench trace-evidence verifier. They are the canonical per-step labels
   used to recompute ETR, CTR, TCV, taxonomy counts, and the manuscript tables.
2. Raw or normalized task specifications, claim logs, event traces, and artifact
   hash records are included under `runs/*/` for auditability. The helper
   functions below validate their schema consistency and verify the released
   normalized reports without invoking any LLM.
"""
from __future__ import annotations
from pathlib import Path
import json
import pandas as pd
from .metrics import recompute_metrics_from_report, recompute_taxonomy_counts

REQUIRED_COLUMNS={
    'run_id','agent','task_id','step_id','expected_tool','expected_op',
    'expected_relation_type','matched_event','event_tool','event_op',
    'expected_pass','taxonomy','step_truthful'
}
VALID_TAXONOMY={'E0','E1','E2','E3','E6'}

def validate_verification_report(path):
    """Validate a locked per-step verification report and return a compact summary."""
    df=pd.read_csv(path)
    missing=sorted(REQUIRED_COLUMNS-set(df.columns))
    if missing:
        raise ValueError(f'Missing required columns in {path}: {missing}')
    if not set(df['taxonomy'].dropna()).issubset(VALID_TAXONOMY):
        raise ValueError(f'Unexpected taxonomy labels in {path}')
    if df[['agent','task_id','step_id']].duplicated().any():
        raise ValueError(f'Duplicate agent/task/step rows in {path}')
    return {
        'path':str(path),
        'rows':len(df),
        'agents':sorted(df.agent.unique()),
        'tasks':int(df.task_id.nunique()),
        'steps_per_agent':df.groupby('agent').size().to_dict(),
        'taxonomy_labels':sorted(df.taxonomy.dropna().unique()),
    }

def _load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))

def audit_run_evidence(run_dir: str|Path) -> dict:
    """Audit that a run directory contains the expected evidence files.

    This checks the presence and basic consistency of task specifications, claim
    logs, event traces, artifact-hash records, and the verification report. It is
    intentionally deterministic and does not call external services.
    """
    run_dir=Path(run_dir)
    report=run_dir/'verification_report.csv'
    summary=validate_verification_report(report)
    evidence={
        'tasks_json':(run_dir/'tasks.json').exists(),
        'claims_json':(run_dir/'claims.json').exists(),
        'events_jsonl':(run_dir/'events.jsonl').exists(),
        'artifacts_sha256_json':(run_dir/'artifacts_sha256.json').exists(),
    }
    if evidence['events_jsonl']:
        n_events=sum(1 for _ in (run_dir/'events.jsonl').open('r',encoding='utf-8'))
        evidence['event_records']=n_events
    if evidence['claims_json']:
        claims=_load_json(run_dir/'claims.json')
        evidence['claim_agents']=sorted(claims.keys())
    if evidence['tasks_json']:
        tasks=_load_json(run_dir/'tasks.json')
        evidence['task_agents']=sorted(tasks.get('by_agent',{}).keys())
    summary['evidence_files']=evidence
    return summary
