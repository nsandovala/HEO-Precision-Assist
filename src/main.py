from capture.mouse_capture import MouseObserver


def interpret_msi(msi: float) -> str:
    if msi >= 80:
        return "Señal motora muy estable"
    if msi >= 65:
        return "Señal motora estable"
    if msi >= 50:
        return "Señal motora moderada"
    if msi >= 35:
        return "Señal motora inestable"
    return "Señal motora muy inestable"


def main() -> None:
    observer = MouseObserver()
    metrics = observer.start()

    if not metrics:
        print("No se pudieron generar métricas.")
        return
    print(metrics)
    print("HEO Precision Assist — Observer Report")
    print("--------------------------------------")
    print(f"Samples:            {metrics['samples']}")
    print(f"Distance:           {metrics['distance']}")
    print(f"Average speed:      {metrics['avg_speed']}")
    print(f"Jitter:             {metrics['jitter']}")
    print(f"Smoothness:         {metrics['smoothness']}")
    print(f"Direction changes:  {metrics['direction_changes']}")
    print(f"Speed consistency:  {metrics['speed_consistency']}")
    print(f"MSI score:          {metrics['msi_score']}/100")
    print(f"Interpretation:     {interpret_msi(metrics['msi_score'])}")


if __name__ == "__main__":
    main()