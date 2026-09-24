import math


def calculate_spatial_error(
    target_x,
    target_y,
    gaze_x,
    gaze_y
):
    """
    Calculate the Euclidean distance between
    the target position and gaze position.

    Returns:
        float: spatial error in pixels
    """

    dx = gaze_x - target_x
    dy = gaze_y - target_y

    distance = math.sqrt(
        dx ** 2 + dy ** 2
    )

    return distance