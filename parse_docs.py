from __future__ import annotations

import csv
import json
from pathlib import Path

from src.workflow.common import Timer, append_log, project_path, resolve_existing


def run(config: dict, limit: int | None = None) -> int:
    with Timer() as timer:
        rows = list(csv.DictReader(resolve_existing(config["paths"]["metadata"]).open("r", encoding="utf-8-sig", newline="")))
        if limit:
            rows = rows[:limit]
        out_path = project_path(config["paths"]["parsed_docs"])
        out_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_dir = project_path(config["paths"]["markdown_dir"])
        count = 0
        with out_path.open("w", encoding="utf-8") as f:
            for row in rows:
                doc_id = row["doc_id"]
                candidates = sorted(markdown_dir.glob(f"doc_{doc_id}_pages_001_*.md"))
                md_path = candidates[0] if candidates else markdown_dir / f"doc_{doc_id}_pages_001_200.md"
                if not md_path.exists():
                    flat_candidates = sorted(project_path(".").glob(f"doc_{doc_id}_pages_001_*.md"))
                    if flat_candidates:
                        md_path = flat_candidates[0]
                if not md_path.exists():
                    raise FileNotFoundError(f"missing MinerU markdown for doc_id={doc_id}: {md_path}")
                text = md_path.read_text(encoding="utf-8", errors="ignore")
                if not text.strip():
                    raise ValueError(f"empty MinerU markdown for doc_id={doc_id}")
                record = {
                    "doc_id": doc_id,
                    "stock_code": row["stock_code"],
                    "stock_name": row["company_name"],
                    "report_year": row.get("report_year", ""),
                    "title": row["announcement_title"],
                    "pdf_path": row["local_pdf_path"],
                    "markdown_path": str(Path(config["paths"]["markdown_dir"]) / md_path.name).replace("\\", "/"),
                    "parser": "mineru",
                    "pages": [{"page_no": 1, "text": text}],
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                count += 1
    append_log(config, "parse", "success", count=count, elapsed=timer.elapsed)
    print(f"[parse] parsed docs={count}")
    return count


if __name__ == "__main__":
    from src.workflow.common import load_workflow_config

    run(load_workflow_config("configs/workflow.yaml"))
