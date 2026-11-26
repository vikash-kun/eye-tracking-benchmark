import pytest

from src.angle import ScreenSetup, add_visual_angles, pixels_to_degrees

SETUP = ScreenSetup(width_px=1000, width_cm=10, viewing_distance_cm=57.3)


def test_cm_per_pixel():
    assert SETUP.cm_per_pixel == pytest.approx(0.01)


def test_zero_pixels_is_zero_degrees():
    assert pixels_to_degrees(0, SETUP) == 0


def test_one_cm_at_57_cm_is_about_one_degree():
    # 100 px * 0.01 cm per px = 1 cm on screen
    assert pixels_to_degrees(100, SETUP) == pytest.approx(1.0, abs=0.01)


def test_larger_distance_gives_larger_angle():
    assert pixels_to_degrees(200, SETUP) > pixels_to_degrees(100, SETUP)


def test_sitting_further_away_shrinks_the_angle():
    far = ScreenSetup(width_px=1000, width_cm=10, viewing_distance_cm=114.6)

    assert pixels_to_degrees(100, far) < pixels_to_degrees(100, SETUP)


@pytest.mark.parametrize(
    "values",
    [
        {"width_px": 0},
        {"width_cm": -5},
        {"viewing_distance_cm": 0},
    ],
)
def test_invalid_setup_raises(values):
    with pytest.raises(ValueError):
        ScreenSetup(**values)


def test_add_visual_angles_adds_degree_columns():
    result = {"accuracy_px": 100, "precision_px": 50}

    converted = add_visual_angles(result, SETUP)

    assert converted["accuracy_px"] == 100
    assert converted["accuracy_deg"] == pytest.approx(
        pixels_to_degrees(100, SETUP)
    )
    assert converted["precision_deg"] == pytest.approx(
        pixels_to_degrees(50, SETUP)
    )


def test_add_visual_angles_does_not_change_the_input():
    result = {"accuracy_px": 100, "precision_px": 50}

    add_visual_angles(result, SETUP)

    assert "accuracy_deg" not in result


def test_add_visual_angles_keeps_none():
    result = {"accuracy_px": None, "precision_px": None}

    converted = add_visual_angles(result, SETUP)

    assert converted["accuracy_deg"] is None
    assert converted["precision_deg"] is None