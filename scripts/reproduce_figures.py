#!/usr/bin/env python
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

out=Path('results/figures'); out.mkdir(parents=True, exist_ok=True)
base=pd.read_csv('runs/baseline/metrics_summary.csv')
e2=pd.read_csv('runs/inject_E2/metrics_summary.csv')
e3=pd.read_csv('runs/inject_E3/metrics_summary.csv')
# Figure 2a: baseline ETR by agent
plt.figure(figsize=(6,4))
plt.bar(base['agent'].str.replace('Agent',''), base['ETR'])
plt.ylabel('ETR'); plt.ylim(0,1.05); plt.title('Baseline execution truthfulness by agent')
plt.xticks(rotation=20, ha='right'); plt.tight_layout(); plt.savefig(out/'figure2a_baseline_etr.png', dpi=200); plt.close()
# Figure 2b: E2/E3 perturbation ETR for WrongTool
plt.figure(figsize=(5,4))
vals=[e2.loc[e2.agent=='AgentWrongTool','ETR'].iloc[0], e3.loc[e3.agent=='AgentWrongTool','ETR'].iloc[0]]
plt.bar(['E2 wrong-tool/op','E3 wrong-argument'], vals)
plt.ylabel('ETR'); plt.ylim(0,1.05); plt.title('WrongTool under controlled perturbations')
plt.xticks(rotation=20, ha='right'); plt.tight_layout(); plt.savefig(out/'figure2b_perturbation_etr.png', dpi=200); plt.close()
# Figure 3a/b from sensitivity outputs
length=pd.read_csv('runs/sensitivity/sensitivity_by_length_FIXED.csv')
tool=pd.read_csv('runs/sensitivity/sensitivity_by_tool_FIXED.csv')
plt.figure(figsize=(6,4))
length_skip = length[length['agent']=='AgentSkip']
plt.bar(length_skip['len_bucket'], length_skip['ETR'])
plt.ylabel('ETR'); plt.ylim(0,1.05); plt.title('ETR by chain-length bucket')
plt.tight_layout(); plt.savefig(out/'figure3a_etr_by_length.png', dpi=200); plt.close()
plt.figure(figsize=(6,4))
tool_skip = tool[tool['agent']=='AgentSkip']
plt.bar(tool_skip['tool'], tool_skip['ETR'])
plt.ylabel('ETR'); plt.ylim(0,1.05); plt.title('ETR by tool category')
plt.xticks(rotation=20, ha='right'); plt.tight_layout(); plt.savefig(out/'figure3b_etr_by_tool.png', dpi=200); plt.close()
print('Figures written to results/figures')
