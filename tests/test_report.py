import json

from src.compare import compare_devices
from src.report import format_comparison, main, run_report
from src.simulate import DEVICE_PROFILES, simulate_recording


def write_example_recordings(folder):
    for name, profile in DEVICE_PROFILES.items():
        simulate_recording(**profile).to_csv(folder / f"{name}.csv", index=False)


def test_format_comparison_shows_devices_and_percent():
    results = {
        "a": [
            {
                "accuracy_px": 10, "accuracy_deg": 0.2,
                "precision_px": 4, "precision_deg": 0.08,
                "n_samples": 10, "n_valid": 9,
            }
        ]
    }

    text = format_comparison(compare_devices(results))

    assert "a" in text
    assert "accuracy_px" in text
    assert "10.0%" in text


def test_run_report_writes_both_tables(tmp_path):
    recordings = tmp_path / "recordings"
    recordings.mkdir()
    write_example_recordings(recordings)
    out_dir = tmp_path / "out"

    comparison = run_report(recordings, out_dir)

    assert len(comparison) == 2
    for name in ("comparison", "per_target"):
        assert (out_dir / f"{name}.csv").exists()
        assert (out_dir / f"{name}.json").exists()


def test_report_json_records_the_screen_setup(tmp_path):
    recordings = tmp_path / "recordings"
    recordings.mkdir()
    write_example_recordings(recordings)

    run_report(recordings, tmp_path / "out")

    data = json.loads((tmp_path / "out" / "comparison.json").read_text())

    assert data["metadata"]["viewing_distance_cm"] == 60.0
    assert len(data["results"]) == 2


def test_per_target_table_has_ten_rows(tmp_path):
    recordings = tmp_path / "recordings"
    recordings.mkdir()
    write_example_recordings(recordings)

    run_report(recordings, tmp_path / "out")

    data = json.loads((tmp_path / "out" / "per_target.json").read_text())

    assert len(data["results"]) == 10


def test_main_prints_the_comparison(tmp_path, capsys):
    recordings = tmp_path / "recordings"
    recordings.mkdir()
    write_example_recordings(recordings)

    main([str(recordings)], out_dir=tmp_path / "out")

    output = capsys.readouterr().out

    assert "simulated_tracker" in output
    assert "simulated_webcam" in output
    assert "Best accuracy: simulated_tracker" in output