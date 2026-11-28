"""Print and export a comparison of devices from a folder of recordings."""

import sys
from dataclasses import asdict
from pathlib import Path

from src.angle import DEFAULT_SETUP
from src.compare import (
    best_device,
    compare_devices,
    devices_from_folder,
    per_target_table,
)
from src.export import export_all


PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = PROJECT_ROOT / "examples"
DATA_DIR = PROJECT_ROOT / "data"


def format_comparison(comparison):
    """Turn the device comparison table into readable text."""

    table = comparison.copy()
    table["data_loss"] = (table["data_loss"] * 100).round(1).astype(str) + "%"

    return table.round(2).to_string(index=False)


def run_report(folder=EXAMPLES_DIR, out_dir=DATA_DIR, setup=DEFAULT_SETUP):
    """
    Compare every recording in a folder and export the results.

    Writes comparison.csv/json (one row per device) and
    per_target.csv/json (one row per device and target) into out_dir.

    Returns:
        DataFrame: the device comparison
    """

    devices = devices_from_folder(folder, setup)
    comparison = compare_devices(devices)

    metadata = {"source": str(folder), **asdict(setup)}

    export_all(comparison, out_dir, name="comparison", metadata=metadata)
    export_all(
        per_target_table(devices),
        out_dir,
        name="per_target",
        metadata=metadata
    )

    return comparison


def main(argv=None, out_dir=DATA_DIR):
    """Command line entry point: python -m src.report [folder]"""

    args = sys.argv[1:] if argv is None else argv
    folder = args[0] if args else EXAMPLES_DIR

    comparison = run_report(folder, out_dir)

    print(format_comparison(comparison))
    print()
    print(f"Best accuracy: {best_device(comparison)}")
    print(f"Results written to {out_dir}")


if __name__ == "__main__":
    main()