from __future__ import annotations

import csv
from collections import Counter

from src.workflow.common import Timer, append_log, project_path, resolve_existing


def run(config: dict, limit: int | None = None) -> int:
    with Timer() as timer:
        rows = list(csv.DictReader(resolve_existing(config["paths"]["validated_results"]).open("r", encoding="utf-8-sig", newline="")))
        if limit:
            rows = rows[:limit]
        quantitative_path = resolve_existing(config.get("paths", {}).get("quantitative_scored_records", "outputs/results/quantitative_scored_records.csv"))
        event_path = resolve_existing(config.get("paths", {}).get("cross_year_events", "outputs/analysis/cross_year_matching_events.csv"))
        quantitative_rows = []
        event_rows = []
        if quantitative_path.exists():
            quantitative_rows = list(csv.DictReader(quantitative_path.open("r", encoding="utf-8-sig", newline="")))
        if event_path.exists():
            event_rows = list(csv.DictReader(event_path.open("r", encoding="utf-8-sig", newline="")))
        risk_counts = Counter(row["liquidity_risk_label"] or "missing" for row in rows)
        score_counts = Counter(row["consistency_score"] or "missing" for row in rows)
        quantitative_risk_counts = Counter(row.get("liquidity_risk_quantile") or "missing" for row in quantitative_rows)
        attention_counts = Counter(row.get("attention_level") or "missing" for row in quantitative_rows)
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
        if quantitative_rows:
            lines += [
                "",
                "## Quantitative Liquidity Risk",
                "- The old `liquidity_risk_label` is retained as a legacy screening field.",
                "- Comparable analysis uses `liquidity_risk_score` and `liquidity_risk_quantile` from weighted risk-term frequency.",
            ]
            for key in ["high", "medium", "low", "none", "missing"]:
                if quantitative_risk_counts.get(key, 0):
                    lines.append(f"- {key}: {quantitative_risk_counts[key]}")
            lines += [
                "",
                "## Attention Scores",
                "- `base_attention_score` is weighted from dividend pressure, cash-flow pressure, profit pressure, and liquidity-risk score.",
                "- Final `attention_score` adds cross-year pressure from same-company matching events, so the review list is connected to cross-year deterioration signals.",
            ]
            for key in ["priority", "watch", "monitor", "routine", "missing"]:
                if attention_counts.get(key, 0):
                    lines.append(f"- {key}: {attention_counts[key]}")
        if event_rows:
            consecutive_count = sum(1 for row in event_rows if str(row.get("is_consecutive_pair")).lower() == "true")
            lines += [
                "",
                "## Cross-Year Matching",
                f"- Same-company year-pair events: {len(event_rows)}",
                f"- Consecutive-year events: {consecutive_count}",
            ]
        lines += [
            "",
            "## Quality Notes",
            "- Rule baseline is intentionally simple and should be reviewed manually.",
            "- Unit-normalized financial fields are available in `records_validated_unit_normalized.csv`.",
            "- High-attention records should be manually verified against evidence before being used as financial conclusions.",
            "- Evidence page numbers are approximate because parsed text may not preserve stable original PDF page markers.",
        ]
        report_path.write_text("\n".join(lines), encoding="utf-8")
    append_log(config, "report", "success", count=len(rows), elapsed=timer.elapsed)
    print(f"[report] summary report={config['paths']['summary_report']}")
    return len(rows)


if __name__ == "__main__":
    from src.workflow.common import load_workflow_config

    run(load_workflow_config("configs/workflow.yaml"))
