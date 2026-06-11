# Final Report Draft

## Project Title
房地产上市公司年报分红政策、经营现金流与流动性风险一致性分析

## Research Question
This project studies whether real-estate listed companies' dividend decisions are consistent with operating cash flow performance and liquidity-risk disclosure in annual reports.

## Data
- Source: CNINFO public annual-report announcements.
- Current executable sample: 37 parsed 2023 annual reports.
- Expanded PDF pool: 37 downloaded 2023 annual reports.
- Parsing tool: MinerU API.

## Workflow
`metadata -> audit -> parse -> parse_check -> route -> extract -> validate -> report`

## Fields
- dividend policy
- cash dividend per 10 shares
- bonus share / capitalization transfer indicator
- parent-company net profit / attributable net profit field
- operating cash flow
- liquidity risk label
- evidence text
- consistency score

## Current Results
The 37-report parsed workflow runs end to end and produces validated structured results.

## Limitations
- Current extraction is still a rule baseline.
- Amount unit normalization needs further improvement.
- Evidence page numbers are approximate.
- Manual evaluation labels still need to be completed.

## Next Improvements
- Fill human evaluation labels for at least 25 PDFs; full-sample evaluation covers 37 PDFs.
- Use LLM extraction only after section routing quality is stable.
