import pytest

from src.loader import load_gaze_csv, summarize_csv

HEADER = "target_id,target_x,target_y,gaze_x,gaze_y\n"


def write_csv(tmp_path, body, header=HEADER):
    path = tmp_path / "recording.csv"
    path.write_text(header + body, encoding="utf-8")
    return path


def test_load_valid_recording(tmp_path):
    path = write_csv(tmp_path, "1,100,100,103,104\n1,100,100,100,100\n")

    df = load_gaze_csv(path)

    assert len(df) == 2
    assert list(df.columns) == [
        "target_id", "target_x", "target_y", "gaze_x", "gaze_y"
    ]


def test_missing_column_raises(tmp_path):
    path = write_csv(
        tmp_path,
        "1,100,100,103\n",
        header="target_id,target_x,target_y,gaze_x\n",
    )

    with pytest.raises(ValueError, match="gaze_y"):
        load_gaze_csv(path)


def test_empty_recording_raises(tmp_path):
    path = write_csv(tmp_path, "")

    with pytest.raises(ValueError):
        load_gaze_csv(path)


def test_non_numeric_gaze_raises(tmp_path):
    path = write_csv(tmp_path, "1,100,100,abc,104\n")

    with pytest.raises(ValueError):
        load_gaze_csv(path)


def test_empty_target_position_raises(tmp_path):
    path = write_csv(tmp_path, "1,,100,103,104\n")

    with pytest.raises(ValueError):
        load_gaze_csv(path)


def test_summary_values(tmp_path):
    # errors are 5 and 0 (one sample is lost), so accuracy is 2.5
    path = write_csv(
        tmp_path,
        "1,100,100,103,104\n1,100,100,100,100\n1,100,100,,\n",
    )

    result = summarize_csv(path)[0]

    assert result["target_id"] == 1
    assert result["n_samples"] == 3
    assert result["n_valid"] == 2
    assert result["accuracy_px"] == pytest.approx(2.5)
    assert result["data_loss"] == pytest.approx(1 / 3)
    assert result["accuracy_deg"] > 0


def test_one_blank_coordinate_counts_as_lost(tmp_path):
    path = write_csv(tmp_path, "1,100,100,103,\n1,100,100,100,100\n")

    result = summarize_csv(path)[0]

    assert result["n_valid"] == 1
    assert result["data_loss"] == pytest.approx(0.5)


def test_one_result_per_target(tmp_path):
    path = write_csv(
        tmp_path,
        "1,100,100,101,101\n2,500,350,502,352\n1,100,100,99,99\n",
    )

    results = summarize_csv(path)

    assert [result["target_id"] for result in results] == [1, 2]
    assert results[0]["n_samples"] == 2


def test_failed_target_has_no_accuracy(tmp_path):
    path = write_csv(tmp_path, "1,100,100,,\n1,100,100,,\n")

    result = summarize_csv(path)[0]

    assert result["accuracy_px"] is None
    assert result["data_loss"] == 1.0


def test_target_with_two_positions_raises(tmp_path):
    path = write_csv(tmp_path, "1,100,100,101,101\n1,200,200,201,201\n")

    with pytest.raises(ValueError):
        summarize_csv(path)