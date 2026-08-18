---
document: GINSENG_D0_INTEGRATION_RECORD
version: 1
status: INTEGRATED / HUMAN_ACCEPTED_D0_CLOSED
owner: USER_FOR_ACCEPTANCE_AND_MERGE_AUTHORITY
recorded_at: 2026-08-19
accepted_technical_head: 05d6f48730b80052bdeab55b52f4a67de5828130
merge_commit: a43a94c246112b72a54e952b52af1eacedaaeb3b
merge_tree: ce7c542095ae243ce07be1e2ee9642cb8c7ea69e
runtime_authorized: false
formal_project_activation: false
whole_project_completion_claim: false
---

# Ginseng D0 — Accepted Integration Record

## 1. Separate Human authorities

The Human first accepted the verified technical closure with:

`AKCEPTUJĘ GINSENG D0 TECHNICAL CLOSURE`

That decision is preserved unchanged in:

`governance/GINSENG_D0_HUMAN_ACCEPTANCE_2026-08-19.md`

At that point merge correctly remained pending.

The Human later gave a separate merge authority with:

`AKCEPTUJĘ MERGE PR #29`

The merge was then executed with the exact accepted PR head:

```text
PR: #29
accepted head: 05d6f48730b80052bdeab55b52f4a67de5828130
merge SHA: a43a94c246112b72a54e952b52af1eacedaaeb3b
merge tree: ce7c542095ae243ce07be1e2ee9642cb8c7ea69e
result: MERGED
```

## 2. Current accepted state

```text
GINSENG_DONE_D0: HUMAN ACCEPTED / CLOSED
D-01: SATISFIED
D-02: SATISFIED
D-03: SATISFIED
D-04: SATISFIED
D-05: SATISFIED
D-06: SATISFIED
D-07: SATISFIED
D-08: SATISFIED
D-09: PASS
PR #29: MERGED
```

## 3. Boundaries

This accepted integration does not authorize or imply:

- Ginseng runtime;
- formal Ginseng project activation;
- whole-project completion beyond the frozen `GINSENG_DONE_D0` scope;
- release, deploy or tag;
- secrets, credentials or spending;
- new Ginseng capability or a new test;
- transfer of semantic ownership between Human, Ginseng, Intelligence, Saddle, COS, Executor or Verifier.

The earlier Human acceptance record remains historically correct in saying that **that earlier acceptance decision by itself** did not authorize merge. This integration record captures the later, separate Human merge decision and resulting accepted repository state instead of rewriting history.
