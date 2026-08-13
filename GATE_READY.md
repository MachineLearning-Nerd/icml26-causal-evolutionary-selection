# Gate meaning

This repository is ready for review and publication of its **bounded finite
graph proxy audit**. It is not a claim that the six paper claims or the paper's
experiments have been reproduced.

## Required checks

~~~bash
python3 repro/src/verify.py
python3 repro/src/finalize_gate.py
python3 -m json.tool outputs/diagnostics.json >/dev/null
python3 -m json.tool outputs/verdict.json >/dev/null
python3 -m json.tool outputs/gate.json >/dev/null
git diff --check
~~~

The gate is expected to report:

- 5/5 finite proxy diagnostics passed.
- 0/6 paper-level claims independently verified.
- C6 real-world validation not reproduced.
- overall status INCONCLUSIVE.

The checked-in source paper copy is a reference artifact. The implementation
is independent clean-room code and is not author code.
