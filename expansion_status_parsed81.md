# Expansion Status: Parsed 81 Samples

## Summary
- Target: 80+ parsed annual reports
- Current parsed markdown files: 81
- Current validated records: 81
- Workflow config: `configs/workflow_parsed81.yaml`
- Metadata file: `data/metadata/metadata_2021_2023_parsed81.csv`
- Latest validated output: `outputs/results/records_validated.csv`
- Latest human evaluation template: `outputs/evaluation/human_eval_template_81.csv`

## Year Distribution
- 2021: 10 reports
- 2022: 34 reports
- 2023: 37 reports

## Latest Workflow Check
Command:

```text
python src/pipeline_run.py --config configs/workflow_parsed81.yaml --step all
```

Result:

```text
[parse] parsed docs=81
[parse_check] checked docs=81
[route] sections=243
[extract] extract records=81
[validate] valid=81, errors=0
```

## MinerU Expansion Notes
- The first 2022 sample was used as a small cross-year test and completed successfully.
- Additional batches were submitted after switching upload from PowerShell `Invoke-WebRequest` to `curl.exe --upload-file`.
- One MinerU zip from Batch 2 item 10 was repeatedly corrupted during download and was not included.
- Despite that failed item, the final parsed sample count reached 81, above the standard-file threshold of 80.

## Submission Safety
- `.env` is ignored by `.gitignore`.
- `.env.example` contains placeholders only.
- Real API tokens should not be uploaded to GitHub.
