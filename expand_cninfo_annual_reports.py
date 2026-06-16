from __future__ import annotations

import argparse
import csv
import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
QUERY_URL = "https://www.cninfo.com.cn/new/hisAnnouncement/query"
STATIC_BASE = "https://static.cninfo.com.cn/"


HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json,text/plain,*/*",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def safe_filename(company_name: str, report_year: str, announcement_id: str) -> str:
    raw = f"{company_name}_{report_year}_{announcement_id}.pdf"
    for bad in '\\/:*?"<>|':
        raw = raw.replace(bad, "_")
    return raw


def org_id_from_url(url: str) -> str:
    match = re.search(r"[?&]orgId=([^&]+)", url or "")
    return urllib.parse.unquote(match.group(1)) if match else ""


def publish_date_from_announcement(item: dict[str, Any]) -> str:
    raw = item.get("announcementTime")
    if isinstance(raw, int):
        # CNINFO returns milliseconds since epoch.
        return time.strftime("%Y-%m-%d", time.localtime(raw / 1000))
    date = str(item.get("announcementDate") or "")
    return date[:10]


def is_revision(title: str) -> bool:
    return any(token in title for token in ["修订", "更正", "更新后"])


def is_full_annual_report(title: str, report_year: int) -> bool:
    if "年度报告" not in title:
        return False
    if str(report_year) not in title:
        return False
    excluded = ["摘要", "英文", "已取消", "取消", "关于", "提示性公告", "说明"]
    return not any(token in title for token in excluded)


def normalize_pdf_url(item: dict[str, Any]) -> str:
    url = str(item.get("adjunctUrl") or "").lstrip("/")
    if not url:
        return ""
    if url.startswith("http"):
        return url
    return urllib.parse.urljoin(STATIC_BASE, url)


def cninfo_detail_url(stock_code: str, announcement_id: str, org_id: str) -> str:
    return (
        "https://www.cninfo.com.cn/new/disclosure/detail?"
        + urllib.parse.urlencode({"stockCode": stock_code, "announcementId": announcement_id, "orgId": org_id})
    )


def query_company_year(stock_code: str, org_id: str, report_year: int, sleep_seconds: float) -> list[dict[str, Any]]:
    publish_year = report_year + 1
    params = {
        "pageNum": "1",
        "pageSize": "30",
        "column": "szse",
        "tabName": "fulltext",
        "plate": "",
        "stock": f"{stock_code},{org_id}",
        "searchkey": "",
        "secid": "",
        "category": "category_ndbg_szsh",
        "trade": "",
        "seDate": f"{publish_year}-01-01~{publish_year}-12-31",
        "sortName": "",
        "sortType": "",
        "isHLtitle": "true",
    }
    payload = urllib.parse.urlencode(params).encode("utf-8")
    request = urllib.request.Request(QUERY_URL, data=payload, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
    finally:
        time.sleep(sleep_seconds)
    return data.get("announcements") or []


def select_annual_report(items: list[dict[str, Any]], report_year: int) -> dict[str, Any] | None:
    candidates = []
    for item in items:
        title = str(item.get("announcementTitle") or "")
        if is_full_annual_report(title, report_year):
            candidates.append(item)
    if not candidates:
        return None
    # Prefer the latest full report, because revised annual reports should be
    # closer to the final disclosed document than the first version.
    return sorted(candidates, key=lambda item: int(item.get("announcementTime") or 0), reverse=True)[0]


def metadata_row(company: dict[str, str], report_year: int, item: dict[str, Any], pdf_dir: Path) -> dict[str, str]:
    announcement_id = str(item.get("announcementId") or "")
    title = str(item.get("announcementTitle") or "")
    pdf_url = normalize_pdf_url(item)
    filename = safe_filename(company["company_name"], str(report_year), announcement_id)
    local_pdf_path = (pdf_dir / filename).relative_to(ROOT).as_posix()
    return {
        "doc_id": announcement_id,
        "company_name": company["company_name"],
        "stock_code": company["stock_code"],
        "report_year": str(report_year),
        "announcement_title": title,
        "announcement_date": publish_date_from_announcement(item),
        "cninfo_url": cninfo_detail_url(company["stock_code"], announcement_id, company["org_id"]),
        "pdf_url": pdf_url,
        "local_pdf_path": local_pdf_path,
        "is_revision": str(is_revision(title)),
        "download_status": "pending",
        "error_message": "",
    }


def download_pdf(url: str, path: Path) -> None:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.cninfo.com.cn/",
        },
    )
    context = ssl.create_default_context()
    with urllib.request.urlopen(request, timeout=180, context=context) as response, path.open("wb") as f:
        f.write(response.read())


def load_companies(seed_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_code: dict[str, dict[str, str]] = {}
    for row in seed_rows:
        org_id = org_id_from_url(row.get("cninfo_url", ""))
        if not org_id:
            continue
        by_code.setdefault(
            row["stock_code"],
            {"stock_code": row["stock_code"], "company_name": row["company_name"], "org_id": org_id},
        )
    return sorted(by_code.values(), key=lambda row: row["stock_code"])


def merge_rows(existing_rows: list[dict[str, str]], new_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_key: dict[tuple[str, str], dict[str, str]] = {}
    for row in existing_rows + new_rows:
        key = (row["stock_code"], row["report_year"])
        old = by_key.get(key)
        if old is None:
            by_key[key] = row
            continue
        # Keep revised/latest rows when duplicate company-year records exist.
        old_date = old.get("announcement_date", "")
        new_date = row.get("announcement_date", "")
        if new_date >= old_date:
            by_key[key] = row
    return sorted(by_key.values(), key=lambda row: (row["stock_code"], row["report_year"]))


def write_report(path: Path, rows: list[dict[str, str]], query_failures: list[dict[str, str]], target: int) -> None:
    year_counts = Counter(row["report_year"] for row in rows)
    companies = {row["stock_code"] for row in rows}
    downloaded = sum(1 for row in rows if row.get("download_status") == "success")
    lines = [
        "# Dataset Expansion To 150",
        "",
        "## Summary",
        f"- Target records: {target}",
        f"- Metadata records: {len(rows)}",
        f"- Companies: {len(companies)}",
        f"- Successful PDFs: {downloaded}",
        f"- Query failures: {len(query_failures)}",
        "",
        "## Year Distribution",
    ]
    for year, count in sorted(year_counts.items()):
        lines.append(f"- {year}: {count}")
    lines += [
        "",
        "## Notes",
        "- Source: CNINFO public annual-report announcements.",
        "- Query uses the public historical announcement endpoint and does not bypass login, captcha, or rate limits.",
        "- One record is kept for each company-year; when revised reports exist, the latest full annual report is preferred.",
    ]
    if query_failures:
        lines += ["", "## Query Failures"]
        for failure in query_failures[:50]:
            lines.append(f"- {failure['stock_code']} {failure['report_year']}: {failure['error_message']}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def run(args: argparse.Namespace) -> int:
    seed_path = ROOT / args.seed
    output_path = ROOT / args.output
    failed_path = ROOT / args.failed
    report_path = ROOT / args.report
    pdf_dir = ROOT / args.pdf_dir
    pdf_dir.mkdir(parents=True, exist_ok=True)

    seed_rows = read_csv(seed_path)
    companies = load_companies(seed_rows)
    new_rows: list[dict[str, str]] = []
    failures: list[dict[str, str]] = []

    if args.download_only:
        rows = seed_rows
    else:
        years = [int(year) for year in args.years.split(",") if year.strip()]
        existing_doc_ids = {row["doc_id"] for row in seed_rows}
        for company in companies:
            for report_year in years:
                if any(row["stock_code"] == company["stock_code"] and row["report_year"] == str(report_year) for row in seed_rows):
                    continue
                try:
                    items = query_company_year(company["stock_code"], company["org_id"], report_year, args.sleep)
                    item = select_annual_report(items, report_year)
                    if item is None:
                        failures.append(
                            {
                                "stock_code": company["stock_code"],
                                "company_name": company["company_name"],
                                "report_year": str(report_year),
                                "error_message": "annual report not found",
                            }
                        )
                        continue
                    row = metadata_row(company, report_year, item, pdf_dir)
                    if row["doc_id"] not in existing_doc_ids:
                        new_rows.append(row)
                except Exception as exc:
                    failures.append(
                        {
                            "stock_code": company["stock_code"],
                            "company_name": company["company_name"],
                            "report_year": str(report_year),
                            "error_message": str(exc),
                        }
                    )

        rows = merge_rows(seed_rows, new_rows)

    download_failures: list[dict[str, str]] = []
    if args.download:
        for row in rows:
            pdf_path = ROOT / row["local_pdf_path"]
            status = "success"
            error_message = ""
            try:
                if not pdf_path.exists() or pdf_path.stat().st_size <= 0:
                    download_pdf(row["pdf_url"], pdf_path)
                    time.sleep(args.download_sleep)
                if not pdf_path.exists() or pdf_path.stat().st_size <= 0:
                    raise RuntimeError("downloaded file missing or empty")
            except Exception as exc:
                status = "failed"
                error_message = str(exc)
                download_failures.append({**row, "error_message": error_message})
            row["download_status"] = status
            row["error_message"] = error_message

    fieldnames = [
        "doc_id",
        "company_name",
        "stock_code",
        "report_year",
        "announcement_title",
        "announcement_date",
        "cninfo_url",
        "pdf_url",
        "local_pdf_path",
        "is_revision",
        "download_status",
        "error_message",
    ]
    write_csv(output_path, rows, fieldnames)
    write_csv(failed_path, failures + download_failures, ["stock_code", "company_name", "report_year", "error_message"])
    write_report(report_path, rows, failures + download_failures, args.target)

    print(f"[expand] companies={len(companies)}")
    print(f"[expand] metadata_records={len(rows)}")
    print(f"[expand] new_records={len(new_rows)}")
    print(f"[expand] failures={len(failures) + len(download_failures)}")
    print(f"[expand] output={args.output}")
    return 0 if len(rows) >= args.target else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Expand CNINFO annual-report PDF metadata and optionally download PDFs.")
    parser.add_argument("--seed", default="metadata_2021_2023_pool107.csv")
    parser.add_argument("--years", default="2020,2024")
    parser.add_argument("--target", type=int, default=150)
    parser.add_argument("--output", default="metadata_2020_2024_pool150.csv")
    parser.add_argument("--failed", default="failed_expansion_to150.csv")
    parser.add_argument("--report", default="outputs/reports/dataset_expansion_to150.md")
    parser.add_argument("--pdf-dir", default="data/pdf")
    parser.add_argument("--sleep", type=float, default=1.0)
    parser.add_argument("--download-sleep", type=float, default=0.5)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--download-only", action="store_true", help="Skip CNINFO queries and download PDFs listed in --seed.")
    return run(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
