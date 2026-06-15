from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, Field, ValidationError


Unit = Literal["yuan", "wan_yuan", "yi_yuan", "unknown"]


class NormalizedRecord(BaseModel):
    doc_id: str
    stock_code: str
    stock_name: str
    report_year: Literal["2021", "2022", "2023"]
    has_cash_dividend: Optional[bool] = None
    cash_dividend_per_10_shares: Optional[float] = None
    parent_net_profit_raw: Optional[float] = None
    parent_net_profit_unit: Unit
    parent_net_profit_cny: Optional[float] = None
    operating_cash_flow_raw: Optional[float] = None
    operating_cash_flow_unit: Unit
    operating_cash_flow_cny: Optional[float] = None
    liquidity_risk_label: Literal["none", "low", "medium", "high", "unknown"]
    risk_keywords: str = ""
    consistency_score: Optional[int] = Field(default=None, ge=1, le=3)
    consistency_reason: str = ""
    unit_source: str = ""
    unit_confidence: Literal["high", "medium", "low", "unknown"]
    unit_note: str = ""


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def to_float(value: str | None) -> Optional[float]:
    if value is None:
        return None
    text = str(value).strip().replace(",", "")
    if text == "":
        return None
    try:
        return float(text)
    except ValueError:
        return None


def to_bool(value: str | None) -> Optional[bool]:
    if value is None:
        return None
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y"}:
        return True
    if text in {"false", "0", "no", "n"}:
        return False
    return None


def to_int(value: str | None) -> Optional[int]:
    number = to_float(value)
    if number is None:
        return None
    return int(number)


def unit_multiplier(unit: Unit) -> Optional[float]:
    if unit == "yuan":
        return 1.0
    if unit == "wan_yuan":
        return 10_000.0
    if unit == "yi_yuan":
        return 100_000_000.0
    return None


def normalize_amount(raw: Optional[float], unit: Unit) -> Optional[float]:
    multiplier = unit_multiplier(unit)
    if raw is None or multiplier is None:
        return None
    return raw * multiplier


def load_markdown_paths(metadata_path: Path, root: Path) -> dict[str, Path]:
    paths: dict[str, Path] = {}
    if metadata_path.exists():
        for row in read_csv(metadata_path):
            doc_id = row.get("doc_id", "").strip()
            markdown = row.get("markdown_path", "").strip()
            if doc_id and markdown:
                paths[doc_id] = Path(markdown)

    markdown_dir = root / "data" / "parsed" / "markdown"
    if markdown_dir.exists():
        for path in markdown_dir.glob("doc_*_pages_*.md"):
            match = re.match(r"doc_(\d+)_", path.name)
            if match:
                paths.setdefault(match.group(1), path.relative_to(root))
    return paths


def detect_unit_from_text(text: str) -> tuple[Unit, str, str, str]:
    compact = re.sub(r"\s+", " ", text)
    financial_terms = [
        "主要会计数据",
        "主要财务指标",
        "主要会计数据和财务指标",
        "经营活动产生的现金流量净额",
        "归属于上市公司股东的净利润",
        "归属于母公司股东的净利润",
    ]
    unit_patterns: list[tuple[Unit, str]] = [
        ("yi_yuan", r"(?:单位|金额单位)[:：]?\s*(?:人民币)?\s*亿元"),
        ("wan_yuan", r"(?:单位|金额单位)[:：]?\s*(?:人民币)?\s*万元"),
        ("yuan", r"(?:单位|金额单位)[:：]?\s*(?:人民币)?\s*元"),
        ("yi_yuan", r"(?:金额|币种|计量单位).{0,20}亿元"),
        ("wan_yuan", r"(?:金额|币种|计量单位).{0,20}万元"),
        ("yuan", r"(?:金额|币种|计量单位).{0,20}元"),
    ]

    windows: list[tuple[str, str]] = []
    for term in financial_terms:
        pos = compact.find(term)
        if pos >= 0:
            start = max(0, pos - 600)
            end = min(len(compact), pos + 1800)
            windows.append((term, compact[start:end]))

    for term, window in windows:
        for unit, pattern in unit_patterns:
            match = re.search(pattern, window)
            if match:
                return unit, match.group(0), "high", f"unit found near {term}"

    early = compact[:15000]
    for unit, pattern in unit_patterns:
        match = re.search(pattern, early)
        if match:
            return unit, match.group(0), "medium", "unit found in early annual-report text"

    for unit, pattern in unit_patterns:
        match = re.search(pattern, compact)
        if match:
            return unit, match.group(0), "low", "unit found outside target financial context"

    return "unknown", "", "unknown", "unit not found automatically"


def detect_doc_unit(doc_id: str, markdown_paths: dict[str, Path], root: Path) -> tuple[Unit, str, str, str]:
    markdown_path = markdown_paths.get(doc_id)
    if not markdown_path:
        return "unknown", "", "unknown", "markdown_path missing"

    path = markdown_path if markdown_path.is_absolute() else root / markdown_path
    if not path.exists():
        return "unknown", "", "unknown", f"markdown file missing: {markdown_path}"

    # Annual-report unit declarations usually appear in the front financial
    # summary. Unknown is safer than guessing when the parser misses the unit.
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        text = f.read(180_000)
    return detect_unit_from_text(text)


