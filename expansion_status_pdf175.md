# Expansion Status: 175 PDF Pool

## Summary

- Target: 150+ annual-report PDFs.
- Current metadata records: 175.
- Current downloaded PDFs: 175.
- Failed downloads: 0.
- Companies: 37.
- Year coverage: 2020-2024.
- Metadata file: `metadata_2020_2024_pool150.csv`.
- Expansion report: `outputs/reports/dataset_expansion_to150.md`.

## Year Distribution

- 2020: 33 reports
- 2021: 35 reports
- 2022: 35 reports
- 2023: 37 reports
- 2024: 35 reports

## Current Workflow Split

- PDF data pool: 175 downloaded CNINFO annual reports.
- Structured parsed/scored sample: 81 annual reports.
- Cross-year matching events in structured sample: 54.

The next expansion step is to parse the additional PDFs with MinerU, then rerun section routing, extraction, validation, unit normalization, and quantitative scoring on the full 175-PDF pool.

## Reproducible Expansion Commands

```bash
python expand_cninfo_annual_reports.py --years 2020,2024 --sleep 0.2
python expand_cninfo_annual_reports.py --seed metadata_2020_2024_pool150.csv --output metadata_2020_2024_pool150.csv --failed failed_downloads_to150.csv --report outputs/reports/dataset_expansion_to150.md --download-only --download --download-sleep 0.2
```

Latest result:

```text
[expand] metadata_records=175
[expand] failures=0
```
