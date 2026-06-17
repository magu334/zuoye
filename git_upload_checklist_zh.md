# GitHub 最终上传清单

本清单依据 `module_b_full.md` 中 Week 16 / 最终提交要求整理。最终提交必须是公开 GitHub 仓库链接，不能只提交压缩包或 PPT。

## 1. 必须上传的顶层文件

| 文件/目录 | 当前状态 | 作用 |
|---|---:|---|
| `README.md` | 已有 | 项目目标、目录结构、环境配置、运行命令、输出位置 |
| `requirements.txt` | 已有 | Python 依赖 |
| `.env.example` | 已有 | 环境变量模板，不包含真实 API Key |
| `.gitignore` | 已有 | 排除密钥、缓存和临时文件 |
| `pipeline_run.py` | 已有 | 统一工作流入口 |
| `final_report.md` | 已更新 | 最终报告，可替代 `final_report.pdf` |
| `demo_script.md` | 已有 | 展示讲稿 / Demo 脚本 |
| `ai_usage_statement.md` | 已有 | AI 使用说明 |
| `ai_worklog_all.md` | 已有 | AI 协作过程记录 |
| `difficulty_declaration.md` | 已有 | 1.1 档难度说明 |
| `optimization_log.md` | 已有 | 迭代优化记录 |
| `AGENTS.md` | 已有 | AI coding agent 使用规则 |
| `proposal_zh.md` | 已新增 | 中文 proposal |
| `ppt_project_steps_zh.md` | 已新增 | PPT 可用的项目步骤说明 |

## 2. 必须上传的配置与代码

| 文件/目录 | 当前状态 | 说明 |
|---|---:|---|
| `configs/` | 已补齐 | 按要求提交配置目录 |
| `configs/workflow.yaml` | 已补齐 | 完整 workflow 配置 |
| `configs/workflow_parsed81.yaml` | 已补齐 | 当前 81 条已解析样本的可复现 workflow |
| `configs/crawl_config.yaml` | 已补齐 | 巨潮样本扩展配置 |
| `configs/model_config.yaml` | 已补齐 | LLM/API 配置模板 |
| `configs/section_rules.yaml` | 已补齐 | Section routing 规则 |
| `src/` | 已有 | 工作流辅助模块 |
| `schemas.py` | 已有 | Pydantic Schema |
| `parse_docs.py` | 已有 | PDF 解析结果整理 |
| `route_sections.py` | 已有 | 章节定位 |
| `extract_fields.py` | 已有 | 字段抽取 |
| `validate_results.py` | 已有 | 结果校验 |
| `normalize_units.py` | 已有 | 金额单位归一化 |
| `quantitative_attention_analysis.py` | 已新增 | 流动性风险量化与关注清单生成 |
| `expand_cninfo_annual_reports.py` | 已新增 | 175 份 PDF 样本池扩展脚本 |
| `audit_dataset.py` / `parse_check.py` / `report_results.py` | 已有 | 数据检查、解析检查、报告生成 |

## 3. 必须上传的数据与样本

| 文件/目录 | 当前状态 | 说明 |
|---|---:|---|
| `data/metadata/metadata.csv` | 已补齐 | 175 份巨潮年报 PDF 的标准 metadata |
| `data/metadata.csv` | 已补齐 | 兼容要求文件中早期写法 `data/metadata.csv` |
| `data/metadata/metadata_2021_2023_parsed81.csv` | 已补齐 | 81 条已解析/已评分样本 metadata |
| `data/parsed/parsed_docs_sample.jsonl` | 已补齐 | 解析文本样本，满足“可检查样本数据”要求 |
| `data/parsed/sections_sample.jsonl` | 已补齐 | Section routing 样本 |
| `data/pdf/` | 已有 175 份 | 原始 PDF 池，总大小约 849 MB |
| `metadata_2020_2024_pool150.csv` | 已有 | 175 份 PDF 池的根目录备份 |
| `failed_downloads_to150.csv` | 已有 | 下载失败记录，当前无失败 |

PDF 上传策略：

- 如果 GitHub 仓库体积允许，可以上传 `data/pdf/` 下 175 份 PDF。
- 如果仓库过大，按要求文件允许“保留样本并提供下载脚本与说明”：至少上传若干可检查 PDF 样本、`data/metadata/metadata.csv`、`expand_cninfo_annual_reports.py`、`outputs/reports/dataset_expansion_to150.md`。
- 不管是否上传完整 PDF，`metadata.csv`、解析样本和下载/扩展脚本必须上传。

## 4. 必须上传的输出文件

