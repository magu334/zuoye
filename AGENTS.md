# Agent Instructions for CNINFO Project

## Project Goal
This project extracts structured financial information from CNINFO annual report PDFs for A-share real-estate listed companies. The current research question is whether dividend policy is consistent with operating cash flow and liquidity risk disclosure.

## Data Rules
- Main data must come from public CNINFO announcements.
- Do not bypass login, captcha, rate limits, or access restrictions.
- Keep original PDFs unchanged.
- Preserve `doc_id` as the primary key across metadata, PDFs, parsed markdown, sections, extraction results, validation, and evaluation.

## Secret Rules
- Never write real API keys into code, README, reports, logs, screenshots, or committed files.
- Keep real keys only in local `.env`.
- Maintain `.env.example` with placeholders only.

## Coding Rules
- Prefer the existing workflow shape: audit -> parse -> parse_check -> route -> extract -> validate -> report.
- Every script should be runnable from the command line.
- All normal outputs should go under `outputs/`.
- Errors and failed records should go under `outputs/logs/`.
- After code changes, report the exact command used for verification.

## Extraction Rules
- Field values must come from the announcement text.
- Key fields need `evidence_text`.
- If a field is absent or uncertain, output `null` instead of guessing.
- Extraction results must pass Pydantic validation.
- Evidence must be traceable back to `sections.jsonl` or `parsed_docs.jsonl`.

## Evaluation Rules
- Do not show only successful examples.
- Maintain a human evaluation table with fixed `error_type` values.
- Classify errors by data, parse, section, prompt, schema, hallucination, normalization, workflow, or unclear human label.
