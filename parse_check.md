# Parse Check

## Summary
- Checked documents: 37
- Non-empty markdown: 37
- Garbled text detected: 0
- Dividend keywords found: 34
- Financial keywords found: 37
- Risk keywords found: 36

## Notes
- Parser is MinerU.
- Current markdown is generated from the first 200-page MinerU split for each annual report.
- Original PDF page numbers are not stably preserved in the current markdown, so page evidence is marked approximate.
- Table text is available in markdown HTML table form, but financial amount unit normalization still needs repair.

## Sample Inspection
| doc_id | stock_name | markdown_non_empty | dividend | financial | risk | needs_manual_fix |
|---|---|---:|---:|---:|---:|---|
| 1219487237 | 万科A | True | True | True | True | no |
| 1219740785 | 保利发展 | True | True | True | True | no |
| 1219330022 | 招商蛇口 | True | True | True | True | no |
| 1219307600 | 金地集团 | True | True | True | True | no |
| 1219860111 | 滨江集团 | True | True | True | True | no |
| 1219875404 | 华发股份 | True | True | True | True | no |
| 1219446608 | 新城控股 | True | True | True | True | no |
| 1219689383 | 首开股份 | True | True | True | True | no |
| 1222823303 | 陆家嘴 | True | True | True | True | no |
| 1219596576 | 上海临港 | True | True | True | True | no |
| 1219463872 | 张江高科 | True | True | True | True | no |
| 1219840458 | 外高桥 | True | True | True | True | no |
| 1219595758 | 城建发展 | True | True | True | True | no |
| 1219412328 | 信达地产 | True | True | True | True | no |
| 1219915446 | 栖霞建设 | True | True | True | True | no |
| 1219876783 | 苏州高新 | True | True | True | True | no |
| 1219493208 | 京投发展 | True | True | True | True | no |
| 1219468516 | 南山控股 | True | False | True | True | no |
| 1219469544 | 城投控股 | True | True | True | True | no |
| 1219865459 | 荣盛发展 | True | True | True | True | no |
| 1219488813 | 华侨城A | True | False | True | True | no |
| 1219863705 | 大悦城 | True | True | True | True | no |
| 1219517434 | 中交地产 | True | True | True | True | no |
| 1219865454 | 深振业A | True | True | True | True | no |
| 1219460432 | 沙河股份 | True | True | True | True | no |
| 1219769062 | 中洲控股 | True | False | True | True | no |
| 1219600830 | 粤宏远A | True | True | True | True | no |
| 1219824168 | 渝开发 | True | True | True | True | no |
| 1219997738 | 津滨发展 | True | True | True | True | no |
| 1219597689 | 中国武夷 | True | True | True | True | no |
| 1219445524 | 天保基建 | True | True | True | True | no |
| 1219854998 | 华远地产 | True | True | True | True | no |
| 1219622167 | 大名城 | True | True | True | True | no |
| 1219650634 | 中华企业 | True | True | True | True | no |
| 1219910873 | 电子城 | True | True | True | True | no |
| 1219583682 | 浦东金桥 | True | True | True | False | no |
| 1219907193 | 天地源 | True | True | True | True | no |