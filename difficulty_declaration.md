# 难度申请

- 申请难度：标准
- 系数：1.0
- 数据量：81 份房地产上市公司年报 PDF / 解析样本
- 公告类型：年报
- 是否多公告匹配：否
- 字段数量：6 个核心评估字段，另含 metadata、evidence、风险关键词和一致性原因字段
- 主要挑战：年报 PDF 解析、分红和财务字段定位、流动性风险 section routing、证据回填、Pydantic 校验、人工评估与错误分类

## 我们认为该难度合理的理由
本项目达到标准档的数据量下限，使用单一但复杂的年报公告类型，抽取分红政策、经营现金流、归母净利润、流动性风险披露和一致性评分等字段，并建立从 CNINFO metadata 到 PDF、MinerU markdown、section、抽取结果、Pydantic validation 和人工评估的完整 workflow。
