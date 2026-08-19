---
document: GINSENG_G01_OWNERSHIP_RECONCILIATION
version: 1
status: HUMAN_ACCEPTED_RECONCILIATION / MERGE_PENDING
owner: USER
accepted_at: 2026-08-19
source_baseline: 1359988df2c78644f9d906518d7e6229c7c60f57
semantic_gap: GINSENG-G01
semantic_decision: ESTABLISHED
repository_integration: PENDING
merge_authorized: false
runtime_authorized: false
release_authorized: false
deploy_authorized: false
new_capability_authorized: false
---

# Ginseng G01 — Problem / Framing Ownership Reconciliation

## 1. Purpose

Close the narrow ownership ambiguity between **Human-owned normative problem/goal**, **Ginseng decision-space analysis**, and **External/Base Intelligence operational interpretation/framing proposal** without changing runtime, capability, product scope or the established ownership of operational HOW.

This is a governance-only reconciliation record. It materializes an explicit Human semantic decision against the accepted COS baseline and does not itself authorize repository integration.

## 2. Human decision

The Human explicitly stated:

`AKCEPTUJĘ GINSENG-G01 RECONCILIATION: HUMAN POSIADA NORMATYWNY PROBLEM/CEL; GINSENG ANALIZUJE SOURCE-BOUND DECISION SPACE, PREMISES, ALTERNATYWY, KONSEKWENCJE I NIEPEWNOŚĆ ORAZ MOŻE UJAWNIAĆ AMBIGUITY/CONSTRAINTS, ALE NIE WYBIERA HOW ANI NIE TWORZY NORMATYWNEGO FRAMINGU; EXTERNAL/BASE INTELLIGENCE POSIADA OPERACYJNĄ INTERPRETACJĘ/FRAMING PROPOSAL ORAZ WYBÓR HOW. AUTORYZUJĘ WYŁĄCZNIE GOVERNANCE-ONLY RECONCILIATION RECORD/PR; BEZ MERGE, RUNTIME, RELEASE, DEPLOY ANI NOWEJ CAPABILITY.`

The semantic decision is therefore Human-established now. Merge and accepted-repository integration remain separate authorities and are not granted here.

## 3. Source baseline and authority

Repository:

`JTJ07/COS`

Exact accepted main observed immediately before this reconciliation branch was created:

`1359988df2c78644f9d906518d7e6229c7c60f57`

Relevant accepted sources on that baseline:

- `governance/GINSENG_CANDIDATE_R0_FREEZE_2026-08-18.md` — Human-frozen R0 ownership boundary: Ginseng owns decision-space analysis / lineage / dependencies / consequences / uncertainty / Human-decision needs; External/Base Intelligence proposes or selects HOW.
- `governance/GINSENG_D0_INTEGRATION_RECORD_2026-08-19.md` — D0 is Human-accepted and integrated without semantic ownership transfer.
- `governance/M05_R1_H1_H2_REQUEST65_2026-08-19.md` — same-identity evidence that Ginseng can analyze a bounded problem/constraint surface and hand it to External Intelligence without selecting HOW.

Historical COS PR #18 remains a superseded/unmerged source for reusable Ginseng semantics only; this reconciliation does not revive its stale global placement or `Creative OS owns canon` language.

## 4. Reconciled semantic ownership

### Human

Owns the **normative problem and goal**: what is wanted, why it matters, the authoritative intent, goal/DONE and any normative change to that meaning.

No downstream layer may manufacture, silently replace or expand this normative framing.

### Ginseng

Owns **source-bound decision-space analysis** around the Human-owned problem/goal, including:

- premises and source-bound facts relevant to the decision space;
- alternatives that exist in the decision space;
- constraints and dependencies;
- consequences and impact paths;
- uncertainty and unresolved assumptions;
- ambiguity that may require clarification or a Human decision.

Ginseng may expose that the supplied problem is ambiguous, constrained, underspecified or decision-blocked. It may represent the Human-owned problem as an observed/source-bound input for analysis.

Ginseng **must not**:

- create or replace normative problem framing;
- redefine Human goal or DONE;
- originate, rank, select, route or optimize operational HOW;
- convert analysis of alternatives into ownership of the solution decision.

### External / Base Intelligence

Owns the **operational interpretation / framing proposal** needed to solve the Human-owned problem and owns proposal/selection of operational HOW.

That operational framing is a non-normative proposal bounded by Human intent. Intelligence may translate the Human-owned problem into a workable operational representation, but it does not acquire authority to change the normative problem, goal or DONE.

### Saddle boundary remains unchanged

Saddle validates the Intelligence-generated direction against Human intent / boundaries / invariants. It does not originate, rank, select or route the direction.

## 5. Interpretation of existing M-05 H1 wording

`governance/M05_R1_H1_H2_REQUEST65_2026-08-19.md` states that the problem, constraints and acceptance surface were sufficiently explicit for Intelligence to propose HOW.

Under this reconciliation, that statement means:

- the **normative problem** remained Human-owned;
- Ginseng performed source-bound analysis of the supplied problem/constraints/acceptance surface;
- `DECISION_SPACE_READY_FOR_INTELLIGENCE` did not constitute normative reframing or solution selection;
- External Intelligence retained ownership of operational framing proposal and HOW.

No M-05 evidence needs to be reinterpreted as Ginseng owning the problem definition.

## 6. Reconstruction classification

Before the Human decision:

```text
GINSENG-G01
SEMANTIC STATUS: GAP
QUESTION: boundary between problem interpretation/framing and decision-space understanding was not explicit enough
```

After this Human decision:

```text
GINSENG-G01 SEMANTIC DECISION: HUMAN RESOLVED
TARGET SEMANTIC STATUS: ALIGNED
REPOSITORY INTEGRATION: PENDING
```

Until this exact governance-only candidate enters accepted repository history through a separately authorized merge, current `main` remains unchanged. This record does not pretend that an unmerged branch is already canonical repository state.

## 7. What remains true if components are replaced

```text
HUMAN normative problem/goal ownership remains Human-owned.
GINSENG decision-space competence does not become normative framing or HOW ownership.
EXTERNAL/BASE INTELLIGENCE operational framing/HOW ownership does not become Human normative authority.
SADDLE validates direction and does not choose it.
COS storage/location does not transfer semantic ownership.
```

Ownership does not derive from competence or repository placement.

## 8. Explicit non-goals / authority boundary

This Human decision authorizes only:

- this governance-only reconciliation record;
- a pull request containing this bounded governance reconciliation.

It does **not** authorize:

- merge of that pull request;
- runtime changes or activation;
- release, deploy or tag;
- secrets, credentials or spending;
- new Ginseng capability;
- new tests or functional gates;
- product activation or completion claims;
- changes to Executor, Saddle or local-project runtime behavior;
- transfer of semantic ownership beyond the exact reconciliation above.

Any merge remains a separate Human-owned consequential decision.
