# Pool20 MinerU Batch Status

## Batch Submitted
- Batch ID: `efcfd0d1-1c96-437c-af0f-91a6a177faf2`
- Submit date: 2026-06-08
- Source: `work/upload_mineru_splits.ps1`
- Result polling script: `work/download_mineru_batch_results.ps1`

## Files Submitted
| Company | Stock Code | doc_id | Split file |
|---|---|---|---|
| 城建发展 | 600266 | 1219595758 | `work/data/pdf_splits/城建发展_2023_1219595758_pages_001_200.pdf` |
| 城投控股 | 600649 | 1219469544 | `work/data/pdf_splits/城投控股_2023_1219469544_pages_001_200.pdf` |
| 京投发展 | 600683 | 1219493208 | `work/data/pdf_splits/京投发展_2023_1219493208_pages_001_200.pdf` |
| 陆家嘴 | 600663 | 1222823303 | `work/data/pdf_splits/陆家嘴_2023_1222823303_pages_001_200.pdf` |

## Current Result
- MinerU accepted the batch and returned a valid `batch_id`.
- Repeated polling did not return `done` within the current waiting window.
- Current observed state for all four files remains `pending`.
- No new markdown files have been written into `work/data/mineru_markdown/` yet.

## Interpretation
- This is a queueing / completion-latency issue on the MinerU side, not a local PDF download failure.
- The four files should be treated as `submitted_pending`, not `not_started`.
- The remaining 8 pending files have not yet been submitted.

## Next Step
1. Re-poll batch `efcfd0d1-1c96-437c-af0f-91a6a177faf2` later and download any finished markdown.
2. Once markdown appears, copy the files into `data/parsed/markdown/`.
3. Update `parsed_docs.jsonl` on the expanded sample pool.
