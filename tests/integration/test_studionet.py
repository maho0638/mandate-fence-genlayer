"""Opt-in network proof. Only run after user authorizes testnet transactions."""
import hashlib
import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded


def pick(result, name):
    return result.get(name) if isinstance(result, dict) else getattr(result,name)


@pytest.mark.integration
def test_network_mandate_lifecycle(default_account):
    c=get_contract_factory("MandateFence").deploy(account=default_account,consensus_max_rotations=4)
    print("MANDATE_ADDRESS="+str(c.address),flush=True)
    agent=str(default_account.address)
    tx=c.create_mandate(args=["paper-one",agent,"Buy office supplies","Buy paper and notebooks","Never buy electronics or subscriptions",100,3]).transact(wait_interval=10000,wait_retries=50)
    assert tx_execution_succeeded(tx)
    print("CREATE_TX="+str(tx.get("hash","")),flush=True)
    m=c.get_mandate(args=["paper-one"]).call()
    assert str(pick(m,"rules_hash"))

    tx=c.assess_action(args=["overbudget","paper-one","Buy paper",101]).transact(wait_interval=10000,wait_retries=50)
    assert tx_execution_succeeded(tx)
    print("HARD_BLOCK_TX="+str(tx.get("hash","")),flush=True)
    r=c.get_receipt(args=["overbudget"]).call()
    assert str(pick(r,"verdict"))=="BLOCKED"
    assert str(pick(r,"evaluation"))=="HARD_BUDGET_BLOCK"

    tx=c.assess_action(args=["semantic","paper-one","Buy two packs of office paper",10]).transact(consensus_max_rotations=4,wait_interval=10000,wait_retries=80)
    assert tx_execution_succeeded(tx)
    print("SEMANTIC_TX="+str(tx.get("hash","")),flush=True)
    r=c.get_receipt(args=["semantic"]).call()
    assert str(pick(r,"evaluation")) in ("ALLOW","DENY","UNCERTAIN")
    assert str(pick(r,"verdict")) in ("APPROVED","BLOCKED")
    assert str(pick(r,"action_hash"))==hashlib.sha256(b"Buy two packs of office paper").hexdigest()
    print("RESULT="+str(pick(r,"evaluation"))+"/"+str(pick(r,"verdict")),flush=True)

    tx=c.revoke(args=["paper-one"]).transact(wait_interval=10000,wait_retries=50)
    assert tx_execution_succeeded(tx)
    print("REVOKE_TX="+str(tx.get("hash","")),flush=True)
    assert pick(c.get_mandate(args=["paper-one"]).call(),"revoked") is True
