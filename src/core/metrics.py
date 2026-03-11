from __future__ import annotations

from typing import Sequence, Tuple
import math
import numpy as np

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


def step_distances(points: Sequence[Point]) -> np.ndarray:
    """Return step-to-step distances as a numpy array."""
    if len(points) < 2:
        return np.array([], dtype=float)

    pos = np.array(points, dtype=float)
    dx = np.diff(pos[:, 0])
    dy = np.diff(pos[:, 1])
    return np.sqrt(dx**2 + dy**2)


def jitter_score(points: Sequence[Point]) -> float:
    """
    Estimate jitter as the standard deviation of step distances.
    Higher score suggests more instability or micro-movement noise.
    """
    distances = step_distances(points)
    if len(distances) == 0:
        return 0.0
    return float(np.std(distances))


def speed_consistency(points: Sequence[Point], timestamps: Sequence[float]) -> float:
    """
    Return a normalized score in [0, 1].
    Higher = more stable speed profile.
    """
    if len(points) < 2 or len(timestamps) < 2:
        return 0.0

    distances = step_distances(points)
    times = np.diff(np.array(timestamps, dtype=float))

    valid = times > 0
    if not np.any(valid):
        return 0.0

    speeds = distances[valid] / times[valid]
    if len(speeds) < 2:
        return 1.0

    mean_speed = float(np.mean(speeds))
    std_speed = float(np.std(speeds))

    if mean_speed <= 1e-9:
        return 0.0

    coeff_var = std_speed / mean_speed
    score = 1.0 / (1.0 + coeff_var)
    return float(max(0.0, min(1.0, score)))


def direction_changes(points: Sequence[Point], angle_threshold_degrees: float = 45.0) -> int:
    """
    Count how many times the trajectory changes direction sharply.
    """
    if len(points) < 3:
        return 0

    pos = np.array(points, dtype=float)

    v1 = pos[1:-1] - pos[:-2]
    v2 = pos[2:] - pos[1:-1]

    count = 0
    threshold = math.radians(angle_threshold_degrees)

    for a, b in zip(v1, v2):
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        if norm_a < 1e-9 or norm_b < 1e-9:
            continue

        cos_theta = float(np.dot(a, b) / (norm_a * norm_b))
        cos_theta = max(-1.0, min(1.0, cos_theta))
        angle = math.acos(cos_theta)

        if angle > threshold:
            count += 1

    return count


def smoothness_score(points: Sequence[Point]) -> float:
    """
    Estimate movement smoothness from acceleration variation.
    Higher = smoother signal.
    """
    if len(points) < 4:
        return 0.0

    distances = step_distances(points)
    if len(distances) < 3:
        return 0.0

    velocity = np.diff(distances)
    acceleration = np.diff(velocity)

    if len(acceleration) == 0:
        return 1.0

    acc_std = float(np.std(acceleration))
    score = 1.0 / (1.0 + acc_std)
    return float(max(0.0, min(1.0, score)))


def normalized_direction_score(points: Sequence[Point]) -> float:
    """
    Convert raw direction changes into a normalized [0, 1] score.
    Higher = fewer abrupt changes.
    """
    if len(points) < 3:
        return 0.0

    changes = direction_changes(points)
    possible_changes = max(1, len(points) - 2)

    ratio = changes / possible_changes
    score = 1.0 - ratio
    return float(max(0.0, min(1.0, score)))


def msi_score(
    points: Sequence[Point],
    timestamps: Sequence[float],
) -> float:
    """
    Motor Stability Index in [0, 100].
    Combines jitter, smoothness, direction stability and speed consistency.
    """
    jitter = jitter_score(points)
    jitter_component = 1.0 / (1.0 + jitter)

    smoothness = smoothness_score(points)
    direction = normalized_direction_score(points)
    speed = speed_consistency(points, timestamps)

    weighted = (
        0.35 * jitter_component
        + 0.25 * smoothness
        + 0.20 * direction
        + 0.20 * speed
    )

    return float(round(max(0.0, min(1.0, weighted)) * 100.0, 2))