# Verification of the packaged checker

All 35 frozen cases passed their expected outcomes in the accepted a01 package, extracted into a clean directory and run under isolated, standard-library-only Python 3.14.8. Revision r2 carries the same checker, driver, certificate and fixtures, with revised documentation and this verification summary.

| Input | Expected outcome | Basis pairs checked | Mismatches | First witness: left, right, expected, actual |
| --- | --- | ---: | ---: | --- |
| Retained 42 terms | Verified, exit 0 | 144 | 0 | None |
| Reversed term order | Verified, exit 0 | 144 | 0 | None |
| Output bit toggled | Semantic failure, exit 1 | 144 | 9 | 1, 1, 1, 0 |
| Input-mask bit toggled | Semantic failure, exit 1 | 144 | 3 | 2, 1, 2, 1956 |
| Term replaced with another term | Semantic failure, exit 1 | 144 | 12 | 1, 1, 1, 1959 |
| 30 malformed or unsupported inputs | Structured rejection, exit 2 | Schema rejection | Not applicable | Diagnostic code, location and message |

A separate Astra High AI agent checked the coefficient tables with its own shift-and-reduce multiplication reference. It also tested all 126 monic potential factors of degrees 1 through 6; their nonzero remainders establish irreducibility of the fixed modulus. Both retained source term lists match the packaged certificate, and the original research file hashes stayed unchanged.

`VERIFICATION.json` records the tested archive identity, hashes of every unchanged executable and fixture, exact outcomes and hashes of the retained audit records. It exports these facts from the local receipts while omitting machine paths and session metadata. The r2 review checks this summary, documentation and archive identities against those records. Its execution evidence is the accepted a01 run.

The proof covers the fixed GF(2^12) classical algebraic identity. Quantum-adapter behavior requires separate validation, as described in `PROOF.md` and `FUTURE_WORK.md`.
