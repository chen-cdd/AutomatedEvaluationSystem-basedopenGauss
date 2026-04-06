from typing import Any


NODE_TYPES = {"user_input", "thought", "action", "tool_call", "observation", "final_answer"}


def normalize_log(payload: dict[str, Any]) -> dict[str, Any]:
    if "events" in payload and isinstance(payload["events"], list):
        events = payload["events"]
    elif "steps" in payload and isinstance(payload["steps"], list):
        events = payload["steps"]
    else:
        events = []

    normalized_events = []
    for index, event in enumerate(events):
        event_type = event.get("type") or event.get("role") or "observation"
        if event_type not in NODE_TYPES:
            event_type = map_event_type(event_type)
        normalized_events.append(
            {
                "id": event.get("id", f"node-{index}"),
                "type": event_type,
                "content": event.get("content") or event.get("message") or event.get("output") or "",
                "tool_name": event.get("tool_name") or event.get("tool") or "",
                "timestamp": event.get("timestamp") or index,
                "parent_id": event.get("parent_id"),
                "metadata": event.get("metadata", {}),
            }
        )

    user_input = payload.get("input") or payload.get("question") or ""
    final_output = payload.get("final_output") or payload.get("answer") or ""

    return {
        "session_id": payload.get("session_id") or payload.get("trace_id") or "unknown-session",
        "user_input": user_input,
        "final_output": final_output,
        "events": normalized_events,
        "source": payload.get("source", "uploaded-json"),
    }


def map_event_type(raw_type: str) -> str:
    raw_type = str(raw_type).lower()
    if raw_type in {"user", "input"}:
        return "user_input"
    if raw_type in {"thought", "reasoning", "plan"}:
        return "thought"
    if raw_type in {"action", "act"}:
        return "action"
    if raw_type in {"tool", "tool_call"}:
        return "tool_call"
    if raw_type in {"observation", "tool_result", "result"}:
        return "observation"
    if raw_type in {"assistant", "final", "final_answer"}:
        return "final_answer"
    return "observation"
