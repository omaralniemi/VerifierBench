from __future__ import annotations
from pathlib import Path
import pandas as pd

def summarize_injected_labels(path):
    df=pd.read_csv(path)
    cols=['agent','inj_type']
    if not set(cols).issubset(df.columns):
        return pd.DataFrame()
    return df.groupby(cols).size().reset_index(name='target_fault_tasks')
