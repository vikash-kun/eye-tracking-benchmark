"""Export benchmark results to CSV and JSON for reporting and reproducibility."""

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


def results_to_dataframe(results):
    """Turn a list of result dicts (or a DataFrame) into a DataFrame."""
    if isinstance(results, pd.DataFrame):
        return results.copy()
    return pd.DataFrame(list(results))


def export_csv(results, path):
    """Write results to a CSV file and return the path."""
    df = results_to_dataframe(results)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


def export_json(results, path, metadata=None):
    """Write results plus run metadata to a JSON file and return the path.

    Lost samples (NaN) are written as null so the file is valid JSON.
    """
    df = results_to_dataframe(results)
    payload = {
        "metadata": {
            "exported_at": datetime.now(timezone.utc).isoformat(),
            **(metadata or {}),
        },
        "results": json.loads(df.to_json(orient="records")),
    }
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return path


def export_all(results, out_dir, name="benchmark", metadata=None):
    """Write both <name>.csv and <name>.json into out_dir."""
    out_dir = Path(out_dir)
    return {
        "csv": export_csv(results, out_dir / f"{name}.csv"),
        "json": export_json(results, out_dir / f"{name}.json", metadata),
    }


