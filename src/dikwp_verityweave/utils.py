from __future__ import annotations

import hashlib
import json
import math
import re
from datetime import datetime, timezone
from typing import Any, Iterable


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, float(value)))


def saturation(count: int, scale: float = 2.0) -> float:
    if count <= 0:
        return 0.0
    return clamp(1.0 - math.exp(-float(count) / max(scale, 0.001)))


def normalize_weights(values: dict[str, float]) -> dict[str, float]:
    cleaned = {key: max(0.0, float(value)) for key, value in values.items()}
    total = sum(cleaned.values())
    if total <= 0:
        return {key: 1.0 / len(cleaned) for key in cleaned}
    return {key: value / total for key, value in cleaned.items()}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def find_markers(text: str, markers: Iterable[str]) -> list[str]:
    lowered = text.casefold()
    found: list[str] = []
    for marker in markers:
        marker_text = str(marker).strip()
        if marker_text and marker_text.casefold() in lowered:
            found.append(marker_text)
    return sorted(set(found))


def tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'-]{1,}", text.casefold())


def safe_filename(value: str, default: str = "result") -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-.")
    return cleaned or default
