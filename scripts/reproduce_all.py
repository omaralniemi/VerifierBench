#!/usr/bin/env python
import subprocess, sys
for cmd in [
    [sys.executable, 'scripts/generate_microbench.py'],
    [sys.executable, 'scripts/verify_hashes.py'],
    [sys.executable, 'scripts/reproduce_tables.py'],
    [sys.executable, 'scripts/validate_package.py'],
    [sys.executable, 'scripts/reproduce_figures.py'],
    [sys.executable, 'scripts/audit_package.py'],
]:
    print('\n$',' '.join(cmd))
    subprocess.check_call(cmd)
print('\nAll VerifierBench reproducibility checks completed successfully.')
