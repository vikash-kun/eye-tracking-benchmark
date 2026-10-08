from src.gaze import generate_gaze_point
from src.metrics import calculate_trial_result


TARGETS = [
    (500, 350),
    (100, 100),
    (900, 100),
    (100, 600),
    (900, 600),
]


def run_benchmark():
    results = []

    for target_id, (target_x, target_y) in enumerate(
        TARGETS,
        start=1
    ):
        gaze = generate_gaze_point(
            target_x,
            target_y,
            noise=10
        )

        result = calculate_trial_result(
            target_x,
            target_y,
            gaze.x,
            gaze.y
        )

        result["target_id"] = target_id
        result["timestamp"] = gaze.timestamp

        results.append(result)

    return results


if __name__ == "__main__":
    results = run_benchmark()

    for result in results:
        print(result)