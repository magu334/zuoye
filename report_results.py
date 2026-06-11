from __future__ import annotations

import csv
from collections import Counter

from src.workflow.common import Timer, append_log, project_path


def run(config: dict, limit: int | None = None) -> int:
    with Timer() as timer:
        rows = list(csv.DictReader(project_path(config["paths"]["validated_results"]).open("r", encoding="utf-8-sig", newline="")))
        if limit:
            rows = rows[:limit]
        risk_counts = Counter(row["liquidity_risk_label"] or "missing" for row in rows)
        score_counts = Counter(row["consistency_score"] or "missing" for row in rows)
        dividend_count = sum(1 for row in rows if str(row["has_cash_dividend"]).lower() == "true")
        no_dividend_count = sum(1 for row in rows if str(row["has_cash_dividend"]).lower() == "false")
        companies = {row["stock_code"] for row in rows}
        years = sorted({row["report_year"] for row in rows if row.get("report_year")})
        if len(years) == 1:
            sample_desc = f"{years[0]} annual reports of {len(companies)} A-share real estate companies"
        else:
            sample_desc = f"{years[0]}-{years[-1]} annual reports covering {len(companies)} A-share real estate companies"
        report_path = project_path(config["paths"]["summary_report"])
        report_path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# Summary Report",
            "",
            "## Scope",
            f"- Validated records: {len(rows)}",
            f"- Current sample: {sample_desc}.",
            "- Note: this is a rule-baseline workflow result and still requires human evaluation.",
            "",
            "## Dividend",
            f"- Cash dividend records: {dividend_count}",
            f"- No cash dividend records: {no_dividend_count}",
            "",
            "## Liquidity Risk Labels",
        ]
        for key, value in sorted(risk_counts.items()):
            lines.append(f"- {key}: {value}")
        lines += ["", "## Consistency Scores"]
        for key, value in sorted(score_counts.items()):
            lines.append(f"- {key}: {value}")
        lines += [
            "",
            "## Quality Notes",
            "- Rule baseline is intentionally simple and should be reviewed manually.",
            "- Financial amount units are not fully normalized yet.",
            "- Evidence page numbers are approximate because the current MinerU markdown keeps text but not stable original PDF page markers.",
        ]
        report_path.write_text("\n".join(lines), encoding="utf-8")
    append_log(config, "report", "success", count=len(rows), elapsed=timer.elapsed)
    print(f"[report] summary report={config['paths']['summary_report']}")
    return len(rows)


if __name__ == "__main__":
    from src.workflow.common import load_workflow_config

    run(load_workflow_config("configs/workflow.yaml"))
