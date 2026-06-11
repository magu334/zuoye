# Optimization Log

## 2026-06-08
- Problem: Initial workflow only covered 8 annual reports.
- Diagnosis: PDF collection was incomplete for standard difficulty; MinerU parsing was the bottleneck.
- Change: Built a 20-company 2023 real-estate annual-report pool and downloaded all 20 PDFs.
- Result: `data/metadata/metadata_2023_pool20.csv` contains 20 records; failed downloads are 0.

## 2026-06-08
- Problem: Section routing sometimes hit directory, definition, or unrelated front-matter text.
- Diagnosis: Keyword matching was too broad and did not distinguish routing from checking.
- Change: Added stronger section rules, exclude terms, minimum line positions, and section check reports.
- Result: The 8-report workflow still runs end to end with 8 validated records.

## 2026-06-08
- Problem: LLM extraction quality depended heavily on section quality.
- Diagnosis: DeepSeek-V4-Pro returned valid JSON, but wrong sections could still produce weak evidence.
- Change: Tested LLM extraction on a small sample after routing improvements.
- Result: Small LLM sample passed Pydantic validation, but bulk extraction should wait for better section checks.

## 2026-06-10
- Problem: Week 15 requires evaluation, project rules, prompts, and final reproducibility materials.
- Diagnosis: The workflow runs, but final repo materials were incomplete.
- Change: Added AGENTS.md, prompt templates, evaluation/report skeletons, and secret-protection `.gitignore`.
- Result: The project is closer to Week 15 deliverable shape; manual evaluation still needs human labels.

## 2026-06-10
- Problem: The parsed/evaluable sample count was below the Week 15 standard-difficulty evaluation recommendation.
- Diagnosis: PDF collection had reached 20 reports, but only 8 had MinerU markdown at the start of the expansion step.
- Change: Re-polled previous MinerU batches, retried failed reports, fixed the PDF split selector, standardized returned markdown filenames, and created `workflow_parsed20.yaml`.
- Result: 20 reports now have MinerU markdown and the workflow runs end to end with 20 validated records and 0 Pydantic validation errors.

## 2026-06-10
- Problem: The course difficulty table recommends at least 30-60 PDFs for the basic data-volume band, while the current parsed sample was still below that threshold.
- Diagnosis: The workflow was stable, but the data pool needed expansion and additional MinerU parsing.
- Change: Expanded the CNINFO 2023 real-estate annual-report PDF pool to 37 reports, parsed all 37 with MinerU, and created `workflow_parsed37.yaml`.
- Result: The full 37-report workflow runs end to end with 37 parsed docs, 111 routed sections, 37 validated records, and 0 Pydantic validation errors. The manual evaluation template now contains 222 rows.
