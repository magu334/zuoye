# Eval Report Final

## Current Evaluation Scope
- Current executable workflow sample: 37 parsed 2023 annual reports.
- Expanded PDF pool: 37 downloaded 2023 annual reports.
- Pending MinerU parse: 0.
- Current limitation: manual gold labels still need to be filled by the project team.

## Metrics To Report
| Metric | Current Status | Notes |
|---|---:|---|
| Data Quality | 37/37 PDFs downloaded | `metadata_2023_pdf37.csv` tracks the expanded PDF pool |
| Parse Quality | 37/37 parsed | MinerU markdown exists for all reports in the current PDF pool |
| Section Quality | needs manual review | `section_check_report.csv` exists but needs human labels |
| Extraction Quality | 37 validated records | rule baseline, not final accuracy |
| Evidence Quality | needs manual review | evidence text exists but page numbers are approximate |
| Pipeline Stability | 37-report workflow passes | end-to-end command runs on current parsed sample |

## Human Evaluation Plan
For standard difficulty, manually label at least 15-25 PDFs. The project now has 37 parsed PDFs, so the recommended evaluation target is at least 25 PDFs, with 37 PDFs as the stronger full-sample evaluation.

Human evaluation fields:

`doc_id,field_name,predicted_value,gold_value,is_correct,evidence_correct,error_type,notes`

The current evaluation template is `outputs/evaluation/human_eval_template.csv`. It contains 222 rows: 37 parsed reports x 6 evaluated fields. The `predicted_value` column has been filled from `outputs/results/records_validated.csv`; the project team should fill `gold_value`, `is_correct`, `evidence_correct`, `error_type`, and `notes`.

Allowed `error_type` values:

`data_error`, `parse_error`, `section_error`, `prompt_error`, `schema_error`, `hallucination`, `normalization_error`, `workflow_error`, `human_label_unclear`

## Known Error Risks
- Financial amounts may have unit ambiguity, especially 元 / 万元 / 亿元.
- Dividend extraction may confuse current-year proposal with prior-year implementation.
- Liquidity risk section may be broad and requires manual section checking.
- MinerU markdown currently keeps text but not stable original PDF page markers.

## Next Evaluation Step
Fill `outputs/evaluation/human_eval_template.csv` with manual gold labels for the current 37 parsed reports.
