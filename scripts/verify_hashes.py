#!/usr/bin/env python
from pathlib import Path
import sys, json
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.hash_utils import sha256_file, validate_hash_manifest

root=Path('.')
reports=[]
for rel in ['runs/baseline/artifacts_sha256.json','runs/inject_E2/artifacts_sha256.json','runs/inject_E3/artifacts_sha256.json']:
    p=root/rel
    if p.exists():
        reports.append(validate_hash_manifest(p, p.parent))
for rel in ['data/tasks/microbench_300.json','data/corpus/manifest.json','data/protocol_lock.json']:
    p=root/rel
    reports.append({'file':rel,'sha256':sha256_file(p)})
out=Path('results/validation/hash_verification.json')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(reports, indent=2), encoding='utf-8')
print(json.dumps(reports, indent=2))
