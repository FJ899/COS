#!/usr/bin/env python3
"""Compare supplied idea evidence without inventing scores or changing priorities."""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


class ComparisonError(ValueError):
    """Invalid comparison input."""


def _object(value: object, name: str) -> dict:
    if not isinstance(value, dict):
        raise ComparisonError(f"{name} must be an object")
    return value


def _text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ComparisonError(f"{name} must be non-empty text")
    return value


def compare(payload: object) -> dict:
    data = _object(payload, "input")
    goal = _text(data.get("goal"), "goal")
    criteria = _object(data.get("criteria"), "criteria")
    if not criteria:
        raise ComparisonError("criteria must not be empty")
    for key, direction in criteria.items():
        _text(key, "criterion name")
        if direction not in ("maximize", "minimize"):
            raise ComparisonError(f"{key}: direction must be maximize or minimize")
    ideas = data.get("ideas")
    if not isinstance(ideas, list) or len(ideas) < 2:
        raise ComparisonError("ideas must contain at least two alternatives")
    seen: set[str] = set()
    eligible: dict[str, dict[str, float]] = {}
    results: list[dict] = []
    for raw in ideas:
        idea = _object(raw, "idea")
        identity = _text(idea.get("id"), "idea.id")
        if identity in seen:
            raise ComparisonError(f"duplicate idea id: {identity}")
        seen.add(identity)
        feasible = idea.get("feasible")
        if feasible is not None and type(feasible) is not bool:
            raise ComparisonError(f"{identity}: feasible must be true, false or null")
        metrics = _object(idea.get("metrics"), f"{identity}.metrics")
        if set(metrics) - set(criteria):
            raise ComparisonError(f"{identity}: unknown criteria: {sorted(set(metrics) - set(criteria))}")
        missing = []
        values: dict[str, float] = {}
        for key in criteria:
            metric = metrics.get(key)
            if metric is None:
                missing.append(key)
                continue
            metric = _object(metric, f"{identity}.{key}")
            value = metric.get("value")
            if type(value) not in (int, float) or (type(value) is float and not math.isfinite(value)):
                raise ComparisonError(f"{identity}.{key}: value must be a finite number")
            evidence = metric.get("evidence")
            if not isinstance(evidence, str) or not evidence.strip():
                missing.append(key)
                continue
            values[key] = value
        feasibility_evidence = idea.get("feasibility_evidence")
        has_feasibility_evidence = isinstance(feasibility_evidence, str) and bool(feasibility_evidence.strip())
        if feasible is False and has_feasibility_evidence:
            status = "INFEASIBLE"
        elif feasible is not True or not has_feasibility_evidence or missing:
            status = "NEEDS_EVIDENCE"
        else:
            status = "COMPARABLE"
            eligible[identity] = values
        results.append({"id": identity, "status": status, "missing_metrics": missing,
                        "feasibility_verified": feasible is not None and has_feasibility_evidence,
                        "dominated_by": []})

    def dominates(left: dict, right: dict) -> bool:
        no_worse = all(left[key] >= right[key] if direction == "maximize" else left[key] <= right[key]
                       for key, direction in criteria.items())
        return no_worse and any(left[key] != right[key] for key in criteria)

    for result in results:
        if result["id"] in eligible:
            result["dominated_by"] = sorted(identity for identity, values in eligible.items()
                                            if dominates(values, eligible[result["id"]]))
    frontier = sorted(result["id"] for result in results
                      if result["status"] == "COMPARABLE" and not result["dominated_by"])
    return {"goal": goal, "results": results, "frontier_among_evidenced": frontier,
            "unresolved": sorted(result["id"] for result in results if result["status"] == "NEEDS_EVIDENCE"),
            "decision": "HUMAN_REVIEW_REQUIRED",
            "limits": "Uses supplied comparable measurements and evidence references only; does not verify their truth, rank unknown ideas, or change portfolio priority."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON comparison input")
    args = parser.parse_args()
    try:
        result = compare(json.loads(args.input.read_text(encoding="utf-8")))
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
