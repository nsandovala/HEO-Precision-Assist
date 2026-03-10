from __future__ import annotations

from typing import Iterable, Sequence, Tuple
import math


Point = Tuple[float, float]


def euclidean_distance(p1: Point, p2: Point) -> float:
    """Return Euclidean distance between two 2D points."""
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def path_length(points: Sequence[Point]) -> float:
    """Return total path length across a sequence of points."""
    if len(points) < 2:
        return 0.0

    total = 0.0
    for i in range(1, len(points)):
        total += euclidean_distance(points[i - 1], points[i])
    return total


def jitter_score(points: Sequence[Point]) -> float:
    """
    Estimate jitter as average step-to-step movement.
    Higher score suggests more instability or micro-movement noise.
    """
    if len(points) < 2:
        return 0.0

    distances = []
    for i in range(1, len(points)):
        distances.append(euclidean_distance(points[i - 1], points[i]))

    return sum(distances) / len(distances)