from core.metrics import (
    direction_changes,
    euclidean_distance,
    jitter_score,
    msi_score,
    path_length,
    smoothness_score,
    speed_consistency,
)


def test_euclidean_distance() -> None:
    assert euclidean_distance((0, 0), (3, 4)) == 5.0


def test_path_length() -> None:
    points = [(0, 0), (3, 4), (6, 8)]
    assert path_length(points) == 10.0


def test_jitter_score_non_negative() -> None:
    points = [(0, 0), (1, 0), (2, 0), (3, 0)]
    assert jitter_score(points) >= 0.0


def test_direction_changes_for_straight_line() -> None:
    points = [(0, 0), (1, 0), (2, 0), (3, 0)]
    assert direction_changes(points) == 0


def test_speed_consistency_range() -> None:
    points = [(0, 0), (1, 0), (2, 0), (3, 0)]
    timestamps = [0.0, 1.0, 2.0, 3.0]
    score = speed_consistency(points, timestamps)
    assert 0.0 <= score <= 1.0


def test_smoothness_range() -> None:
    points = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    score = smoothness_score(points)
    assert 0.0 <= score <= 1.0


def test_msi_range() -> None:
    points = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    timestamps = [0.0, 1.0, 2.0, 3.0, 4.0]
    score = msi_score(points, timestamps)
    assert 0.0 <= score <= 100.0