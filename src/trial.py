"""Per-target accuracy, precision and data loss from many gaze samples."""

from src.metrics import calculate_precision, calculate_spatial_error


def get_valid_samples(gaze_points):
    """Drop lost samples (None) and keep the real (x, y) points."""
    return [point for point in gaze_points if point is not None]


def calculate_accuracy(target_x, target_y, gaze_points):
    """
    Accuracy: mean spatial error (pixels) over the valid samples.

    Returns None when every sample was lost, so a failed target
    is never mistaken for a perfect one.
    """

    valid = get_valid_samples(gaze_points)

    if not valid:
        return None

    errors = [
        calculate_spatial_error(target_x, target_y, x, y)
        for x, y in valid
    ]

    return sum(errors) / len(errors)


def calculate_data_loss(gaze_points):
    """Fraction of samples that were lost (0.0 to 1.0)."""

    if not gaze_points:
        return 0.0

    lost = sum(1 for point in gaze_points if point is None)

    return lost / len(gaze_points)


def summarize_target(target_id, target_x, target_y, gaze_points):
    """
    Summarize one target: accuracy, precision and data loss.

    Returns:
        dict: one row of benchmark results for this target
    """

    valid = get_valid_samples(gaze_points)

    return {
        "target_id": target_id,
        "target_x": target_x,
        "target_y": target_y,
        "n_samples": len(gaze_points),
        "n_valid": len(valid),
        "accuracy_px": calculate_accuracy(target_x, target_y, gaze_points),
        "precision_px": calculate_precision(valid) if valid else None,
        "data_loss": calculate_data_loss(gaze_points)
    }