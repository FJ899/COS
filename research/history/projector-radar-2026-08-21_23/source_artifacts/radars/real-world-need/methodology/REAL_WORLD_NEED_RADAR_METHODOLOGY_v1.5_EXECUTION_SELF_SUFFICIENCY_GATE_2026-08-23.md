# REAL-WORLD NEED RADAR — METHODOLOGY v1.5
## Execution-Self-Sufficiency Gate for Projector Test Selection
Date: 2026-08-23

## Trigger

After BIR-01 failed the effect-time solution-state preflight, fallback candidates from the five independent Blocked Intent runs were requalified against a stricter question:

`Can Projector itself execute a meaningful closed loop on this case now, using accessible artifacts and without depending on the original Human for every critical experiment?`

This exposed a gap in the earlier `ACTIONABILITY` field.

## Key distinction

```text
ACTIONABLE IN PRINCIPLE
!=
EXECUTABLE BY THIS TEST ENVIRONMENT
```

A case can be a real, excellent Blocked Intent project and still be unusable as a Projector test because it requires:
- the original Human's private files;
- proprietary or unpublished experiment code;
- rare GPU / Apple Silicon / specific phone or embedded hardware;
- private business history;
- physical access to the owner's device;
- incumbent/platform-owner action.

Therefore add:

`EXECUTION_SELF_SUFFICIENCY`

## Execution-self-sufficiency definition

HIGH:
- all critical artifacts are public or reproducible;
- first experiments can be run without the original Human;
- required compute/hardware is reasonably available;
- objective feedback can be produced locally or through public CI;
- no incumbent-only action is on the critical path.

MEDIUM:
- most work can proceed independently, but final verification requires the owner/device/credentials.

LOW:
- the real experiment cannot be run without private artifacts, rare hardware, or repeated Human execution.

## Requalification observations

### BIR-01 — FreeCAD Slider collapse
Rejected by solution-state gate:
root cause and local fix already published.

### BIR-02 — FreeCAD CAM
Rejected as primary unknown-HOW case:
real trigger identified, workaround documented, public PR #31863 already addresses main bug.

### BI-01 — GS-DIFF / PGSR reproduction
Live unknown-HOW remains, but the public repository currently exposes only README + LICENSE.
The code/scenes/experiment state needed for reproduction are not publicly available.

Execution self-sufficiency: LOW.

### Test 2 B — single-H100 training efficiency
The feedback loop is excellent, but the actual experiment depends on H100-class compute and the original training workload/configuration.

Execution self-sufficiency: LOW/MEDIUM.

### Test 2 B — courier profitability
The project is real-world and operational, but objective validation depends on the company's historical jobs, realized costs, traffic/parking exceptions and operator ground truth.

Execution self-sufficiency: LOW without the original business dataset.

### Gemini — watermark-resistant PDF OCR
Potentially executable as a generic technical project, but the discovered primary case is older than the preferred horizon and the exact original document corpus is not clearly frozen as a current external benchmark.

Execution self-sufficiency: MEDIUM for a synthetic/generalized problem, lower for the exact Human case.

### Genspark — paper reproduction 73% vs 77%
Strong scientific structure, but the report itself says there is no public repo from the paper authors and the original Human owns the working reimplementation/data/compute.

Execution self-sufficiency: LOW.

### Genspark — mlx-lm / MTPLX
Public code exists, but meaningful verification is tied to Apple Silicon / specialized inference environment and the project is already actively being developed by the original contributors.

Execution self-sufficiency: MEDIUM at best.

### Grok — custom microWakeWord
Excellent physical feedback, but flashing and final verification require the owner's Voice PE hardware.

Execution self-sufficiency: MEDIUM/LOW.

### Grok — PinePhone FDE
Requires the owner's specific phone and carries brick risk.

Execution self-sufficiency: LOW.

### Grok — llama.cpp gfx1151 HIP
Requires specific Strix Halo / gfx1151 hardware to reproduce the numerical backend failure.

Execution self-sufficiency: LOW.

## Current pool verdict

```text
FIVE-RUN BLOCKED INTENT DISCOVERY
= SUCCESS

CLEAN PROJECTOR EXECUTION CANDIDATE
= NOT YET ESTABLISHED
```

This does NOT invalidate the Radar.

It shows that the Radar was optimized for:

`REAL BLOCKED HUMAN PROJECT`

but the immediate Projector test additionally requires:

`REAL BLOCKED HUMAN PROJECT + EXECUTION SELF-SUFFICIENCY`.

## New mandatory Projector-test gate

Before selection, require:

```text
E1 CURRENT BLOCKER STILL ACTIVE
E2 UNKNOWN HOW STILL UNKNOWN
E3 PUBLIC / RETRIEVABLE INPUT ARTIFACTS
E4 REPRODUCIBLE BASELINE
E5 NO RARE HARDWARE ON CRITICAL PATH
E6 NO PRIVATE DATA ON CRITICAL PATH
E7 NO ORIGINAL-HUMAN ACTION REQUIRED FOR EACH ITERATION
E8 OBJECTIVE FEEDBACK PRODUCIBLE BY US
E9 SAFE / REVERSIBLE FIRST EXPERIMENT
E10 MULTI-STEP DEPTH
```

Suggested selection rule:

`E1–E9 must PASS; E10 should PASS.`

If any of E1–E9 fails, the candidate is not the primary Projector live test.

## Revised scan target

For future Projector-test discovery, add this explicit requirement:

```text
PREFER CASES WHERE:
the source repository contains enough code/data/reproducer/tests
for an independent third party to start the first experiment
without asking the original author for missing inputs.
```

This will reduce false positives caused by:
- beautifully documented but already solved issues;
- private-data research;
- hardware-dependent cases;
- owner-dependent physical systems.

## Updated sequence

```text
BLOCKED INTENT DISCOVERY
→ STRUCTURED-EVIDENCE CHECK
→ PROJECTOR TEST SUITABILITY
→ EXECUTION SELF-SUFFICIENCY
→ EFFECT-TIME SOLUTION-STATE CHECK
→ FREEZE BASELINE
→ START REAL WORK
```

## Operational consequence

Do not activate a candidate merely because it has a high Blocked Intent score.

The current five-run candidate pool should be treated as:

`DISCOVERY EVIDENCE`

not yet:

`AUTHORIZED LIVE PROJECT`.

A new selection pass should search specifically for a case with public executable artifacts and independent verification capability.
