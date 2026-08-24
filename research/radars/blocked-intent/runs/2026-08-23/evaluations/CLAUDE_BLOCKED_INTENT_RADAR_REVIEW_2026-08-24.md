# Claude Blocked Intent Radar — Archive Review

Date archived: 2026-08-24
Source run date: 2026-08-23
Source artifact: `CLAUDE_BLOCKED_INTENT_RADAR_RAW.docx`
Source title: `BLOCKED INTENT RADAR — RUN 2026-08-23`

## Source-run facts

- Mode: `BLIND / INDEPENDENT DISCOVERY`.
- Planned primary sources: Reddit + GitHub.
- Actual availability: GitHub available; Reddit unavailable after repeated attempts.
- Claude reported 42 search/fetch calls.
- Four fully qualifying cases retained; the list was not padded to the requested count.
- Search bias: stale/highly-linked GitHub results and technical domains were overrepresented.

## Archived disposition

### KEEP

1. **BIR-02 — Open WebUI accessibility**
   - Strongest human-need signal in the set.
   - Real professional users: blind / visually impaired colleagues unable to use the product independently.
   - Concrete barriers: missing ARIA labels, hover-only controls, focus-order problems, missing live announcements for streamed responses.
   - Small, independently testable first experiment exists: fix one component and verify with NVDA/JAWS.
   - Maintainer welcomes small scoped accessibility PRs.

2. **BIR-01 — OOMWOO open-source robot vacuum**
   - Strong real-project candidate with rich current state, explicit open modules, simulation, hardware placeholder, BOM and active community.
   - Best interpreted as a real execution / contribution case rather than as a new market opportunity.
   - Fast feedback loop exists through Gazebo simulation; slower physical validation can follow.

### WATCH / RABBIT HOLE

3. **BIR-03 — Hubspace / Home Assistant BLE fallback**
   - Technically interesting local-control / cloud-dependency problem.
   - Keep only as WATCH because the key BLE claim was not re-confirmed on the current live repository page.
   - Physical device access may be required for meaningful progress.

### DROP

4. **BIR-04 — utahexpungements.org parser**
   - Issue dates to 2020.
   - No confirmed 2026 project activity.
   - Too stale for the intended freshness bar despite real-world legal stakes.

## Review verdict

```text
FILTERING QUALITY = HIGH
METHODOLOGICAL HONESTY = HIGH
FRESHNESS = MEDIUM / LOW
SOURCE DIVERSITY = LOW
USEFUL DISCOVERIES = 2 STRONG + 1 WATCH + 1 DROP
VALUE / TIME = NOT STRONG ENOUGH FOR VERY LONG SEARCH AS DEFAULT
```

## Valuable observation

**Longer search did not produce proportionally more value.**

The run reported 42 search/fetch calls and retained only four qualified cases, of which only two are strong enough to keep. This supports testing a future Radar rule based on a `QUALITY STOP CONDITION` rather than `continue until N results exist`.

Candidate rule:

```text
QUALITY STOP CONDITION

Stop discovery when:
- additional queries mostly return stale, duplicate, solved, or weak-signal cases;
- source coverage has become structurally biased by tool limitations;
- marginal probability of finding a materially better case is low;
- enough high-confidence cases exist to justify deeper validation.

DO NOT pad output to a target count.
```

## Governance

```text
RAW SOURCE = ARCHIVED
KEEP = BIR-02, BIR-01
WATCH = BIR-03
DROP = BIR-04
NEW DEVELOPMENT TASK = NO
NEW PRODUCT DECISION = NO
FINDING != TASK
```