def run(
    input_csv: Path,
    metadata_csv: Path,
    output_csv: Path,
    errors_jsonl: Path,
    report_md: Path,
    root: Path,
) -> int:
    rows = read_csv(input_csv)
    markdown_paths = load_markdown_paths(metadata_csv, root)
    output_rows: list[dict[str, object]] = []
    errors: list[dict[str, object]] = []
    unit_counts: dict[str, int] = {"yuan": 0, "wan_yuan": 0, "yi_yuan": 0, "unknown": 0}
    confidence_counts: dict[str, int] = {"high": 0, "medium": 0, "low": 0, "unknown": 0}

    for row in rows:
        doc_id = row.get("doc_id", "").strip()
        unit, source, confidence, note = detect_doc_unit(doc_id, markdown_paths, root)
        unit_counts[unit] += 1
        confidence_counts[confidence] += 1

        parent_raw = to_float(row.get("parent_net_profit"))
        ocf_raw = to_float(row.get("operating_cash_flow"))

        record_data = {
            "doc_id": doc_id,
            "stock_code": row.get("stock_code", "").strip(),
            "stock_name": row.get("stock_name", "").strip(),
            "report_year": row.get("report_year", "").strip(),
            "has_cash_dividend": to_bool(row.get("has_cash_dividend")),
            "cash_dividend_per_10_shares": to_float(row.get("cash_dividend_per_10_shares")),
            "parent_net_profit_raw": parent_raw,
            "parent_net_profit_unit": unit,
            "parent_net_profit_cny": normalize_amount(parent_raw, unit),
            "operating_cash_flow_raw": ocf_raw,
            "operating_cash_flow_unit": unit,
            "operating_cash_flow_cny": normalize_amount(ocf_raw, unit),
            "liquidity_risk_label": row.get("liquidity_risk_label", "unknown").strip() or "unknown",
            "risk_keywords": row.get("risk_keywords", ""),
            "consistency_score": to_int(row.get("consistency_score")),
            "consistency_reason": row.get("consistency_reason", ""),
            "unit_source": source,
            "unit_confidence": confidence,
            "unit_note": note,
        }

        try:
            record = NormalizedRecord.model_validate(record_data)
            output_rows.append(record.model_dump())
        except ValidationError as exc:
            errors.append({"doc_id": doc_id, "error": exc.errors(), "row": record_data})

    fields = list(NormalizedRecord.model_fields.keys())
    write_csv(output_csv, output_rows, fields)

    errors_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with errors_jsonl.open("w", encoding="utf-8") as f:
        for error in errors:
            f.write(json.dumps(error, ensure_ascii=False) + "\n")

    report_lines = [
        "# Unit Normalization Report",
        "",
        "## Summary",
        f"- Input records: {len(rows)}",
        f"- Valid normalized records: {len(output_rows)}",
        f"- Pydantic validation errors: {len(errors)}",
        "",
        "## Detected Units",
    ]
    for unit, count in unit_counts.items():
        report_lines.append(f"- {unit}: {count}")
    report_lines += ["", "## Unit Confidence"]
    for confidence, count in confidence_counts.items():
        report_lines.append(f"- {confidence}: {count}")
    report_lines += [
        "",
        "## Output Fields",
        "- `parent_net_profit_raw` and `operating_cash_flow_raw` preserve the original extracted values.",
        "- `parent_net_profit_unit` and `operating_cash_flow_unit` record detected table units.",
        "- `parent_net_profit_cny` and `operating_cash_flow_cny` convert values to yuan when a unit is detected.",
        "- Records with `unit = unknown` keep CNY fields empty and require manual review before amount ranking.",
        "",
        "## Important Note",
        "This normalization is an enhanced output for analysis. It does not overwrite the original extraction result.",
    ]
    report_md.parent.mkdir(parents=True, exist_ok=True)
    report_md.write_text("\n".join(report_lines), encoding="utf-8")

    return 0 if not errors else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize financial amount units and validate with Pydantic.")
    parser.add_argument("--input", default="outputs/results/final_results.csv")
    parser.add_argument("--metadata", default="data/metadata/metadata.csv")
    parser.add_argument("--output", default="outputs/results/final_results_unit_normalized.csv")
    parser.add_argument("--errors", default="outputs/logs/unit_normalization_validation_errors.jsonl")
    parser.add_argument("--report", default="outputs/reports/unit_normalization_report.md")
    args = parser.parse_args()

    root = Path.cwd()
    return run(
        input_csv=root / args.input,
        metadata_csv=root / args.metadata,
        output_csv=root / args.output,
        errors_jsonl=root / args.errors,
        report_md=root / args.report,
        root=root,
    )


if __name__ == "__main__":
    raise SystemExit(main())
