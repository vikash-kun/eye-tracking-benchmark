from src.metrics import calculate_spatial_error


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