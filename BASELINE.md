# Exact baseline coupling comparison

This comparison inspects the retained entrypoints' imports and checks standalone execution of the new interface. The historical backend evidence is identified separately below.

| Property | Retained research entrypoints | New certificate checker |
| --- | --- | --- |
| Input | A Python derivation embedded in the research tree; generated terms are also retained in a historical JSON receipt | A fixed bounded JSON certificate with one authoritative term list |
| Import coupling | `tower_multiplier.py` line 6 imports `kickmix`; line 8 imports `reversible_primitives.emit_gf12_bilinear_xor` unconditionally | Standard-library imports only; clean verification uses `python -I -S` |
| Existing test coupling | `test_tower_primitive.py` lines 6-10 import NumPy, Kickmix, derivation/emitter helpers and native-test helpers; after its 144-basis loop it executes simulator checks | The standalone checker evaluates the 144 algebraic identities without the derivation or simulator |
| Error contract | Existing basis check asserts equality inside the combined research test | Strict structural errors are distinct from semantic failures with an explicit basis witness |
| Equivalent data | No standalone certificate consumer at these inspected entrypoints | Reordered 42-term certificate is accepted, despite a different input/canonical digest |
| Verification scope | Retained native receipts describe their own finite-shot contracts and resource counts | Classical multiplication identity; a quantum adapter requires separate validation |

The improvement is a separately usable dependency-free certificate interface. The new checker should be run from a clean extraction on both retained/reordered inputs and frozen corruptions. Independent audit verifies the source imports and runtime module evidence. The comparison covers the entrypoints listed above.

The retained native comparison receipt records the following historical resource tradeoffs:

| Resource | Native helper | Tower candidate |
| --- | ---: | ---: |
| Toffoli-like gates | 63 | 42 |
| Qubits | 36 | 39 |
| Classical bits | 0 | 1 |
| CX | 481 | 1,268 |
| SWAP | 21 | 0 |
| CZ | 0 | 42 |
| Reset (`R`) | 0 | 42 |
| Measurement/reset (`HMR`) | 0 | 42 |

The tower uses fewer Toffoli-like gates and more qubits, classical storage and several other operations. These counts belong to the prior circuit execution; the current checker verifies its classical algebraic certificate.

Exact retained source and receipt hashes are listed in `PROVENANCE.md`. The old files remain unchanged and outside this package.
