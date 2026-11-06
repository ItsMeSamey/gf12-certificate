# Verification of the packaged checker

All 35 frozen cases passed their expected outcomes in the accepted a01 package, extracted into a clean directory and run under isolated, standard-library-only Python 3.14.8. The published v0.1.0 r2 package carried identical checker, driver, certificate and fixture bytes. These are retained execution results.

| Input | Expected outcome | Basis pairs checked | Mismatches | First witness: left, right, expected, actual |
| --- | --- | ---: | ---: | --- |
| Retained 42 terms | Verified, exit 0 | 144 | 0 | None |
| Reversed term order | Verified, exit 0 | 144 | 0 | None |
| Output bit toggled | Semantic failure, exit 1 | 144 | 9 | 1, 1, 1, 0 |
| Input-mask bit toggled | Semantic failure, exit 1 | 144 | 3 | 2, 1, 2, 1956 |
| Term replaced with another term | Semantic failure, exit 1 | 144 | 12 | 1, 1, 1, 1959 |
| 30 malformed or unsupported inputs | Structured rejection, exit 2 | Schema rejection | Not applicable | Diagnostic code, location and message |

A separate Astra High AI agent checked the coefficient tables with its own shift-and-reduce multiplication reference. It also tested all 126 monic potential factors of degrees 1 through 6; their nonzero remainders establish irreducibility of the fixed modulus. Both retained source term lists match the packaged certificate, and the original research file hashes stayed unchanged.

`VERIFICATION.json` records the original tested archive identity, historical code and fixture hashes, exact outcomes and hashes of the retained audit records.

Version 0.1.1 adds an explicit `sys.stdin is None` guard in the CLI input branch. Previously, starting Python with file descriptor 0 closed produced an uncaught `AttributeError`, empty stdout and exit 1. The guard routes unavailable stdin through the existing structured input-error handler, returning exit 2. Removing these two lines recovers the entire v0.1.0 checker source byte-for-byte; an independent AST comparison also passed. The arithmetic, parser, certificate, driver and fixtures remain unchanged.

A separate Astra High AI agent ran five focused CLI cases once on the sealed v0.1.1 checker under isolated, standard-library-only Python 3.14.8 on Linux. All passed: unavailable stdin, empty readable stdin, missing file, directory input and valid stdin. Empty stdin matched the retained baseline output exactly. Valid stdin matched the original accepted positive output exactly, including all 144 basis-pair results. The original 35-case suite was not rerun for this maintenance change. `CLI_VERIFICATION.json` binds these facts to source and retained receipt hashes; `CLI_REGRESSIONS.md` gives equivalent reproduction commands.

The proof covers the fixed GF(2^12) classical algebraic identity. Quantum-adapter behavior requires separate validation, as described in `PROOF.md` and `FUTURE_WORK.md`.
