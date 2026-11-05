from src.samples import generate_gaze_samples
from src.trial import summarize_target


TARGETS = [
    (500, 350),
    (100, 100),
    (900, 100),
    (100, 600),
    (900, 600),
]


def run_benchmark(n_samples=60, noise=10, loss_rate=0.05, seed=None):
    """
    Run the benchmark with many gaze samples per target.

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

        results.append(
            summarize_target(
                target_id,
                target_x,
                target_y,
                samples
            )
        )

    return results


def format_result(result):
    """Turn one result dict into a readable line."""

    accuracy = result["accuracy_px"]
    precision = result["precision_px"]

    accuracy_text = "n/a" if accuracy is None else f"{accuracy:.2f}px"
    precision_text = "n/a" if precision is None else f"{precision:.2f}px"

    return (
        f"Target {result['target_id']} "
        f"({result['target_x']}, {result['target_y']}): "
        f"accuracy={accuracy_text} "
        f"precision={precision_text} "
        f"data_loss={result['data_loss']:.1%} "
        f"valid={result['n_valid']}/{result['n_samples']}"
    )


if __name__ == "__main__":
    for result in run_benchmark():
        print(format_result(result))