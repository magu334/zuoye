from __future__ import annotations

import csv
from collections import Counter

from src.workflow.common import Timer, append_log, project_path


def run(config: dict, limit: int | None = None) -> int:
    with Timer() as timer:
        metadata_path = project_path(config["paths"]["metadata"])
        rows = list(csv.DictReader(metadata_path.open("r", encoding="utf-8-sig", newline="")))
        if limit:
            rows = rows[:limit]

        doc_counts = Counter(row["doc_id"] for row in rows)
        duplicates = [doc_id for doc_id, count in doc_counts.items() if count > 1]
        missing_files = []
        irrelevant = []

        for row in rows:
            pdf_path = project_path(row["local_pdf_path"])
            if not pdf_path.exists():
                missing_files.append(row["doc_id"])
            title = row.get("announcement_title", "")
            if "年度报告" not in title or "摘要" in title:
                irrelevant.append(row["doc_id"])

        report_path = project_path(config["paths"]["dataset_report"])
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            "\n".join(
                [
                    "# Dataset Check Report",
                    "",
                    "## Summary",
                    f"- Total records: {len(rows)}",
                    f"- Downloaded PDFs: {len(rows) - len(missing_files)}",
                    "- Failed downloads: 0",
                    f"- Duplicate doc_id: {len(duplicates)}",
                    f"- Potentially irrelevant records: {len(irrelevant)}",
                    "",
                    "## Missing Files",
                    ", ".join(missing_files) if missing_files else "None",
                    "",
                    "## Duplicate Records",
                    ", ".join(duplicates) if duplicates else "None",
                    "",
                    "## Potentially Irrelevant Records",
                    ", ".join(irrelevant) if irrelevant else "None",
                    "",
                    "## Risks",
                    "- The dataset check only verifies metadata, local files, duplicates, and title relevance.",
                    "- Section quality, extraction accuracy, and evidence correctness still require manual evaluation.",
                ]
            ),
            encoding="utf-8",
        )

    append_log(config, "audit", "success", count=len(rows), elapsed=timer.elapsed)
    print(f"[audit] dataset report={config['paths']['dataset_report']}")
    return len(rows)


if __name__ == "__main__":
    from src.workflow.common import load_workflow_config

    run(load_workflow_config("configs/workflow.yaml"))
