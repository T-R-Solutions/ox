# Final envelope observation

Semantic review/validation, focused tests and documentation disposition are recorded
in sibling reports. The selected-feature automated gate is executed after all bound
inputs stabilize; this file records that observation without changing those inputs.

Coordinator executed from the Ox root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --features sdd/features --feature windows-design-baseline --require-approved --require-fresh --check-convergence
```

Observed exit 0, selected windows-design-baseline, PASS for scoped files, configured
bridges and requested evidence checks. This does not imply global governance or
product acceptance. The final schema-2 envelope binds the stabilized inputs listed
in final-inputs.json; original source/native/skill observations were not rehashed
to imply a new execution. Documentary semantic verdicts are in validation.md.

The independent validator then reinspected final tasks, traceability, schema-2
evidence and convergence; each evidence binds60 inputs including the four required
contracts. It repeated the exact selected command above: exit 0, PASS. Final
independent verdict AC-01/02/03 APPROVED only for documentary/preservation scope.
No repository file was changed by that validator.

Final observed feature hashes:

| File | SHA-256 |
| --- | --- |
| tasks.md | eb12ff6bc58bbb0c6e0be529f3be85e6f522efda2d9ab77c024b28cd373a6055 |
| traceability.json | 3142dea958e79d33ebec1f32ec96be9723b4902f9e8e69d18423e70c8a3efc6e |
| evidence.json | 3cd8eb0c3085bb5967fa5a34e9cb9493557902fe184d07f69e5f3376ca147ee5 |
| converge.md | 6b13cd936d283d18f2d63571303d28624903bb45fa756c9a05c8f92c93e939ef |

Global historical failures remain explicit; no visual fidelity, accessibility or
native behavior is approved. Later changed inputs require affected reevaluation.
All delegated writer/reviewer/validator work is complete; no process remains.
