from __future__ import annotations

from typing import Sequence, Tuple

from core.metrics import jitter_score, path_length

Point = Tuple[float, float]


def analyze_signal(points: Sequence[Point]) -> dict:
    """Analyze a captured pointer signal and return basic metrics."""
    return {
        "samples": len(points),
        "path_length": round(path_length(points), 3),
        "jitter_score": round(jitter_score(points), 3),
    }