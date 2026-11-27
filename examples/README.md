# Example recordings

These two files are simulated gaze recordings in the CSV format the benchmark can read. They are generated test data and are not measurements from real devices.

- simulated_tracker.csv: low noise, a small offset and little data loss, like a well calibrated external tracker
- simulated_webcam.csv: high noise, a larger offset and more data loss, like a webcam-based tracker

Both files have 60 samples for each of the five targets, at 30 samples per second. Recreate them with `python -m src.simulate` from the project root.