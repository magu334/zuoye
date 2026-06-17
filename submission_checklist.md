# Final Submission Checklist

## Required Files
| Requirement | Current File | Status |
|---|---|---|
| GitHub public repository URL | to be filled by team | Pending |
| README.md | `README.md` | Done |
| requirements.txt | `requirements.txt` | Done |
| .env.example | `.env.example` | Done |
| configs/ | `configs/` | Done |
| pipeline_run.py or run.py | `pipeline_run.py` | Done |
| src/ | `src/` | Done |
| metadata | `data/metadata/metadata.csv` | Done |
| expanded 150+ metadata | `metadata_2020_2024_pool150.csv` | Done |
| expanded 150+ PDF pool | metadata + download script | Done; PDF originals are intentionally not committed |
| parsed sample data | `data/parsed/parsed_docs_sample.jsonl` | Done |
| section sample data | `data/parsed/sections_sample.jsonl` | Done |
| sample run log | `outputs/logs/sample_run_log.jsonl` | Done |
| final results | `outputs/results/final_results.csv` | Done, 175 rows |
| quantitative scored results | `outputs/results/quantitative_scored_records.csv` | Done, 175 rows |
| cross-year matching events | `outputs/analysis/cross_year_matching_events.csv` | Done, 342 rows |
| attention review list | `outputs/analysis/attention_review_list.csv` | Done, 27 rows |
| 1.1 upgrade report | `outputs/reports/challenge_1_1_upgrade_report.md` | Done |
| full PDF extraction report | `outputs/reports/full_pdf_extraction_report.md` | Done |
| final evaluation report | `outputs/reports/eval_report_final.md` | Done |
| final report | `final_report.md` | Done |
| demo script | `demo_script.md` | Done |
| final slides | `final_slides.pdf`, `final_slides.pptx` | Pending export |
| AI usage statement | `ai_usage_statement.md` | Done |
| AI worklog | `ai_worklog_all.md` | Done |

## Self Check
- [x] Metadata can trace records back to CNINFO announcements.
- [x] 175 PDFs have been downloaded locally for the challenge-track data pool.
- [x] The 175 records have been parsed, extracted, validated, normalized, and scored.
- [x] Original PDF files are excluded from Git; metadata and download script are committed instead.
- [x] Full parsed text caches are excluded from Git; parsed and section samples are committed instead.
- [x] Pydantic schema exists in `schemas.py`.
- [x] Section check report exists.
- [x] Final results contain quantitative scoring fields.
- [x] Human evaluation template exists.
- [x] Run log exists.
- [x] README contains reproduction commands.
- [x] `.env.example` contains placeholders only.
- [ ] GitHub repository has been made public.
- [ ] `final_slides.pdf` has been exported.
