from __future__ import annotations
from pathlib import Path
import json, random, hashlib

def generate_microbench(seed:int=20260211, n_tasks:int=300):
    random.seed(seed)
    tasks=[]
    for t in range(n_tasks):
        tid=f"VB-{t+1:03d}"
        n_steps=2+(t%7)
        steps=[]
        for s in range(1,n_steps+1):
            if s==1:
                steps.append({'step_id':s,'expected_tool':'FileTool','expected_op':'write_csv','inputs':{'path':f'artifacts/{tid}/table.csv'},'expected_relation_type':'artifact_written_exists','expected_relation':{'path':f'artifacts/{tid}/table.csv'}})
            elif s==2:
                steps.append({'step_id':s,'expected_tool':'FileTool','expected_op':'read_csv','inputs':{'path':f'artifacts/{tid}/table.csv'},'expected_relation_type':'read_after_write_dependency','expected_relation':{'path':f'artifacts/{tid}/table.csv'}})
            else:
                if s%3==0:
                    q=f"key{(t+s)%11}"
                    steps.append({'step_id':s,'expected_tool':'QueryTool','expected_op':'search','inputs':{'query':q,'top_k':10},'expected_relation_type':'query_hits_reproducible','expected_relation':{'min_hits':1,'hits_doc_ids':None}})
                else:
                    steps.append({'step_id':s,'expected_tool':'CalcTool','expected_op':'sum','inputs':{'values':[t,s,(t+s)%13]},'expected_relation_type':'value_equals','expected_relation':{'value':t+s+((t+s)%13)}})
        tasks.append({'task_id':tid,'steps':steps})
    return tasks

def write_microbench(out_path:str|Path, seed:int=20260211, n_tasks:int=300):
    out=Path(out_path); out.parent.mkdir(parents=True, exist_ok=True)
    tasks=generate_microbench(seed,n_tasks)
    out.write_text(json.dumps(tasks,ensure_ascii=False,indent=2),encoding='utf-8')
    return out

def semantic_equal(path_a:str|Path, path_b:str|Path) -> bool:
    return json.loads(Path(path_a).read_text(encoding='utf-8')) == json.loads(Path(path_b).read_text(encoding='utf-8'))
