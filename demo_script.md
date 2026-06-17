# Demo Script

## 3-Minute Demo Flow

### 1. Research Question
Show the project title:

`Real-estate listed companies: dividend policy, operating cash flow, and liquidity-risk consistency in annual reports`

Say:

We use public CNINFO annual reports to check whether real-estate companies' dividend decisions are consistent with operating cash flow, profitability pressure, and liquidity-risk disclosure.

### 2. Difficulty Claim
Open `difficulty_declaration.md`.

Say:

The upgraded project applies for challenge track 1.1. It has 175 CNINFO annual-report PDFs and 175 structured scored records, exceeding the 150+ PDF threshold. It also produces 342 same-company cross-year matching events, exceeding the 50+ multi-document event threshold.

### 3. Data Provenance
Open `data/metadata/metadata.csv` and one row from `outputs/results/final_results.csv`.

Point to:

- `doc_id`
- `stock_code`
- `stock_name`
- `report_year`
- `cninfo_url`
- `pdf_url`
- `local_pdf_path`

Say:

`doc_id` is the primary key across metadata, local PDF, parsed text, routed sections, extraction results, validation, scoring, and evaluation.

### 4. Workflow Command
Show:

```bash
python pipeline_run.py --config configs/workflow.yaml --step all
```

Expected result:

```text
[parse] parsed docs=175, mineru=0, pdf_text_fallback=175
[validate] valid=175, errors=0
[analysis] scored_records=175
[analysis] flagged_records=27
[analysis] cross_year_events=342
```

Say:

The parser prefers MinerU markdown when available. In the current full run, MinerU markdown was absent for the full pool, so the project used reproducible local PDF text fallback for all 175 PDFs.

### 5. Evidence And Structured Results
Open:

- `outputs/results/extract_results.jsonl`
- `outputs/results/records_validated_unit_normalized.csv`
- `outputs/results/quantitative_scored_records.csv`

Explain:

- The original extraction keeps dividend, profit, cash-flow, risk evidence, and old screening labels.
- Unit normalization converts financial fields into comparable CNY columns.
- Quantitative scoring adds `liquidity_risk_score`, `liquidity_risk_quantile`, `base_attention_score`, `cross_year_pressure_score`, final `attention_score`, and `attention_level`.

### 6. Cross-Year Matching
Open:

- `outputs/analysis/cross_year_matching_events.csv`

Explain one event row:

- Same company, two annual reports.
- Dividend change.
- Operating cash-flow change.
- Net-profit change.
- Liquidity-risk score change.
- Base-attention-score change.
- Cross-year pressure score.
- Final attention-score change.
- Event type.

### 7. Review List
Open:

- `outputs/analysis/attention_review_list.csv`

Say:

This is the final analyst review list. It contains 27 records and is sorted by final `attention_score`, which combines single-year pressure and same-company cross-year deterioration signals. It no longer relies only on subjective high/medium/low labels.

### 8. Evaluation And Caveat
Open:

- `outputs/reports/eval_report_final.md`
- `outputs/reports/challenge_1_1_upgrade_report.md`
- `outputs/reports/quantitative_attention_report.md`

Say:

The project now completes the full 175-record workflow. The key caveat is that this is a rule baseline from parsed PDF text, so high-attention records should still be manually checked against the original annual report before being used as financial conclusions.
