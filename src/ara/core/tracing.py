from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict
from ara.core.state import ARAState


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def write_run_artifacts(state: ARAState, out_dir: str = "outputs/sample_runs") -> str:
    ensure_dir(out_dir)
    run_id = state.run_metadata.run_id if state.run_metadata else "run"
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    base = f"{run_id}_{ts}"

    json_path = os.path.join(out_dir, f"{base}.json")
    md_path = os.path.join(out_dir, f"{base}_report.md")

    with open(json_path, "w", encoding="utf-8") as f:
        f.write(state.model_dump_json(indent=2))

    if state.final_answer_md:
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(state.final_answer_md)

    return json_path
