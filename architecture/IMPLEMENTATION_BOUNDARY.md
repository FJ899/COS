---
document: IMPLEMENTATION_BOUNDARY
version: 1.1
status: CANONICAL_PENDING_MERGE
owner: USER
updated_at: 2026-08-04
---

# Implementation Boundary

## Frozen now

The following define the enduring meaning and responsibility of Ginseng:

- `Ginseng = Decision Intelligence Layer`;
- the boundary between Ginseng, Creative OS, Executor and Verifier;
- separation of `FACT / DECISION / HYPOTHESIS`;
- Decision Lineage;
- relation authority;
- the ability to explain impact through `ELEMENT → FUNCTION / CAPABILITY → EFFECT`;
- prohibition on AI confirming its own hypothesis or relation;
- Creative OS ownership of canon;
- prohibition on Ginseng executing external changes.

Changing these items requires a new canonical user decision and Human Decision Gate.

## Technically open

The following remain implementation decisions:

- `Node`, `Entity` or another internal name;
- database model;
- JSON, SQL or another storage representation;
- API design;
- indexing strategy;
- query language;
- internal module boundaries;
- deployment topology;
- UI technology;
- graph rendering technology.

These choices may change after tests without changing the meaning of Ginseng.

## Development order

```text
1. Executor P1
2. Executor P2
3. P3A value validation
4. P3B safe execution validation
5. full P3 verdict
```

After **Executor P1 ACCEPT**, work may begin only on the definition and tests of the Ginseng Minimal Kernel, Impact Class, confidence/uncertainty model and Creative OS self-test.

After **full P3 ACCEPT**, a separate Human Decision Gate may authorize Ginseng runtime, visualization, multi-variant scenarios and external imports.

## Current prohibition

Until the gates above are passed, do not build:

- Ginseng runtime;
- graph UI;
- external imports;
- automatic confirmed-relation creation;
- enterprise platform features.

The current implementation priority remains:

```text
EXECUTOR P1
PR #32
P1-001–P1-006
GREEN SECURITY CONTRACT VERIFIED
```
