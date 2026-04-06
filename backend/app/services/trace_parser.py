from typing import Any


def build_trace_views(normalized: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    nodes = normalized["events"]
    if normalized["user_input"]:
        nodes = [{"id": "root-input", "type": "user_input", "content": normalized["user_input"], "parent_id": None, "timestamp": -1, "tool_name": "", "metadata": {}}] + nodes
    if normalized["final_output"]:
        nodes = nodes + [{"id": "root-output", "type": "final_answer", "content": normalized["final_output"], "parent_id": nodes[-1]["id"] if nodes else None, "timestamp": len(nodes), "tool_name": "", "metadata": {}}]

    node_map = {}
    roots = []
    timeline = []

    previous_id = None
    for index, node in enumerate(nodes):
        current = {
            "id": node["id"],
            "type": node["type"],
            "title": node["type"].replace("_", " ").title(),
            "content": node["content"],
            "tool_name": node.get("tool_name", ""),
            "timestamp": node.get("timestamp", index),
            "children": [],
        }
        node_map[current["id"]] = current
        parent_id = node.get("parent_id") or previous_id
        if parent_id and parent_id in node_map:
            node_map[parent_id]["children"].append(current)
        else:
            roots.append(current)
        timeline.append(
            {
                "index": index,
                "node_id": current["id"],
                "type": current["type"],
                "title": current["title"],
                "content": current["content"],
                "tool_name": current["tool_name"],
            }
        )
        previous_id = current["id"]

    tree = {
        "session_id": normalized["session_id"],
        "source": normalized["source"],
        "roots": roots,
    }
    return tree, timeline
