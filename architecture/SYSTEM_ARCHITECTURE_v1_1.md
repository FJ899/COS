---
document: SYSTEM_ARCHITECTURE
version: 1.1
status: CANONICAL_PENDING_MERGE
owner: USER
updated_at: 2026-08-04
---

# Ecosystem Architecture v1.1

```text
User
  ↓
Ginseng
Decision Intelligence Layer
  ↓
Creative OS
Canonical Memory + Decisions
  ↓
PROJECT CONTRACT
  ↓
TASK CONTRACT
  ↓
Executor
Controlled Execution
  ↓
Verifier
Independent Proof
```

## Responsibility boundaries

### User

Owns goals, priorities, canon, risk acceptance, merge and final decisions.

### Ginseng

Explains why the current state exists, which alternatives were considered, which functions create effects and what may change when assumptions change.

Ginseng does not execute work, does not own canon and does not issue an authoritative technical `ACCEPT`.

### Creative OS

Owns canonical truth, project state, explicit user decisions, governance and references to local sources of truth.

Creative OS records what is currently true. It does not replace the Executor or Verifier.

### Project Contract

Defines the durable purpose, value, boundaries, forbidden directions, decision owner and closure conditions of one project.

### Task Contract

Defines one authorized operation. It cannot change the Project Contract.

### Executor

Performs contracted work inside the authorized scope and produces raw evidence. It cannot choose the goal or certify its own success.

### Verifier

Checks exact code, environment, scope, evidence and replay. It owns the technical `ACCEPT / REWORK / STOP` verdict but does not own merge or business acceptance.

## Prohibited shortcut

```text
AI → Executor → external change
```

Every execution must remain bound to a Project Contract, Task Contract, authorized scope and independent proof.

## Canonical references

- `governance/ECOSYSTEM_EXECUTION_CONTROL_PACKAGE_v1.1.md`
- `governance/SYSTEM_INVARIANTS.md`
- `governance/GINSENG_DECISION_INTELLIGENCE_CONTRACT.md`
- `governance/ECOSYSTEM_DECISION_REGISTER.md`
