---
document: DECISION_LINEAGE_SCHEMA
version: 1.1
status: CANONICAL_PENDING_MERGE
owner: USER
updated_at: 2026-08-04
---

# Decision Lineage Schema

Every important decision must preserve enough information to answer why it exists and what would be affected if its premises changed.

## Decision record

```text
DECISION_ID
PROBLEM
CONTEXT
PREMISES
SOURCE_REFERENCES
CONSIDERED_OPTIONS
SELECTED_OPTION
SELECTION_REASON
REJECTED_OPTIONS
REJECTION_REASONS
EXPECTED_CONSEQUENCES
OBSERVED_CONSEQUENCES
DECISION_OWNER
DECIDED_AT
SUPERSEDES
SUPERSEDED_BY
STATUS
```

A decision is incomplete when its selected option is known but its owner, premises, alternatives or reason are missing.

## Truth classes

### FACT

A statement supported by an identified authoritative source or verified observation.

Required minimum:

```text
STATEMENT
SOURCE_ID
OBSERVED_AT
STATUS
```

### DECISION

A choice explicitly made by an authorized human decision owner.

Required minimum:

```text
DECISION_ID
DECISION_OWNER
DECIDED_AT
DECISION_LINEAGE
STATUS
```

### HYPOTHESIS

An uncertain interpretation, predicted relation, recommendation or possible consequence.

Required minimum:

```text
STATEMENT
PROPOSED_BY
SOURCE_OR_REASONING_REFERENCE
CONFIDENCE
STATUS
```

## Promotion rule

No automatic promotion is allowed:

```text
HYPOTHESIS → FACT
HYPOTHESIS → DECISION
AI_RECOMMENDATION → DECISION
AI_PROPOSED_RELATION → CONFIRMED_RELATION
```

Promotion requires an authoritative source or an explicit act of the authorized human decision owner.

## Relation authority

Every important relation must expose:

```text
RELATION_TYPE
SOURCE_ID
PROPOSED_BY
CONFIDENCE
STATUS
```

Confidence expresses uncertainty. It does not grant authority.
