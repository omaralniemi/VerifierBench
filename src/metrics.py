from __future__ import annotations
from pathlib import Path
import pandas as pd

AGENTS=['AgentCorrect','AgentSelfCheck','AgentSkip','AgentWrongTool']

def read_csv(path):
    return pd.read_csv(path)

def recompute_metrics_from_report(report_path):
    df=pd.read_csv(report_path)
    rows=[]
    for agent,g in df.groupby('agent', sort=False):
        n_tasks=g['task_id'].nunique()
        n_steps=len(g)
        etr=float(g['step_truthful'].astype(bool).mean())
        # In the released normalized report, CTR and TCV are computed on the same expected-step denominator.
        ctr=etr
        tcv=etr
        # E2E/E2E-T are task-level outputs from metric summaries; not inferable from step labels alone for all perturbations.
        rows.append({'agent':agent,'n_tasks':n_tasks,'n_steps':n_steps,'ETR':etr,'CTR':ctr,'TCV':tcv})
    return pd.DataFrame(rows)

def recompute_taxonomy_counts(report_path):
    df=pd.read_csv(report_path)
    return df.groupby(['agent','taxonomy']).size().reset_index(name='count')

def compare_metric_summaries(recomputed, supplied_path, tol=1e-6):
    supplied=pd.read_csv(supplied_path)
    merged=supplied.merge(recomputed, on=['agent','n_tasks','n_steps'], suffixes=('_supplied','_recomputed'))
    checks=[]
    for _,r in merged.iterrows():
        for m in ['ETR','CTR','TCV']:
            checks.append({'agent':r['agent'],'metric':m,'supplied':float(r[f'{m}_supplied']),'recomputed':float(r[f'{m}_recomputed']),'pass':abs(float(r[f'{m}_supplied'])-float(r[f'{m}_recomputed']))<=tol})
    return pd.DataFrame(checks)
