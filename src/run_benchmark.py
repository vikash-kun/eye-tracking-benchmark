from src.angle import DEFAULT_SETUP, add_visual_angles
from src.samples import generate_gaze_samples
from src.trial import summarize_target


TARGETS = [
    (500, 350),
    (100, 100),
    (900, 100),
    (100, 600),
    (900, 600),
]


def run_benchmark(
    n_samples=60,
    noise=10,
    loss_rate=0.05,
    seed=None,
    setup=DEFAULT_SETUP
):
    """
    Run the benchmark with many gaze samples per target.

    Accuracy and precision are reported in pixels and in degrees
    of visual angle, using the screen setup given.

    Returns:
        list: one summary dict per target
    """

    results = []

    for target_id, (target_x, target_y) in enumerate(
        TARGETS,
        start=1
    ):
        target_seed = None if seed is None else seed + target_id

        samples = generate_gaze_samples(
            target_x,
            target_y,
            n_samples=n_samples,
            noise=noise,
            loss_rate=loss_rate,
            seed=target_seed
        )

        summary = summarize_target(
            target_id,
            target_x,
            target_y,
            samples
        )

        results.append(add_visual_angles(summary, setup))

    return results


def format_value(pixels, degrees):
    """Show a value in pixels and, when known, in degrees."""

    if pixels is None:
        return "n/a"

    text = f"{pixels:.2f}px"

    if degrees is not None:
        text += f" ({degrees:.2f} deg)"

    return text


def format_result(result):
    """Turn one result dict into a readable line."""

    accuracy = format_value(
        result["accuracy_px"],
        result.get("accuracy_deg")
    )
    precision = format_value(
        result["precision_px"],
        result.get("precision_deg")
    )

    return (
        f"Target {result['target_id']} "
        f"({result['target_x']}, {result['target_y']}): "
        f"accuracy={accuracy} "
        f"precision={precision} "
        f"data_loss={result['data_loss']:.1%} "
        f"valid={result['n_valid']}/{result['n_samples']}"
    )


if __name__ == "__main__":
    for result in run_benchmark():
        print(format_result(result))