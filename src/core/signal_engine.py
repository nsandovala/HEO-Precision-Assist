from __future__ import annotations

from typing import Sequence, Tuple

from core.metrics import (
    direction_changes,
    jitter_score,
    msi_score,
    path_length,
    smoothness_score,
    speed_consistency,
)

Point = Tuple[float, float]


def analyze_signal(points: Sequence[Point], timestamps: Sequence[float]) -> dict:
    """Analyze a captured pointer signal and return core motor metrics."""
    samples = len(points)
    total_path = path_length(points)
    jitter = jitter_score(points)
    smoothness = smoothness_score(points)
    directions = direction_changes(points)
    speed_score = speed_consistency(points, timestamps)
    msi = msi_score(points, timestamps)

    duration = 0.0
    if len(timestamps) >= 2:
        duration = timestamps[-1] - timestamps[0]

    avg_speed = total_path / duration if duration > 0 else 0.0

    return {
        "samples": samples,
        "distance": round(total_path, 3),
        "avg_speed": round(avg_speed, 3),
        "jitter": round(jitter, 6),
        "smoothness": round(smoothness, 6),
        "direction_changes": directions,
        "speed_consistency": round(speed_score, 6),
        "msi_score": msi,
    }