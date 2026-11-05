import math

import pytest

from src.trial import (
    calculate_accuracy,
    calculate_data_loss,
    get_valid_samples,
    summarize_target,
)


def test_get_valid_samples_drops_none():
    points = [(1, 2), None, (3, 4)]

    assert get_valid_samples(points) == [(1, 2), (3, 4)]


def test_accuracy_is_mean_error_of_valid_samples():
    points = [(503, 354), (500, 350), None]

    # errors are 5 and 0, so the mean is 2.5
    assert calculate_accuracy(500, 350, points) == pytest.approx(2.5)


def test_accuracy_is_none_when_everything_is_lost():
    assert calculate_accuracy(500, 350, [None, None]) is None


def test_data_loss_fraction():
    points = [(1, 1), None, (2, 2), (3, 3)]

    assert calculate_data_loss(points) == pytest.approx(0.25)


def test_data_loss_for_empty_input():
    assert calculate_data_loss([]) == 0.0


def test_summarize_target_values():
    points = [(490, 340), (510, 360), None, (500, 350)]

    summary = summarize_target(1, 500, 350, points)

    assert summary["target_id"] == 1
    assert summary["n_samples"] == 4
    assert summary["n_valid"] == 3
    assert summary["data_loss"] == pytest.approx(0.25)
    assert summary["accuracy_px"] == pytest.approx(
        2 * math.sqrt(200) / 3
    )
    assert summary["precision_px"] == pytest.approx(
        math.sqrt(400 / 3)
    )


def test_summarize_target_when_everything_is_lost():
    summary = summarize_target(2, 100, 100, [None, None, None])

    assert summary["n_valid"] == 0
    assert summary["accuracy_px"] is None
    assert summary["precision_px"] is None
    assert summary["data_loss"] == 1.0