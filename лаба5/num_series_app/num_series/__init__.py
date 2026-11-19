"""Пакет алгоритмической обработки числовых рядов (Вариант 2)."""

from .generator import gauss_series, constant_series, random_series
from .stats import mean, median, spread, stdev, mode, summarize
from .moving_average import (
    simple_moving_average,
    weighted_moving_average,
    benchmark_moving_average,
)
from .deque_average import (
    simple_moving_average_deque,
    centered_moving_average_deque,
    exponential_moving_average_deque,
    weighted_moving_average_deque,
)
from .io_json import save_series_json, load_series_json
from .io_file import load_series_txt, load_series_csv, load_series_auto

__all__ = [
    # генерация
    "gauss_series", "constant_series", "random_series",
    # статистика
    "mean", "median", "spread", "stdev", "mode", "summarize",
    # скользящие средние (list и бенчмарк)
    "simple_moving_average",
    "weighted_moving_average",
    "benchmark_moving_average",
    # скользящие средние (deque)
    "simple_moving_average_deque",
    "centered_moving_average_deque",
    "exponential_moving_average_deque",
    "weighted_moving_average_deque",
    # ввод-вывод
    "save_series_json", "load_series_json",
    "load_series_txt", "load_series_csv", "load_series_auto",
]

__version__ = "2.1.0"

