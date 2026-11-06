# GF12 certificate checker

Verify one fixed 42-term bilinear multiplication certificate without installing or importing a quantum backend. The supported contract is GF(2^12), modulus `0x1053`, polynomial basis, with bit i representing the coefficient of X^i. Terms are JSON data; they never name code, modules or resources to execute.

The retained research entrypoint imports Kickmix and its reversible emitter at module import time. Its existing tensor test also imports NumPy and runs native circuit checks. This package separates the mathematical identity check and gives invalid certificates concrete diagnostics. See `BASELINE.md` for the exact static comparison.

## Run

Python 3.14 is the locally verified interpreter. No third-party package is required. From a clean extraction:

```sh
python3 -I -S -B gf12_checker.py certificate.json
python3 -I -S -B gf12_checker.py fixtures/reversed.json
python3 -I -S -B gf12_checker.py fixtures/output_bit.json
python3 -I -S -B run_checks.py --output /tmp/new-gf12-checks
```

The third command intentionally returns exit 1 with the witness left=1, right=1, expected=1, actual=0. The test driver expects this failure and verifies it. Its output directory must be new. Use `-` instead of a filename to read a certificate from stdin. `-I -S` isolates the interpreter and disables site packages; the JSON report records that execution context.

Exit codes are 0 for a verified identity, 1 for a semantic mismatch, and 2 for malformed/unsupported input or a file error. Reports include the first mismatching basis pair, expected and actual products, their XOR difference, and the total mismatch count. Every well-formed certificate is evaluated on all 144 basis pairs. SHA-256 values identify the input and canonical JSON; acceptance never depends on an allowlisted digest. Reordered terms are accepted.

## Fixed schema

Exactly three top-level keys are allowed:

```json
{
  "schema_version": 1,
  "field": {
    "degree": 12,
    "modulus": 4179,
    "basis": "polynomial",
    "bit_order": "little-endian"
  },
  "terms": [[321, 321, 1958]]
}
```

The example shows the first triple only. A valid certificate must contain exactly 42 triples. Each triple is `[a_mask, b_mask, c_mask]`, with each mask an integer from 0 to 4095. Booleans and floating-point numbers are rejected. Duplicate JSON object keys, missing/unknown keys, non-finite numbers, unsupported field declarations and claimed success or gate-count fields are rejected.

Input is limited to 16 KiB, enough for the fixed 42 triples, metadata and ordinary pretty-printing. This bounds parser input for this schema. Deep malformed JSON returns an invalid-input diagnostic. A large input is read only up to the bound plus one byte.

## What is proved

For each pair of basis elements, the checker evaluates the parity-product tensor and compares it with independently written carryless polynomial multiplication and long division by `0x1053`. Both maps are bilinear over GF(2), so agreement on the 144 basis pairs proves agreement for all 16,777,216 pairs of 12-bit operands. XORing this verified classical product into any classical output word has the corresponding algebraic identity.

Quantum adapters require separate validation of relative phases, measurement branches, scratch cleanup, compiled circuit identity, gate counts and hardware behavior. The retained quantum receipts provide historical context. `PROOF.md` explains the classical argument and the frozen corruption witnesses.

The 35 frozen cases cover retained and reversed positives, three semantic corruptions and 30 malformed or unsupported inputs. `fixtures/FROZEN_CASES.json` was written before checker implementation or execution. `PACKAGE_MANIFEST.json` pins the package files. `VERIFICATION.md` and `VERIFICATION.json` bind the accepted test results to the unchanged checker, driver and fixtures in this documentation revision.

## Provenance and license

The 42 triples were extracted from the retained `classical_results/tower_verification.json`, and its two term lists were checked equal. `PROVENANCE.md` records exact source hashes and mathematical citations. The derivation uses established field-extension/interpolation ideas.

The original checker, driver and documentation are MIT-licensed. They were generated with OpenAI Codex, with a separate Astra High AI agent reviewing the proof and execution. The package contains the checker, mathematical certificate, fixtures and documentation. `FUTURE_WORK.md` describes prospective derivation and quantum-adapter work.
