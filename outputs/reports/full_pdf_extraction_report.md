# Full PDF Extraction Report

## Summary
- Target PDF pool: 175 annual reports.
- Parsed records: 175.
- Routed sections: 525.
- Extracted records: 175.
- Validated records: 175.
- Validation errors: 0.
- Unit-normalized records: 175.
- Quantitative scored records: 175.
- Attention review records: 27.
- Cross-year matching events: 342.

## Parser Split
- MinerU markdown: 0.
- `pypdf_text_fallback`: 175.

The parser is designed to use MinerU markdown first when it exists for a `doc_id`. Because the repository did not contain a complete MinerU markdown batch for the 175 PDF pool, the latest run used local PDF text extraction for all records.

## Latest Command

```bash
python pipeline_run.py --config configs/workflow.yaml --step all
```

## Latest Run Log

```text
[audit] dataset report=outputs/reports/dataset_check_report.md
[parse] parsed docs=175, mineru=0, pdf_text_fallback=175
[parse_check] checked docs=175
[route] sections=525
[extract] extract records=175
[validate] valid=175, errors=0
[analysis] scored_records=175
[analysis] flagged_records=27
[analysis] cross_year_events=342
[analysis] report=outputs/reports/quantitative_attention_report.md
[report] summary report=outputs/reports/summary_report.md
```

## Field Completeness
- `parent_net_profit`: 175/175.
- `operating_cash_flow`: 175/175.
- `parent_net_profit_cny`: 175/175.
- `operating_cash_flow_cny`: 175/175.
- `unit_confidence = high`: 175/175.

## Git Upload Note
The generated full parsed text cache is intentionally excluded from Git:

- `data/pdf/`
- `data/parsed/pdf_text/`
- `data/parsed/parsed_docs.jsonl`
- `data/parsed/sections.jsonl`

The repository keeps metadata, scripts, sample parsed text, sample sections, structured outputs, analysis tables, and reports.
