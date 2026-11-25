"""Тесты модуля num_series.deque_average и дифференциальная проверка с list-версией (Вариант 2)."""
import random
import pytest
from num_series.moving_average import (
    simple_moving_average,
    weighted_moving_average,
)
from num_series.deque_average import (
    simple_moving_average_deque,
    centered_moving_average_deque,
    exponential_moving_average_deque,
    weighted_moving_average_deque,
)


class TestDequeMovingAverage:
    def test_sma_classic(self):
        assert simple_moving_average_deque([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]

    def test_sma_matches_list_implementation(self):
        rng = random.Random(42)
        data = [rng.uniform(-100, 100) for _ in range(200)]
        for w in (1, 3, 7, 25, 200):
            expected = simple_moving_average(data, w)
            actual = simple_moving_average_deque(data, w)
            assert actual == pytest.approx(expected)

    def test_wma_matches_list_implementation(self):
        """Дифференциальный тест WMA: сравнение deque и list реализаций (Вариант 2)."""
        rng = random.Random(99)
        data = [rng.uniform(-50, 50) for _ in range(100)]
        for w in (1, 3, 5, 12, 100):
            expected = weighted_moving_average(data, w)
            actual = weighted_moving_average_deque(data, w)
            assert actual == pytest.approx(expected)

    def test_cma_basic_and_even_window_raises(self):
        assert centered_moving_average_deque([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]
        with pytest.raises(ValueError, match="нечётного"):
            centered_moving_average_deque([1, 2, 3, 4], 2)

    def test_ema_basic_and_invalid_alpha(self):
        data = [1.0, 2.0, 3.0]
        assert exponential_moving_average_deque(data, alpha=0.5) == pytest.approx(
            [1.0, 1.5, 2.25]
        )
        assert exponential_moving_average_deque(data, alpha=1.0) == data
        with pytest.raises(ValueError):
            exponential_moving_average_deque(data, alpha=0.0)
        with pytest.raises(ValueError):
            exponential_moving_average_deque(data, alpha=1.5)

    def test_empty_and_invalid_window(self):
        with pytest.raises(ValueError, match="пуст"):
            simple_moving_average_deque([], 3)
        with pytest.raises(ValueError, match="больше длины"):
            simple_moving_average_deque([1, 2], 5)
        with pytest.raises(ValueError, match="пуст"):
            weighted_moving_average_deque([], 3)
