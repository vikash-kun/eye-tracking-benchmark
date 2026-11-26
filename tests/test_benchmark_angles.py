import pytest

from src.angle import ScreenSetup, pixels_to_degrees
from src.run_benchmark import format_result, run_benchmark


def test_results_include_degrees():
    for result in run_benchmark(seed=1):
        assert result["accuracy_deg"] > 0
        assert result["precision_deg"] > 0


def test_degrees_follow_the_screen_setup():
    setup = ScreenSetup(width_px=1000, width_cm=30, viewing_distance_cm=50)

    result = run_benchmark(seed=1, setup=setup)[0]

    assert result["accuracy_deg"] == pytest.approx(
        pixels_to_degrees(result["accuracy_px"], setup)
    )


def test_failed_target_has_no_degrees():
    result = run_benchmark(loss_rate=1.0, seed=1)[0]

    assert result["accuracy_deg"] is None
    assert result["precision_deg"] is None


def test_format_result_shows_degrees():
    result = run_benchmark(seed=1)[0]

    assert "deg" in format_result(result)