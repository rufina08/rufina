from typing import List, Sequence


def check_window(window: int, n: int) -> None:
    """Проверка корректности окна: целое >= 1 и window <= n."""
    if isinstance(window, bool) or not isinstance(window, int) or window < 1:
        raise ValueError(f"window должно быть целым числом >= 1 (получено: {window!r})")
    if window > n:
        raise ValueError(f"window ({window}) больше длины ряда ({n})")


def simple_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Простое скользящее среднее (SMA) через бегущую сумму (O(n))."""
    if not data:
        raise ValueError("Ряд пуст: расчёт SMA невозможен")
    check_window(window, len(data))
    running = sum(data[:window])
    result = [running / window]
    for i in range(window, len(data)):
        running += data[i] - data[i - window]
        result.append(running / window)
    return result

def centered_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Центрированное скользящее среднее (окно нечётное, выход выровнен по центру)."""
    if not data:
        raise ValueError("Ряд пуст: расчёт центрированного MA невозможен")
    check_window(window, len(data))
    if window % 2 == 0:
        raise ValueError(f"Для центрированного MA окно должно быть нечётным (получено: {window})")
    return simple_moving_average(data, window)

def exponential_moving_average(data: Sequence[float], alpha: float) -> List[float]:
    """Экспоненциальное скользящее среднее (EMA), 0 < alpha <= 1."""
    if not data:
        raise ValueError("Ряд пуст: расчёт EMA невозможен")
    if isinstance(alpha, bool) or not isinstance(alpha, (int, float)) or not (0 < alpha <= 1):
        raise ValueError(f"alpha должно удовлетворять условию 0 < alpha <= 1 (получено: {alpha!r})")
    ema = [float(data[0])]
    for i in range(1, len(data)):
        ema.append(alpha * data[i] + (1 - alpha) * ema[i - 1])
    return ema