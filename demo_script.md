# Demo Script

## 3-Minute Demo Flow

### 1. Research Question
Show the project title:

`房地产上市公司年报分红政策、经营现金流与流动性风险一致性分析`

Explain in one sentence:

We use CNINFO annual reports to check whether real-estate companies' dividend decisions are consistent with operating cash flow, profitability pressure, and liquidity-risk disclosure.

### 2. Data Provenance
Open `data/metadata/metadata.csv`.

Point to:
- `doc_id`
- `stock_code`
- `stock_name`
- `title`
- `cninfo_url`
- `pdf_url`
- `local_pdf_path`

Say: `doc_id` is the primary key across metadata, PDF, MinerU markdown, routed sections, extraction results, validation, and evaluation.

### 3. PDF To Parsed Text
Open one sample PDF under `data/pdf/`.

Then open the matching MinerU markdown under `data/parsed/markdown/`.

Say: the project does not extract directly from a spreadsheet; it first parses real CNINFO PDF annual reports into markdown and unified JSONL.

### 4. Workflow Command
Show the full workflow command:

```bash
python pipeline_run.py --config configs/workflow_parsed81.yaml --step all
```

Expected result:

```text
[parse] parsed docs=81
[parse_check] checked docs=81
[route] sections=243
[extract] extract records=81
[validate] valid=81, errors=0
```

### 5. Intermediate Evidence
Open:
- `data/parsed/parsed_docs.jsonl`
- `data/parsed/sections.jsonl`
- `outputs/reports/section_check_report.csv`

Explain the difference:
- Routing means the program finds candidate sections.
- Checking means humans inspect whether those sections are actually correct.

### 6. Structured Results
Open:
- `outputs/results/final_results.csv`
- `outputs/analysis/flagged_review_list.csv`

Explain one result row:
- Whether the company paid cash dividends.
- Operating cash flow sign.
- Liquidity-risk label.
- Consistency score.
- Why it is or is not flagged for review.

### 7. Evaluation And Failure Case
Open:
- `outputs/evaluation/human_eval_template_81.csv`
- `outputs/reports/eval_report_final.md`

Say:

The earlier manual audit showed that financial numeric fields are more stable, while liquidity-risk evidence routing is the main error source. Therefore, the final output is used as an analyst screening list, not as unchecked truth.

### 8. Closing
Final sentence:

This project demonstrates a complete evidence chain from CNINFO PDF to MinerU markdown, routed sections, structured extraction, Pydantic validation, human evaluation, and a reusable review list.
