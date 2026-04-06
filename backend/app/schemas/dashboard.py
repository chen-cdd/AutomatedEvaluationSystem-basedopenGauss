from pydantic import BaseModel


class OverviewStats(BaseModel):
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    average_score: float
    average_processing_seconds: float
    average_tokens: float


class RadarPoint(BaseModel):
    label: str
    value: float


class DashboardOverview(BaseModel):
    stats: OverviewStats
    radar: list[RadarPoint]
    model_comparison: list[dict]
    bad_cases: list[dict]
