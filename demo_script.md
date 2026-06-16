# Demo Script

## 3-Minute Demo Flow

### 1. Research Question

Show the project title:

`Real-estate listed companies: dividend policy, operating cash flow, and liquidity-risk consistency in annual reports`

Explain in one sentence:

We use public CNINFO annual reports to check whether real-estate companies' dividend decisions are consistent with operating cash flow, profitability pressure, and liquidity-risk disclosure.

### 2. Difficulty Claim

Show `difficulty_declaration.md`.

Say:

The upgraded project applies for challenge track 1.1. It now has 175 downloaded CNINFO annual-report PDFs, exceeding the 150+ PDF threshold. The structured 81-record workflow also produces 54 same-company cross-year matching events.

### 3. Data Provenance

Open `metadata_2020_2024_pool150.csv` and one row from the final result.

Point to:

- `doc_id`
- `stock_code`
- `stock_name`
- `report_year`
- `cninfo_url`
- `pdf_url`
- `local_pdf_path`

Say:

`doc_id` is the primary key across metadata, PDF, MinerU markdown, routed sections, extraction results, validation, scoring, and evaluation.

### 4. Workflow Command

Show:

```bash
python pipeline_run.py --config configs/workflow_parsed81.yaml --step all
```

Expected result:

```text
[validate] valid=81, errors=0
[report] summary report=outputs/reports/summary_report.md
[analysis] scored_records=81
[analysis] flagged_records=4
[analysis] cross_year_events=54
```

### 5. Evidence And Structured Results

Open:

- `extract_results.jsonl`
- `records_validated_unit_normalized.csv`
- `outputs/results/quantitative_scored_records.csv`

Explain:

- The original extraction keeps dividend, profit, cash-flow, risk evidence, and old screening labels.
- Unit normalization converts financial fields into comparable CNY columns.
- Quantitative scoring adds `liquidity_risk_score`, `liquidity_risk_quantile`, `attention_score`, and `attention_level`.

### 6. Cross-Year Matching

Open:

- `outputs/analysis/cross_year_matching_events.csv`

Explain one event row:

- Same company, two annual reports.
- Dividend change.
- Operating cash-flow change.
- Net-profit change.
- Liquidity-risk score change.
- Attention-score change.
- Event type.

### 7. Review List

Open:

- `outputs/analysis/attention_review_list.csv`

Say:

This is the final analyst review list. It is sorted by `attention_score`, a weighted 0-100 score, instead of relying only on subjective high/medium/low labels.

### 8. Expansion Status And Caveat

Open:

- `human_eval_template_81.csv`
- `human_eval_audit_summary.md`
- `expansion_status_pdf175.md`
- `outputs/reports/challenge_1_1_upgrade_report.md`

Say:

The earlier human audit showed that financial numeric fields are more stable than liquidity-risk evidence routing. The project now has 175 PDFs downloaded, while the structured scored workflow covers 81 parsed reports. The remaining PDFs should go through MinerU before they are included in field extraction and scoring.
