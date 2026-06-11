# LLM Test Report: DeepSeek-V4-Pro

## Test Setup

- Provider: SiliconFlow
- Model: DeepSeek-V4-Pro
- Method: `extract_fields.py --method llm`
- Input: routed sections from 3 real estate annual reports
- Temperature: 0
- Output format: JSON validated by `DividendCashflowLiquidityExtract`

## Result

- LLM extraction records: 3
- Pydantic valid records: 3
- Validation errors: 0
- Output saved as:
  - `outputs/results/extract_results_llm_sample.jsonl`
  - `outputs/results/records_validated_llm_sample.csv`

## Observations

1. The API key and model call worked.
2. DeepSeek-V4-Pro produced valid JSON for the tested records.
3. The model gave better evidence snippets than the rule baseline for dividend and financial fields.
4. Runtime was slow: 3 records took close to 3 minutes after prompt shortening.
5. The third sample exposed a section routing problem: the liquidity risk section for 招商蛇口 hit a financial indicator table area instead of a real liquidity/risk discussion section.

## Current Judgment

DeepSeek-V4-Pro can be used for high-quality sample extraction and final demonstration, but it may be too slow for large-batch extraction unless we reduce section length, improve routing, or use a faster model for bulk runs.

For this project, the next bottleneck is not the LLM. The next bottleneck is section routing quality.

## Next Steps

1. Improve `liquidity_risk` section routing to avoid financial tables and directory/definition areas.
2. Route risk sections using stronger headings such as `可能面对的风险`, `风险与机遇`, `融资情况`, `资金情况`, `流动性风险`.
3. Add `wrong_section` and `toc_hit` manual review labels in `section_check_report.csv`.
4. Re-run LLM extraction on 3-5 records after section routing is repaired.
5. Only after routing is stable, expand LLM extraction to 20-40 records.

## Update On June 8, 2026

- Section routing was improved for:
  - dividend front-matter priority
  - financial heading priority
  - liquidity risk routing with stronger heading preference and exclusion of table-of-contents style hits
- A second LLM validation run was completed on 2 records.
- Updated sample outputs:
  - `outputs/results/extract_results_llm_sample_v2.jsonl`
  - `outputs/results/records_validated_llm_sample_v2.csv`
- The second run passed validation with 2 valid records and 0 errors.
- Compared with the first run, the new sections gave cleaner financial evidence and better dividend extraction for 万科A.
