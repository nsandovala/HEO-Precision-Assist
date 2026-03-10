from core.metrics import euclidean_distance, path_length, jitter_score


def test_euclidean_distance() -> None:
    assert euclidean_distance((0, 0), (3, 4)) == 5.0


def test_path_length() -> None:
    points = [(0, 0), (3, 4), (6, 8)]
    assert path_length(points) == 10.0


def test_jitter_score() -> None:
    points = [(0, 0), (1, 0), (2, 0)]
    assert jitter_score(points) == 1.0