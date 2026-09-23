from dataclasses import dataclass
import random
from datetime import datetime


@dataclass
class GazePoint:
    x: float
    y: float
    timestamp: str


def generate_gaze_point(target_x, target_y, noise=10):
    """
    Generate simulated gaze data around a target.

    This is test data and does not represent
    real eye-tracking measurements.
    """

    gaze_x = target_x + random.randint(-noise, noise)
    gaze_y = target_y + random.randint(-noise, noise)

    timestamp = datetime.now().isoformat(timespec="seconds")

    return GazePoint(
        x=gaze_x,
        y=gaze_y,
        timestamp=timestamp
    )

if __name__ == "__main__":
    targets = [
        (500, 350),
        (100, 100),
        (900, 100),
        (100, 600),
        (900, 600),
    ]

    for target_id, (target_x, target_y) in enumerate(targets, start=1):
        gaze = generate_gaze_point(
            target_x,
            target_y
        )

        print(
            f"Target {target_id}: "
            f"target=({target_x}, {target_y}) "
            f"gaze=({gaze.x}, {gaze.y}) "
            f"time={gaze.timestamp}"
        )