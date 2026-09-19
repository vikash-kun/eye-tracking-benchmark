import tkinter as tk


def create_window():
    window = tk.Tk()

    window.title("Eye-Tracking Benchmark")
    window.geometry("1000x700")
    window.configure(bg="white")

    return window


def show_target(window, x, y):
    canvas = tk.Canvas(
        window,
        width=1000,
        height=700,
        bg="white",
        highlightthickness=0
    )

    canvas.pack()

    radius = 10

    canvas.create_oval(
        x - radius,
        y - radius,
        x + radius,
        y + radius,
        fill="red"
    )


if __name__ == "__main__":
    window = create_window()

    targets = [
        (500, 350),
        (100, 100),
        (900, 100),
        (100, 600),
        (900, 600),
    ]

    for x, y in targets:
        print(f"Target position: ({x}, {y})")

    show_target(window, *targets[0])

    window.mainloop()