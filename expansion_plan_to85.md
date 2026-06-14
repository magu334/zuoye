# Expansion Plan To 80 Parsed Samples

## Current Target
- Target sample count: 85
- Already parsed within target: 43
- Pending MinerU parse within target: 42
- Queue file: outputs\reports\expansion_queue_to85.csv

## Year Distribution In Target Queue
- 2021: 13
- 2022: 35
- 2023: 37

## Pending MinerU Batches
- Batch 1, count=10, doc_ids=1216492720,1216169340,1216276910,1216663767,1216702482,1216280228,1216235519,1216273292,1216402029,1216690726
- Batch 2, count=10, doc_ids=1216269818,1216402918,1216655440,1216741112,1216705586,1216277657,1216094888,1216389638,1216273938,1216298501
- Batch 3, count=10, doc_ids=1216245554,1216221769,1216299891,1216411318,1216166724,1216380526,1216259939,1216358368,1216380219,1212964021
- Batch 4, count=10, doc_ids=1213249284,1212942161,1212687124,1213255431,1212886659,1212974325,1212857761,1212757289,1212974730,1213086449
- Batch 5, count=2, doc_ids=1213001265,1212897448

## How To Run
1. Put a valid MinerU bearer token in .env as MINERU_API_KEY.
2. Submit each pending batch with work/submit_mineru_splits_no_wait.ps1.
3. Download each finished batch with work/download_mineru_batch_results.ps1.
4. Normalize downloaded markdown names to data/parsed/markdown/doc_<doc_id>_pages_001_*.md.
5. Rebuild metadata and run the workflow.
