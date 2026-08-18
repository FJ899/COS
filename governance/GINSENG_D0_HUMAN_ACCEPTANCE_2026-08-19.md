---
document: GINSENG_D0_HUMAN_ACCEPTANCE
version: 1
status: HUMAN_ACCEPTED_TECHNICAL_CLOSURE / MERGE_PENDING
owner: USER
accepted_at: 2026-08-19
candidate: GINSENG_CANDIDATE_R0
done_scope: GINSENG_DONE_D0
accepted_technical_head: ed4c7031a03c27ff5b8d68aba3fb9d6340a55469
accepted_technical_ci_run: 61
merge_authorized: false
runtime_authorized: false
formal_project_activation: false
project_completion_claim: NONE
---

# Ginseng D0 — Human Acceptance Record

## 1. Human decision

The Human explicitly stated:

`AKCEPTUJĘ GINSENG D0 TECHNICAL CLOSURE`

This accepts the independently verified Ginseng D0 technical closure candidate for the Human-frozen `GINSENG_DONE_D0` scope.

The accepted technical candidate was:

```text
PR: JTJ07/COS #29
head: ed4c7031a03c27ff5b8d68aba3fb9d6340a55469
Verify Creative OS run: #61 / SUCCESS
GINSENG_D05_DECISION_LINEAGE: PASS
GINSENG_D09_FINAL_RECHECK: PASS
GINSENG_D0_TECHNICAL_CLOSURE: PASS_IF_MERGED
```

## 2. Meaning of this acceptance

This Human decision means:

```text
GINSENG D0 TECHNICAL CLOSURE: HUMAN ACCEPTED
GINSENG_DONE_D0: ACCEPTED AS SATISFIED IF THE VERIFIED CLOSURE ENTERS ACCEPTED COS HISTORY
MERGE PR #29: NOT YET AUTHORIZED BY THIS DECISION
```

The technical closure record remains a pre-acceptance proof artifact. This separate Human record supplies the Human-owned acceptance rather than rewriting the verifier output after the fact.

## 3. Boundaries

This decision does not authorize or claim:

- merge of PR #29;
- Ginseng runtime;
- formal Ginseng project activation;
- whole-project completion beyond the frozen D0 scope;
- release, deploy or tag;
- secrets, credentials or spending;
- a new capability, Test-004 or broader product scope;
- transfer of semantic ownership between Human, Ginseng, Intelligence, Saddle, COS, Executor or Verifier.

Human acceptance of D0 technical closure is therefore distinct from repository integration and from any later product/runtime decision.

## 4. Next authority boundary

The next consequential action is merge of PR #29.

That merge remains separately Human-owned and requires explicit merge authorization.
