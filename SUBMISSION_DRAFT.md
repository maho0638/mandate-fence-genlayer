# Portal draft — Intelligent Contracts (NOT SUBMITTED)

**Title:** MandateFence — Revocable AI Agent Mandates with Consensus-Verified Authority

**Category:** Developer / Intelligent Contracts

**Pitch:** MandateFence gives AI agents narrowly scoped, revocable mandates rather than unlimited autonomy. A principal freezes an objective, authorized/prohibited action classes, a bookkeeping budget and an approval quota. The named agent can request a bounded action evaluation. Hard spending/quota rules are deterministic, while ambiguous natural-language permission checks run under GenLayer's independent leader/validator mechanism. Validators must match the thresholded ALLOW / DENY / UNCERTAIN class, so numerical confidence drift cannot cross an approval boundary. Denial/uncertainty fail closed; receipts bind immutable rule and action SHA-256 hashes. A principal can revoke authority at any time. This is a reusable authority-decision gate, not an executor or wallet; outside systems are responsible for preventing receipt reuse and enforcing the result.

**Evidence:** Add repository, passing Direct Mode CI, linter, real Studionet explorer contract address, full transaction hashes, and reviewer guide **only after independently verified**. See `docs/PROOF_STATUS.md`.

**Known limits:** No automatic action execution, no token custody, no verifiable off-chain service identity; natural language evaluation may be mistaken despite validator consensus.

## Verified evidence (19 October 2026)
- Source: https://github.com/maho0638/mandate-fence-genlayer
- Offline 19/19, Direct Mode 22/22, GenVM lint 3/3: https://github.com/maho0638/mandate-fence-genlayer/actions/runs/39205923090
- Real Studionet 4-transaction lifecycle 1/1 passed: https://github.com/maho0638/mandate-fence-genlayer/actions/runs/39207914290
- GenLayer Explorer contract: https://explorer-studio.genlayer.com/address/0x68096c6cf490F0Dc3768E630197BE1A9E101AB8E
- Full transaction hashes and observed results: https://github.com/maho0638/mandate-fence-genlayer/blob/main/docs/PROOF_MANIFEST.json
- Reproduction: https://github.com/maho0638/mandate-fence-genlayer/blob/main/docs/REVIEWER_GUIDE.md
- Outcome: `ALLOW/APPROVED`. Registered an AI mandate, deterministically blocked an over-budget request, obtained a consensus-backed ALLOW/APPROVED decision, and revoked the mandate; readback checks passed.
