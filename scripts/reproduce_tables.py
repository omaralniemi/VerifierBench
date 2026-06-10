#!/usr/bin/env python
from pathlib import Path
import pandas as pd

out=Path('results/tables'); out.mkdir(parents=True, exist_ok=True)
base=pd.read_csv('runs/baseline/metrics_summary.csv')
e2=pd.read_csv('runs/inject_E2/metrics_summary.csv')
e3=pd.read_csv('runs/inject_E3/metrics_summary.csv')
base_tax=pd.read_csv('runs/baseline/taxonomy_counts.csv')
e2_tax=pd.read_csv('runs/inject_E2/taxonomy_counts.csv')
e3_tax=pd.read_csv('runs/inject_E3/taxonomy_counts.csv')
base_sla=pd.read_csv('runs/baseline/sla_summary.csv')
e2_sla=pd.read_csv('runs/inject_E2/sla_summary.csv')
e3_sla=pd.read_csv('runs/inject_E3/sla_summary.csv')

# Table 4 in the manuscript: Baseline metrics on MicroBench-300.
t4=base[['agent','n_tasks','n_steps','ETR','CTR','TCV','E2E','E2E_T']].copy()
t4.columns=['Agent','Tasks','Steps','ETR','CTR','TCV','E2E','E2E-T']
t4.to_csv(out/'table4_baseline_metrics.csv', index=False)

# Table 5 in the manuscript: Perturbation-specific metrics for WrongTool under E2/E3.
t5=pd.DataFrame([
    {'Condition':'E2 wrong-tool/op','Agent':'WrongTool', **e2.loc[e2.agent=='AgentWrongTool',['n_tasks','n_steps','ETR','CTR','TCV','E2E','E2E_T']].iloc[0].to_dict()},
    {'Condition':'E3 wrong-argument','Agent':'WrongTool', **e3.loc[e3.agent=='AgentWrongTool',['n_tasks','n_steps','ETR','CTR','TCV','E2E','E2E_T']].iloc[0].to_dict()},
])
t5['Tasks/Steps']=t5['n_tasks'].astype(int).astype(str)+'/'+t5['n_steps'].astype(int).astype(str)
t5=t5[['Condition','Agent','Tasks/Steps','ETR','CTR','TCV','E2E','E2E_T']]
t5.columns=['Condition','Agent','Tasks/Steps','ETR','CTR','TCV','E2E','E2E-T']
t5.to_csv(out/'table5_perturbation_metrics.csv', index=False)

# Table 6 in the manuscript: Diagnostic breakdown of target-fault tasks.
def diag_counts(tax_df, agent):
    g=tax_df[tax_df.agent==agent]
    return '; '.join([f"{r.taxonomy}={int(r['count'])}" for _,r in g.iterrows()])
def injected(sla_df, agent):
    x=sla_df[sla_df.agent==agent]
    if len(x)==0: return '0', 'N/A', 'N/A'
    return int(x.injected_tasks.iloc[0]), x.SLA.iloc[0], x.True_SLA.iloc[0]
rows=[]
for cond,agent,taxdf,sladf in [
    ('E2 wrong-tool/op','AgentCorrect',e2_tax,e2_sla),
    ('E2 wrong-tool/op','AgentSelfCheck',e2_tax,e2_sla),
    ('Missing-event skip','AgentSkip',base_tax,base_sla),
    ('E2 wrong-tool/op','AgentWrongTool',e2_tax,e2_sla),
    ('E3 wrong-argument','AgentWrongTool',e3_tax,e3_sla),
]:
    inj,sla,tsla=injected(sladf,agent)
    rows.append({'Condition':cond,'Agent':agent.replace('Agent',''),'Target-fault tasks':inj,'Diagnostic counts':diag_counts(taxdf,agent),'SLA':sla,'True-SLA':tsla})
t6=pd.DataFrame(rows)
t6.to_csv(out/'table6_diagnostic_breakdown.csv', index=False)

# Table 7 in the manuscript: diagnostic comparison with reproducible evaluator baselines.
def matched_event_score(run):
    df=pd.read_csv(f'runs/{run}/verification_report.csv')
    return df.groupby('agent')['matched_event'].mean().to_dict()
comparison=pd.DataFrame([
    {'Evaluation view':'Outcome-only evaluator','Signal':'Final task success (E2E)','AgentSkip':base.loc[base.agent=='AgentSkip','E2E'].iloc[0],'E2 WrongTool':e2.loc[e2.agent=='AgentWrongTool','E2E'].iloc[0],'E3 WrongTool':e3.loc[e3.agent=='AgentWrongTool','E2E'].iloc[0],'Diagnostic resolution':'Pass/fail only; no failure type or first step'},
    {'Evaluation view':'Trajectory/event-presence evaluator','Signal':'Expected step has recorded event','AgentSkip':matched_event_score('baseline')['AgentSkip'],'E2 WrongTool':matched_event_score('inject_E2')['AgentWrongTool'],'E3 WrongTool':matched_event_score('inject_E3')['AgentWrongTool'],'Diagnostic resolution':'Shows omitted events, but not wrong arguments or evidence failure'},
    {'Evaluation view':'Function-call matching evaluator','Signal':'Tool/op/argument validity (TCV)','AgentSkip':base.loc[base.agent=='AgentSkip','TCV'].iloc[0],'E2 WrongTool':e2.loc[e2.agent=='AgentWrongTool','TCV'].iloc[0],'E3 WrongTool':e3.loc[e3.agent=='AgentWrongTool','TCV'].iloc[0],'Diagnostic resolution':'Detects call-level mismatch; no artifact/hash localization'},
    {'Evaluation view':'VerifierBench trace-evidence evaluator','Signal':'Trace + claim + evidence relation + taxonomy','AgentSkip':'E0=1112; E1=385','E2 WrongTool':'E0=1407; E2=90','E3 WrongTool':'E0=1022; E3=475','Diagnostic resolution':'Failure type and first-failure localization under controlled target-fault denominators'},
])
comparison.to_csv(out/'table7_evaluator_comparison.csv', index=False)

# Backward-compatible aliases for older manuscript drafts are intentionally not written.
written=[p.name for p in sorted(out.glob('table*.csv'))]
print('Wrote:', ', '.join(written))
