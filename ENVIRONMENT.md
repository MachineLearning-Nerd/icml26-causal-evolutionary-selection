# Environment and execution contract

This standardization consumes the existing raw diagnostics. It does not run
the scientific implementation or regenerate experiment measurements.

## Metadata-only commands

~~~bash
python3 repro/src/finalize_gate.py
python3 verify_final.py
~~~

The finalizer reads outputs/diagnostics.json and writes the canonical verdict
and gate files. The final verifier checks documentation, structured counts,
claim statuses, branch refs, commit identities, recovery markers, and
fail-closed publication flags.

## Scientific source retained for provenance

The original diagnostic command is:

~~~bash
python3 repro/src/verify.py
~~~

It is retained as provenance only for this documentation pass. The five
measurements in outputs/diagnostics.json are existing evidence; C6 is an
explicit no-run record. No causal-discovery package, dataset, or GPU runtime is
assumed.

If raw diagnostics are regenerated later, rerun finalize_gate.py and
verify_final.py, then review the claim ledger before publication.
