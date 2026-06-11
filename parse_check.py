from __future__ import annotations

import csv
import json

from src.workflow.common import Timer, append_log, project_path


TARGET_KEYWORDS = {
    "dividend": ["利润分配预案", "分红派息预案", "不派发股息", "每10股", "每 10 股"],
    "financial": ["主要会计数据和财务指标", "归属于上市公司股东的净利润", "经营活动产生的现金流量净额"],
    "risk": ["流动性", "融资", "资金情况", "偿债", "销售回款", "可能面对的风险"],
}


def run(config: dict, limit: int | None = None) -> int:
    with Timer() as timer:
        parsed_path = project_path(config["paths"]["parsed_docs"])
        docs = [json.loads(line) for line in parsed_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if limit:
            docs = docs[:limit]

        rows = []
        for doc in docs:
            text = "\n".join(page["text"] for page in doc["pages"])
            rows.append(
                {
                    "doc_id": doc["doc_id"],
                    "stock_code": doc["stock_code"],
                    "stock_name": doc["stock_name"],
                    "title": doc["title"],
                    "pdf_path": doc["pdf_path"],
                    "markdown_path": doc["markdown_path"],
                    "parser": doc["parser"],
                    "markdown_non_empty": bool(text.strip()),
                    "has_garbled_text": "�" in text,
                    "has_dividend_keyword": any(k in text for k in TARGET_KEYWORDS["dividend"]),
                    "has_financial_keyword": any(k in text for k in TARGET_KEYWORDS["financial"]),
                    "has_risk_keyword": any(k in text for k in TARGET_KEYWORDS["risk"]),
                    "page_no_preserved": "approximate",
                    "needs_manual_fix": "yes" if "�" in text else "no",
                }
            )

        report_path = project_path("parse_check.md")
        lines = [
            "# Parse Check",
            "",
            "## Summary",
            f"- Checked documents: {len(rows)}",
            f"- Non-empty markdown: {sum(1 for row in rows if row['markdown_non_empty'])}",
            f"- Garbled text detected: {sum(1 for row in rows if row['has_garbled_text'])}",
            f"- Dividend keywords found: {sum(1 for row in rows if row['has_dividend_keyword'])}",
            f"- Financial keywords found: {sum(1 for row in rows if row['has_financial_keyword'])}",
            f"- Risk keywords found: {sum(1 for row in rows if row['has_risk_keyword'])}",
            "",
            "## Notes",
            "- Parser is MinerU.",
            "- Current markdown is generated from the first 200-page MinerU split for each annual report.",
            "- Original PDF page numbers are not stably preserved in the current markdown, so page evidence is marked approximate.",
            "- Table text is available in markdown HTML table form, but financial amount unit normalization still needs repair.",
            "",
            "## Sample Inspection",
            "| doc_id | stock_name | markdown_non_empty | dividend | financial | risk | needs_manual_fix |",
            "|---|---|---:|---:|---:|---:|---|",
        ]
        for row in rows:
            lines.append(
                f"| {row['doc_id']} | {row['stock_name']} | {row['markdown_non_empty']} | "
                f"{row['has_dividend_keyword']} | {row['has_financial_keyword']} | {row['has_risk_keyword']} | {row['needs_manual_fix']} |"
            )
        report_path.write_text("\n".join(lines), encoding="utf-8")

        csv_path = project_path("outputs/reports/parse_check.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    append_log(config, "parse_check", "success", count=len(rows), elapsed=timer.elapsed)
    print(f"[parse_check] checked docs={len(rows)}")
    return len(rows)


if __name__ == "__main__":
    from src.workflow.common import load_workflow_config

    run(load_workflow_config("configs/workflow.yaml"))
