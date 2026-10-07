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

def calculate_precision(gaze_points):
    """
    Calculate gaze precision using the standard deviation
    of the X and Y coordinates.

    Args:
        gaze_points: list of (x, y) gaze coordinates

    Returns:
        float: combined spatial standard deviation
    """

    if not gaze_points:
        return 0.0

    x_values = [point[0] for point in gaze_points]
    y_values = [point[1] for point in gaze_points]

    x_mean = sum(x_values) / len(x_values)
    y_mean = sum(y_values) / len(y_values)

    x_variance = sum(
        (x - x_mean) ** 2
        for x in x_values
    ) / len(x_values)

    y_variance = sum(
        (y - y_mean) ** 2
        for y in y_values
    ) / len(y_values)

    x_std = math.sqrt(x_variance)
    y_std = math.sqrt(y_variance)

    precision = math.sqrt(
        x_std ** 2 + y_std ** 2
    )

    return precision    