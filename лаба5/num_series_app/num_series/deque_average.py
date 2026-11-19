"""Скользящие средние на основе collections.deque (Вариант 2).

Отдельный модуль, не заменяющий moving_average.py:
- сохраняет публичный контракт (Sequence[float] -> list[float]);
- реализует SMA, CMA, EMA и WMA через deque(maxlen=...);
- удобен для потоковой обработки и для сравнения с «индексной» версией.
"""
from __future__ import annotations

from collections import deque
from typing import Deque, List, Sequence


def _ensure_not_empty(data: Sequence[float]) -> None:
    if not data:
        raise ValueError("Ряд пуст: расчёт скользящей средней невозможен")


def _check_window(window: int, n: int) -> None:
    if not isinstance(window, int) or isinstance(window, bool):
        raise ValueError(f"window должен быть целым, получено: {window!r}")
    if window < 1:
        raise ValueError(f"window должен быть >= 1, получено: {window}")
    if window > n:
        raise ValueError(
            f"window ({window}) больше длины ряда ({n}) — SMA невозможна"
        )


def _check_alpha(alpha: float) -> None:
    if not (0 < alpha <= 1):
        raise ValueError(f"alpha должен быть в (0, 1], получено: {alpha}")


def simple_moving_average_deque(
    data: Sequence[float],
    window: int,
) -> List[float]:
    """SMA через deque(maxlen=window)."""
    _ensure_not_empty(data)
    _check_window(window, len(data))

    buf: Deque[float] = deque(maxlen=window)
    running = 0.0
    result: List[float] = []

    for i, x in enumerate(data):
        if len(buf) == window:
            running -= buf[0]
        buf.append(x)
        running += x
        if i >= window - 1:
            result.append(running / window)
    return result


def centered_moving_average_deque(
    data: Sequence[float],
    window: int,
) -> List[float]:
    """Центрированное MA: окно нечётное, результат выровнен по центру."""
    _ensure_not_empty(data)
    _check_window(window, len(data))
    if window % 2 == 0:
        raise ValueError(
            f"Центрированное MA требует нечётного window, получено: {window}"
        )

    buf: Deque[float] = deque(maxlen=window)
    running = 0.0
    result: List[float] = []

    for x in data:
        if len(buf) == window:
            running -= buf[0]
        buf.append(x)
        running += x
        if len(buf) == window:
            result.append(running / window)

    return result


def exponential_moving_average_deque(
    data: Sequence[float],
    alpha: float,
) -> List[float]:
    """EMA через ring-buffer deque(maxlen=1)."""
    _ensure_not_empty(data)
    _check_alpha(alpha)

    buf: Deque[float] = deque(maxlen=1)
    prev: float = float(data[0])
    result: List[float] = [prev]
    buf.append(prev)

    for x in data[1:]:
        prev = alpha * x + (1.0 - alpha) * prev
        result.append(prev)
        buf.append(prev)
    return result


def weighted_moving_average_deque(
    data: Sequence[float],
    window: int,
) -> List[float]:
    """WMA с линейными весами 1, 2, ..., window на основе deque."""
    _ensure_not_empty(data)
    _check_window(window, len(data))

    buf: Deque[float] = deque(maxlen=window)
    weights = list(range(1, window + 1))
    weight_sum = window * (window + 1) / 2.0
    result: List[float] = []

    for x in data:
        buf.append(x)
        if len(buf) == window:
            weighted_val = sum(val * w for val, w in zip(buf, weights)) / weight_sum
            result.append(weighted_val)
    return result


__all__ = [
    "simple_moving_average_deque",
    "centered_moving_average_deque",
    "exponential_moving_average_deque",
    "weighted_moving_average_deque",
]

