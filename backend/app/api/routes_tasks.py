import json

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import SessionLocal, get_db
from app.models.entities import EvaluationTask
from app.schemas.common import MessageResponse
from app.schemas.tasks import TaskDetail, TaskRead
from app.services.task_runner import mark_task_failed, process_task
from app.utils.files import compute_sha256, save_upload

router = APIRouter(prefix="/tasks", tags=["tasks"])
settings = get_settings()


async def run_task_in_background(task_id: int) -> None:
    db = SessionLocal()
    task = None
    try:
        task = db.get(EvaluationTask, task_id)
        if not task:
            return
        await process_task(db, task)
    except Exception as exc:
        if task:
            mark_task_failed(db, task, exc)
    finally:
        db.close()


@router.get("", response_model=list[TaskRead])
def list_tasks(status: str | None = Query(default=None), db: Session = Depends(get_db)) -> list[EvaluationTask]:
    stmt = select(EvaluationTask).order_by(desc(EvaluationTask.created_at))
    if status:
        stmt = stmt.where(EvaluationTask.status == status)
    return list(db.scalars(stmt).all())


@router.get("/{task_id}", response_model=TaskDetail)
def get_task(task_id: int, db: Session = Depends(get_db)) -> TaskDetail:
    task = db.get(EvaluationTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskDetail(
        **TaskRead.model_validate(task).model_dump(),
        parsed_trace=task.parsed_trace.tree_payload if task.parsed_trace else None,
        score_result={
            "accuracy": task.score_result.accuracy,
            "logic_consistency": task.score_result.logic_consistency,
            "tool_efficiency": task.score_result.tool_efficiency,
            "safety": task.score_result.safety,
            "total_score": task.score_result.total_score,
            "verdict": task.score_result.verdict,
            "summary": task.score_result.summary,
            "deduction_reasons": task.score_result.deduction_reasons,
            "chain_of_thought": task.score_result.chain_of_thought,
            "judge_model": task.score_result.judge_model,
        } if task.score_result else None,
        metrics={
            "processing_seconds": task.metrics.processing_seconds,
            "token_consumption": task.metrics.token_consumption,
            "success_rate": task.metrics.success_rate,
            "bad_case": task.metrics.bad_case,
        } if task.metrics else None,
    )


@router.post("/upload", response_model=list[TaskRead])
async def upload_logs(background_tasks: BackgroundTasks, files: list[UploadFile] = File(...), db: Session = Depends(get_db)) -> list[EvaluationTask]:
    created_tasks = []
    for upload in files:
        if not upload.filename.lower().endswith(".json"):
            raise HTTPException(status_code=400, detail="Only JSON log files are supported")
        raw = await upload.read()
        if len(raw) > settings.max_upload_size_mb * 1024 * 1024:
            raise HTTPException(status_code=400, detail=f"File {upload.filename} exceeds upload limit")
        try:
            json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=400, detail=f"Invalid JSON in {upload.filename}: {exc}") from exc

        duplicate_hash = compute_sha256(raw)
        file_path = save_upload(settings.storage_path / "logs", upload, raw)
        task = EvaluationTask(
            name=file_path.stem,
            status="pending",
            file_name=file_path.name,
            file_path=str(file_path),
            file_format="json",
            duplicate_hash=duplicate_hash,
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        created_tasks.append(task)
        background_tasks.add_task(run_task_in_background, task.id)
    return created_tasks


@router.post("/{task_id}/run", response_model=MessageResponse)
def rerun_task(task_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)) -> MessageResponse:
    task = db.get(EvaluationTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = "pending"
    task.error_message = ""
    db.add(task)
    db.commit()
    background_tasks.add_task(run_task_in_background, task.id)
    return MessageResponse(message=f"Task {task_id} has been queued")


@router.delete("/{task_id}", response_model=MessageResponse)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> MessageResponse:
    task = db.get(EvaluationTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return MessageResponse(message=f"Task {task_id} deleted")
