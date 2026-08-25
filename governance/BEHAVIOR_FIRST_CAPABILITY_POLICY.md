# BEHAVIOR-FIRST CAPABILITY POLICY

Status: `ACTIVE / HUMAN-DIRECTED GOVERNANCE`
Decision date: 2026-08-25
Scope: capability claims preserved or promoted through COS. Local semantic owners keep their own domain truth; when COS reports a capability status, this policy applies.

## Hard invariants

```text
ARCHITECTURE != PROGRESS

SPECIFICATION
!= IMPLEMENTATION
!= WORKING CAPABILITY
!= RELIABLE CAPABILITY

README CLAIM + NO EXECUTABLE PROOF = HYPOTHESIS
```

A README, diagram, interface, folder, class, schema, agent name, prompt or architecture document is not a capability. It may describe an intended mechanism, but it cannot promote capability status.

The governing rule is:

> A function does not exist as a supported capability until executable evidence demonstrates the claimed behavior.

## 1. Behavior before architecture

Before a new mechanism is created, record one concrete behavioral case:

```text
INPUT
-> EXPECTED EFFECT
-> VERIFICATION METHOD
```

Architecture may follow a real case. A diagram or interface cannot substitute for the case.

## 2. No component without pressure

A new module, layer, router, scheduler, agent, cache, runtime, adapter or abstraction may be introduced only when a named current case is blocked or failing without it.

Forbidden justification:

```text
"we will probably need it"
```

Required justification:

```text
"this current test / real workflow fails for this observed reason"
```

## 3. Every promoted claim requires executable evidence

If documentation claims that the system performs behavior X, the capability must be registered in `governance/CAPABILITY_REGISTRY.json`.

For `TESTED` or higher, the registry must identify executable proof that CI actually runs. If the proof does not exist or is not executed in CI, the claim cannot be promoted beyond `IMPLEMENTED`.

## 4. Vertical slice before system skeleton

Prefer one complete flow:

```text
input -> operation -> effect -> verification
```

over a skeleton of empty subsystems.

Do not create placeholder trees such as `router/`, `memory/`, `planner/`, `executor/`, `evaluator/` unless current behavior requires them.

## 5. Definition of Done is effect-based

Invalid DONE:

```text
Executor implemented.
```

Valid form:

```text
Given X, the system performs Y, persists/reports Z as required,
and the specified verification passes.
```

Code volume, file count, architecture coverage and documentation completeness do not satisfy behavior DONE by themselves.

## 6. Stubs never count as capability

`pass`, `NotImplementedError`, empty critical handlers, fake adapters, hardcoded success paths, mock-only responses and TODO implementations are incomplete.

The CI gate automatically rejects obvious Python stubs inside implementation files registered for `IMPLEMENTED` or higher. Semantic fake-success patterns that cannot be detected mechanically remain a review obligation.

## 7. Failure paths before demo confidence

Before promotion to `TESTED`, at least one executable failure-path proof is required in addition to the happy behavior proof.

Prefer tests that break assumptions deliberately: invalid input, missing dependency, missing file, duplicate execution, dependency failure, interrupted state or other domain-appropriate faults.

## 8. CI blocks unsupported promotion

The minimum central gate is:

- registered implementation exists for `IMPLEMENTED+`;
- executable proof exists for `TESTED+`;
- failure-path evidence exists for `TESTED+`;
- declared test commands are actually present in GitHub Actions;
- integration proof exists for `INTEGRATION_TESTED+`;
- real-work evidence exists for `OBSERVED_IN_REAL_WORK+`;
- repeated independent real-work evidence plus reliability evidence exists for `RELIABLE`;
- formal Markdown capability claims reference a registered capability ID;
- obvious stubs in registered Python implementation paths fail validation.

## 9. ADRs must close the loop

Any architecture decision that creates or materially changes a mechanism must include:

```text
OBSERVED PROBLEM
EVIDENCE
MINIMAL SOLUTION
ALTERNATIVES REJECTED
EXECUTABLE TEST PROVING THE SOLUTION
```

An ADR that only says what will be built is a proposal, not evidence of progress.

## 10. README is not capability truth

The canonical machine-readable capability status source is:

`governance/CAPABILITY_REGISTRY.json`

README files may explain results and usage. They cannot originate or promote a capability status.

A formal documentation claim uses:

```text
CAPABILITY CLAIM: CAP-...
```

The CI gate rejects a formal claim whose ID is absent from the registry.

Free prose that sounds like a capability but is not linked to a registry ID has no authoritative capability status and must be treated as a hypothesis.

## 11. New abstraction requires two real uses

Do not extract a new reusable abstraction from one case unless a safety/integrity boundary requires it.

Default sequence:

```text
first real use -> simple local solution
second independent real use -> identify what is actually common
then consider abstraction
```

One use can justify working code. It does not normally justify a reusable architecture.

## 12. Demolition review

At each material architecture checkpoint, and before promoting an abstraction as necessary, ask:

```text
If this component were removed today, which executable test or observed real-work behavior would stop passing?
```

If the answer is `none`, the component is presumptively decorative and should be removed, collapsed or returned to `PROPOSED` status.

## Capability Registry status ladder

Only these statuses are allowed, in this order:

```text
PROPOSED
IMPLEMENTED
TESTED
INTEGRATION_TESTED
OBSERVED_IN_REAL_WORK
RELIABLE
```

Promotion prerequisites are mechanical:

### PROPOSED
A defined behavioral claim may exist. No implementation claim is made.

### IMPLEMENTED
Implementation path(s) must exist and registered critical implementation paths may not contain obvious stubs.

### TESTED
All `IMPLEMENTED` requirements plus:
- executable proof path(s);
- executable failure-path proof path(s);
- CI command(s) that run those proofs.

### INTEGRATION_TESTED
All `TESTED` requirements plus integration proof path(s) and CI command(s) that execute them.

### OBSERVED_IN_REAL_WORK
All `INTEGRATION_TESTED` requirements plus at least one preserved real-work evidence record for the claimed behavior.

### RELIABLE
All previous requirements plus:
- at least two independent real-work evidence records;
- preserved reliability/regression evidence;
- no evidence omission may be replaced by a prose assertion.

Writing `RELIABLE` manually without these prerequisites causes CI failure.

## Progress sequence

Preferred development order:

```text
real task
-> failure / friction
-> smallest working solution
-> tests
-> repeated use
-> measured problems
-> refactor
-> architecture emerges
```

Forbidden proxy-progress order:

```text
vision
-> architecture
-> interfaces
-> schemas
-> folders
-> README
-> someday functions
```

## Epistemic boundary

The automated gate can verify registered paths, status prerequisites, formal claim linkage, CI command presence and a bounded class of obvious stubs. It cannot understand every natural-language capability claim or prove that a test is semantically sufficient.

Therefore:

```text
CI PASS != RELIABLE CAPABILITY
```

CI prevents specific unsupported promotions; real-work evidence and Human review remain necessary for higher claims.
