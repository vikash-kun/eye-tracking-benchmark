import math

from src.run_benchmark import TARGETS, format_result, run_benchmark


def test_one_result_per_target():
    assert len(run_benchmark(seed=1)) == len(TARGETS)


def test_result_has_expected_keys():
    result = run_benchmark(seed=1)[0]

    assert set(result) == {
        "target_id",
        "target_x",
        "target_y",
        "n_samples",
        "n_valid",
        "accuracy_px",
        "precision_px",
        "data_loss",
    }


def test_same_seed_gives_same_results():
    assert run_benchmark(seed=7) == run_benchmark(seed=7)


def test_accuracy_is_bounded_by_noise():
    # with noise=10 no sample is farther than 10 * sqrt(2) from its target
    for result in run_benchmark(noise=10, seed=3):
        assert result["accuracy_px"] <= 10 * math.sqrt(2)


def test_no_loss_when_loss_rate_is_zero():
    for result in run_benchmark(loss_rate=0.0, seed=3):
        assert result["data_loss"] == 0.0
        assert result["n_valid"] == result["n_samples"]


def test_format_result_handles_failed_target():
    result = {
        "target_id": 1,
        "target_x": 500,
        "target_y": 350,
        "n_samples": 10,
        "n_valid": 0,
        "accuracy_px": None,
        "precision_px": None,
        "data_loss": 1.0,
    }

    assert "n/a" in format_result(result)