# Real Estate Dividend, Cash Flow, and Liquidity Risk Project

## Project Goal
This project analyzes whether A-share real-estate listed companies' dividend policies are consistent with operating cash flow and liquidity-risk disclosure in annual reports.

## Data Source
The main data source is public annual-report announcements from CNINFO. Each document is tracked by `doc_id`, announcement URL, PDF URL, and local PDF path.

## Directory Structure
- `configs/`: workflow and section-routing configuration.
- `data/metadata/`: metadata CSV files.
- `data/pdf/`: downloaded CNINFO PDF files.
- `data/parsed/`: MinerU markdown, parsed documents, and routed sections.
- `src/`: workflow, parsing, routing, extraction, validation, and reporting scripts.
- `outputs/`: logs, reports, results, and proposal materials.
- `prompts/`: extraction prompt templates.
- `work/`: temporary working files for MinerU batching and PDF splitting.

## Setup
```bash
python -m pip install -r requirements.txt
```

Create a local `.env` from `.env.example` and fill real keys locally only. Do not commit `.env`.

## Minimal Run
```bash
python src/pipeline_run.py --config configs/workflow.yaml --step all --limit 3
```

## Full Current Sample Run
```bash
python src/pipeline_run.py --config configs/workflow_parsed37.yaml --step all
```

## Dataset Status
- PDF pool: 37 CNINFO 2023 annual-report PDFs have been downloaded and tracked in `data/metadata/metadata_2023_pdf37.csv`.
- Executable parsed sample: all 37 reports currently have MinerU Markdown and can run through the full workflow.
- Pending parse sample: 0.
- Current difficulty positioning: the 37 parsed PDFs satisfy the basic-difficulty data-volume band. The workflow, field design, section checking, evidence handling, and evaluation plan remain the current standard-track prototype. A full standard-track data-volume claim would require expanding parsed PDFs toward 80+ reports or adding multi-year/multi-document matching.

## Outputs
- `outputs/logs/run_log.jsonl`: workflow logs.
- `data/parsed/parsed_docs.jsonl`: unified parsed-document input.
- `data/parsed/sections.jsonl`: routed target sections.
- `outputs/results/extract_results.jsonl`: structured extraction results.
- `outputs/results/records_validated.csv`: validated CSV output.
- `outputs/reports/summary_report.md`: summary report.
- `outputs/evaluation/human_eval_template.csv`: manual evaluation template for the 37 parsed reports.

## Current Status
- 37 CNINFO 2023 annual-report PDFs downloaded.
- 37 reports have MinerU markdown and can run through the workflow.
- Latest run: 37 parsed docs, 111 routed sections, 37 extracted records, 37 valid records, 0 validation errors.
- Manual evaluation labels still need to be completed for Week 15.
