from __future__ import annotations

import csv
import ssl
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANNOUNCEMENTS = ROOT / "outputs" / "real_estate_2023_pool20_announcements.csv"
PDF_DIR = ROOT / "data" / "pdf"
META_OUT = ROOT / "data" / "metadata" / "metadata_2023_pool20.csv"
FAILED_OUT = ROOT / "outputs" / "logs" / "failed_downloads_pool20.csv"


def safe_filename(company_name: str, report_year: str, announcement_id: str) -> str:
    raw = f"{company_name}_{report_year}_{announcement_id}.pdf"
    for bad in '\\/:*?"<>|':
        raw = raw.replace(bad, "_")
    return raw


def download(url: str, path: Path) -> None:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.cninfo.com.cn/",
        },
    )
    context = ssl.create_default_context()
    with urllib.request.urlopen(request, timeout=120, context=context) as response, path.open("wb") as out:
        out.write(response.read())


def main() -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    META_OUT.parent.mkdir(parents=True, exist_ok=True)
    FAILED_OUT.parent.mkdir(parents=True, exist_ok=True)

    rows = list(csv.DictReader(ANNOUNCEMENTS.open("r", encoding="utf-8-sig", newline="")))
    metadata_rows: list[dict[str, str]] = []
    failed_rows: list[dict[str, str]] = []

    for row in rows:
        filename = safe_filename(row["company_name"], row["report_year"], row["announcement_id"])
        pdf_path = PDF_DIR / filename
        status = "success"
        error_message = ""

        try:
            if not pdf_path.exists() or pdf_path.stat().st_size <= 0:
                download(row["pdf_url"], pdf_path)
                time.sleep(1.0)
            if not pdf_path.exists() or pdf_path.stat().st_size <= 0:
                raise RuntimeError("downloaded file missing or empty")
        except Exception as exc:
            status = "failed"
            error_message = str(exc)
            failed_rows.append(
                {
                    "doc_id": row["announcement_id"],
                    "company_name": row["company_name"],
                    "stock_code": row["stock_code"],
                    "pdf_url": row["pdf_url"],
                    "error_message": error_message,
                }
            )

        metadata_rows.append(
            {
                "doc_id": row["announcement_id"],
                "company_name": row["company_name"],
                "stock_code": row["stock_code"],
                "report_year": row["report_year"],
                "announcement_title": row["announcement_title"],
                "announcement_date": row["announcement_date"],
                "cninfo_url": row["cninfo_url"],
                "pdf_url": row["pdf_url"],
                "local_pdf_path": str(Path("data/pdf") / filename).replace("\\", "/"),
                "is_revision": "修订" in row["announcement_title"],
                "download_status": status,
                "error_message": error_message,
            }
        )

    with META_OUT.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(metadata_rows[0].keys()))
        writer.writeheader()
        writer.writerows(metadata_rows)

    with FAILED_OUT.open("w", encoding="utf-8-sig", newline="") as f:
        fieldnames = ["doc_id", "company_name", "stock_code", "pdf_url", "error_message"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(failed_rows)

    print(f"metadata rows={len(metadata_rows)}")
    print(f"failed downloads={len(failed_rows)}")
    print(META_OUT)
    print(FAILED_OUT)


if __name__ == "__main__":
    main()
