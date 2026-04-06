import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.entities import EvaluationTask, ModelRegistry
from app.utils.files import compute_sha256


def ensure_seed_data(db: Session) -> None:
    model = db.scalar(select(ModelRegistry).where(ModelRegistry.name == "deepseek-v3"))
    if not model:
        model = ModelRegistry(name="deepseek-v3", version="api", model_type="judge", description="Default judge model")
        db.add(model)
        db.commit()
        db.refresh(model)

    if db.scalar(select(EvaluationTask.id).limit(1)):
        return

    settings = get_settings()
    sample_dir = settings.storage_path / "samples"
    sample_dir.mkdir(parents=True, exist_ok=True)
    sample_path = sample_dir / "sample_trace.json"
    if not sample_path.exists():
        sample_payload = {
            "session_id": "demo-session-001",
            "input": "请帮我查询北京今天的天气，并给出穿衣建议。",
            "events": [
                {"id": "e1", "type": "thought", "content": "我需要先查询天气信息。"},
                {"id": "e2", "type": "tool_call", "tool_name": "weather_api", "content": "调用天气接口查询北京天气。"},
                {"id": "e3", "type": "observation", "content": "北京今天多云，18 到 27 摄氏度。"},
                {"id": "e4", "type": "final_answer", "content": "北京今天多云，建议穿薄外套并携带雨伞。"},
            ],
            "final_output": "北京今天多云，建议穿薄外套并携带雨伞。",
            "source": "seed",
        }
        sample_path.write_text(json.dumps(sample_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    task = EvaluationTask(
        name="示例任务",
        status="pending",
        file_name=sample_path.name,
        file_path=str(sample_path),
        file_format="json",
        duplicate_hash=compute_sha256(sample_path.read_bytes()),
        model_id=model.id,
    )
    db.add(task)
    db.commit()
