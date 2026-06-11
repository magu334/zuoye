# Pool20 Download And Parse Status

## Summary
- Company pool size: 20
- Target report year: 2023
- Downloaded PDFs: 20
- Failed downloads: 0
- MinerU markdown available: 20
- Workflow parsed records: 20
- Validation errors: 0

## Current Assessment
- The 2023 real-estate annual-report pool has been expanded from 8 to 20 local PDFs.
- `data/metadata/metadata_2023_pool20.csv` is the complete 20-PDF metadata file.
- `data/metadata/metadata_2023_parsed20.csv` is the executable 20-report parsed metadata file.
- All 20 reports now have standardized MinerU markdown under `data/parsed/markdown/`.
- The 20-report workflow has run end to end.

## Parsed Report Pool
| Company | Stock Code | doc_id | Markdown |
|---|---|---|---|
| 万科A | 000002 | 1219487237 | `data/parsed/markdown/doc_1219487237_pages_001_200.md` |
| 保利发展 | 600048 | 1219740785 | `data/parsed/markdown/doc_1219740785_pages_001_200.md` |
| 招商蛇口 | 001979 | 1219330022 | `data/parsed/markdown/doc_1219330022_pages_001_200.md` |
| 金地集团 | 600383 | 1219307600 | `data/parsed/markdown/doc_1219307600_pages_001_200.md` |
| 滨江集团 | 002244 | 1219860111 | `data/parsed/markdown/doc_1219860111_pages_001_200.md` |
| 华发股份 | 600325 | 1219875404 | `data/parsed/markdown/doc_1219875404_pages_001_200.md` |
| 新城控股 | 601155 | 1219446608 | `data/parsed/markdown/doc_1219446608_pages_001_200.md` |
| 首开股份 | 600376 | 1219689383 | `data/parsed/markdown/doc_1219689383_pages_001_200.md` |
| 陆家嘴 | 600663 | 1222823303 | `data/parsed/markdown/doc_1222823303_pages_001_200.md` |
| 上海临港 | 600848 | 1219596576 | `data/parsed/markdown/doc_1219596576_pages_001_200.md` |
| 张江高科 | 600895 | 1219463872 | `data/parsed/markdown/doc_1219463872_pages_001_198.md` |
| 外高桥 | 600648 | 1219840458 | `data/parsed/markdown/doc_1219840458_pages_001_200.md` |
| 城建发展 | 600266 | 1219595758 | `data/parsed/markdown/doc_1219595758_pages_001_200.md` |
| 信达地产 | 600657 | 1219412328 | `data/parsed/markdown/doc_1219412328_pages_001_200.md` |
| 栖霞建设 | 600533 | 1219915446 | `data/parsed/markdown/doc_1219915446_pages_001_178.md` |
| 苏州高新 | 600736 | 1219876783 | `data/parsed/markdown/doc_1219876783_pages_001_200.md` |
| 京投发展 | 600683 | 1219493208 | `data/parsed/markdown/doc_1219493208_pages_001_200.md` |
| 南山控股 | 002314 | 1219468516 | `data/parsed/markdown/doc_1219468516_pages_001_200.md` |
| 城投控股 | 600649 | 1219469544 | `data/parsed/markdown/doc_1219469544_pages_001_200.md` |
| 荣盛发展 | 002146 | 1219865459 | `data/parsed/markdown/doc_1219865459_pages_001_200.md` |

## Verification Command
```bash
python src/pipeline_run.py --config configs/workflow_parsed20.yaml --step all
```
