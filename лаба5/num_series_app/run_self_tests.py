"""Самодостаточный запуск проверок без внешних зависимостей (Вариант 2)."""
from __future__ import annotations

import random
import traceback

from num_series import (
    gauss_series,
    constant_series,
    random_series,
    mean,
    median,
    spread,
    stdev,
    mode,
    summarize,
    simple_moving_average,
    weighted_moving_average,
)
from num_series.deque_average import (
    simple_moving_average_deque,
    centered_moving_average_deque,
    exponential_moving_average_deque,
    weighted_moving_average_deque,
)

_CHECKS = []


def check(name: str):
    def wrap(fn):
        _CHECKS.append((name, fn))
        return fn

    return wrap


def _approx(a, b, eps: float = 1e-9) -> bool:
    if isinstance(a, list):
        return len(a) == len(b) and all(_approx(x, y, eps) for x, y in zip(a, b))
    return abs(a - b) <= eps


def _raises(fn, exc_type=ValueError) -> bool:
    try:
        fn()
    except exc_type:
        return True
    except Exception:
        return False
    return False


@check("mean: базовые случаи")
def _():
    assert _approx(mean([1, 2, 3]), 2.0)
    assert _approx(mean([1, 2, 3, 4]), 2.5)


@check("mean: пустой ряд -> ValueError")
def _():
    assert _raises(lambda: mean([]))


@check("median: нечётный/чётный и устойчивость к выбросу")
def _():
    assert median([1, 2, 3]) == 2.0
    assert _approx(median([1, 2, 3, 4]), 2.5)
    assert median([1, 2, 3, 4, 1000]) == 3.0


@check("Вариант 2: stdev, mode и краевой кейс constant (СКО = 0)")
def _():
    assert _approx(stdev([-1, 0, 1]), 1.0)
    assert stdev(constant_series(10, value=7.0)) == 0.0
    assert mode([1, 2, 2, 3]) == [2.0]
    assert mode([1, 1, 3, 3]) == [1.0, 3.0]


@check("spread и summarize")
def _():
    assert _approx(spread([-5, 5]), 10.0)
    s = summarize([1, 2, 2, 3, 4])
    assert set(s) == {"count", "mean", "median", "spread", "stdev", "mode", "min", "max"}
    assert s["count"] == 5 and _approx(s["mean"], 2.4)


@check("SMA: классика, длина и совпадение с наивной версией")
def _():
    assert _approx(simple_moving_average([1, 2, 3, 4, 5], 3), [2.0, 3.0, 4.0])
    rng = random.Random(0)
    data = [rng.uniform(-10, 10) for _ in range(50)]
    w = 7
    naive = [sum(data[i : i + w]) / w for i in range(len(data) - w + 1)]
    assert _approx(simple_moving_average(data, w), naive)


@check("SMA и WMA: совпадение list и deque реализаций")
def _():
    rng = random.Random(42)
    data = [rng.uniform(-20, 20) for _ in range(60)]
    assert _approx(simple_moving_average_deque(data, 5), simple_moving_average(data, 5))
    assert _approx(weighted_moving_average_deque(data, 5), weighted_moving_average(data, 5))


@check("SMA/WMA/CMA/EMA: проверка ошибок")
def _():
    assert _raises(lambda: simple_moving_average([1, 2, 3], 0))
    assert _raises(lambda: simple_moving_average([1, 2], 5))
    assert _raises(lambda: weighted_moving_average([1, 2], 5))
    assert _raises(lambda: centered_moving_average_deque([1, 2, 3, 4], 2))
    assert _raises(lambda: exponential_moving_average_deque([1, 2], 0))
    assert _raises(lambda: exponential_moving_average_deque([1, 2], 1.5))


@check("generator: воспроизводимость с seed и _validate_n")
def _():
    from num_series.generator import _validate_n

    assert gauss_series(10, seed=42) == gauss_series(10, seed=42)
    assert random_series(10, seed=42) == random_series(10, seed=42)
    assert constant_series(4, value=3.0) == [3.0, 3.0, 3.0, 3.0]
    for bad in (-1, 0, 3.5, "abc", None, [5]):
        assert _raises(lambda b=bad: _validate_n(b))


def main() -> int:
    passed, failed = 0, 0
    print(f"Запуск {len(_CHECKS)} проверок...\n")
    for name, fn in _CHECKS:
        try:
            fn()
        except Exception:
            failed += 1
            print(f"  FAIL  {name}")
            traceback.print_exc()
        else:
            passed += 1
            print(f"  OK    {name}")
    total = passed + failed
    print(f"\nИтог: {passed}/{total} прошло, {failed} упало.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
