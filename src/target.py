import tkinter as tk
import csv
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
TARGET_RADIUS = 10
TARGET_DURATION = 2000  


def create_window():
    window = tk.Tk()

    window.title("Eye-Tracking Benchmark")
    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    window.configure(bg="white")

    return window


def create_canvas(window):
    canvas = tk.Canvas(
        window,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        bg="white",
        highlightthickness=0
    )

    canvas.pack()

    return canvas


def show_target(canvas, x, y):
    canvas.delete("all")

    canvas.create_oval(
        x - TARGET_RADIUS,
        y - TARGET_RADIUS,
        x + TARGET_RADIUS,
        y + TARGET_RADIUS,
        fill="red"
    )


def save_trial_data(trials):
    with open("data/target_trials.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "target_id",
                "target_x",
                "target_y",
                "timestamp"
            ]
        )

        writer.writeheader()
        writer.writerows(trials)


def run_benchmark(window, canvas, targets, current_index, trials):
    if current_index >= len(targets):
        save_trial_data(trials)

        canvas.delete("all")

        canvas.create_text(
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2,
            text="Benchmark Complete",
            font=("Arial", 24),
            fill="black"
        )

        print("Benchmark completed.")
        print("Trial data saved to data/target_trials.csv")

        return

    x, y = targets[current_index]

    target_id = current_index + 1

    timestamp = datetime.now().isoformat(timespec="seconds")

    trial = {
        "target_id": target_id,
        "target_x": x,
        "target_y": y,
        "timestamp": timestamp
    }

    trials.append(trial)

    print(
        f"Target {target_id}: "
        f"({x}, {y}) "
        f"at {timestamp}"
    )

    show_target(canvas, x, y)

    window.after(
        TARGET_DURATION,
        lambda: run_benchmark(
            window,
            canvas,
            targets,
            current_index + 1,
            trials
        )
    )


if __name__ == "__main__":
    window = create_window()

    canvas = create_canvas(window)

    targets = [
        (500, 350),
        (100, 100),
        (900, 100),
        (100, 600),
        (900, 600),
    ]

    trials = []

    run_benchmark(
        window,
        canvas,
        targets,
        0,
        trials
    )

    window.mainloop()