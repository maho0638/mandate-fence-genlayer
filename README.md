# MandateFence — Revocable AI Agent Authority on GenLayer

**One standalone, reusable Intelligent Contract for bounded agent delegations.** A user commits a mandate naming a permitted AI agent, allowed and forbidden action classes, a fixed spend-equivalent *accounting* budget, and a maximum number of approvals. The designated agent submits a natural-language action proposal. GenLayer validators independently assess its *semantic* fit against the frozen mandate; deterministic rules block budget violations and revoked mandates.

This is a **decision primitive, not a wallet, funds escrow, transaction router, execution engine, or signature scheme**. It neither holds money nor proves that an off-chain agent obeys the decision. External integrations must enforce decisions securely and prevent re-use; reading an old receipt alone is insufficient authorization to execute value transfers.

## Why GenLayer?

Pure smart contracts can count spend and check addresses, but cannot reliably decide whether a proposed natural-language action stays within a human's stated intent. A single centralized LLM is not an independent arbiter. Here, GenLayer's `run_nondet_unsafe` forces independent validators to reproduce the **thresholded decision class** (`ALLOW`, `DENY`, `UNCERTAIN`) before a state mutation. Confidence below 80, malformed JSON, or ambiguous proposals become `UNCERTAIN`, never an approval. Comparing the normalized decision prevents the Sightline-style failure where small confidence variations cross a decision boundary after validator acceptance.

## API and behavior

- `create_mandate(id, agent_address, objective, allowed_actions, forbidden_actions, budget, max_approvals)` — immutable identity and rules; `budget` is caller-defined bookkeeping units, *not native GEN*.
- `assess_action(receipt_id, mandate_id, action, amount)` — **designated agent only**. If amount exceeds remaining budget, deterministic `HARD_BUDGET_BLOCK` skips the LLM. Otherwise validators judge scope. A successful `ALLOW` consumes allowance and one approval. Every assessment gets a bound SHA-256 receipt; receipt IDs cannot be reused.
- `revoke(mandate_id)` — **owner only**, irreversible. A revoked mandate cannot authorize any more proposals.
- `get_mandate`, `get_receipt`, `is_approved` — views. `is_approved` reports a historically accepted proposal only while the associated mandate has not been revoked; **it is not a one-shot transaction authorization**.

**Safety**: no privileged administrator; strict IDs, bounded natural language, no executable prompt fragments; hard budget and total approvals applied outside nondeterministic execution; validator decision class must match; actions and mandate rules SHA-256 bound to receipts; no external calls or funds. Unsupported requests are blocked, not guessed as safe.

## Reproduce

```bash
pip install -r requirements.txt
python -m pytest tests/offline -q      # SDK stub only, NOT chain proof
python -m pytest tests/direct -q       # genuine GenLayer Direct Mode, mocked LLM
 genvm-lint check contracts/mandate_fence.py
```

CI: `.github/workflows/ci.yml` (push / manual). Manual real-Studionet test: `.github/workflows/studionet.yml`. **Never confuse source compilation or offline tests with verified multi-validator Studionet consensus**. See `docs/PROOF_STATUS.md`, `docs/REVIEWER_GUIDE.md`, and `docs/THREAT_MODEL.md`.

No claims of Portal acceptance, guaranteed points, real GEN spending, or deployed address until observed and documented.

## Verified GitHub CI (19 October 2026)

- 19/19 offline SDK-stub logic tests passed (not on-chain proof).
- 22/22 GenLayer Direct Mode tests passed with validator re-execution mocks.
- GenVM linter: 3/3 checks passed.
- [GitHub Actions run](https://github.com/maho0638/mandate-fence-genlayer/actions/runs/39205923090).
- Source SHA-256: `243bc2786fa04b665e169c9222d86d6f90b92af88fdc6261fc62679c739436b4`.
- **No live Studionet run or Portal submission is claimed.**
