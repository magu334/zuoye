from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


RISK_TERMS: dict[str, dict[str, object]] = {
    "liquidity": {"weight": 4.0, "terms": ["流动性", "资金压力", "资金安全", "资金链"]},
    "financing": {"weight": 2.0, "terms": ["融资", "借款", "贷款", "授信", "债券", "有息负债"]},
    "debt": {"weight": 2.5, "terms": ["债务", "偿债", "负债", "资产负债率", "短期借款"]},
    "cashflow": {"weight": 2.0, "terms": ["现金流", "经营活动现金流", "回款"]},
    "market": {"weight": 1.5, "terms": ["销售回款", "去化", "市场下行", "行业下行", "需求下行", "调控"]},
}


ANALYSIS_FIELDS = [
    "doc_id",
    "stock_code",
    "stock_name",
    "report_year",
    "has_cash_dividend",
    "cash_dividend_per_10_shares",
    "parent_net_profit_cny",
    "operating_cash_flow_cny",
    "ocf_to_profit_ratio",
    "dividend_pressure_score",
    "profit_pressure_score",
    "cashflow_pressure_score",
    "liquidity_term_hits",
    "liquidity_weighted_hits",
    "liquidity_risk_score",
    "liquidity_risk_quantile",
    "legacy_liquidity_risk_label",
    "base_attention_score",
    "cross_year_pressure_score",
    "cross_year_pressure_level",
    "cross_year_reason",
    "attention_score",
    "attention_level",
    "review_reason",
]


