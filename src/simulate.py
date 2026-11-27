"""
Create example gaze recordings (CSV) from simulated devices.

These recordings are test data. They do not represent real
eye-tracking measurements or real devices.
"""

from pathlib import Path

import pandas as pd

from src.run_benchmark import TARGETS
from src.samples import generate_gaze_samples


EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"

DEVICE_PROFILES = {
    "simulated_tracker": {
        "noise": 15,
        "loss_rate": 0.02,
        "offset": (5, -3),
        "seed": 100,
    },
    "simulated_webcam": {
        "noise": 80,
        "loss_rate": 0.10,
        "offset": (30, -20),
        "seed": 200,
    },
}


def simulate_recording(
    noise,
    loss_rate,
    offset=(0, 0),
    n_samples=60,
    sample_rate_hz=30,
    seed=None
):
    """
    Simulate a full recording: n_samples gaze samples for every target.

    The offset shifts every sample by a fixed amount (in pixels), like
    the systematic error of a poorly calibrated device.

    Returns:
        DataFrame: one row per gaze sample, in the CSV format that
        load_gaze_csv reads
    """

    rows = []

    for target_id, (target_x, target_y) in enumerate(TARGETS, start=1):
        target_seed = None if seed is None else seed + target_id

        samples = generate_gaze_samples(
            target_x,
            target_y,
            n_samples=n_samples,
            noise=noise,
            loss_rate=loss_rate,
            seed=target_seed
        )

        for index, sample in enumerate(samples):
            if sample is None:
                gaze_x = gaze_y = None
            else:
                gaze_x = sample[0] + offset[0]
                gaze_y = sample[1] + offset[1]

            rows.append(
                {
                    "target_id": target_id,
                    "target_x": target_x,
                    "target_y": target_y,
                    "timestamp_ms": round(index * 1000 / sample_rate_hz),
                    "gaze_x": gaze_x,
                    "gaze_y": gaze_y,
                }
            )

    df = pd.DataFrame(rows)

    # whole numbers with blanks for lost samples (not 503.0 and NaN)
    df[["gaze_x", "gaze_y"]] = df[["gaze_x", "gaze_y"]].astype("Int64")

    return df


def write_examples():
    """Write one example CSV per device profile into examples/."""

    EXAMPLES_DIR.mkdir(exist_ok=True)

    paths = []

    for name, profile in DEVICE_PROFILES.items():
        path = EXAMPLES_DIR / f"{name}.csv"
        simulate_recording(**profile).to_csv(path, index=False)
        paths.append(path)

    return paths


if __name__ == "__main__":
    for path in write_examples():
        print(f"Wrote {path}")