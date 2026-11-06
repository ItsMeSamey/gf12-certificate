# Provenance and credits

The certificate contains the exact 42 mathematical triples retained in the locally authored `ml/quantum-circuits/classical_results/tower_verification.json`. Its `bilinear_terms` and `tower_derivation.terms` lists were checked equal before extraction. The new certificate contains the field declaration and one authoritative term list. Acceptance depends on the algebraic check.

Verified original SHA-256 values:

- `tower_multiplier.py`: `74f56baf3428c26c3be4868b206718953d4ab83530d6fae918a53d4a357997b5`
- `classical_results/tower_verification.json`: `f4264432bc5b5fbcb758e4e96dc0840db7e3b94039384778d9f8fca82d74d704`
- `classical_results/native_gf_comparison.json`: `41e4844718a5061488b89f836efdc3684db2f52bfd7261531933f722645895eb`

Extracted certificate SHA-256: `35ae0ded19965326e1744d27a6dead67b26768cec3247ed789ba03f429f1dd90`.

Preimplementation fixture freeze SHA-256: `527ee896a47a6d7f668c070436b327bdfc65c0431e78b5924a32bcaf8e418fa1`.

The retained derivation embeds GF(8), changes basis and uses seven-point interpolation to construct the tensor. The earlier research documentation attributes field conventions to the public task specification. Field-extension/interpolation is established mathematics. This project adds the separate certificate interface and verification.

Relevant mathematical and software prior art:

- Cenk, Koc and Ozbudak, *Polynomial Multiplication over Finite Fields using Field Extensions and Interpolation*, DOI 10.1109/ARITH.2009.11. Author-hosted paper: https://cetinkayakoc.net/docs/c44.pdf
- Qualtran finite-field multiplication documentation: https://qualtran.readthedocs.io/en/latest/bloqs/gf_arithmetic/gf2_multiplication.html

These references come from the retained source assessment. The package consists of the original checker and driver, mathematical certificate, frozen fixtures and documentation; its runtime uses Python's standard library.

The new checker, driver and documentation were generated with OpenAI Codex. A separate Astra High AI agent reviewed the proof, frozen fixtures and clean execution. The original new code is explicitly MIT-licensed. The mathematical masks are retained data with the source identity above; this package's provenance covers those masks and the new files.
