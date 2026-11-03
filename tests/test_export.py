import json

import numpy as np
import pandas as pd

from src.export import export_all, export_csv, export_json, results_to_dataframe

RESULTS = [
    {"device": "webcam", "target": 1, "accuracy_px": 42.5, "data_loss": 0.1},
    {"device": "tobii", "target": 1, "accuracy_px": 12.0, "data_loss": np.nan},
]


def test_results_to_dataframe_accepts_list_and_dataframe():
    from_list = results_to_dataframe(RESULTS)
    from_df = results_to_dataframe(from_list)
    assert list(from_list.columns) == list(from_df.columns)
    assert len(from_df) == 2


def test_export_csv_round_trip(tmp_path):
    path = export_csv(RESULTS, tmp_path / "out.csv")
    loaded = pd.read_csv(path)
    assert len(loaded) == 2
    assert loaded.loc[0, "device"] == "webcam"
    assert loaded.loc[0, "accuracy_px"] == 42.5


def test_export_csv_creates_missing_folders(tmp_path):
    path = export_csv(RESULTS, tmp_path / "nested" / "dir" / "out.csv")
    assert path.exists()


def test_export_json_has_metadata_and_results(tmp_path):
    path = export_json(RESULTS, tmp_path / "out.json",
                       metadata={"screen": "1920x1080"})
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["metadata"]["screen"] == "1920x1080"
    assert "exported_at" in data["metadata"]
    assert len(data["results"]) == 2


def test_export_json_turns_nan_into_null(tmp_path):
    path = export_json(RESULTS, tmp_path / "out.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["results"][1]["data_loss"] is None


def test_export_all_writes_both_files(tmp_path):
    paths = export_all(RESULTS, tmp_path, name="run1")
    assert paths["csv"].name == "run1.csv"
    assert paths["json"].name == "run1.json"
    assert paths["csv"].exists() and paths["json"].exists()