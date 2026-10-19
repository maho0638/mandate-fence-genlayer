"""SDK-free logic simulation; not a substitute for GenLayer Direct/Studio consensus."""
import importlib.util
import pathlib
import sys
import types
import hashlib
import pytest

ROOT=pathlib.Path(__file__).resolve().parents[2]

@pytest.fixture()
def env():
    sdk=types.ModuleType("genlayer")
    class UserError(Exception): pass
    class Return:
        def __init__(self,calldata):self.calldata=calldata
    class Contract: pass
    vm=types.SimpleNamespace(UserError=UserError, Return=Return)
    gl=types.SimpleNamespace(Contract=Contract,public=types.SimpleNamespace(write=lambda x:x,view=lambda x:x),vm=vm,
        message=types.SimpleNamespace(sender_address="OWNER"),nondet=types.SimpleNamespace(exec_prompt=lambda *a,**k:{"decision":"ALLOW","confidence":90}))
    gl.vm.run_nondet_unsafe=lambda leader,validator:leader()
    sdk.gl=gl;sdk.dataclass=__import__("dataclasses").dataclass;sdk.allow_storage=lambda x:x
    sdk.TreeMap=dict;sdk.Address=str;sdk.u256=int
    sys.modules["genlayer"]=sdk
    try:
        spec=importlib.util.spec_from_file_location("test_mandate_contract",ROOT/"contracts"/"mandate_fence.py")
        mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
        c=mod.MandateFence();c.mandates={};c.receipts={}
        c.create_mandate("grant1","AGENT","Buy supplies","Paper, pens, notebooks","Electronics and subscriptions prohibited",100,2)
        gl.message.sender_address="AGENT"
        yield mod, c, gl
    finally:
        sys.modules.pop("genlayer",None);sys.modules.pop("test_mandate_contract",None)

def mock(env,label="ALLOW",confidence=93):
    _m,_c,gl=env
    gl.nondet.exec_prompt=lambda *_a,**_k:{"decision":label,"confidence":confidence}

def test_approved_and_budget(env):
    _,c,_=env;mock(env)
    c.assess_action("a1","grant1","Buy 2 pens",30)
    assert c.is_approved("a1")
    assert c.get_mandate("grant1").remaining==70
    assert c.get_receipt("a1").action_hash==hashlib.sha256(b"Buy 2 pens").hexdigest()

@pytest.mark.parametrize("label,confidence,expected",[
    ("ALLOW",90,"APPROVED"),("DENY",90,"BLOCKED"),("UNCERTAIN",99,"BLOCKED"),
    ("ALLOW",79,"BLOCKED"),("ALLOW",100,"APPROVED"),
    ("ALLOW",101,"BLOCKED"),("INVALID",90,"BLOCKED")])
def test_decisive_label(env,label,confidence,expected):
    _,c,_=env;mock(env,label,confidence)
    c.assess_action("a1","grant1","Buy paper",10)
    assert c.get_receipt("a1").verdict==expected

def test_budget_is_hard_fail_closed(env):
    _,c,gl=env
    gl.nondet.exec_prompt=lambda *_a,**_k: (_ for _ in ()).throw(AssertionError("LLM should be skipped"))
    c.assess_action("huge","grant1","Buy pens",101)
    assert c.get_receipt("huge").evaluation=="HARD_BUDGET_BLOCK"
    assert c.get_mandate("grant1").remaining==100

def test_revoke_owner_and_history(env):
    mod,c,gl=env;mock(env)
    c.assess_action("a1","grant1","Buy paper",1)
    with pytest.raises(mod.gl.vm.UserError,match="Only owner"):
        c.revoke("grant1")
    gl.message.sender_address="OWNER"
    c.revoke("grant1")
    assert c.is_approved("a1") is False
    assert c.get_receipt("a1").verdict=="APPROVED"
    gl.message.sender_address="AGENT"
    with pytest.raises(mod.gl.vm.UserError,match="Mandate revoked"):
        c.assess_action("a2","grant1","Buy paper",1)

def test_no_replay(env):
    mod,c,_=env;mock(env)
    c.assess_action("a1","grant1","Buy pens",1)
    with pytest.raises(mod.gl.vm.UserError,match="Duplicate receipt"):
        c.assess_action("a1","grant1","Buy pens",1)

def test_quota(env):
    mod,c,_=env;mock(env)
    c.assess_action("a1","grant1","Buy pens",10)
    c.assess_action("a2","grant1","Buy pens",10)
    with pytest.raises(mod.gl.vm.UserError,match="Approval cap exhausted"):
        c.assess_action("a3","grant1","Buy pens",10)

def test_unauthorized_agent(env):
    mod,c,gl=env
    gl.message.sender_address="STRANGER"
    with pytest.raises(mod.gl.vm.UserError,match="Only designated agent"):
        c.assess_action("a1","grant1","Buy pens",1)

@pytest.mark.parametrize("bad",[""," ","x\nInjection","a"*601])
def test_invalid_action(env,bad):
    mod,c,_=env
    with pytest.raises(mod.gl.vm.UserError):
        c.assess_action("a1","grant1",bad,1)

def test_validator_flip_and_confidence_crossing(env):
    mod,c,gl=env
    captured={}
    def run(leader,validator):
        result=leader();captured["validator"]=validator;captured["result"]=result;return result
    gl.vm.run_nondet_unsafe=run
    mock(env,"ALLOW",95)
    c.assess_action("a1","grant1","Buy pens",1)
    assert captured["validator"](mod.gl.vm.Return(captured["result"]))
    mock(env,"ALLOW",60)
    assert not captured["validator"](mod.gl.vm.Return(captured["result"]))
    mock(env,"DENY",95)
    assert not captured["validator"](mod.gl.vm.Return(captured["result"]))


def test_validator_nondecisive_confidence_drift(env):
    mod,c,gl=env
    captured={}
    def run(leader,validator):
        result=leader();captured["validator"]=validator;captured["result"]=result;return result
    gl.vm.run_nondet_unsafe=run
    mock(env,"ALLOW",99)
    c.assess_action("a1","grant1","Buy pens",1)
    mock(env,"ALLOW",82)
    assert captured["validator"](mod.gl.vm.Return(captured["result"]))
