from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import DashboardMetric, EvaluationTask, ModelRegistry, ScoreResult
from app.schemas.dashboard import DashboardOverview, OverviewStats, RadarPoint

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/overview", response_model=DashboardOverview)
def get_overview(db: Session = Depends(get_db)) -> DashboardOverview:
    total_tasks = db.scalar(select(func.count(EvaluationTask.id))) or 0
    completed_tasks = db.scalar(select(func.count(EvaluationTask.id)).where(EvaluationTask.status == "completed")) or 0
    failed_tasks = db.scalar(select(func.count(EvaluationTask.id)).where(EvaluationTask.status == "failed")) or 0
    average_score = db.scalar(select(func.avg(ScoreResult.total_score))) or 0
    average_processing_seconds = db.scalar(select(func.avg(DashboardMetric.processing_seconds))) or 0
    average_tokens = db.scalar(select(func.avg(DashboardMetric.token_consumption))) or 0

    score_row = db.execute(
        select(
            func.avg(ScoreResult.accuracy),
            func.avg(ScoreResult.logic_consistency),
            func.avg(ScoreResult.tool_efficiency),
            func.avg(ScoreResult.safety),
        )
    ).one()
    radar = [
        RadarPoint(label="准确性", value=round(score_row[0] or 0, 2)),
        RadarPoint(label="逻辑连贯性", value=round(score_row[1] or 0, 2)),
        RadarPoint(label="工具效率", value=round(score_row[2] or 0, 2)),
        RadarPoint(label="安全性", value=round(score_row[3] or 0, 2)),
    ]

    model_comparison = []
    rows = db.execute(
        select(
            ModelRegistry.name,
            func.count(EvaluationTask.id),
            func.avg(ScoreResult.total_score),
        )
        .join(EvaluationTask, EvaluationTask.model_id == ModelRegistry.id, isouter=True)
        .join(ScoreResult, ScoreResult.task_id == EvaluationTask.id, isouter=True)
        .group_by(ModelRegistry.name)
    ).all()
    for name, task_count, avg_score in rows:
        model_comparison.append({"model_name": name, "task_count": task_count or 0, "average_score": round(avg_score or 0, 2)})

    bad_cases = []
    bad_rows = db.execute(
        select(EvaluationTask.id, EvaluationTask.name, ScoreResult.total_score, ScoreResult.summary)
        .join(ScoreResult, ScoreResult.task_id == EvaluationTask.id)
        .where(ScoreResult.total_score < 70)
        .order_by(ScoreResult.total_score.asc())
        .limit(10)
    ).all()
    for task_id, name, total_score, summary in bad_rows:
        bad_cases.append({"task_id": task_id, "task_name": name, "total_score": total_score, "summary": summary})

    return DashboardOverview(
        stats=OverviewStats(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            failed_tasks=failed_tasks,
            average_score=round(average_score, 2),
            average_processing_seconds=round(average_processing_seconds, 2),
            average_tokens=round(average_tokens, 2),
        ),
        radar=radar,
        model_comparison=model_comparison,
        bad_cases=bad_cases,
    )
