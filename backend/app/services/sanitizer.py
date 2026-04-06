import re
from copy import deepcopy


SENSITIVE_PATTERNS = [
    (re.compile(r"sk-[A-Za-z0-9]{10,}"), "sk-***"),
    (re.compile(r"(?i)api[_-]?key['\"]?\s*[:=]\s*['\"][^'\"]+['\"]"), 'api_key="***"'),
    (re.compile(r"[A-Za-z]:\\\\Users\\\\[^\\\\]+"), r"C:\\Users\\***"),
]


def _sanitize_text(value: str) -> str:
    result = value
    for pattern, replacement in SENSITIVE_PATTERNS:
        result = pattern.sub(replacement, result)
    return result


def sanitize_payload(payload: dict | list | str | int | float | None):
    if isinstance(payload, dict):
        sanitized = {}
        for key, value in payload.items():
            if any(secret in key.lower() for secret in ("token", "secret", "password", "key")):
                sanitized[key] = "***"
            else:
                sanitized[key] = sanitize_payload(value)
        return sanitized
    if isinstance(payload, list):
        return [sanitize_payload(item) for item in payload]
    if isinstance(payload, str):
        return _sanitize_text(payload)
    return deepcopy(payload)
