# Eye-Tracking Accuracy Benchmarking and Validation Tool

A Python tool that measures how accurate and precise an eye tracker is. It presents known targets on screen, compares the recorded gaze against them, and reports gaze error, stability and data loss, so webcam-based tracking and external devices can be compared in the same way. The longer-term goal is to run it as a study type or pre-study validation step in RUXAILAB.

## Status

Early development. The full pipeline currently runs on simulated gaze data. Importing real device data, device comparison, plots and the RUXAILAB integration are still to come (see Roadmap).

## What works now

- A target display window that shows known targets one at a time
- Simulated gaze data with noise and lost samples, repeatable with a seed
- Per-target accuracy, precision and data loss
- Conversion of pixel errors to degrees of visual angle
- Export of results to CSV and JSON

## Setup

```
pip install -r requirements.txt
```

## Usage

Run all commands from the project root.

Run the benchmark on simulated data and print one line per target:

```
python -m src.run_benchmark
```

Show the targets in a window (needs a display):

```
python -m src.target
```

Run the tests:

```
python -m pytest
```

## Metrics

- Accuracy: the mean distance between the valid gaze samples and the target. Lower is better.
- Precision: the combined standard deviation of the x and y positions of the valid gaze samples, which shows how stable the gaze is. Lower is better.
- Data loss: the fraction of samples where the tracker did not return a gaze point.
- Visual angle: accuracy and precision are also given in degrees, using the screen width in pixels, the screen width in centimeters and the viewing distance. The defaults in `src/angle.py` describe a laptop viewed from 60 cm, so replace them with the values of the device under test.

A target where every sample is lost has no accuracy or precision value (they are left empty) rather than a value of 0.

## Project structure

```
src/
  target.py         target display window
  gaze.py           single simulated gaze point
  samples.py        many simulated gaze samples per target
  metrics.py        spatial error and precision
  trial.py          accuracy, precision and data loss per target
  angle.py          pixels to degrees of visual angle
  run_benchmark.py  runs the benchmark across all targets
  export.py         CSV and JSON export
tests/              pytest tests for each module
data/               generated results (CSV and JSON files are not committed)
```

## Roadmap

- Import real gaze data from webcam and external eye trackers
- Compare results across devices and setups
- Plots of gaze error and stability
- Command-line interface
- RUXAILAB integration as a study type or pre-study validation step