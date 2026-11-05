"""Simulated multi-sample gaze data for one target."""

import random


def generate_gaze_samples(
    target_x,
    target_y,
    n_samples=60,
    noise=10,
    loss_rate=0.0,
    seed=None
):
    """
    Simulate many gaze samples around one target.

    A lost sample (the tracker could not find the eye) is None.
    Passing a seed makes the samples repeatable.

    This is test data and does not represent
    real eye-tracking measurements.

    Returns:
        list: (x, y) tuples, or None for lost samples
    """

    if n_samples < 1:
        raise ValueError("n_samples must be at least 1")

    if not 0 <= loss_rate <= 1:
        raise ValueError("loss_rate must be between 0 and 1")

    rng = random.Random(seed)

    samples = []

    for _ in range(n_samples):
        if rng.random() < loss_rate:
            samples.append(None)
        else:
            samples.append(
                (
                    target_x + rng.randint(-noise, noise),
                    target_y + rng.randint(-noise, noise)
                )
            )

    return samples