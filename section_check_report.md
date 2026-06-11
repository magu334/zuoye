# Section Check Report

## Purpose

This report records whether automatic section routing found useful candidate text for the project fields:

- dividend policy
- major financial indicators
- liquidity / financing risk

The CSV version is `outputs/reports/section_check_report.csv`.

## Current Rule

Sections are routed by keyword rules in `configs/section_rules.yaml`.

## Quality Issue Labels

- `ok`: candidate section found and long enough for extraction.
- `not_found`: no keyword hit.
- `too_short`: keyword hit exists but candidate text is too short.
- `wrong_section`: reserved for manual review when the section is not actually relevant.
- `toc_hit`: reserved for manual review when the section comes from table of contents.

## Manual Review Columns

The current CSV includes:

- `human_check_status`: default `pending`
- `review_notes`: blank by default

These fields should be filled after manually checking several routed sections against the original annual report PDF and MinerU markdown.

## Known Risks

- Dividend extraction may accidentally hit historical dividend implementation sections.
- Risk keywords may hit general industry discussion rather than company-specific liquidity pressure.
- Financial tables may use different units, so section routing alone cannot solve amount normalization.
