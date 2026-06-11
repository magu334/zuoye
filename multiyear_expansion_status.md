# Multiyear Expansion Status

## Current Status

- Existing completed workflow sample: 37 parsed 2023 annual reports.
- Expanded metadata pool: 107 annual reports from 2021-2023.
- Downloaded PDFs: 107/107.
- Failed downloads: 0.
- New 2021/2022 reports found from CNINFO: 70.
- New reports needed to reach 80 parsed samples: 43.
- Current parsed reports in the 107-PDF pool: 37.
- Current unparsed reports in the 107-PDF pool: 70.

## Year Coverage

| report_year | records |
|---|---:|
| 2021 | 35 |
| 2022 | 35 |
| 2023 | 37 |

## Files Created

- `outputs/real_estate_multiyear_availability.csv`
- `outputs/reports/multiyear_80_feasibility.md`
- `data/metadata/metadata_2021_2023_pool107.csv`
- `outputs/logs/failed_downloads_2021_2023_pool107.csv`
- `outputs/reports/dataset_expansion_2021_2023.md`

## MinerU Status

The first new 10-report MinerU batch has been submitted:

- batch_id: `c4c99903-1686-4ca6-8aec-b070e48272e5`
- current state: all 10 files are still `pending` as of the latest poll
- likely reason: MinerU queue or daily priority-page limit

No new 2021/2022 Markdown files have been added yet from this batch.

Additional small-batch upload attempts also stalled before writing a new batch log, so the immediate bottleneck appears to be MinerU upload/queue availability rather than local metadata or PDF download.

## Next Step

Wait and re-poll the MinerU batch. If it moves from `pending` to `running` or `done`, download the Markdown results, sync them into `data/parsed/markdown/`, and rebuild parsed metadata.

Do not submit many more batches while this batch is pending, because that may only increase queue backlog. The practical next action is to wait for this batch to start or complete, or check the MinerU dashboard for queue/page-limit information.

## Difficulty Implication

The project now has enough CNINFO PDF data to support the standard 80-PDF threshold once MinerU parsing catches up. However, the executable workflow sample is still 37 parsed PDFs until the 2021/2022 MinerU Markdown files are completed.
