from __future__ import annotations

import uuid


VALID_PREFIXES = {
    "signal": "s",
    "emission": "e",
    "task": "t",
    "result": "r",
    "entity": "ent",
}


def generate_id(prefix: str | None = None) -> str:
    token = uuid.uuid4().hex
    if prefix is None:
        return token
    normalized = prefix.strip().lower()
    mapped = VALID_PREFIXES.get(normalized, normalized)
    return f"{mapped}_{token}"
