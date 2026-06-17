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

## Current Workflow Status

- PDF data pool: 175 downloaded CNINFO annual reports.
- Structured parsed/scored sample: 175 annual reports.
- Routed sections: 525.
- Validated records: 175.
- Unit-normalized records: 175.
- Attention review records: 27.
- Cross-year matching events: 342.

Latest full workflow:

```bash
python pipeline_run.py --config configs/workflow.yaml --step all
```

Latest result:

```text
[parse] parsed docs=175, mineru=0, pdf_text_fallback=175
[validate] valid=175, errors=0
[analysis] scored_records=175
[analysis] flagged_records=27
[analysis] cross_year_events=342
```

## Parser Note

The full 175-record run used `pypdf_text_fallback` because complete MinerU markdown was not available in the repository. `parse_docs.py` still prefers MinerU markdown when matching files exist.

## Reproducible Expansion Commands

```bash
python expand_cninfo_annual_reports.py --years 2020,2024 --sleep 0.2
python expand_cninfo_annual_reports.py --seed metadata_2020_2024_pool150.csv --output metadata_2020_2024_pool150.csv --failed failed_downloads_to150.csv --report outputs/reports/dataset_expansion_to150.md --download-only --download --download-sleep 0.2
```

Expansion result:

```text
[expand] metadata_records=175
[expand] failures=0
```
