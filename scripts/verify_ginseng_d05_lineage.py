#!/usr/bin/env python3
"""Fail-closed verification for the minimal Ginseng D-05 lineage proof."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROOF_PATH = "governance/GINSENG_D05_DECISION_LINEAGE_PROOF_2026-08-19.json"

SOURCE_BINDINGS = {
    "test_contract_current": (
        "tests/ginseng/GINSENG_TEST-003_SINGLE_GATE_CLOSURE.md",
        "b901fde1601d21acf04513971f39a8e977e6f96f",
    ),
    "test_decision_fixture": (
        "tests/ginseng/GINSENG_TEST-003_DECISION_A_2026-08-18.json",
        "93c648ee9e9f69b60a62f00b7d5b007d84ec32a3",
    ),
    "input_manifest": (
        "tests/ginseng/GINSENG_TEST-003_INPUT_MANIFEST_2026-08-18.json",
        "e3eb9cdee59cfd248892435cc6b130992a7160c7",
    ),
    "execution_protocol": (
        "tests/ginseng/GINSENG_TEST-003_EXECUTION_PROTOCOL_2026-08-18.md",
        "d94cf828c42ac52ab875c729eccede06cbb795df",
    ),
    "result_record": (
        "tests/ginseng/GINSENG_TEST-003_RESULT_RECORD_2026-08-18.md",
        "4ca0bb2065d3914e73b5ec8f3283894b681f9d54",
    ),
    "d0_done_freeze": (
        "governance/GINSENG_DONE_D0_FREEZE_2026-08-18.md",
        "eafc5d21729c393801ee3f1c7e3d57e7da883ee3",
    ),
    "d0_evidence_audit": (
        "governance/GINSENG_D0_EVIDENCE_AUDIT_2026-08-18.md",
        "48065e555c338ba68f309d879080dfcdf81ba3c2",
    ),
}

REQUIRED_FIELDS = [
    "DECISION_ID",
    "PROBLEM",
    "PREMISES",
    "CONSIDERED_OPTIONS",
    "SELECTED_OPTION",
    "SELECTION_REASON",
    "REJECTED_OPTIONS",
    "REJECTION_REASONS",
    "EXPECTED_CONSEQUENCES",
    "DECISION_OWNER",
    "DECIDED_AT",
    "SOURCE_REFERENCES",
    "SUPERSEDES",
    "SUPERSEDED_BY",
    "STATUS",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def load_text(path: str) -> str:
    try:
        return (ROOT / path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        fail(f"cannot read {path}: {exc}")
    raise AssertionError("unreachable")


def load_json(path: str) -> dict:
    try:
        value = json.loads(load_text(path))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain a JSON object")
    return value


def git_blob_sha(path: str) -> str:
    raw = (ROOT / path).read_bytes()
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def require_markers(content: str, markers: list[str], owner: str) -> None:
    for marker in markers:
        if marker not in content:
            fail(f"{owner} missing source marker: {marker}")


def verify_sources(proof: dict) -> None:
    bindings = proof.get("source_bindings")
    if not isinstance(bindings, dict):
        fail("source_bindings must be an object")
    if set(bindings) != set(SOURCE_BINDINGS):
        fail("source_bindings differ from the exact accepted D0 evidence set")

    for source_id, (path, expected_sha) in SOURCE_BINDINGS.items():
        entry = bindings.get(source_id)
        if entry != {"path": path, "git_blob_sha": expected_sha}:
            fail(f"source binding mismatch: {source_id}")
        actual_sha = git_blob_sha(path)
        if actual_sha != expected_sha:
            fail(f"source bytes changed: {source_id} expected={expected_sha} actual={actual_sha}")
    print("[PASS] exact source bytes are bound")


def verify_source_semantics() -> None:
    contract = load_text(SOURCE_BINDINGS["test_contract_current"][0])
    require_markers(
        contract,
        [
            "ACT002",
            "DEC002",
            "VARIANT_A_KEEP_DEC002",
            "VARIANT_B_SUPERSEDE_DEC002",
            "Domyślnym wariantem pierwszego uruchomienia jest `VARIANT_A_KEEP_DEC002`, ponieważ nie wymaga zmiany zatwierdzonej decyzji bazowej.",
            "blocking_gate_count_after = 6",
            "implementation_readiness_after = BLOCKED",
            "baseline_mutated_after = false",
        ],
        "Test-003 contract",
    )

    fixture = load_json(SOURCE_BINDINGS["test_decision_fixture"][0])
    if fixture.get("decision_id") != "GINSENG_TEST003_DECISION_A":
        fail("fixture decision_id mismatch")
    if fixture.get("decision_type") != "TEST_ONLY_DECISION":
        fail("fixture decision type mismatch")
    if fixture.get("variant") != "VARIANT_A_KEEP_DEC002":
        fail("fixture variant mismatch")
    if fixture.get("subject") != ["DEC002", "R003", "P002"]:
        fail("fixture subject mismatch")
    authority = fixture.get("authority", {})
    if authority.get("production_decision") is not False or authority.get("baseline_change_authorized") is not False:
        fail("fixture authority boundary mismatch")
    expected_scope = fixture.get("expected_scope", {})
    expected_fixture_scope = {
        "resolve_exactly_one_gate": "complaints_ownership",
        "resolve_overlay_gate": "PROCESS_OWNER_GATE",
        "remaining_blocking_gate_count": 6,
        "implementation_readiness": "BLOCKED",
        "baseline_mutated": False,
    }
    if expected_scope != expected_fixture_scope:
        fail("fixture expected_scope mismatch")

    manifest = load_json(SOURCE_BINDINGS["input_manifest"][0])
    test_decision = manifest.get("test_decision", {})
    if test_decision.get("decision_id") != "GINSENG_TEST003_DECISION_A":
        fail("input manifest decision_id mismatch")
    if test_decision.get("decision_type") != "TEST_ONLY_DECISION":
        fail("input manifest decision_type mismatch")
    if test_decision.get("variant") != "VARIANT_A_KEEP_DEC002":
        fail("input manifest selected variant mismatch")
    if test_decision.get("production_effect") != "NONE":
        fail("input manifest production effect mismatch")
    after = manifest.get("expected_after_constraints", {})
    if after.get("blocking_gate_count") != 6:
        fail("input manifest blocking gate count mismatch")
    if after.get("removed_active_gate_exactly") != "complaints_ownership":
        fail("input manifest active gate mismatch")
    if after.get("resolved_overlay_gate_exactly") != "PROCESS_OWNER_GATE":
        fail("input manifest overlay gate mismatch")
    if after.get("remaining_gates_semantically_preserved") is not True:
        fail("input manifest remaining-gates premise missing")
    if after.get("implementation_readiness") != "BLOCKED" or after.get("baseline_mutated") is not False:
        fail("input manifest readiness/baseline mismatch")
    if after.get("no_impact_controls_preserved_unless_new_causal_path_is_proved") is not True:
        fail("input manifest NO_IMPACT preservation missing")
    if after.get("source_traceability_complete") is not True:
        fail("input manifest source traceability missing")

    protocol = load_text(SOURCE_BINDINGS["execution_protocol"][0])
    require_markers(
        protocol,
        [
            "owner: HUMAN_TEST_CONTRACT",
            "production_effect: NONE",
            "because it does not supersede the approved baseline decision",
            "GINSENG_TEST003_DECISION_A",
        ],
        "execution protocol",
    )

    result = load_text(SOURCE_BINDINGS["result_record"][0])
    require_markers(
        result,
        [
            "recorded_at: 2026-08-18",
            "executed_at: 2026-08-18",
            "variant: VARIANT_A_KEEP_DEC002",
            "GINSENG_TEST-003: PASS",
            "GINSENG_TEST003_DECISION_A",
            "TEST_ONLY_DECISION",
            "production effect: NONE",
        ],
        "Test-003 result record",
    )

    done = load_text(SOURCE_BINDINGS["d0_done_freeze"][0])
    for field in REQUIRED_FIELDS:
        require_markers(done, [field], "GINSENG_DONE_D0")

    audit = load_text(SOURCE_BINDINGS["d0_evidence_audit"][0])
    require_markers(
        audit,
        [
            "### D-05 — DECISION LINEAGE",
            "NOT SATISFIED",
            "This is the smallest currently measured functional proof gap.",
        ],
        "D0 evidence audit",
    )
    print("[PASS] every lineage semantic is supported by existing accepted sources")


def verify_no_superseder() -> None:
    patterns = [
        re.compile(r'(?i)\"supersedes\"\s*:\s*\"GINSENG_TEST003_DECISION_A\"'),
        re.compile(r'(?i)\"superseded_by\"\s*:\s*\"GINSENG_TEST003_DECISION_A\"'),
        re.compile(r'(?i)\bSUPERSEDES\b\s*[:=]\s*`?GINSENG_TEST003_DECISION_A\b'),
        re.compile(r'(?i)\bSUPERSEDED_BY\b\s*[:=]\s*`?GINSENG_TEST003_DECISION_A\b'),
    ]
    proof_file = (ROOT / PROOF_PATH).resolve()
    for base in (ROOT / "tests/ginseng", ROOT / "governance"):
        for path in base.rglob("*"):
            if path.resolve() == proof_file or path.suffix.lower() not in {".md", ".json"}:
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for pattern in patterns:
                if pattern.search(content):
                    fail(f"accepted evidence contains a superseder reference in {path.relative_to(ROOT)}")
    print("[PASS] no superseder is present in current accepted D0 text evidence")


def verify_proof() -> None:
    proof = load_json(PROOF_PATH)
    expected_top = {
        "schema_version": "ginseng-d05-decision-lineage-proof/1.0",
        "record_status": "D05_SATISFIED_IF_VERIFIED_AND_ACCEPTED",
        "candidate": "GINSENG_CANDIDATE_R0",
        "done_scope": "GINSENG_DONE_D0",
        "gate": "D-05 DECISION LINEAGE",
        "proof_method": "SOURCE_BOUND_RECONSTRUCTION_ONLY",
        "new_behavioral_test": False,
        "new_runtime_capability": False,
    }
    for key, value in expected_top.items():
        if proof.get(key) != value:
            fail(f"proof metadata mismatch: {key}")

    lineage = proof.get("decision_lineage")
    if not isinstance(lineage, dict):
        fail("decision_lineage must be an object")
    if list(lineage) != REQUIRED_FIELDS:
        fail("decision_lineage fields/order differ from frozen D-05 minimum")

    expected_lineage = {
        "DECISION_ID": "GINSENG_TEST003_DECISION_A",
        "PROBLEM": {
            "conflict": "ACT002 <-> DEC002",
            "action_meaning": "przeniesienie wlasciciela reklamacji",
            "baseline_decision_meaning": "wlasciciel procesu reklamacji pozostaje w Obsludze Klienta",
        },
        "PREMISES": [
            "DEC002 is the approved baseline decision used by Test-003 and Variant A preserves it.",
            "GINSENG_TEST003_DECISION_A is TEST_ONLY_DECISION with no production effect and no authority to mutate the baseline.",
            "The bounded decision subject is DEC002 / R003 / P002.",
        ],
        "CONSIDERED_OPTIONS": [
            {
                "id": "VARIANT_A_KEEP_DEC002",
                "meaning": "Preserve DEC002 and preserve the complaints-process owner in a distinct Customer Service function inside the proposed Customer Operations structure.",
            },
            {
                "id": "VARIANT_B_SUPERSEDE_DEC002",
                "meaning": "Add a formal decision superseding DEC002 and move responsibility to a new role.",
            },
        ],
        "SELECTED_OPTION": "VARIANT_A_KEEP_DEC002",
        "SELECTION_REASON": "Variant A is the default first-run variant because it does not require changing the approved baseline decision.",
        "REJECTED_OPTIONS": ["VARIANT_B_SUPERSEDE_DEC002"],
        "REJECTION_REASONS": {
            "VARIANT_B_SUPERSEDE_DEC002": "Not selected for the first run: Variant B requires a formal decision superseding DEC002, while the contract selects Variant A specifically to avoid changing the approved baseline decision."
        },
        "EXPECTED_CONSEQUENCES": {
            "resolve_active_gate": "complaints_ownership",
            "resolve_overlay_gate": "PROCESS_OWNER_GATE",
            "remaining_blocking_gate_count": 6,
            "remaining_gates_semantically_preserved": True,
            "implementation_readiness": "BLOCKED",
            "baseline_mutated": False,
            "no_impact_controls_preserved_unless_new_causal_path_is_proved": True,
            "source_traceability_complete": True,
        },
        "DECISION_OWNER": "HUMAN_TEST_CONTRACT",
        "DECIDED_AT": "2026-08-18",
        "SOURCE_REFERENCES": list(SOURCE_BINDINGS),
        "SUPERSEDES": [],
        "SUPERSEDED_BY": [],
        "STATUS": "APPLIED_IN_GINSENG_TEST003 / TEST_ONLY_DECISION / NO_PRODUCTION_EFFECT",
    }
    if lineage != expected_lineage:
        fail("decision_lineage content differs from the source-bound expected record")

    provenance = proof.get("field_provenance")
    if not isinstance(provenance, dict) or list(provenance) != REQUIRED_FIELDS:
        fail("field_provenance is incomplete or reordered")
    allowed_modes = {
        "DIRECT",
        "DIRECT_COMPOSITION",
        "DETERMINISTIC_FROM_TWO_OPTION_SELECTION",
        "DETERMINISTIC_SOURCE_COMPOSITION",
        "BOUND_TO_AUTHORIZED_EXECUTION_DATE",
        "DIRECT_NEGATIVE",
        "CURRENT_ACCEPTED_EVIDENCE_NEGATIVE_SCAN",
    }
    for field, record in provenance.items():
        if not isinstance(record, dict) or record.get("mode") not in allowed_modes:
            fail(f"unsupported provenance mode for {field}")
        sources = record.get("sources")
        if not isinstance(sources, list) or not sources or any(source not in SOURCE_BINDINGS for source in sources):
            fail(f"invalid provenance sources for {field}")

    negatives = proof.get("negative_assertions")
    if negatives != {
        "production_decision_created": False,
        "baseline_change_claimed": False,
        "runtime_required": False,
        "new_normative_meaning_added": False,
        "known_superseder_in_current_accepted_d0_evidence": False,
    }:
        fail("negative assertions mismatch")

    closure = proof.get("closure_condition", "")
    if "passes the fail-closed repository verifier" not in closure or "does not claim Ginseng D0 completion" not in closure:
        fail("closure condition is missing fail-closed/non-completion boundary")
    print("[PASS] complete 15-field Decision Lineage record is deterministic")


def main() -> None:
    verify_sources(load_json(PROOF_PATH))
    verify_source_semantics()
    verify_no_superseder()
    verify_proof()
    print("[PASS] no new behavior, runtime capability, production decision or baseline mutation was introduced")
    print("GINSENG_D05_DECISION_LINEAGE: PASS")


if __name__ == "__main__":
    main()
