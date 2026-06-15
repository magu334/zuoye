from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    text: str = Field(..., min_length=1)
    source: Literal["section", "parsed_doc"]
    section_type: Optional[str] = None


class NumericField(BaseModel):
    value: Optional[float] = None
    raw_text: Optional[str] = None
    unit: Optional[Literal["CNY", "CNY_10K", "CNY_100M", "unknown"]] = None
    evidence: Optional[Evidence] = None


class DividendPlan(BaseModel):
    has_cash_dividend: Optional[bool] = None
    cash_dividend_per_10_shares: Optional[float] = None
    bonus_or_conversion: Optional[bool] = None
    evidence: Optional[Evidence] = None


class LiquidityRisk(BaseModel):
    label: Literal["none", "low", "medium", "high", "unknown"]
    keywords: list[str] = []
    evidence: Optional[Evidence] = None


class DividendCashflowLiquidityExtract(BaseModel):
    doc_id: str
    stock_code: str
    stock_name: str
    report_year: Literal["2021", "2022", "2023"]
    title: str
    event_type: str
    dividend_plan: Optional[DividendPlan] = None
    parent_net_profit: Optional[NumericField] = None
    operating_cash_flow: Optional[NumericField] = None
    liquidity_risk: Optional[LiquidityRisk] = None
    consistency_score: Optional[int] = Field(default=None, ge=1, le=3)
    consistency_reason: Optional[str] = None
