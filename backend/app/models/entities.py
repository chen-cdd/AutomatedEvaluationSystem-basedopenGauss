from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ModelRegistry(Base):
    __tablename__ = "model_registry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    version: Mapped[str] = mapped_column(String(64), default="v1")
    model_type: Mapped[str] = mapped_column(String(64), default="judge")
    description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    tasks: Mapped[list["EvaluationTask"]] = relationship(back_populates="model")


class EvaluationTask(Base):
    __tablename__ = "evaluation_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="pending", index=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_format: Mapped[str] = mapped_column(String(32), default="json")
    duplicate_hash: Mapped[str] = mapped_column(String(128), index=True)
    is_desensitized: Mapped[bool] = mapped_column(Boolean, default=False)
    error_message: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    model_id: Mapped[int | None] = mapped_column(ForeignKey("model_registry.id"), nullable=True)

    model: Mapped[ModelRegistry | None] = relationship(back_populates="tasks")
    parsed_trace: Mapped["ParsedTrace | None"] = relationship(back_populates="task", cascade="all, delete-orphan")
    score_result: Mapped["ScoreResult | None"] = relationship(back_populates="task", cascade="all, delete-orphan")
    metrics: Mapped["DashboardMetric | None"] = relationship(back_populates="task", cascade="all, delete-orphan")


class ParsedTrace(Base):
    __tablename__ = "parsed_traces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("evaluation_tasks.id"), unique=True)
    parse_status: Mapped[str] = mapped_column(String(32), default="pending")
    node_count: Mapped[int] = mapped_column(Integer, default=0)
    normalized_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    tree_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    timeline_payload: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    task: Mapped[EvaluationTask] = relationship(back_populates="parsed_trace")


class ScoreResult(Base):
    __tablename__ = "score_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("evaluation_tasks.id"), unique=True)
    accuracy: Mapped[float] = mapped_column(Float, default=0)
    logic_consistency: Mapped[float] = mapped_column(Float, default=0)
    tool_efficiency: Mapped[float] = mapped_column(Float, default=0)
    safety: Mapped[float] = mapped_column(Float, default=0)
    total_score: Mapped[float] = mapped_column(Float, default=0, index=True)
    verdict: Mapped[str] = mapped_column(String(32), default="pending")
    summary: Mapped[str] = mapped_column(Text, default="")
    deduction_reasons: Mapped[list] = mapped_column(JSON, default=list)
    chain_of_thought: Mapped[str] = mapped_column(Text, default="")
    scoring_status: Mapped[str] = mapped_column(String(32), default="pending")
    judge_model: Mapped[str] = mapped_column(String(128), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    task: Mapped[EvaluationTask] = relationship(back_populates="score_result")


class DashboardMetric(Base):
    __tablename__ = "dashboard_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("evaluation_tasks.id"), unique=True)
    processing_seconds: Mapped[float] = mapped_column(Float, default=0)
    token_consumption: Mapped[int] = mapped_column(Integer, default=0)
    success_rate: Mapped[float] = mapped_column(Float, default=0)
    bad_case: Mapped[bool] = mapped_column(Boolean, default=False)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    task: Mapped[EvaluationTask] = relationship(back_populates="metrics")
