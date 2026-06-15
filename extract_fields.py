from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.workflow.common import Timer, append_log, project_path


RISK_KEYWORDS = ["流动性", "融资", "资金压力", "资金安全", "偿债", "债务", "销售回款", "行业下行", "市场下行", "现金流"]


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def number_from_nearby(label: str, text: str) -> tuple[float | None, str | None]:
    compact = clean(text)
    idx = compact.find(label)
    if idx < 0:
        return None, None
    snippet = compact[idx : idx + 260]
    match = re.search(r"(-?\d[\d,]*(?:\.\d+)?)", snippet)
    if not match:
        return None, snippet
    raw = match.group(1)
    try:
        return float(raw.replace(",", "")), snippet
    except ValueError:
        return None, snippet


def extract_dividend(section: dict) -> dict | None:
    text = clean(section.get("text", ""))
    if not text:
        return None
    no_dividend = bool(re.search(r"不派发(?:股息|现金红利)|不进行现金分红|不分配现金红利", text))
    per10 = None
    match = re.search(r"每\s*10\s*股.{0,80}?(?:派发|派|分配).{0,30}?([0-9]+(?:\.[0-9]+)?)\s*元", text)
    if match:
        per10 = float(match.group(1))
    if no_dividend:
        per10 = 0.0
    return {
        "has_cash_dividend": None if per10 is None else per10 > 0,
        "cash_dividend_per_10_shares": per10,
        "bonus_or_conversion": False if ("不送红股" in text or "不进行资本公积金转增" in text) else None,
        "evidence": {"text": text[:500], "source": "section", "section_type": "dividend"},
    }


def extract_numeric(section: dict, label: str) -> dict | None:
    value, snippet = number_from_nearby(label, section.get("text", ""))
    if snippet is None:
        return None
    return {
        "value": value,
        "raw_text": snippet[:500],
        "unit": "unknown",
        "evidence": {"text": snippet[:500], "source": "section", "section_type": "financial"},
    }


def extract_risk(section: dict) -> dict | None:
    text = clean(section.get("text", ""))
    if not text:
        return None
    found = [kw for kw in RISK_KEYWORDS if kw in text]
    if len(found) >= 5:
        label = "high"
    elif len(found) >= 3:
        label = "medium"
    elif found:
        label = "low"
    else:
        label = "none"
    return {
        "label": label,
        "keywords": found,
        "evidence": {"text": text[:700], "source": "section", "section_type": "liquidity_risk"} if found else None,
    }


def score_record(dividend: dict | None, risk: dict | None) -> tuple[int | None, str | None]:
    if not dividend or not risk:
        return None, "关键字段缺失，暂不评分"
    per10 = dividend.get("cash_dividend_per_10_shares")
    risk_label = risk.get("label")
    if per10 == 0 and risk_label in {"medium", "high"}:
        return 3, "不分红或低分红与较高流动性/行业风险披露基本一致"
    if per10 and per10 > 0 and risk_label == "high":
        return 1, "存在现金分红且风险披露较强，需要人工复核是否存在不一致"
    return 2, "初步未发现强烈不一致，但仍需人工复核 evidence"


def load_env() -> None:
    env_path = project_path(".env")
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.strip().startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def parse_json_object(content: str) -> dict:
    content = content.strip()
    content = re.sub(r"^```(?:json)?", "", content).strip()
    content = re.sub(r"```$", "", content).strip()
    start = content.find("{")
    end = content.rfind("}")
    if start >= 0 and end > start:
        content = content[start : end + 1]
    return json.loads(content)


def call_siliconflow_llm(prompt: str) -> dict:
    load_env()
    api_key = os.environ.get("LLM_API_KEY")
    base_url = os.environ.get("LLM_BASE_URL", "https://api.siliconflow.cn/v1").rstrip("/")
    model = os.environ.get("LLM_MODEL", "deepseek-ai/DeepSeek-V4-Pro")
    if not api_key:
        raise RuntimeError("missing LLM_API_KEY in .env")
    url = f"{base_url}/chat/completions"
    payload = {
        "model": model,
        "temperature": 0,
        "max_tokens": 1800,
        "messages": [
            {
                "role": "system",
                "content": (
                    "你是金融公告字段抽取助手。只根据用户提供的年报片段抽取字段。"
                    "不确定时输出 null。evidence.text 必须来自输入原文。只输出合法 JSON。"
                ),
            },
            {"role": "user", "content": prompt},
        ],
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"LLM HTTP error {exc.code}: {detail[:500]}") from exc
    content = data["choices"][0]["message"]["content"]
    return parse_json_object(content)


