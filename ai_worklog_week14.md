# AI Worklog Week 14

## Task

Build a minimal end-to-end workflow for the project "房地产上市公司年报分红政策、经营现金流与流动性风险一致性分析".

## Student Specification

- Use the existing 8 real estate annual report samples from CNInfo.
- Keep the standard course workflow shape: metadata -> audit -> parse -> route -> extract -> validate -> report.
- Generate logs and outputs for each step.
- Support single-step runs and `--step all`.
- Support `--limit` for small sample demo.
- Do not put real API keys in code or `.env.example`.

## AI Assistance

Codex helped create:

- `workflow_design.md`
- `workflow_graph.md`
- `configs/workflow.yaml`
- `configs/section_rules.yaml`
- `src/pipeline_run.py`
- `src/audit_dataset.py`
- `src/parse_docs.py`
- `src/route_sections.py`
- `src/extract_fields.py`
- `src/validate_results.py`
- `src/report_results.py`
- `src/schemas.py`

## Commands Run

```bash
python src/pipeline_run.py --help
python src/pipeline_run.py --config configs/workflow.yaml --step all --limit 3
python src/pipeline_run.py --config configs/workflow.yaml --step all --limit 8
```

In the Codex environment, the bundled Python executable was used because the plain `python` command was not on PATH.

## Verification

The 8-sample workflow completed successfully:

- audit: 8 records
- parse: 8 parsed docs
- route: 24 section records
- extract: 8 extraction records
- validate: 8 valid records, 0 validation errors
- report: summary report generated

Generated outputs:

- `outputs/logs/run_log.jsonl`
- `data/parsed/parsed_docs.jsonl`
- `data/parsed/sections.jsonl`
- `outputs/reports/section_check_report.csv`
- `outputs/results/extract_results.jsonl`
- `outputs/results/records_validated.csv`
- `outputs/logs/validation_errors.jsonl`
- `outputs/reports/summary_report.md`

## Known Issues

- The current extraction is a rule baseline, not final LLM extraction.
- Financial amount units are not fully normalized.
- MinerU markdown keeps text but not stable original PDF page numbers, so `page_no` is currently approximate.
- Risk labels are keyword-based and need manual review.
- Some fields may be missed by rules, for example 金地集团的经营活动现金流净额.
- The current dataset has only 8 annual reports, enough for workflow demo but not enough for final standard difficulty 1.0.

## Next Repair Plan

1. Improve section rules to avoid directory hits and catch missing cash-flow sections.
2. Add amount unit normalization.
3. Add manual review columns to `section_check_report.csv`.
4. Expand sample to 20-40 PDFs for Week 13/14 compliance.
5. Later replace rule baseline with LLM extraction while keeping the same Pydantic schema.
