# Demo Script

## 3-Minute Demo Flow

1. Show the research question:
   - 房地产上市公司年报分红政策、经营现金流与流动性风险是否一致。

2. Show data provenance:
   - Open `data/metadata/metadata.csv`.
   - Point to `doc_id`, `cninfo_url`, `pdf_url`, and `local_pdf_path`.

3. Show one PDF and parsed markdown:
   - Open one file under `data/pdf/`.
   - Open the matching file under `data/parsed/markdown/`.

4. Run the workflow:

```bash
python src/pipeline_run.py --config configs/workflow.yaml --step all --limit 3
```

For the full parsed sample:

```bash
python src/pipeline_run.py --config configs/workflow_parsed37.yaml --step all
```

5. Show intermediate evidence:
   - `data/parsed/parsed_docs.jsonl`
   - `data/parsed/sections.jsonl`
   - `outputs/reports/section_check_report.csv`

6. Show structured results:
   - `outputs/results/extract_results.jsonl`
   - `outputs/results/records_validated.csv`

7. Show evaluation and known failure:
   - Explain one likely section or normalization error.
   - Show `eval_report_final.md` and `optimization_log.md`.

## Backup Demo Command

```bash
python src/pipeline_run.py --config configs/workflow.yaml --step validate
```
