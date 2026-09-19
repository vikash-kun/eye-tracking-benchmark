import tkinter as tk


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
TARGET_RADIUS = 10


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

    for x, y in targets:
        print(f"Target position: ({x}, {y})")

    show_target(canvas, *targets[0])

    window.mainloop()