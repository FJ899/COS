#!/usr/bin/env python3
"""Canonical effect-capable Projector v2.1 trusted runtime.

This layer deliberately owns the trust boundary.  It never accepts Human
authority, ancestry, object metadata, topology, base identity, or write-time
revalidation as caller dictionaries.  It invokes the concrete Git read adapter
and concrete GitHub Human-authority adapter itself.
"""

from __future__ import annotations

import copy
from typing import Any

from projector_public_effect_gate import (
    GitHubIssueCommentAuthoritySource,
    GitRepositoryEvidenceSource,
    InMemoryNonPublicTestSink,
    PublicEffectWriteSink,
    _Blocked,
    _blocked,
    _object,
    _prepare,
    _validate_human_authority,
    _validated_write_result,
    authority_request,
)


def _canonicalize_trusted_git_proof(observed: dict[str, Any]) -> dict[str, Any]:
    """Keep freshness in source_invocation_id while making proof identity fact-bound.

    The frozen D_PRE_X binds ancestry proof identity.  A new live read of the same
    exact Git relation must reproduce the same D_HASH_X; freshness is separately
    proven by the trusted adapter invocation identity and timestamps.
    """
    value = copy.deepcopy(observed)
    repo = value["repository"]
    frozen = value["frozen_source_sha"]
    base = value["base_observation"]["sha"]
    candidate = value["candidate_observation"]["sha"]
    frozen_status = value["ancestry"]["frozen_to_base"]["status"]
    candidate_status = value["ancestry"]["base_to_candidate"]["status"]
    value["ancestry"]["frozen_to_base"]["evidence_ref"] = (
        f"git-proof:{repo}:frozen-to-base:{frozen_status}:{frozen}:{base}"
    )
    value["ancestry"]["base_to_candidate"]["evidence_ref"] = (
        f"git-proof:{repo}:base-to-candidate:{candidate_status}:{base}:{candidate}"
    )
    return value


def _fresh_prepare(spec: dict[str, Any], git_source: GitRepositoryEvidenceSource, trust_level: str) -> dict[str, Any]:
    observed = git_source.observe(_object(spec, "effect spec"))
    canonical = _canonicalize_trusted_git_proof(observed)
    return _prepare(canonical, trust_level=trust_level)


def prepare_trusted_public_effect_authority_request(
    spec: dict[str, Any],
    git_source: GitRepositoryEvidenceSource,
) -> dict[str, Any]:
    """Fresh trusted B_PRE_X/Git proof for the Human gate; no write capability."""
    if type(git_source) is not GitRepositoryEvidenceSource:
        return _blocked("UNTRUSTED_GIT_EVIDENCE_SOURCE_TYPE")
    try:
        prepared = _fresh_prepare(spec, git_source, "TRUSTED_LIVE_GIT_PRE_HUMAN_GATE")
        return {
            "status": "AWAITING_HUMAN_PUBLIC_EFFECT_AUTHORITY",
            "prepared": prepared,
            "authority_request": authority_request(prepared),
            "source_invocation_id": prepared["source_invocation_id"],
            "target_write_performed": False,
        }
    except _Blocked as exc:
        return _blocked(exc.reason)


def _load_human_authority_fail_closed(
    source: GitHubIssueCommentAuthoritySource,
    request: dict[str, Any],
) -> dict[str, Any]:
    """Convert malformed/app-mediated authority source failures to BLOCKED semantics."""
    try:
        return source.load_authority(request)
    except _Blocked:
        raise
    except TypeError as exc:
        # GitHub REST represents performed_via_github_app as an object when set.
        # A malformed or app-mediated authority record must never escape as an
        # uncaught exception on the effect-capable path; it is UNKNOWN/BLOCKED.
        raise _Blocked("GitHub App-mediated or malformed Human authority record rejected") from exc
    except Exception as exc:
        raise _Blocked(f"trusted Human authority source failed closed: {type(exc).__name__}") from exc


