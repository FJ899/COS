---
document: GINSENG_INVARIANTS_REFERENCE
version: 1.1
status: CANONICAL_REFERENCE_PENDING_MERGE
owner: USER
updated_at: 2026-08-04
authoritative_source: governance/GINSENG_DECISION_INTELLIGENCE_CONTRACT.md
---

# Ginseng Invariants

Authoritative definitions remain in `governance/GINSENG_DECISION_INTELLIGENCE_CONTRACT.md`. This file is a stable architecture index and must not redefine the invariant IDs.

## GIN-001 — Decision Intelligence, not graph product

Ginseng preserves and analyzes decisions. A graph is only a representation.

## GIN-002 — Truth types never mix

`FACT`, `DECISION` and `HYPOTHESIS` remain separate in data, analysis and presentation.

## GIN-003 — Important decisions require lineage

An important decision without premises, alternatives, rationale and consequences is incomplete.

## GIN-004 — AI cannot confirm its own relation

An AI-proposed relation remains `UNCONFIRMED` or `AI_ESTIMATE` until confirmed by an authoritative source or authorized human.

## GIN-005 — Impact must explain function

A relevant effect must be traceable through the function or capability that produces it.

## GIN-006 — Question precedes map

A full map without an analytical question is supporting material, not a valuable Ginseng result.

## GIN-007 — Creative OS owns canon

Ginseng explains reasons and change impact. Creative OS remains the owner of canonical project truth.

## Consequences derived from the invariants

- alternative branches and rejected options must not be silently discarded;
- important relations expose source, proposer, confidence and status;
- Ginseng does not execute external changes;
- technical implementation choices do not become semantic invariants.
