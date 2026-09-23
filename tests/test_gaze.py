from src.gaze import generate_gaze_point


def test_gaze_point_is_near_target():
    target_x = 500
    target_y = 350

    gaze = generate_gaze_point(
        target_x,
        target_y,
        noise=10
    )

    assert 490 <= gaze.x <= 510
    assert 340 <= gaze.y <= 360