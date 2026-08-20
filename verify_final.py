#!/usr/bin/env python3
"""Verify the published causal-selection bounded-audit contract."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_IDENTITY = (
    "MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>"
)
EXPECTED_RECOVERY_SHA = (
    "db65d45de07d47b5e44dd4cd60bb5509ace09a69dca1de7cffea56e7c97f0250"
)
EXPECTED_SOURCE_TIP = "486571731bda5986ad65d2d9bd00d710522b260f"
EXPECTED_STATUS = (
    "INCONCLUSIVE_C1_FINITE_MODEL_CONSTRUCTION_PROXY_"
    "C2_FINITE_GRAPH_STRUCTURE_PROXY_C3_FINITE_DSEP_ENUMERATION_PROXY_"
    "C4_FINITE_PC_GRAPH_PROXY_C5_TAUTOLOGICAL_MULTI_ENV_PROXY_"
    "C6_NOT_REPRODUCED_NO_PAPER_CLAIMS_VERIFIED_NO_CURRENT_SCORE"
)
EXPECTED_CLAIMS = {
    "C1": "FINITE_MODEL_CONSTRUCTION_PROXY",
    "C2": "FINITE_GRAPH_STRUCTURE_PROXY",
    "C3": "FINITE_DSEP_ENUMERATION_PROXY",
    "C4": "FINITE_PC_GRAPH_PROXY",
    "C5": "TAUTOLOGICAL_MULTI_ENV_PROXY",
    "C6": "NOT_REPRODUCED",
}


def fail(reason: str) -> None:
    print("FINAL_AUDIT=FAILED reason=" + reason)
    raise SystemExit(1)


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        fail("git_" + "_".join(args))
    return result.stdout.strip()


def load(relative_path: str) -> dict:
    try:
        with (ROOT / relative_path).open(encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        fail(relative_path + "_invalid_" + type(error).__name__)
    raise AssertionError("unreachable")


local_heads = {
    line
    for line in git(
        "for-each-ref",
        "refs/heads",
        "--format=%(refname:short)",
    ).splitlines()
    if line
}
if local_heads != {"main"}:
    fail("branches_" + ",".join(sorted(local_heads)))
if git("branch", "--show-current") != "main":
    fail("head_not_main")

remote_heads = {
    line.removeprefix("origin/")
    for line in git(
        "for-each-ref",
        "refs/remotes/origin",
        "--format=%(refname:short)",
    ).splitlines()
    if line.startswith("origin/") and not line.endswith("/HEAD")
}
if remote_heads and remote_heads != {"main"}:
    fail("remote_branches_" + ",".join(sorted(remote_heads)))

all_refs = git("for-each-ref", "--format=%(refname)").splitlines()
if any(
    ref.endswith("/master")
    or "/orx/" in ref
    or ref.endswith("/orx")
    or ref.startswith("refs/original/")
    for ref in all_refs
):
    fail("legacy_branch_ref")

commit_count = int(git("rev-list", "--count", "--all"))
if commit_count < 4:
    fail("commit_count_" + str(commit_count))

identity_rows = git(
    "log",
    "--all",
    "--format=%an <%ae>|%cn <%ce>",
).splitlines()
expected_row = EXPECTED_IDENTITY + "|" + EXPECTED_IDENTITY
if not identity_rows or any(row != expected_row for row in identity_rows):
    fail("noncanonical_commit_identity")

claims_doc = load("claims.json")
claims = {claim["id"]: claim for claim in claims_doc["claims"]}
if set(claims) != set(EXPECTED_CLAIMS):
    fail("claim_ids")
if {
    claim_id: claims[claim_id]["status"]
    for claim_id in EXPECTED_CLAIMS
} != EXPECTED_CLAIMS:
    fail("claim_statuses")
if claims_doc.get("overall_status") != EXPECTED_STATUS:
    fail("claims_status")
for claim in claims.values():
    if claim.get("paper_claim_reproduced") is not False:
        fail("paper_claim_reproduced")

audit = claims_doc.get("audit", {})
for field, expected in (
    ("finite_proxy_diagnostics_passed", 5),
    ("finite_proxy_diagnostics_total", 5),
    ("negative_diagnostics", 0),
    ("claims_not_reproduced", 1),
    ("paper_claims_not_verified", 6),
    ("claims_total", 6),
    ("evidence_points", 10),
    ("evidence_points_total", 12),
    ("paper_claims_verified", 0),
):
    if audit.get(field) != expected:
        fail("claims_" + field)
for field in ("current_score_claim", "publication_allowed"):
    if audit.get(field) is not False:
        fail("claims_" + field)

verdict = load("outputs/verdict.json")
if verdict.get("overall_status") != EXPECTED_STATUS:
    fail("verdict_status")
if verdict.get("paper_reproduction") != "inconclusive":
    fail("verdict_paper_reproduction")
for field, expected in (
    ("claims_total", 6),
    ("finite_proxy_diagnostics_passed", 5),
    ("finite_proxy_diagnostics_total", 5),
    ("negative_diagnostics", 0),
    ("claims_not_reproduced", 1),
    ("paper_claims_not_verified", 6),
    ("evidence_points", 10),
    ("evidence_points_total", 12),
    ("paper_claims_verified", 0),
):
    if verdict.get(field) != expected:
        fail("verdict_" + field)
for field in ("current_score_claim", "publication_allowed"):
    if verdict.get(field) is not False:
        fail("verdict_" + field)
if verdict.get("claim_status") != EXPECTED_CLAIMS:
    fail("verdict_claim_status")

verdict_claims = {claim["id"]: claim for claim in verdict.get("claims", [])}
for claim_id, expected_status in EXPECTED_CLAIMS.items():
    claim = verdict_claims.get(claim_id, {})
    if claim.get("status") != expected_status:
        fail("verdict_" + claim_id)
    if claim.get("paper_claim_reproduced") is not False:
        fail("verdict_" + claim_id + "_paper_claim")

diagnostics = load("outputs/diagnostics.json")
expected_diagnostics = {
    "C1_model": ("FINITE_MODEL_CONSTRUCTION_PROXY", True),
    "C2_induced_deps": ("FINITE_GRAPH_STRUCTURE_PROXY", True),
    "C3_dsep_capture": ("FINITE_DSEP_ENUMERATION_PROXY", True),
    "C4_pc_sound": ("FINITE_PC_GRAPH_PROXY", True),
    "C5_multi_env": ("TAUTOLOGICAL_MULTI_ENV_PROXY", True),
    "C6_real_data": ("NOT_REPRODUCED", False),
}
if set(diagnostics.get("claims", {})) != set(expected_diagnostics):
    fail("diagnostic_keys")
for key, (expected_status, expected_pass) in expected_diagnostics.items():
    diagnostic = diagnostics["claims"][key]
    if diagnostic.get("status") != expected_status:
        fail("diagnostic_" + key)
    if diagnostic.get("finite_proxy_passed") is not expected_pass:
        fail("diagnostic_" + key + "_pass")

gate = load("outputs/gate.json")
for field in ("tests_passed", "documentation_gate_passed", "publication_gate_passed"):
    if gate.get(field) is not True:
        fail("gate_" + field)
for field in (
    "paper_reproduction_gate_passed",
    "paper_algorithm_implemented",
    "paper_claims_reproduced",
    "current_score_claim",
    "publication_allowed",
):
    if gate.get(field) is not False:
        fail("gate_" + field)
if gate.get("overall_status") != EXPECTED_STATUS:
    fail("gate_status")
if gate.get("claim_status") != EXPECTED_CLAIMS:
    fail("gate_claim_status")

publication_gate = load("publication_gate.json")
if publication_gate.get("overall_status") != EXPECTED_STATUS:
    fail("publication_status")
if publication_gate.get("paper_reproduction_gate_passed") is not False:
    fail("publication_paper_gate")
if publication_gate.get("publication_allowed") is not False:
    fail("publication_allowed")

verdicts = load("reproduction_verdicts.json")
if verdicts.get("overall_status") != EXPECTED_STATUS:
    fail("reproduction_status")
if verdicts.get("claim_statuses") != EXPECTED_CLAIMS:
    fail("reproduction_claim_statuses")
if verdicts.get("evidence", {}).get("paper_claims_verified") != 0:
    fail("reproduction_paper_claims")
if verdicts.get("evidence", {}).get("evidence_points") != 10:
    fail("reproduction_evidence_points")

state = load("AUTONOMOUS_STATE.json")
if state.get("status") != EXPECTED_STATUS:
    fail("state_status")
if state.get("repository", {}).get("recovery_bundle_sha256") != EXPECTED_RECOVERY_SHA:
    fail("state_recovery_sha")
if state.get("repository", {}).get("canonical_email") != (
    "MachineLearning-Nerd@users.noreply.github.com"
):
    fail("state_identity")
if state.get("source", {}).get("source_tip_before_standardization") != EXPECTED_SOURCE_TIP:
    fail("state_source_tip")

manifest = load("EVIDENCE_MANIFEST.json")
missing = [
    path
    for path in manifest["required_paths"]
    if not (ROOT / path).is_file()
]
if missing:
    fail("missing_paths_" + ",".join(missing))

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for marker in (
    "2606.05689",
    "CLAIM_EVIDENCE.md",
    "CITATION.cff",
    "Thank you",
    "0/6",
    "10/12",
    "TAUTOLOGICAL_MULTI_ENV_PROXY",
    "MachineLearning-Nerd",
):
    if marker not in readme:
        fail("readme_" + marker.replace(" ", "_"))

branch_audit = (ROOT / "BRANCH_AUDIT.md").read_text(encoding="utf-8")
for marker in (EXPECTED_IDENTITY, EXPECTED_SOURCE_TIP, EXPECTED_RECOVERY_SHA):
    if marker not in branch_audit:
        fail("branch_audit_" + marker[:12])

print(
    "FINAL_AUDIT=VERIFIED "
    "branches=1 commits="
    + str(commit_count)
    + " claims=C1:model,C2:graph,C3:dsep,C4:pc,C5:tautological,C6:not_reproduced "
    + "evidence_points=10 paper_claims_verified=0 current_score_claim=false "
    + "publication_allowed=false"
)
