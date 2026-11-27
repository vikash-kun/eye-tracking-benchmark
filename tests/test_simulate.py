import pytest

from src.loader import load_gaze_csv, summarize_csv, summarize_recording
from src.run_benchmark import TARGETS
from src.simulate import DEVICE_PROFILES, simulate_recording


def test_recording_has_expected_shape():
    df = simulate_recording(noise=10, loss_rate=0.0, n_samples=20, seed=1)

    assert len(df) == 20 * len(TARGETS)
    assert list(df.columns) == [
        "target_id", "target_x", "target_y",
        "timestamp_ms", "gaze_x", "gaze_y",
    ]


def test_same_seed_gives_same_recording():
    first = simulate_recording(noise=10, loss_rate=0.1, seed=5)
    second = simulate_recording(noise=10, loss_rate=0.1, seed=5)

    assert first.equals(second)


def test_no_blank_samples_when_loss_rate_is_zero():
    df = simulate_recording(noise=10, loss_rate=0.0, seed=1)

    assert not df["gaze_x"].isna().any()


def test_offset_shifts_every_sample():
    df = simulate_recording(
        noise=0, loss_rate=0.0, offset=(5, -3), n_samples=5, seed=1
    )

    assert (df["gaze_x"] == df["target_x"] + 5).all()
    assert (df["gaze_y"] == df["target_y"] - 3).all()


def test_recording_round_trips_through_csv(tmp_path):
    path = tmp_path / "recording.csv"
    simulate_recording(
        noise=0, loss_rate=0.0, offset=(3, 4), n_samples=5, seed=1
    ).to_csv(path, index=False)

    results = summarize_csv(path)

    # a fixed (3, 4) offset is exactly 5 pixels from every target
    assert len(results) == len(TARGETS)
    for result in results:
        assert result["accuracy_px"] == pytest.approx(5.0)
        assert result["precision_px"] == pytest.approx(0.0)


def test_webcam_profile_is_worse_than_tracker_profile():
    tracker = summarize_recording(
        simulate_recording(**DEVICE_PROFILES["simulated_tracker"])
    )
    webcam = summarize_recording(
        simulate_recording(**DEVICE_PROFILES["simulated_webcam"])
    )

    for good, bad in zip(tracker, webcam):
        assert bad["accuracy_px"] > good["accuracy_px"]
        assert bad["precision_px"] > good["precision_px"]


def test_blank_cells_survive_the_csv(tmp_path):
    path = tmp_path / "recording.csv"
    simulate_recording(noise=10, loss_rate=1.0, n_samples=5, seed=1).to_csv(
        path, index=False
    )

    df = load_gaze_csv(path)

    assert df["gaze_x"].isna().all()