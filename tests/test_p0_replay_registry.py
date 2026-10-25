import sys,tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from krc_research.replay_registry import ReplayRegistry

def test_persists_restart():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'claims.sqlite'
        ReplayRegistry(p).claim('K_Science','task-1')
        with pytest.raises(ValueError): ReplayRegistry(p).claim('K_Science','task-1')

def test_different_principals():
    with tempfile.TemporaryDirectory() as d:
        r=ReplayRegistry(Path(d)/'db')
        r.claim('K_Science','task-1');r.claim('Other','task-1')

def test_concurrent_atomicity():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'db';ReplayRegistry(p)
        def claim(_):
            try: ReplayRegistry(p).claim('K_Science','repeat');return True
            except ValueError:return False
        with ThreadPoolExecutor(max_workers=4) as pool:
            res=list(pool.map(claim,range(4)))
        assert sum(res)==1

def test_retention():
    with tempfile.TemporaryDirectory() as d:
        r=ReplayRegistry(Path(d)/'db')
        r.claim('K_Science','old',now=100)
        r.claim('K_Science','new',now=100000)
        assert r.prune(now=100001,retention=3600)==1
        r.claim('K_Science','old',now=100002)

def test_bad_identity():
    with tempfile.TemporaryDirectory() as d:
        r=ReplayRegistry(Path(d)/'db')
        with pytest.raises(ValueError):r.claim('','task')
