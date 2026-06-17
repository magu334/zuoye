from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


ReportYear = Literal["2020", "2021", "2022", "2023", "2024"]


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
    report_year: ReportYear
    title: str
    event_type: str
    dividend_plan: Optional[DividendPlan] = None
    parent_net_profit: Optional[NumericField] = None
    operating_cash_flow: Optional[NumericField] = None
    liquidity_risk: Optional[LiquidityRisk] = None
    consistency_score: Optional[int] = Field(default=None, ge=1, le=3)
    consistency_reason: Optional[str] = None


class QuantitativeScoredRecord(BaseModel):
    doc_id: str
    stock_code: str
    stock_name: str
    report_year: ReportYear
    has_cash_dividend: Optional[bool] = None
    cash_dividend_per_10_shares: Optional[float] = None
    parent_net_profit_cny: Optional[float] = None
    operating_cash_flow_cny: Optional[float] = None
    ocf_to_profit_ratio: Optional[float] = None
    dividend_pressure_score: float = Field(..., ge=0, le=100)
    profit_pressure_score: float = Field(..., ge=0, le=100)
    cashflow_pressure_score: float = Field(..., ge=0, le=100)
    liquidity_term_hits: int = Field(..., ge=0)
    liquidity_weighted_hits: float = Field(..., ge=0)
    liquidity_risk_score: float = Field(..., ge=0, le=100)
    liquidity_risk_quantile: Literal["none", "low", "medium", "high"]
    legacy_liquidity_risk_label: Literal["none", "low", "medium", "high", "unknown"]
    attention_score: float = Field(..., ge=0, le=100)
    attention_level: Literal["routine", "monitor", "watch", "priority"]
    review_reason: str


class CrossYearMatchingEvent(BaseModel):
    event_id: str
    stock_code: str
    stock_name: str
    from_year: ReportYear
    to_year: ReportYear
    year_gap: int = Field(..., ge=1, le=4)
    is_consecutive_pair: bool
    from_doc_id: str
    to_doc_id: str
    dividend_delta: Optional[float] = None
    ocf_delta_cny: Optional[float] = None
    profit_delta_cny: Optional[float] = None
    risk_score_delta: float
    base_attention_score_delta: float
    final_attention_score_delta: float
    cross_year_pressure_score: float = Field(..., ge=0, le=100)
    event_type: str
    review_reason: str
