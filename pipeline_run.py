from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import audit_dataset, extract_fields, parse_check, parse_docs, report_results, route_sections, validate_results
from src.workflow.common import append_log, load_workflow_config


STEPS = ["audit", "parse", "parse_check", "route", "extract", "validate", "report"]


def run_step(step: str, config: dict, limit: int | None) -> int:
    if step == "audit":
        return audit_dataset.run(config, limit=limit)
    if step == "parse":
        return parse_docs.run(config, limit=limit)
    if step == "parse_check":
        return parse_check.run(config, limit=limit)
    if step == "route":
        return route_sections.run(config, limit=limit)
    if step == "extract":
        method = config.get("steps", {}).get("extract", {}).get("method", "rule")
        return extract_fields.run(config, limit=limit, method=method)
    if step == "validate":
        return validate_results.run(config, limit=limit)
    if step == "report":
        return report_results.run(config, limit=limit)
    raise ValueError(f"unknown step: {step}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the real estate annual report workflow.")
    parser.add_argument("--config", default="configs/workflow.yaml")
    parser.add_argument("--step", choices=STEPS + ["all"], default="all")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    config = load_workflow_config(args.config)
    steps = STEPS if args.step == "all" else [args.step]
    for step in steps:
        try:
            run_step(step, config, args.limit)
        except Exception as exc:
            append_log(config, step, "failed", error=str(exc))
            print(f"[{step}] failed: {exc}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
