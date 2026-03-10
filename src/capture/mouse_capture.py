from __future__ import annotations

from typing import List, Tuple
from pynput import mouse

Point = Tuple[float, float]


class MouseCaptureSession:
    def __init__(self) -> None:
        self.points: List[Point] = []

    def on_move(self, x: float, y: float) -> None:
        self.points.append((x, y))

    def run(self) -> List[Point]:
        print("Capturing mouse movement... Press Ctrl+C to stop.")
        try:
            with mouse.Listener(on_move=self.on_move) as listener:
                listener.join()
        except KeyboardInterrupt:
            print("\nCapture stopped.")
        return self.points