def build_llm_prompt(base: dict, parts: dict[str, dict]) -> str:
    section_payload = {
        key: {
            "quality_issue": value.get("quality_issue"),
            "text": (value.get("text") or "")[:1800],
        }
        for key, value in parts.items()
    }
    return json.dumps(
        {
            "task": "抽取房地产上市公司年报中的分红政策、经营现金流、流动性风险与一致性评分。",
            "null_rule": "如果输入片段中找不到字段，输出 null，不得根据常识补全。",
            "required_json_shape": {
                "dividend_plan": {
                    "has_cash_dividend": "boolean|null",
                    "cash_dividend_per_10_shares": "number|null",
                    "bonus_or_conversion": "boolean|null",
                    "evidence": {"text": "原文片段", "source": "section", "section_type": "dividend"},
                },
                "parent_net_profit": {
                    "value": "number|null",
                    "raw_text": "原文金额或表格片段|null",
                    "unit": "元/万元/亿元/unknown|null",
                    "evidence": {"text": "原文片段", "source": "section", "section_type": "financial"},
                },
                "operating_cash_flow": {
                    "value": "number|null",
                    "raw_text": "原文金额或表格片段|null",
                    "unit": "元/万元/亿元/unknown|null",
                    "evidence": {"text": "原文片段", "source": "section", "section_type": "financial"},
                },
                "liquidity_risk": {
                    "label": "none|low|medium|high|unknown",
                    "keywords": ["命中的风险关键词"],
                    "evidence": {"text": "原文片段", "source": "section", "section_type": "liquidity_risk"},
                },
                "consistency_score": "1|2|3|null",
                "consistency_reason": "简短理由|null",
            },
            "scoring_rule": {
                "3": "分红较低/不分红与较强现金流压力或流动性风险披露一致",
                "2": "未发现明显不一致，但需要人工复核",
                "1": "现金分红较高，同时现金流或流动性压力较强，疑似不一致",
            },
            "document": {
                "doc_id": base["doc_id"],
                "stock_code": base["stock_code"],
                "stock_name": base["stock_name"],
                "title": base["title"],
                "report_year": base.get("report_year", ""),
            },
            "sections": section_payload,
        },
        ensure_ascii=False,
    )


def run(config: dict, limit: int | None = None, method: str = "rule") -> int:
    with Timer() as timer:
        sections = [json.loads(line) for line in project_path(config["paths"]["sections"]).read_text(encoding="utf-8").splitlines() if line.strip()]
        grouped: dict[str, dict[str, dict]] = defaultdict(dict)
        meta: dict[str, dict] = {}
        for sec in sections:
            grouped[sec["doc_id"]][sec["section_type"]] = sec
            meta[sec["doc_id"]] = sec
        doc_ids = list(grouped.keys())
        if limit:
            doc_ids = doc_ids[:limit]
        out_path = project_path(config["paths"]["extract_results"])
        out_path.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with out_path.open("w", encoding="utf-8") as f:
            for doc_id in doc_ids:
                parts = grouped[doc_id]
                base = meta[doc_id]
                if method == "rule":
                    dividend = extract_dividend(parts.get("dividend", {}))
                    parent_profit = extract_numeric(parts.get("financial", {}), "归属于上市公司股东的净利润")
                    ocf = extract_numeric(parts.get("financial", {}), "经营活动产生的现金流量净额")
                    risk = extract_risk(parts.get("liquidity_risk", {}))
                    score, reason = score_record(dividend, risk)
                elif method == "llm":
                    llm_data = call_siliconflow_llm(build_llm_prompt(base, parts))
                    dividend = llm_data.get("dividend_plan")
                    parent_profit = llm_data.get("parent_net_profit")
                    ocf = llm_data.get("operating_cash_flow")
                    risk = llm_data.get("liquidity_risk")
                    score = llm_data.get("consistency_score")
                    reason = llm_data.get("consistency_reason")
                else:
                    raise ValueError(f"unknown extract method: {method}")
                record = {
                    "doc_id": doc_id,
                    "stock_code": base["stock_code"],
                    "stock_name": base["stock_name"],
                    "report_year": base.get("report_year", ""),
                    "title": base["title"],
                    "event_type": "房地产年报分红现金流流动性一致性分析",
                    "dividend_plan": dividend,
                    "parent_net_profit": parent_profit,
                    "operating_cash_flow": ocf,
                    "liquidity_risk": risk,
                    "consistency_score": score,
                    "consistency_reason": reason,
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                count += 1
    append_log(config, "extract", "success", count=count, elapsed=timer.elapsed)
    print(f"[extract] extract records={count}")
    return count


if __name__ == "__main__":
    from src.workflow.common import load_workflow_config

    parser = argparse.ArgumentParser()
    parser.add_argument("--method", default="rule")
    args = parser.parse_args()
    run(load_workflow_config("configs/workflow.yaml"), method=args.method)
