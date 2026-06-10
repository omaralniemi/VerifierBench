#!/usr/bin/env python
"""Repository hygiene checks for the GitHub-ready VerifierBench package."""
from pathlib import Path
import json, re, shutil

root=Path('.')
# Remove runtime Python caches before checking the repository tree.
for cache in root.rglob('__pycache__'):
    shutil.rmtree(cache, ignore_errors=True)
for pyc in root.rglob('*.pyc'):
    pyc.unlink(missing_ok=True)

problems=[]
this_file=Path('scripts/audit_package.py')
local_path_re=re.compile(r'(?:C:' + r'\\' + 'Users|C:/' + 'Users|/Users/' + 'User)')
for p in root.rglob('*'):
    if '__pycache__' in p.parts or p.suffix=='.pyc':
        problems.append(f'Python cache file/directory remains: {p}')
        continue
    if p.is_file() and p != this_file and p.suffix.lower() in {'.py','.md','.txt','.json','.jsonl','.csv'}:
        try:
            txt=p.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        if local_path_re.search(txt):
            problems.append(f'Local user path found in {p}')
        if ('During ' + 'review') in txt:
            problems.append(f'Review-only wording found in {p}')
expected=[
 'results/tables/table4_baseline_metrics.csv',
 'results/tables/table5_perturbation_metrics.csv',
 'results/tables/table6_diagnostic_breakdown.csv',
 'results/tables/table7_evaluator_comparison.csv',
]
for rel in expected:
    if not (root/rel).exists():
        problems.append(f'Missing manuscript-aligned output: {rel}')
if problems:
    print(json.dumps({'repository_hygiene_pass': False, 'problems': problems}, indent=2))
    raise SystemExit(1)
print(json.dumps({'repository_hygiene_pass': True, 'problems': []}, indent=2))
