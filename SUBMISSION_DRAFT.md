# Portal draft — Intelligent Contracts (NOT SUBMITTED)

**Title:** MandateFence — Revocable AI Agent Mandates with Consensus-Verified Authority

**Category:** Developer / Intelligent Contracts

**Pitch:** MandateFence gives AI agents narrowly scoped, revocable mandates rather than unlimited autonomy. A principal freezes an objective, authorized/prohibited action classes, a bookkeeping budget and an approval quota. The named agent can request a bounded action evaluation. Hard spending/quota rules are deterministic, while ambiguous natural-language permission checks run under GenLayer's independent leader/validator mechanism. Validators must match the thresholded ALLOW / DENY / UNCERTAIN class, so numerical confidence drift cannot cross an approval boundary. Denial/uncertainty fail closed; receipts bind immutable rule and action SHA-256 hashes. A principal can revoke authority at any time. This is a reusable authority-decision gate, not an executor or wallet; outside systems are responsible for preventing receipt reuse and enforcing the result.

**Evidence:** Add repository, passing Direct Mode CI, linter, real Studionet explorer contract address, full transaction hashes, and reviewer guide **only after independently verified**. See `docs/PROOF_STATUS.md`.

**Known limits:** No automatic action execution, no token custody, no verifiable off-chain service identity; natural language evaluation may be mistaken despite validator consensus.
