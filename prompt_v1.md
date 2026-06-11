# Prompt V1

请从房地产上市公司年报相关章节中抽取分红、经营现金流和流动性风险信息，输出 JSON。

要求：
- 只根据输入文本。
- 不确定输出 null。
- 提供证据片段。
- 输出通过 Pydantic schema 校验。

备注：这一版较简略，后续根据 section 命中错误、金额单位错误和 evidence 错误优化为 `prompt_final.md`。
