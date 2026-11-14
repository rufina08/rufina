"""Модуль скользящих средних. Реализация вручную (без numpy/pandas)."""

from typing import Sequence


def _check_window(window: int, n: int) -> None:
    if not isinstance(window, int) or window < 1:
        raise ValueError(f"window должен быть целым числом ≥ 1 (получено: {window!r})")
    if window > n:
        raise ValueError(f"window ({window}) не должен превышать длину ряда ({n})")


def simple_moving_average(data: Sequence[float], window: int) -> list[float]:
    """SMA через бегущую сумму. Длина результата: n - window + 1.

    Контрольная точка: simple_moving_average([1, 2, 3, 4, 5], 3) → [2.0, 3.0, 4.0]
    """
    n = len(data)
    _check_window(window, n)

    running = sum(data[:window])
    result = [running / window]

    for i in range(window, n):
        running += data[i] - data[i - window]
        result.append(running / window)

    return result


def centered_moving_average(data: Sequence[float], window: int) -> list[float]:
    """Центрированное скользящее среднее. Окно должно быть нечётным."""
    n = len(data)
    if not isinstance(window, int) or window < 1 or window % 2 == 0:
        raise ValueError("window должен быть нечётным положительным целым числом")
    if window > n:
        raise ValueError(f"window ({window}) не должен превышать длину ряда ({n})")

    half = (window - 1) // 2
    result = [float("nan")] * half

    for i in range(half, n - half):
        s = sum(data[i - half:i + half + 1])
        result.append(s / window)

    result.extend([float("nan")] * half)
    return result


def exponential_moving_average(data: Sequence[float], alpha: float) -> list[float]:
    """EMA: EMA = alpha * x_t + (1 - alpha) * EMA_prev.
    0 < alpha <= 1. EMA[0] = data[0].
    """
    if not data:
        return []
    if not (0 < alpha <= 1):
        raise ValueError("alpha должен быть в диапазоне (0, 1]")

    result = [data[0]]
    for x in data[1:]:
        result.append(alpha * x + (1 - alpha) * result[-1])
    return result