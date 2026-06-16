from __future__ import annotations

import csv
import json

from src.schemas import DividendCashflowLiquidityExtract
from src.workflow.common import Timer, append_log, project_path, resolve_existing


def validate_model(data: dict) -> DividendCashflowLiquidityExtract:
    if hasattr(DividendCashflowLiquidityExtract, "model_validate"):
        return DividendCashflowLiquidityExtract.model_validate(data)
    return DividendCashflowLiquidityExtract.parse_obj(data)


def run(config: dict, limit: int | None = None) -> int:
    with Timer() as timer:
        rows = [json.loads(line) for line in resolve_existing(config["paths"]["extract_results"]).read_text(encoding="utf-8").splitlines() if line.strip()]
        if limit:
            rows = rows[:limit]
        valid_rows = []
        errors = []
        for row in rows:
            try:
                item = validate_model(row)
                dividend = item.dividend_plan
                parent_profit = item.parent_net_profit
                ocf = item.operating_cash_flow
                risk = item.liquidity_risk
                valid_rows.append(
                    {
                        "doc_id": item.doc_id,
                        "stock_code": item.stock_code,
                        "stock_name": item.stock_name,
                        "report_year": item.report_year,
                        "has_cash_dividend": "" if dividend is None or dividend.has_cash_dividend is None else dividend.has_cash_dividend,
                        "cash_dividend_per_10_shares": "" if dividend is None else dividend.cash_dividend_per_10_shares,
                        "parent_net_profit": "" if parent_profit is None else parent_profit.value,
                        "operating_cash_flow": "" if ocf is None else ocf.value,
                        "liquidity_risk_label": "" if risk is None else risk.label,
                        "risk_keywords": "" if risk is None else ";".join(risk.keywords),
                        "consistency_score": item.consistency_score,
                        "consistency_reason": item.consistency_reason,
                    }
                )
            except Exception as exc:
                errors.append({"doc_id": row.get("doc_id"), "error": str(exc), "raw": row})

        validated_path = project_path(config["paths"]["validated_results"])
        validated_path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = [
            "doc_id",
            "stock_code",
            "stock_name",
            "report_year",
            "has_cash_dividend",
            "cash_dividend_per_10_shares",
            "parent_net_profit",
            "operating_cash_flow",
            "liquidity_risk_label",
            "risk_keywords",
            "consistency_score",
            "consistency_reason",
        ]
        with validated_path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(valid_rows)

        error_path = project_path(config["paths"]["validation_errors"])
        error_path.parent.mkdir(parents=True, exist_ok=True)
        with error_path.open("w", encoding="utf-8") as f:
            for error in errors:
                f.write(json.dumps(error, ensure_ascii=False) + "\n")
    append_log(config, "validate", "success", count=len(valid_rows), error=None if not errors else f"errors={len(errors)}", elapsed=timer.elapsed)
    print(f"[validate] valid={len(valid_rows)}, errors={len(errors)}")
    return len(valid_rows)


if __name__ == "__main__":
    from src.workflow.common import load_workflow_config

    run(load_workflow_config("configs/workflow.yaml"))