def execute_trusted_public_effect(
    spec: dict[str, Any],
    human_authority_source: GitHubIssueCommentAuthoritySource,
    git_source: GitRepositoryEvidenceSource,
    sink: PublicEffectWriteSink,
) -> dict[str, Any]:
    """Only canonical PUBLIC_EFFECT consumer: live Git -> Human -> live Git -> sink."""
    if type(git_source) is not GitRepositoryEvidenceSource:
        return _blocked("UNTRUSTED_GIT_EVIDENCE_SOURCE_TYPE")
    if type(human_authority_source) is not GitHubIssueCommentAuthoritySource:
        return _blocked("UNTRUSTED_HUMAN_AUTHORITY_SOURCE_TYPE")
    if (git_source.test_only or human_authority_source.test_only) and type(sink) is not InMemoryNonPublicTestSink:
        return _blocked("TEST_ONLY_TRUSTED_SOURCE_CANNOT_REACH_EXTERNAL_SINK")

    try:
        pre_authority = _fresh_prepare(spec, git_source, "TRUSTED_LIVE_GIT_AUTHORITY_VERIFICATION")
        request = authority_request(pre_authority)
        authority = _load_human_authority_fail_closed(human_authority_source, request)
        _validate_human_authority(pre_authority, authority)

        write_time = _fresh_prepare(spec, git_source, "TRUSTED_LIVE_GIT_WRITE_TIME_REVALIDATION")
        if pre_authority["source_invocation_id"] == write_time["source_invocation_id"]:
            raise _Blocked("write-time Git observation was not a distinct trusted invocation")
        if authority_request(write_time) != request:
            raise _Blocked("write-time live Git state differs from Human-authorized tuple")
        _validate_human_authority(write_time, authority)
    except _Blocked as exc:
        return _blocked(exc.reason)

    write_result = sink.write(write_time["public_effect_gate"]["effect_descriptor"])
    try:
        result = _validated_write_result(write_result)
    except _Blocked as exc:
        raise RuntimeError(
            "external write occurred but exact result identity is unavailable; reconciliation required: " + exc.reason
        ) from exc

    gate = write_time["public_effect_gate"]
    return {
        "schema_version": "projector-public-effect-gate-result/1.1",
        "status": "PUBLIC_EFFECT_COMPLETED_REVIEW_REQUIRED",
        "effect_evidence_status": "OBSERVED",
        "target_write_performed": True,
        "target_write_result": result,
        "public_effect_gate": {
            "effect_kind": gate["effect_kind"],
            "repository": gate["repository"],
            "base_ref": gate["base_ref"],
            "frozen_source_sha": gate["frozen_source_sha"],
            "fresh_base_sha": gate["fresh_base_sha"],
            "base_relation": gate["base_relation"],
            "candidate_sha": gate["candidate_sha"],
            "ancestry_evidence_refs": gate["ancestry_evidence_refs"],
            "diff_manifest_ref": f"sha256:{gate['diff_manifest_sha256']}",
            "diff_manifest_sha256": gate["diff_manifest_sha256"],
            "effect_descriptor_ref": f"sha256:{gate['effect_sha256']}",
            "effect_sha256": gate["effect_sha256"],
            "human_authority_evidence_ref": authority["human_decision_evidence_ref"],
            "authority_classification": "GENUINE_HUMAN_OWNED_GATE",
            "authority_basis": "PUBLIC_EFFECT",
            "write_time_revalidation": "PASS",
            "write_time_revalidation_evidence_ref": gate["base_observation_ref"],
            "write_time_source_invocation_id": write_time["source_invocation_id"],
            "write_performed": True,
            "write_result_ref": result["result_ref"],
        },
        "merge_authorized": False,
        "release_authorized": False,
        "deploy_authorized": False,
        "capability_promotion_authorized": False,
        "human_final_acceptance_created": False,
    }