| 文件/目录 | 当前状态 | 说明 |
|---|---:|---|
| `outputs/logs/sample_run_log.jsonl` | 已补齐 | 要求明确点名的示例运行日志 |
| `outputs/logs/run_log.jsonl` | 已有 | 当前 workflow 日志 |
| `outputs/logs/validation_errors.jsonl` | 已有 | 校验错误日志，当前为空 |
| `outputs/results/final_results.csv` | 已补齐 | 最终结果表，包含量化评分字段 |
| `outputs/results/records_validated.csv` | 已有 | 81 条 Pydantic 校验结果 |
| `outputs/results/quantitative_scored_records.csv` | 已有 | 81 条量化评分结果 |
| `outputs/results/quantitative_scored_records.jsonl` | 已有 | JSONL 版量化结果 |
| `outputs/analysis/attention_review_list.csv` | 已有 | 值得关注的人工复核清单 |
| `outputs/analysis/cross_year_matching_events.csv` | 已有 | 同公司跨年匹配事件 |
| `outputs/reports/eval_report_final.md` | 已补齐 | 要求明确点名的最终评估报告 |
| `outputs/reports/summary_report.md` | 已有 | workflow 汇总报告 |
| `outputs/reports/quantitative_attention_report.md` | 已有 | 量化关注模型说明 |
| `outputs/reports/challenge_1_1_upgrade_report.md` | 已有 | 1.1 档升级说明 |
| `outputs/reports/dataset_expansion_to150.md` | 已有 | 样本扩展到 150+ 的说明 |
| `outputs/sample_outputs/` | 已补齐 | 小体积样例输出，方便展示和检查 |

## 5. 展示材料

| 文件 | 当前状态 | 说明 |
|---|---:|---|
| `demo_script.md` | 已有 | 展示讲稿 |
| `ppt_project_steps_zh.md` | 已新增 | 可直接拆成 PPT 的项目步骤 |
| `proposal_zh.md` | 已新增 | 中文 proposal |
| `final_slides.pdf` | 仍需生成 | 要求明确点名，完成 PPT 后导出为 PDF 并放在仓库根目录 |

## 6. 不要上传的内容

| 路径/文件 | 原因 |
|---|---|
| `.env` | 可能包含真实 API Key |
| `*.key` | 密钥文件 |
| `__pycache__/` | Python 缓存 |
| `*.pyc` | Python 编译缓存 |
| `work/data/`、`work/logs/` | 临时工作区 |
| `outputs/logs/*.tmp` | 临时日志 |
| `测试.docx` | 与最终提交无关 |

## 7. 上传前最终自查

- [ ] GitHub 仓库设为 Public。
- [ ] `README.md` 写明环境配置、运行命令和输出位置。
- [ ] `data/metadata/metadata.csv` 能追溯到巨潮公告 URL、PDF URL 和本地 PDF 路径。
- [ ] PDF 样本或解析样本能与 metadata 对应。
- [ ] `outputs/logs/sample_run_log.jsonl` 存在。
- [ ] `outputs/results/final_results.csv` 存在，并包含 `liquidity_risk_score`、`base_attention_score`、`cross_year_pressure_score`、`attention_score`、`attention_level`。
- [ ] `outputs/reports/eval_report_final.md` 存在。
- [ ] `final_report.md` 或 `final_report.pdf` 存在。
- [ ] `demo_script.md` 存在。
- [ ] `final_slides.pdf` 已导出并放在根目录。
- [ ] `.env`、真实密钥、缓存文件没有被加入 Git。

## 8. 建议的 Git 命令

```bash
git status
git add README.md requirements.txt .env.example .gitignore AGENTS.md
git add configs src pipeline_run.py schemas.py parse_docs.py route_sections.py extract_fields.py validate_results.py normalize_units.py quantitative_attention_analysis.py expand_cninfo_annual_reports.py audit_dataset.py parse_check.py report_results.py
git add data/metadata.csv data/metadata data/parsed
git add metadata_2020_2024_pool150.csv failed_downloads_to150.csv expansion_status_pdf175.md
git add outputs/logs/sample_run_log.jsonl outputs/logs/run_log.jsonl outputs/logs/validation_errors.jsonl
git add outputs/results outputs/analysis outputs/reports outputs/sample_outputs
git add final_report.md eval_report_final.md demo_script.md ai_usage_statement.md ai_worklog_all.md difficulty_declaration.md optimization_log.md proposal_zh.md topic_proposal.md ppt_project_steps_zh.md git_upload_checklist_zh.md
git add prompt_v1.md prompt_final.md
```

如果决定上传完整 PDF 池，再执行：

```bash
git add data/pdf
```

如果仓库体积过大，只上传 PDF 样本，并在 README 中说明可用 `expand_cninfo_annual_reports.py` 重新下载完整样本池。
