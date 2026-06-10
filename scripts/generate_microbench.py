#!/usr/bin/env python
from pathlib import Path
import sys, json
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.microbench_generator import write_microbench, semantic_equal

out=Path('results/validation/generated_microbench_300.json')
write_microbench(out)
release=Path('data/tasks/microbench_300.json')
print(f'generated={out}')
print(f'semantic_match_release={semantic_equal(out, release)}')
if not semantic_equal(out, release):
    raise SystemExit('Generated task set does not semantically match data/tasks/microbench_300.json')
