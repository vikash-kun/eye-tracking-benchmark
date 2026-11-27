"""
Load recorded gaze data from CSV files so real devices can be benchmarked.

Expected columns, one row per gaze sample:
    target_id, target_x, target_y, gaze_x, gaze_y

An optional timestamp_ms column is allowed and is ignored for now.
A lost sample (the tracker returned no gaze point) has empty
gaze_x and gaze_y cells.
"""

import pandas as pd

from src.angle import DEFAULT_SETUP, add_visual_angles
from src.trial import summarize_target


REQUIRED_COLUMNS = ["target_id", "target_x", "target_y", "gaze_x", "gaze_y"]
NUMERIC_COLUMNS = ["target_x", "target_y", "gaze_x", "gaze_y"]


def _clean_number(value):
    """Show whole numbers as ints (500, not 500.0)."""

    value = float(value)

    return int(value) if value.is_integer() else value


def load_gaze_csv(path):
    """
    Read and check a gaze recording.

    Returns:
        DataFrame: one row per gaze sample
    """

    df = pd.read_csv(path)

    missing = [name for name in REQUIRED_COLUMNS if name not in df.columns]

    if missing:
        raise ValueError("missing columns: " + ", ".join(missing))

    if df.empty:
        raise ValueError("the recording has no samples")

    for name in NUMERIC_COLUMNS:
        df[name] = pd.to_numeric(df[name])

    if df[["target_id", "target_x", "target_y"]].isna().any().any():
        raise ValueError("target_id, target_x and target_y cannot be empty")

    return df


def summarize_recording(df, setup=DEFAULT_SETUP):
    """
    Summarize a gaze recording with one result per target.

    The results have the same columns as run_benchmark, so they can be
    exported and compared in the same way.
    """

    results = []

    for target_id, group in df.groupby("target_id", sort=False):
        positions = group[["target_x", "target_y"]].drop_duplicates()

        if len(positions) != 1:
            raise ValueError(
                f"target {target_id} has more than one position"
            )

        target_x, target_y = positions.iloc[0]

        gaze_points = [
            None if pd.isna(x) or pd.isna(y) else (float(x), float(y))
            for x, y in zip(group["gaze_x"], group["gaze_y"])
        ]

        summary = summarize_target(
            target_id.item() if hasattr(target_id, "item") else target_id,
            _clean_number(target_x),
            _clean_number(target_y),
            gaze_points
        )

        results.append(add_visual_angles(summary, setup))

    return results


def summarize_csv(path, setup=DEFAULT_SETUP):
    """Load a gaze recording from a CSV file and summarize it."""

    return summarize_recording(load_gaze_csv(path), setup)