import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ScreenSetup:
    

    width_px: int = 1920
    width_cm: float = 34.5
    viewing_distance_cm: float = 60.0

    def __post_init__(self):
        if (
            self.width_px <= 0
            or self.width_cm <= 0
            or self.viewing_distance_cm <= 0
        ):
            raise ValueError("screen setup values must be positive")

    @property
    def cm_per_pixel(self):
        return self.width_cm / self.width_px


DEFAULT_SETUP = ScreenSetup()


def pixels_to_degrees(distance_px, setup=DEFAULT_SETUP):
    

    distance_cm = distance_px * setup.cm_per_pixel

    return math.degrees(
        2 * math.atan(distance_cm / (2 * setup.viewing_distance_cm))
    )


def add_visual_angles(result, setup=DEFAULT_SETUP):
    

    converted = dict(result)

    for name in ("accuracy", "precision"):
        pixels = result[f"{name}_px"]

        converted[f"{name}_deg"] = (
            None if pixels is None else pixels_to_degrees(pixels, setup)
        )

    return converted