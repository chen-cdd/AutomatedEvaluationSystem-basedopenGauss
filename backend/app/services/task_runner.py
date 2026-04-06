import asyncio
import json
import time
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.entities import DashboardMetric, EvaluationTask, ParsedTrace, ScoreResult
from app.services.normalizer import normalize_log
from app.services.sanitizer import sanitize_payload
from app.services.scoring import score_trace
from app.services.trace_parser import build_trace_views


async def process_task(db: Session, task: EvaluationTask) -> None:
    started = time.perf_counter()
    task.status = "parsing"
    db.add(task)
    db.commit()
    db.refresh(task)

    file_path = Path(task.file_path)
    payload = json.loads(file_path.read_text(encoding="utf-8"))
    sanitized = sanitize_payload(payload)
    normalized = normalize_log(sanitized)
    tree, timeline = build_trace_views(normalized)

    parsed = task.parsed_trace or ParsedTrace(task_id=task.id)
    parsed.parse_status = "completed"
    parsed.node_count = len(timeline)
    parsed.normalized_payload = normalized
    parsed.tree_payload = tree
    parsed.timeline_payload = timeline
    task.is_desensitized = True
    task.status = "scoring"
    db.add(parsed)
    db.add(task)
    db.commit()

    await asyncio.sleep(0)

    score_payload = score_trace(normalized, tree)
    score = task.score_result or ScoreResult(task_id=task.id)
    score.accuracy = score_payload["accuracy"]
    score.logic_consistency = score_payload["logic_consistency"]
    score.tool_efficiency = score_payload["tool_efficiency"]
    score.safety = score_payload["safety"]
    score.total_score = score_payload["total_score"]
    score.verdict = score_payload["verdict"]
    score.summary = score_payload["summary"]
    score.deduction_reasons = score_payload["deduction_reasons"]
    score.chain_of_thought = score_payload["chain_of_thought"]
    score.scoring_status = score_payload["scoring_status"]
    score.judge_model = score_payload["judge_model"]

    elapsed = round(time.perf_counter() - started, 3)
    metric = task.metrics or DashboardMetric(task_id=task.id)
    metric.processing_seconds = elapsed
    metric.token_consumption = max(150, len(score_payload["judge_prompt"]) // 4)
    metric.success_rate = 1.0 if score.total_score >= 60 else 0.0
    metric.bad_case = score.total_score < 70
    metric.retry_count = 0

    task.status = "completed"
    db.add_all([score, metric, task])
    db.commit()


def mark_task_failed(db: Session, task: EvaluationTask, error: Exception) -> None:
    task.status = "failed"
    task.error_message = str(error)
    db.add(task)
    db.commit()
