from __future__ import annotations
from pathlib import Path
import hashlib, json, re

HEX64=re.compile(r'^[0-9a-f]{64}$')

def sha256_file(path: str|Path) -> str:
    p=Path(path)
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def load_json(path: str|Path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def validate_hash_manifest(manifest_path: str|Path, run_dir: str|Path|None=None) -> dict:
    manifest_path=Path(manifest_path)
    manifest=load_json(manifest_path)
    out={'manifest_path':str(manifest_path),'n_records':len(manifest),'invalid_hashes':0,'checked_files':0,'missing_files':0,'mismatched_files':0,'mode':'manifest-only'}
    for rel,digest in manifest.items():
        if not isinstance(digest,str) or not HEX64.match(digest):
            out['invalid_hashes']+=1
        if run_dir is not None:
            p=Path(run_dir)/rel
            if p.exists():
                out['mode']='file-verification'
                out['checked_files']+=1
                if sha256_file(p)!=digest:
                    out['mismatched_files']+=1
            else:
                out['missing_files']+=1
    return out
