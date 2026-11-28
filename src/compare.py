"""Compare benchmark results across devices and setups."""

from pathlib import Path

import pandas as pd

from src.angle import DEFAULT_SETUP
from src.loader import summarize_csv


def _mean(values):
    """Average of the values that are not None (None if there are none)."""

    values = [value for value in values if value is not None]

    return sum(values) / len(values) if values else None


def summarize_device(results):
    """
    Overall accuracy, precision and data loss for one device.

    Accuracy and precision are the mean of the per-target values, so every
    target counts equally and targets where all samples were lost are left
    out. Data loss is the share of all samples that were lost.
    """

    if not results:
        raise ValueError("no results to summarize")

    total_samples = sum(result["n_samples"] for result in results)
    total_valid = sum(result["n_valid"] for result in results)

    return {
        "n_targets": len(results),
        "n_samples": total_samples,
        "accuracy_px": _mean([r["accuracy_px"] for r in results]),
        "accuracy_deg": _mean([r.get("accuracy_deg") for r in results]),
        "precision_px": _mean([r["precision_px"] for r in results]),
        "precision_deg": _mean([r.get("precision_deg") for r in results]),
        "data_loss": 1 - total_valid / total_samples,
    }


def compare_devices(device_results):
    """
    Build a table with one row per device.

    Args:
        device_results: dict of device name -> list of per-target results

    Returns:
        DataFrame: device, n_targets, n_samples, accuracy, precision, data_loss
    """

    rows = []

    for name, results in device_results.items():
        rows.append({"device": name, **summarize_device(results)})

    return pd.DataFrame(rows)


def per_target_table(device_results):
    """Build a table with one row per device and target."""

    rows = []

    for name, results in device_results.items():
        for result in results:
            rows.append({"device": name, **result})

    return pd.DataFrame(rows)


def best_device(comparison, metric="accuracy_px"):
    """Name of the device with the lowest value of a metric (None if unknown)."""

    valid = comparison.dropna(subset=[metric])

    if valid.empty:
        return None

    return valid.loc[valid[metric].idxmin(), "device"]


def devices_from_folder(folder, setup=DEFAULT_SETUP):
    """
    Summarize every CSV recording in a folder, one device per file.

    The device name is the file name without the .csv ending.
    """

    paths = sorted(Path(folder).glob("*.csv"))

    if not paths:
        raise ValueError(f"no CSV recordings found in {folder}")

    return {path.stem: summarize_csv(path, setup) for path in paths}