EVENT_FIELDS = [
    "event_id",
    "stock_code",
    "stock_name",
    "from_year",
    "to_year",
    "year_gap",
    "is_consecutive_pair",
    "from_doc_id",
    "to_doc_id",
    "dividend_delta",
    "ocf_delta_cny",
    "profit_delta_cny",
    "risk_score_delta",
    "base_attention_score_delta",
    "final_attention_score_delta",
    "cross_year_pressure_score",
    "event_type",
    "review_reason",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl(path: Path, rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def resolve_existing(root: Path, path_text: str) -> Path:
    path = Path(path_text)
    direct = path if path.is_absolute() else root / path
    if direct.exists():
        return direct
    flat = root / path.name
    if flat.exists():
        return flat
    return direct


def to_float(value: object) -> float | None:
    if value is None:
        return None
    text = str(value).strip().replace(",", "")
    if not text:
        return None
    try:
        value_float = float(text)
    except ValueError:
        return None
    if math.isnan(value_float):
        return None
    return value_float


def to_bool(value: object) -> bool | None:
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y"}:
        return True
    if text in {"false", "0", "no", "n"}:
        return False
    return None


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def load_extract_context(path: Path) -> dict[str, dict[str, object]]:
    context: dict[str, dict[str, object]] = {}
    if not path.exists():
        return context
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)
            risk = item.get("liquidity_risk") or {}
            evidence = risk.get("evidence") or {}
            context[item["doc_id"]] = {
                "legacy_liquidity_risk_label": risk.get("label") or "unknown",
                "risk_keywords": risk.get("keywords") or [],
                "risk_evidence_text": evidence.get("text") or "",
            }
    return context


def count_risk_terms(text: str, keywords: list[str]) -> tuple[int, float]:
    compact = re.sub(r"\s+", "", text or "")
    raw_hits = 0
    weighted_hits = 0.0
    for spec in RISK_TERMS.values():
        terms = spec["terms"]
        weight = float(spec["weight"])
        count = sum(compact.count(term) for term in terms)  # type: ignore[arg-type]
        count += sum(1 for keyword in keywords if any(term in keyword or keyword in term for term in terms))  # type: ignore[arg-type]
        raw_hits += count
        weighted_hits += count * weight
    return raw_hits, weighted_hits


def assign_quantile_labels(rows: list[dict[str, object]]) -> None:
    scored = sorted((float(row["liquidity_risk_score"]), idx) for idx, row in enumerate(rows))
    n = len(scored)
    if not n:
        return
    for rank, (score, idx) in enumerate(scored, start=1):
        percentile = rank / n
        if score <= 0:
            label = "none"
        elif percentile >= 0.80:
            label = "high"
        elif percentile >= 0.45:
            label = "medium"
        else:
            label = "low"
        rows[idx]["liquidity_risk_quantile"] = label


def pressure_scores(row: dict[str, str]) -> tuple[float, float, float, float | None]:
    dividend = to_float(row.get("cash_dividend_per_10_shares"))
    profit = to_float(row.get("parent_net_profit_cny"))
    ocf = to_float(row.get("operating_cash_flow_cny"))
    has_dividend = to_bool(row.get("has_cash_dividend"))

    dividend_score = 0.0
    if has_dividend is True:
        dividend_score = clamp((dividend or 0.0) / 5.0 * 100.0)
    elif has_dividend is None:
        dividend_score = 15.0

    if profit is None:
        profit_score = 20.0
    elif profit < 0:
        profit_score = 100.0
    elif profit < 100_000_000:
        profit_score = 60.0
    elif profit < 500_000_000:
        profit_score = 35.0
    else:
        profit_score = 10.0

    ratio = None
    if ocf is None:
        cashflow_score = 25.0
    elif ocf < 0:
        cashflow_score = 100.0
    else:
        denominator = abs(profit) if profit not in (None, 0) else None
        if denominator:
            ratio = ocf / denominator
            if ratio < 0.3:
                cashflow_score = 70.0
            elif ratio < 0.8:
                cashflow_score = 40.0
            else:
                cashflow_score = 10.0
        else:
            cashflow_score = 25.0
    return dividend_score, profit_score, cashflow_score, ratio


def attention_level(score: float) -> str:
    if score >= 75:
        return "priority"
    if score >= 55:
        return "watch"
    if score >= 35:
        return "monitor"
    return "routine"


def cross_year_pressure_level(score: float) -> str:
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    if score > 0:
        return "low"
    return "none"


def build_reason(row: dict[str, object]) -> str:
    reasons: list[str] = []
    if row["has_cash_dividend"] == "True" and float(row["cashflow_pressure_score"]) >= 70:
        reasons.append("cash dividend while operating cash flow is weak or negative")
    if float(row["profit_pressure_score"]) >= 80:
        reasons.append("net profit is negative")
    if float(row["liquidity_risk_score"]) >= 60:
        reasons.append("liquidity-risk term frequency is high")
    cross_reason = str(row.get("cross_year_reason") or "").strip()
    if cross_reason:
        reasons.append(cross_reason)
    if row["has_cash_dividend"] == "":
        reasons.append("dividend field is missing")
    return "; ".join(reasons) or "routine review"


def cross_year_pressure(left: dict[str, object], right: dict[str, object]) -> tuple[float, list[str]]:
    reasons: list[str] = []
    pressure = 0.0
    left_div = to_float(left.get("cash_dividend_per_10_shares"))
    right_div = to_float(right.get("cash_dividend_per_10_shares"))
    left_ocf = to_float(left.get("operating_cash_flow_cny"))
    right_ocf = to_float(right.get("operating_cash_flow_cny"))
    left_profit = to_float(left.get("parent_net_profit_cny"))
    right_profit = to_float(right.get("parent_net_profit_cny"))
    left_risk = float(left["liquidity_risk_score"])
    right_risk = float(right["liquidity_risk_score"])
    left_base_attention = float(left["base_attention_score"])
    right_base_attention = float(right["base_attention_score"])

    dividend_delta = None if left_div is None or right_div is None else right_div - left_div
    ocf_delta = None if left_ocf is None or right_ocf is None else right_ocf - left_ocf
    profit_delta = None if left_profit is None or right_profit is None else right_profit - left_profit
    risk_delta = right_risk - left_risk
    base_attention_delta = right_base_attention - left_base_attention

    if risk_delta >= 25:
        pressure += 35
        reasons.append("cross-year liquidity-risk score jumps")
    elif risk_delta >= 15:
        pressure += 20
        reasons.append("cross-year liquidity-risk score rises")

    if base_attention_delta >= 20:
        pressure += 30
        reasons.append("cross-year base attention score jumps")
    elif base_attention_delta >= 10:
        pressure += 15
        reasons.append("cross-year base attention score rises")

    if dividend_delta is not None and dividend_delta > 0 and ocf_delta is not None and ocf_delta < 0:
        pressure += 25
        reasons.append("dividend rises while operating cash flow declines")

    if right_div and right_div > 0 and right_ocf is not None and right_ocf < 0:
        pressure += 25
        reasons.append("current-year dividend with negative operating cash flow")

    if profit_delta is not None and profit_delta < 0 and right_div and right_div > 0:
        pressure += 20
        reasons.append("profit declines while dividend remains")

    if right_profit is not None and right_profit < 0 and (profit_delta is None or profit_delta < 0):
        pressure += 20
        reasons.append("profit turns or remains negative")

    return clamp(pressure), reasons


def build_record_scores(rows: list[dict[str, str]], context: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    intermediate: list[dict[str, object]] = []
    max_weighted_hits = 0.0
    for row in rows:
        ctx = context.get(row["doc_id"], {})
        keywords = list(ctx.get("risk_keywords") or [])
        raw_hits, weighted_hits = count_risk_terms(str(ctx.get("risk_evidence_text") or ""), keywords)
        max_weighted_hits = max(max_weighted_hits, weighted_hits)
        dividend_score, profit_score, cashflow_score, ratio = pressure_scores(row)
        intermediate.append(
            {
                "row": row,
                "raw_hits": raw_hits,
                "weighted_hits": weighted_hits,
                "dividend_score": dividend_score,
                "profit_score": profit_score,
                "cashflow_score": cashflow_score,
                "ratio": ratio,
                "legacy_label": ctx.get("legacy_liquidity_risk_label", row.get("liquidity_risk_label") or "unknown"),
            }
        )

    scored: list[dict[str, object]] = []
    for item in intermediate:
        row = item["row"]
        liquidity_score = 0.0 if max_weighted_hits <= 0 else clamp(float(item["weighted_hits"]) / max_weighted_hits * 100.0)
        base_attention = clamp(
            0.30 * float(item["dividend_score"])
            + 0.25 * float(item["cashflow_score"])
            + 0.20 * float(item["profit_score"])
            + 0.25 * liquidity_score
        )
        result = {
            "doc_id": row["doc_id"],
            "stock_code": row["stock_code"],
            "stock_name": row["stock_name"],
            "report_year": row["report_year"],
            "has_cash_dividend": row.get("has_cash_dividend", ""),
            "cash_dividend_per_10_shares": row.get("cash_dividend_per_10_shares", ""),
            "parent_net_profit_cny": row.get("parent_net_profit_cny", ""),
            "operating_cash_flow_cny": row.get("operating_cash_flow_cny", ""),
            "ocf_to_profit_ratio": "" if item["ratio"] is None else round(float(item["ratio"]), 4),
            "dividend_pressure_score": round(float(item["dividend_score"]), 2),
            "profit_pressure_score": round(float(item["profit_score"]), 2),
            "cashflow_pressure_score": round(float(item["cashflow_score"]), 2),
            "liquidity_term_hits": item["raw_hits"],
            "liquidity_weighted_hits": round(float(item["weighted_hits"]), 2),
            "liquidity_risk_score": round(liquidity_score, 2),
            "liquidity_risk_quantile": "",
            "legacy_liquidity_risk_label": item["legacy_label"],
            "base_attention_score": round(base_attention, 2),
            "cross_year_pressure_score": 0.0,
            "cross_year_pressure_level": "none",
            "cross_year_reason": "",
            "attention_score": round(base_attention, 2),
            "attention_level": attention_level(base_attention),
            "review_reason": "",
        }
        result["review_reason"] = build_reason(result)
        scored.append(result)

    assign_quantile_labels(scored)
    apply_cross_year_pressure(scored)
    return scored


def apply_cross_year_pressure(scored: list[dict[str, object]]) -> None:
    by_company: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in scored:
        by_company[str(row["stock_code"])].append(row)

    for company_rows in by_company.values():
        company_rows = sorted(company_rows, key=lambda item: int(str(item["report_year"])))
        best_pressure_by_doc: dict[str, tuple[float, list[str]]] = {}
        for index, right in enumerate(company_rows):
            for left in company_rows[:index]:
                year_gap = int(str(right["report_year"])) - int(str(left["report_year"]))
                pressure, reasons = cross_year_pressure(left, right)
                if year_gap == 1:
                    pressure = clamp(pressure + 10 if pressure else 0)
                else:
                    pressure = round(pressure * 0.75, 2)
                doc_id = str(right["doc_id"])
                current_pressure, _ = best_pressure_by_doc.get(doc_id, (0.0, []))
                if pressure > current_pressure:
                    best_pressure_by_doc[doc_id] = (pressure, reasons)

        for row in company_rows:
            pressure, reasons = best_pressure_by_doc.get(str(row["doc_id"]), (0.0, []))
            base_attention = float(row["base_attention_score"])
            final_attention = clamp(base_attention + 0.20 * pressure)
            row["cross_year_pressure_score"] = round(pressure, 2)
            row["cross_year_pressure_level"] = cross_year_pressure_level(pressure)
            row["cross_year_reason"] = "; ".join(dict.fromkeys(reasons))
            row["attention_score"] = round(final_attention, 2)
            row["attention_level"] = attention_level(final_attention)
            row["review_reason"] = build_reason(row)


def build_events(scored: list[dict[str, object]]) -> list[dict[str, object]]:
    by_company: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in scored:
        by_company[str(row["stock_code"])].append(row)

    events: list[dict[str, object]] = []
    for stock_code, company_rows in by_company.items():
        company_rows = sorted(company_rows, key=lambda item: int(str(item["report_year"])))
        for left_index, left in enumerate(company_rows):
            for right in company_rows[left_index + 1 :]:
                events.append(build_event_row(stock_code, left, right))
    return events


def build_event_row(stock_code: str, left: dict[str, object], right: dict[str, object]) -> dict[str, object]:
    event_type: list[str] = []
    left_div = to_float(left.get("cash_dividend_per_10_shares"))
    right_div = to_float(right.get("cash_dividend_per_10_shares"))
    left_ocf = to_float(left.get("operating_cash_flow_cny"))
    right_ocf = to_float(right.get("operating_cash_flow_cny"))
    left_profit = to_float(left.get("parent_net_profit_cny"))
    right_profit = to_float(right.get("parent_net_profit_cny"))
    left_risk = float(left["liquidity_risk_score"])
    right_risk = float(right["liquidity_risk_score"])
    left_base_attention = float(left["base_attention_score"])
    right_base_attention = float(right["base_attention_score"])
    left_final_attention = float(left["attention_score"])
    right_final_attention = float(right["attention_score"])

    dividend_delta = None if left_div is None or right_div is None else right_div - left_div
    ocf_delta = None if left_ocf is None or right_ocf is None else right_ocf - left_ocf
    profit_delta = None if left_profit is None or right_profit is None else right_profit - left_profit
    risk_delta = right_risk - left_risk
    base_attention_delta = right_base_attention - left_base_attention
    final_attention_delta = right_final_attention - left_final_attention
    cross_pressure, pressure_reasons = cross_year_pressure(left, right)

    if dividend_delta is not None and dividend_delta > 0 and (ocf_delta is not None and ocf_delta < 0):
        event_type.append("dividend_up_cashflow_down")
    if right_div and right_div > 0 and right_ocf is not None and right_ocf < 0:
        event_type.append("dividend_with_negative_cashflow")
    if profit_delta is not None and profit_delta < 0 and right_div and right_div > 0:
        event_type.append("dividend_with_profit_decline")
    if risk_delta >= 25:
        event_type.append("risk_score_jump")
    if base_attention_delta >= 20:
        event_type.append("attention_score_jump")
    if cross_pressure >= 70:
        event_type.append("high_cross_year_pressure")

    year_gap = int(str(right["report_year"])) - int(str(left["report_year"]))
    if year_gap == 1 and cross_pressure:
        cross_pressure = clamp(cross_pressure + 10)
    elif year_gap > 1:
        cross_pressure = round(cross_pressure * 0.75, 2)
    return {
        "event_id": f"{stock_code}_{left['report_year']}_{right['report_year']}",
        "stock_code": stock_code,
        "stock_name": right["stock_name"],
        "from_year": left["report_year"],
        "to_year": right["report_year"],
        "year_gap": year_gap,
        "is_consecutive_pair": year_gap == 1,
        "from_doc_id": left["doc_id"],
        "to_doc_id": right["doc_id"],
        "dividend_delta": "" if dividend_delta is None else round(dividend_delta, 4),
        "ocf_delta_cny": "" if ocf_delta is None else round(ocf_delta, 2),
        "profit_delta_cny": "" if profit_delta is None else round(profit_delta, 2),
        "risk_score_delta": round(risk_delta, 2),
        "base_attention_score_delta": round(base_attention_delta, 2),
        "final_attention_score_delta": round(final_attention_delta, 2),
        "cross_year_pressure_score": round(cross_pressure, 2),
        "event_type": ";".join(event_type) or "baseline",
        "review_reason": "; ".join(pressure_reasons or event_type) if (pressure_reasons or event_type) else "cross-year baseline comparison",
    }


def report_lines(scored: list[dict[str, object]], events: list[dict[str, object]], flagged: list[dict[str, object]]) -> list[str]:
    levels = Counter(str(row["attention_level"]) for row in scored)
    risk_labels = Counter(str(row["liquidity_risk_quantile"]) for row in scored)
    cross_pressure_labels = Counter(str(row.get("cross_year_pressure_level") or "missing") for row in scored)
    event_types = Counter()
    for event in events:
        for event_type in str(event["event_type"]).split(";"):
            if event_type:
                event_types[event_type] += 1

    companies = {str(row["stock_code"]) for row in scored}
    matched_companies = {
        str(row["stock_code"])
        for row in scored
        if sum(1 for other in scored if other["stock_code"] == row["stock_code"]) >= 2
    }
    years = sorted({str(row["report_year"]) for row in scored})
    consecutive_events = [event for event in events if str(event["is_consecutive_pair"]).lower() == "true"]
    lines = [
        "# Quantitative Attention Analysis",
        "",
        "## Scope",
        f"- Annual-report records: {len(scored)}",
        f"- Companies: {len(companies)}",
        f"- Year coverage: {', '.join(years)}",
        f"- Companies with at least two years: {len(matched_companies)}",
        f"- Cross-year matching events, all same-company year pairs: {len(events)}",
        f"- Consecutive cross-year matching events: {len(consecutive_events)}",
        "",
        "## Quantitative Scoring",
        "- `liquidity_risk_score` is a normalized 0-100 score from weighted risk-term frequency in the routed risk evidence plus extracted risk keywords.",
        "- `liquidity_risk_quantile` is assigned from the full-sample score distribution, so high/medium/low are comparable across documents in the same run.",
        "- `base_attention_score` is a 0-100 single-year weighted score: dividend pressure 30%, cash-flow pressure 25%, profit pressure 20%, liquidity-risk score 25%.",
        "- `cross_year_pressure_score` is derived from same-company year-to-year signals such as risk-score jumps, base-attention jumps, dividend up while cash flow declines, and profit decline while dividends remain.",
        "- Final `attention_score` is `base_attention_score + 20% * cross_year_pressure_score`, capped at 100, so cross-year deterioration directly affects the priority review list.",
        "- The priority review list is sorted by `attention_score` rather than by a single subjective label.",
        "",
        "## Liquidity Risk Quantiles",
    ]
    for key in ["high", "medium", "low", "none"]:
        lines.append(f"- {key}: {risk_labels.get(key, 0)}")
    lines += ["", "## Attention Levels"]
    for key in ["priority", "watch", "monitor", "routine"]:
        lines.append(f"- {key}: {levels.get(key, 0)}")
    lines += ["", "## Cross-Year Pressure Levels"]
    for key in ["high", "medium", "low", "none", "missing"]:
        if cross_pressure_labels.get(key, 0):
            lines.append(f"- {key}: {cross_pressure_labels[key]}")
    lines += ["", "## Cross-Year Event Types"]
    for key, value in event_types.most_common():
        lines.append(f"- {key}: {value}")
    lines += [
        "",
        "## Top Priority Records",
        "| Rank | Stock | Name | Year | Attention | Reason |",
        "|---:|---|---|---:|---:|---|",
    ]
    for rank, row in enumerate(flagged[:10], start=1):
        lines.append(
            f"| {rank} | {row['stock_code']} | {row['stock_name']} | {row['report_year']} | {row['attention_score']} | {row['review_reason']} |"
        )
    return lines


def run(args: argparse.Namespace) -> int:
    root = Path.cwd()
    rows = read_csv(resolve_existing(root, args.input))
    context = load_extract_context(resolve_existing(root, args.extract))
    scored = build_record_scores(rows, context)
    events = build_events(scored)
    flagged = sorted(
        [row for row in scored if row["attention_level"] in {"priority", "watch"}],
        key=lambda item: float(item["attention_score"]),
        reverse=True,
    )

    write_csv(root / args.scored_output, scored, ANALYSIS_FIELDS)
    write_csv(root / args.flagged_output, flagged, ANALYSIS_FIELDS)
    write_csv(root / args.events_output, events, EVENT_FIELDS)
    write_jsonl(root / args.scored_jsonl, scored)
    report_path = root / args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines(scored, events, flagged)), encoding="utf-8")

    print(f"[analysis] scored_records={len(scored)}")
    print(f"[analysis] flagged_records={len(flagged)}")
    print(f"[analysis] cross_year_events={len(events)}")
    print(f"[analysis] report={args.report}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build quantitative risk and attention scores.")
    parser.add_argument("--input", default="records_validated_unit_normalized.csv")
    parser.add_argument("--extract", default="extract_results.jsonl")
    parser.add_argument("--scored-output", default="outputs/results/quantitative_scored_records.csv")
    parser.add_argument("--scored-jsonl", default="outputs/results/quantitative_scored_records.jsonl")
    parser.add_argument("--flagged-output", default="outputs/analysis/attention_review_list.csv")
    parser.add_argument("--events-output", default="outputs/analysis/cross_year_matching_events.csv")
    parser.add_argument("--report", default="outputs/reports/quantitative_attention_report.md")
    return run(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
