from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.workflow.common import Timer, append_log, project_path


RULES = {
    "dividend": {
        "priority_keywords": ["利润分配预案", "分红派息预案", "分红派息方案", "现金分红"],
        "fallback_keywords": ["不派发股息", "不派发现金红利", "每10股", "每 10 股"],
        "min_line": 0,
        "window_lines": 70,
        "context_before": 5,
    },
    "financial": {
        "priority_keywords": ["主要会计数据和财务指标", "主要会计数据和财务指标摘要"],
        "fallback_keywords": ["归属于上市公司股东的净利润", "经营活动产生的现金流量净额"],
        "min_line": 0,
        "window_lines": 110,
        "context_before": 0,
    },
    "liquidity_risk": {
        "priority_keywords": [
            "可能面对的风险",
            "风险与机遇",
            "风险因素",
            "风险管理",
            "内部控制和风险管理",
            "融资情况",
            "财务融资情况",
            "资金情况",
            "房地产开发企业到位资金情况",
        ],
        "fallback_keywords": ["流动性风险", "资金压力", "现金短债比", "偿债", "债务", "销售回款", "行业下行", "市场下行"],
        "min_line": 120,
        "window_lines": 170,
        "context_before": 3,
    },
}

EXCLUDE_NEARBY = ["目录", "释义", "备查文件目录"]
RISK_CONTEXT_KEYWORDS = ["融资", "资金", "现金流", "偿债", "债务", "销售回款", "行业下行", "市场下行", "流动性", "去化"]


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def normalize_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def line_has_any(line: str, keywords: list[str]) -> bool:
    return any(keyword in line for keyword in keywords)


def line_looks_like_heading(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("#") or len(stripped) <= 40


def nearby_text(lines: list[str], idx: int, radius: int = 5) -> str:
    start = max(0, idx - radius)
    end = min(len(lines), idx + radius + 1)
    return clean(" ".join(lines[start:end]))


def is_excluded_hit(lines: list[str], idx: int) -> bool:
    nearby = nearby_text(lines, idx, radius=4)
    return any(keyword in nearby for keyword in EXCLUDE_NEARBY)


def section_candidate(lines: list[str], idx: int, window_lines: int, context_before: int) -> str:
    start = max(0, idx - context_before)
    end = min(len(lines), idx + window_lines)
    return clean("\n".join(lines[start:end]))


def risk_candidate_is_relevant(candidate: str) -> bool:
    return sum(1 for keyword in RISK_CONTEXT_KEYWORDS if keyword in candidate) >= 2


def quality_for_candidate(section_type: str, candidate: str, source: str) -> tuple[str, str]:
    if len(candidate) < 80:
        return "too_short", "candidate_too_short"
    if section_type == "liquidity_risk" and not risk_candidate_is_relevant(candidate):
        return "wrong_section", f"{source}; lacks_liquidity_context"
    return "ok", source


def find_section(text: str, section_type: str) -> tuple[str, str, str]:
    lines = normalize_lines(text)
    rule = RULES[section_type]
    min_line = int(rule["min_line"])
    window_lines = int(rule["window_lines"])
    context_before = int(rule["context_before"])

    if section_type == "dividend":
        front_limit = min(len(lines), 220)
        front_keywords = rule["priority_keywords"] + rule["fallback_keywords"]
        for idx in range(front_limit):
            if line_has_any(lines[idx], front_keywords):
                candidate = section_candidate(lines, idx, window_lines=45, context_before=2)
                quality, note = quality_for_candidate(section_type, candidate, "candidate_from_front_matter")
                return quality, candidate, note

    for source, keywords in [
        ("candidate_from_heading", rule["priority_keywords"]),
        ("candidate_from_fallback_keyword", rule["fallback_keywords"]),
    ]:
        for idx, line in enumerate(lines):
            if idx < min_line:
                continue
            if not line_has_any(line, keywords):
                continue
            if source == "candidate_from_heading" and not line_looks_like_heading(line):
                continue
            if is_excluded_hit(lines, idx):
                continue
            candidate = section_candidate(lines, idx, window_lines, context_before)
            quality, note = quality_for_candidate(section_type, candidate, source)
            return quality, candidate, note
    return "not_found", "", "no_candidate"


def run(config: dict, limit: int | None = None) -> int:
    with Timer() as timer:
        parsed_path = project_path(config["paths"]["parsed_docs"])
        records = [json.loads(line) for line in parsed_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if limit:
            records = records[:limit]
        sections_path = project_path(config["paths"]["sections"])
        sections_path.parent.mkdir(parents=True, exist_ok=True)
        report_path = project_path(config["paths"]["section_report"])
        report_path.parent.mkdir(parents=True, exist_ok=True)
        section_count = 0
        report_rows = []
        with sections_path.open("w", encoding="utf-8") as out:
            for doc in records:
                full_text = "\n".join(page["text"] for page in doc["pages"])
                for section_type in RULES:
                    quality, text, note = find_section(full_text, section_type)
                    item = {
                        "doc_id": doc["doc_id"],
                        "stock_code": doc["stock_code"],
                        "stock_name": doc["stock_name"],
                        "report_year": doc.get("report_year", ""),
                        "title": doc["title"],
                        "section_type": section_type,
                        "quality_issue": quality,
                        "page_no": 1,
                        "text": text,
                    }
                    out.write(json.dumps(item, ensure_ascii=False) + "\n")
                    section_count += 1
                    report_rows.append(
                        {
                            "doc_id": doc["doc_id"],
                            "stock_name": doc["stock_name"],
                            "section_type": section_type,
                            "quality_issue": quality,
                            "page_no": 1,
                            "evidence_preview": text[:120],
                            "human_check_status": "pending",
                            "review_notes": note,
                        }
                    )
        with report_path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(report_rows[0].keys()))
            writer.writeheader()
            writer.writerows(report_rows)
    append_log(config, "route", "success", count=section_count, elapsed=timer.elapsed)
    print(f"[route] sections={section_count}")
    return section_count


if __name__ == "__main__":
    from src.workflow.common import load_workflow_config

    run(load_workflow_config("configs/workflow.yaml"))
