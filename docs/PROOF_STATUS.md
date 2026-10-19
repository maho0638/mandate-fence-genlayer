# Verified Studionet proof — MandateFence

- **State**: live Studionet integration 1/1 passed on 19 October 2026.
- **CI / offline**: 19/19 SDK stub tests, 22/22 GenLayer Direct Mode tests, 3/3 GenVM lint: https://github.com/maho0638/mandate-fence-genlayer/actions/runs/39205923090
- **Live**: https://github.com/maho0638/mandate-fence-genlayer/actions/runs/39207914290
- **Contract source**: `contracts/mandate_fence.py`; SHA-256 `243bc2786fa04b665e169c9222d86d6f90b92af88fdc6261fc62679c739436b4` matched both CI and live test logs.
- **Contract address**: `0x68096c6cf490F0Dc3768E630197BE1A9E101AB8E`
- **Explorer**: https://explorer-studio.genlayer.com/address/0x68096c6cf490F0Dc3768E630197BE1A9E101AB8E
- **Observed on-chain result**: `ALLOW/APPROVED`
- **Observed lifecycle**: Registered an AI mandate, deterministically blocked an over-budget request, obtained a consensus-backed ALLOW/APPROVED decision, and revoked the mandate; readback checks passed.

- **CREATE_TX**: `0x805ec44001901c0fdda84fff8661ae0723f25546b53e72021a114eb1abfb5b9a`
- **HARD_BLOCK_TX**: `0xe9513bbd6aced5701358f96887e3155c8cf81a54825a89a87e52609e1ac2a3e5`
- **SEMANTIC_TX**: `0x20b89366130c607931962977b60d36a66466dcae82d76d40ebac8279877ca51e`
- **REVOKE_TX**: `0xcbe99c09749597fedf683a4e5a47a2c0c3b8da933b559b45149ba302569a9349`

## Limits
This proves only the observed integration lifecycle and readback, not a formal security audit, perfect model accuracy, or all possible validator rotations. Direct Mode separately tests edge cases and disagreement. No native-GEN escrow or user wallet custody is part of these contracts. No Portal submission or rating is claimed.
