# What remains after this prototype

This checker, its fixed certificate and focused tests are complete. The retained 42-term construction and circuit measurements are prior work as well.

Two prospective deliverables address the remaining coupling:

1. **Reproducible derivation export.** Separate the exact GF(8) embedding, basis transforms and interpolation derivation from the backend. Export their intermediate mathematical evidence and independently check it, while retaining the present tensor checker as a separate final identity check. Document failure diagnostics and source provenance for the exact supported field. Broader fields require their own specified construction and tests.
2. **Optional quantum-circuit adapter.** Isolate the existing emitter behind an explicit optional dependency boundary. Review the precise pinned backend and licenses, preserve arbitrary-output XOR behavior, both inputs and clean scratch, and examine phase and measurement-branch assumptions. Compare the emitted circuit against the pinned native control under matched contracts and report every gate category, qubits and classical bits. Finite-shot tests must remain labeled as such; any stronger semantic claim needs a separate argument.

Packaging, examples and documentation would support those deliverables. The existing CPU is sufficient for the initial focused engineering work.

A prospective funding scope should select and size an actual remaining deliverable, with a measurable midpoint and completion condition. The separately reviewed Unitary FAQ permits funding developer time. Budget, schedule and availability belong in a specific proposal. If the selected work ends at this fixed checker, there is little substantive work left to fund and the request should be reduced or reconsidered.
