from pathlib import Path

import pytest

from src.compare import (
    best_device,
    compare_devices,
    devices_from_folder,
    per_target_table,
    summarize_device,
)
from src.simulate import DEVICE_PROFILES, simulate_recording


def make_result(accuracy, precision, n_samples=10, n_valid=10):
    return {
        "accuracy_px": accuracy,
        "accuracy_deg": None if accuracy is None else accuracy / 50,
        "precision_px": precision,
        "precision_deg": None if precision is None else precision / 50,
        "n_samples": n_samples,
        "n_valid": n_valid,
    }


def test_summarize_device_averages_the_targets():
    results = [make_result(10, 4), make_result(20, 6)]

    summary = summarize_device(results)

    assert summary["n_targets"] == 2
    assert summary["n_samples"] == 20
    assert summary["accuracy_px"] == pytest.approx(15)
    assert summary["precision_px"] == pytest.approx(5)
    assert summary["accuracy_deg"] == pytest.approx(0.3)


def test_data_loss_counts_all_samples():
    results = [
        make_result(10, 4, n_samples=10, n_valid=9),
        make_result(20, 6, n_samples=10, n_valid=7),
    ]

    assert summarize_device(results)["data_loss"] == pytest.approx(0.2)


def test_failed_target_is_left_out_of_the_averages():
    results = [
        make_result(10, 4),
        make_result(None, None, n_valid=0),
    ]

    summary = summarize_device(results)

    assert summary["accuracy_px"] == pytest.approx(10)
    assert summary["data_loss"] == pytest.approx(0.5)


def test_all_targets_failed_gives_no_accuracy():
    summary = summarize_device([make_result(None, None, n_valid=0)])

    assert summary["accuracy_px"] is None


def test_summarize_device_needs_results():
    with pytest.raises(ValueError):
        summarize_device([])


def test_compare_devices_has_one_row_per_device():
    comparison = compare_devices(
        {
            "a": [make_result(10, 4)],
            "b": [make_result(30, 8)],
        }
    )

    assert list(comparison["device"]) == ["a", "b"]
    assert list(comparison["accuracy_px"]) == [10, 30]


def test_per_target_table_has_one_row_per_device_and_target():
    table = per_target_table(
        {
            "a": [make_result(10, 4), make_result(12, 5)],
            "b": [make_result(30, 8), make_result(32, 9)],
        }
    )

    assert len(table) == 4
    assert list(table["device"]) == ["a", "a", "b", "b"]


def test_best_device_has_the_lowest_value():
    comparison = compare_devices(
        {
            "slow": [make_result(30, 8)],
            "good": [make_result(10, 4)],
        }
    )

    assert best_device(comparison) == "good"
    assert best_device(comparison, metric="precision_px") == "good"


def test_best_device_ignores_devices_without_values():
    comparison = compare_devices(
        {
            "failed": [make_result(None, None, n_valid=0)],
            "works": [make_result(10, 4)],
        }
    )

    assert best_device(comparison) == "works"


def test_best_device_is_none_when_nothing_is_known():
    comparison = compare_devices(
        {"failed": [make_result(None, None, n_valid=0)]}
    )

    assert best_device(comparison) is None


def test_devices_from_folder_uses_file_names(tmp_path):
    for name, profile in DEVICE_PROFILES.items():
        simulate_recording(**profile).to_csv(tmp_path / f"{name}.csv", index=False)

    devices = devices_from_folder(tmp_path)

    assert list(devices) == ["simulated_tracker", "simulated_webcam"]
    assert len(devices["simulated_tracker"]) == 5


def test_devices_from_folder_needs_csv_files(tmp_path):
    with pytest.raises(ValueError):
        devices_from_folder(tmp_path)


def test_example_recordings_show_webcam_worse_than_tracker():
    examples = Path(__file__).resolve().parent.parent / "examples"

    comparison = compare_devices(devices_from_folder(examples))
    tracker = comparison[comparison["device"] == "simulated_tracker"].iloc[0]
    webcam = comparison[comparison["device"] == "simulated_webcam"].iloc[0]

    assert webcam["accuracy_px"] > tracker["accuracy_px"]
    assert webcam["precision_px"] > tracker["precision_px"]
    assert webcam["data_loss"] > tracker["data_loss"]