import random
from typing import List, Optional


def _validate_n(n: int) -> None:
    """Проверка, что n — положительное целое число."""
    try:
        is_positive_int = (n > 0) and (int(n) == n)
    except (TypeError, ValueError) as err:
        raise ValueError(
            f"n должно быть положительным целым числом "
            f"(получено: {n!r}; причина: {err.args})"
        ) from err
    if not is_positive_int:
        raise ValueError(
            f"n должно быть положительным целым числом (получено: {n!r})"
        )


def gauss_series(
    n: int = 500,
    mu: float = 50.0,
    sigma: float = 10.0,
    seed: Optional[int] = None,
) -> List[float]:
    """Ряд из n чисел нормального распределения N(mu, sigma^2) (Вариант 2)."""
    _validate_n(n)
    if sigma < 0:
        raise ValueError(f"sigma не может быть отрицательным (получено: {sigma})")
    rng = random.Random(seed)
    return [rng.gauss(mu, sigma) for _ in range(n)]


def constant_series(n: int = 500, value: float = 50.0) -> List[float]:
    """Ряд из одинаковых значений (для проверки краевого кейса СКО = 0)."""
    _validate_n(n)
    return [float(value) for _ in range(n)]


def random_series(
    n: int,
    low: float = -100.0,
    high: float = 100.0,
    seed: Optional[int] = None,
) -> List[float]:
    """Ряд из n равномерно распределённых случайных чисел на [low, high]."""
    _validate_n(n)
    if low >= high:
        raise ValueError(f"low должно быть меньше high (получено: {low} >= {high})")
    rng = random.Random(seed)
    return [rng.uniform(low, high) for _ in range(n)]

