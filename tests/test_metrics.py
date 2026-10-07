from src.metrics import (
    calculate_spatial_error,
    calculate_precision
)


def test_zero_error():
    error = calculate_spatial_error(
        500, 350,
        500, 350
    )

    assert error == 0


def test_known_distance():
    error = calculate_spatial_error(
        500, 350,
        503, 354
    )

    assert error == 5
def test_precision_for_identical_points():
    gaze_points = [
        (500, 350),
        (500, 350),
        (500, 350),
        (500, 350)
    ]

    precision = calculate_precision(gaze_points)

    assert precision == 0


def test_precision_detects_spread():
    gaze_points = [
        (490, 340),
        (510, 360)
    ]

    precision = calculate_precision(gaze_points)

    assert precision > 0


def test_precision_empty_input():
    precision = calculate_precision([])

    assert precision == 0.0    