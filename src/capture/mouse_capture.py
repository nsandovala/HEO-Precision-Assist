from __future__ import annotations

import time
from typing import List, Tuple
from pynput import mouse
from core.signal_engine import analyze_signal

Point = Tuple[float, float]


class MouseObserver:
    def __init__(self) -> None:
        self.positions: List[Point] = []
        self.timestamps: List[float] = []
        self.running = False

    def on_move(self, x: float, y: float) -> None:
        if not self.running:
            return

        self.positions.append((x, y))
        self.timestamps.append(time.time())

    def start(self) -> dict | None:
        print("\n🧠 HEO Observer iniciado")
        print("Mueve el mouse por 10 segundos...\n")

        self.running = True

        listener = mouse.Listener(on_move=self.on_move)
        listener.start()

        time.sleep(10)

        self.running = False
        listener.stop()

        print("Captura finalizada\n")

        if len(self.positions) < 5:
            print("Datos insuficientes")
            return None

        return analyze_signal(self.positions, self.timestamps)