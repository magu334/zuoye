from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]


class Timer:
    def __enter__(self) -> "Timer":
        self.start = time.perf_counter()
        self.elapsed = 0.0
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.elapsed = round(time.perf_counter() - self.start, 4)


def project_path(path: str | Path) -> Path:
    path = Path(path)
    if path.is_absolute():
        return path
    return ROOT / path


def _flat_path(path: str | Path) -> Path:
    """Fallback for the legacy flat repository layout."""
    return ROOT / Path(path).name


def resolve_existing(path: str | Path) -> Path:
    direct = project_path(path)
    if direct.exists():
        return direct
    flat = _flat_path(path)
    if flat.exists():
        return flat
    return direct


def load_workflow_config(path: str | Path) -> dict[str, Any]:
    config_path = resolve_existing(path)
    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}
    config["_config_path"] = str(config_path.relative_to(ROOT))
    return config


def append_log(
    config: dict[str, Any],
    step: str,
    status: str,
    *,
    count: int | None = None,
    error: str | None = None,
    elapsed: float | None = None,
) -> None:
    log_path = project_path(config.get("paths", {}).get("run_log", "outputs/logs/run_log.jsonl"))
    log_path.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "time": datetime.now(timezone.utc).isoformat(),
        "step": step,
        "status": status,
        "count": count,
        "elapsed": elapsed,
        "error": error,
    }
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
