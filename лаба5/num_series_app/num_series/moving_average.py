import time
from typing import Dict, List, Sequence

from .deque_average import simple_moving_average_deque


def check_window(window: int, n: int) -> None:
    """Валидация размера окна."""
    if not isinstance(window, int) or isinstance(window, bool):
        raise ValueError(f"window должен быть целым числом, получено: {window!r}")
    if window < 1:
        raise ValueError(f"window должен быть >= 1, получено: {window}")
    if window > n:
        raise ValueError(f"window ({window}) больше длины ряда ({n})")


def simple_moving_average(data: Sequence[float], window: int) -> List[float]:
    """SMA через бегущую сумму по списку (O(n))."""
    if not data:
        raise ValueError("Ряд пуст")
    check_window(window, len(data))

    running = sum(data[:window])
    result = [running / window]
    for i in range(window, len(data)):
        running += data[i] - data[i - window]
        result.append(running / window)
    return result


def weighted_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Взвешенная скользящая средняя (WMA) с линейными весами 1, 2, ..., window."""
    if not data:
        raise ValueError("Ряд пуст")
    check_window(window, len(data))

    weights = list(range(1, window + 1))
    weight_sum = window * (window + 1) / 2.0
    result: List[float] = []

    for i in range(len(data) - window + 1):
        window_slice = data[i : i + window]
        weighted_val = sum(x * w for x, w in zip(window_slice, weights)) / weight_sum
        result.append(weighted_val)

    return result


def benchmark_moving_average(
    data: Sequence[float], window: int, repeats: int = 1000
) -> Dict[str, float]:
    """Замеряет среднее время выполнения SMA для реализаций на list и deque."""
    check_window(window, len(data))

    t0 = time.perf_counter()
    for _ in range(repeats):
        simple_moving_average(data, window)
    t_list = (time.perf_counter() - t0) / repeats

    t0 = time.perf_counter()
    for _ in range(repeats):
        simple_moving_average_deque(data, window)
    t_deque = (time.perf_counter() - t0) / repeats

    return {"list": t_list, "deque": t_deque}

