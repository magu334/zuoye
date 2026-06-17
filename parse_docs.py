from __future__ import annotations

import csv
import json
from pathlib import Path

from pypdf import PdfReader

from src.workflow.common import Timer, append_log, project_path, resolve_existing


def extract_pdf_text(pdf_path: Path, max_pages: int | None = None) -> tuple[str, int]:
    reader = PdfReader(str(pdf_path))
    page_texts: list[str] = []
    pages = reader.pages if max_pages is None else reader.pages[:max_pages]
    for index, page in enumerate(pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:
            text = f"\n[page {index} text extraction failed: {exc}]\n"
        page_texts.append(f"\n\n<!-- page {index} -->\n{text}")
    return "\n".join(page_texts).strip(), len(page_texts)


def find_mineru_markdown(markdown_dir: Path, doc_id: str) -> Path | None:
    candidates = sorted(markdown_dir.glob(f"doc_{doc_id}_pages_001_*.md"))
    if candidates:
        return candidates[0]
    fallback = markdown_dir / f"doc_{doc_id}_pages_001_200.md"
    if fallback.exists():
        return fallback
    flat_candidates = sorted(project_path(".").glob(f"doc_{doc_id}_pages_001_*.md"))
    if flat_candidates:
        return flat_candidates[0]
    return None


def run(config: dict, limit: int | None = None) -> int:
    with Timer() as timer:
        rows = list(csv.DictReader(resolve_existing(config["paths"]["metadata"]).open("r", encoding="utf-8-sig", newline="")))
        if limit:
            rows = rows[:limit]
        out_path = project_path(config["paths"]["parsed_docs"])
        out_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_dir = project_path(config["paths"]["markdown_dir"])
        pdf_text_dir = project_path(config["paths"].get("pdf_text_dir", "data/parsed/pdf_text"))
        pdf_text_dir.mkdir(parents=True, exist_ok=True)
        max_pages = config.get("steps", {}).get("parse", {}).get("max_pages")
        count = 0
        mineru_count = 0
        pdf_text_count = 0
        with out_path.open("w", encoding="utf-8") as f:
            for row in rows:
                doc_id = row["doc_id"]
                md_path = find_mineru_markdown(markdown_dir, doc_id)
                parser_name = "mineru"
                page_count = 1
                if md_path:
                    text = md_path.read_text(encoding="utf-8", errors="ignore")
                    markdown_path = md_path
                    mineru_count += 1
                else:
                    pdf_path = resolve_existing(row["local_pdf_path"])
                    if not pdf_path.exists():
                        raise FileNotFoundError(f"missing PDF for doc_id={doc_id}: {pdf_path}")
                    text, page_count = extract_pdf_text(pdf_path, max_pages=max_pages)
                    markdown_path = pdf_text_dir / f"doc_{doc_id}_pdf_text.md"
                    markdown_path.write_text(text, encoding="utf-8")
                    parser_name = "pypdf_text_fallback"
                    pdf_text_count += 1
                if not text.strip():
                    raise ValueError(f"empty parsed text for doc_id={doc_id}")
                record = {
                    "doc_id": doc_id,
                    "stock_code": row["stock_code"],
                    "stock_name": row["company_name"],
                    "report_year": row.get("report_year", ""),
                    "title": row["announcement_title"],
                    "pdf_path": row["local_pdf_path"],
                    "markdown_path": str(markdown_path.relative_to(project_path("."))).replace("\\", "/"),
                    "parser": parser_name,
                    "page_count": page_count,
                    "pages": [{"page_no": 1, "text": text}],
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                count += 1
    append_log(config, "parse", "success", count=count, elapsed=timer.elapsed)
    print(f"[parse] parsed docs={count}, mineru={mineru_count}, pdf_text_fallback={pdf_text_count}")
    return count


if __name__ == "__main__":
    from src.workflow.common import load_workflow_config

    run(load_workflow_config("configs/workflow.yaml"))
