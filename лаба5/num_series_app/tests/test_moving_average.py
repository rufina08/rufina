"""Тесты модуля num_series.moving_average (SMA, WMA, benchmark — Вариант 2)."""
import random
import pytest
from num_series.moving_average import (
    simple_moving_average,
    weighted_moving_average,
    benchmark_moving_average,
)


class TestSimpleMovingAverage:
    def test_window_equals_length(self):
        assert simple_moving_average([1, 2, 3], 3) == [2.0]

    def test_classic_example(self):
        assert simple_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]

    def test_window_1_returns_original(self):
        data = [1.0, 2.5, -3.0, 4.0]
        assert simple_moving_average(data, 1) == data

    def test_output_length(self):
        data = list(range(10))
        for w in range(1, 11):
            assert len(simple_moving_average(data, w)) == len(data) - w + 1

    def test_constant_series(self):
        data = [5.0] * 10
        assert simple_moving_average(data, 3) == [5.0] * 8

    def test_matches_naive(self):
        rng = random.Random(0)
        data = [rng.uniform(-10, 10) for _ in range(50)]
        w = 7
        naive = [sum(data[i : i + w]) / w for i in range(len(data) - w + 1)]
        fast = simple_moving_average(data, w)
        assert fast == pytest.approx(naive)

    @pytest.mark.parametrize("bad_window", [0, -1, 1.5, True])
    def test_invalid_window_raises(self, bad_window):
        with pytest.raises(ValueError):
            simple_moving_average([1, 2, 3], bad_window)

    def test_window_bigger_than_data_raises(self):
        with pytest.raises(ValueError, match="больше длины"):
            simple_moving_average([1, 2], 5)

    def test_empty_data_raises(self):
        with pytest.raises(ValueError, match="пуст"):
            simple_moving_average([], 1)


class TestWeightedMovingAverage:
    """Тесты взвешенной скользящей средней WMA (Вариант 2)."""

    def test_classic_example(self):
        # Окно [1, 2, 3] с весами: (1*1 + 2*2 + 3*3) / 6 = 14/6
        # Окно [2, 3, 4] с весами: (2*1 + 3*2 + 4*3) / 6 = 20/6
        # Окно [3, 4, 5] с весами: (3*1 + 4*2 + 5*3) / 6 = 26/6
        res = weighted_moving_average([1, 2, 3, 4, 5], 3)
        assert res == pytest.approx([14 / 6, 20 / 6, 26 / 6])

    def test_window_1_returns_original(self):
        data = [10.0, -5.0, 3.5]
        assert weighted_moving_average(data, 1) == pytest.approx(data)

    def test_constant_series(self):
        data = [7.0] * 6
        assert weighted_moving_average(data, 4) == pytest.approx([7.0, 7.0, 7.0])

    @pytest.mark.parametrize("bad_window", [0, -2, 2.5, False])
    def test_invalid_window_raises(self, bad_window):
        with pytest.raises(ValueError):
            weighted_moving_average([1, 2, 3], bad_window)

    def test_window_bigger_than_data_raises(self):
        with pytest.raises(ValueError, match="больше длины"):
            weighted_moving_average([1, 2], 4)

    def test_empty_data_raises(self):
        with pytest.raises(ValueError, match="пуст"):
            weighted_moving_average([], 2)


class TestBenchmarkMovingAverage:
    def test_returns_positive_timings(self):
        data = list(range(100))
        res = benchmark_moving_average(data, window=5, repeats=10)
        assert set(res) == {"list", "deque"}
        assert res["list"] >= 0.0
        assert res["deque"] >= 0.0

    def test_invalid_window_raises(self):
        with pytest.raises(ValueError):
            benchmark_moving_average([1, 2], window=5, repeats=5)
