import pytest

from src.samples import generate_gaze_samples


def test_returns_requested_number_of_samples():
    samples = generate_gaze_samples(500, 350, n_samples=25, seed=1)

    assert len(samples) == 25


def test_samples_stay_within_noise_of_target():
    samples = generate_gaze_samples(
        500, 350, n_samples=100, noise=10, seed=1
    )

    for x, y in samples:
        assert 490 <= x <= 510
        assert 340 <= y <= 360


def test_no_lost_samples_when_loss_rate_is_zero():
    samples = generate_gaze_samples(
        500, 350, n_samples=50, loss_rate=0.0, seed=1
    )

    assert None not in samples


def test_all_samples_lost_when_loss_rate_is_one():
    samples = generate_gaze_samples(
        500, 350, n_samples=50, loss_rate=1.0, seed=1
    )

    assert all(sample is None for sample in samples)


def test_same_seed_gives_same_samples():
    first = generate_gaze_samples(500, 350, loss_rate=0.2, seed=42)
    second = generate_gaze_samples(500, 350, loss_rate=0.2, seed=42)

    assert first == second


def test_invalid_loss_rate_raises():
    with pytest.raises(ValueError):
        generate_gaze_samples(500, 350, loss_rate=1.5)


def test_zero_samples_raises():
    with pytest.raises(ValueError):
        generate_gaze_samples(500, 350, n_samples=0)