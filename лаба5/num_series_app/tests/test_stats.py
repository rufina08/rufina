"""Тесты модуля num_series.stats (Вариант 2)."""
import pytest
from num_series.stats import mean, median, spread, stdev, mode, summarize


class TestMean:
    @pytest.mark.parametrize("data,expected", [
        ([1], 1.0),
        ([1, 2, 3], 2.0),
        ([1, 2, 3, 4], 2.5),
        ([-5, 5], 0.0),
        ([0, 0, 0], 0.0),
    ])
    def test_basic(self, data, expected):
        assert mean(data) == pytest.approx(expected)

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="пуст"):
            mean([])

    def test_floats(self):
        assert mean([0.1, 0.2, 0.3]) == pytest.approx(0.2)


class TestMedian:
    @pytest.mark.parametrize("data,expected", [
        ([1], 1.0),
        ([1, 2, 3], 2.0),
        ([3, 1, 2], 2.0),
        ([1, 2, 3, 4], 2.5),
        ([4, 1, 3, 2], 2.5),
        ([-3, -1, -2], -2.0),
        ([0, 0, 0, 0], 0.0),
    ])
    def test_basic(self, data, expected):
        assert median(data) == pytest.approx(expected)

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="пуст"):
            median([])

    def test_resistant_to_outlier(self):
        clean = [1, 2, 3, 4, 5]
        with_outlier = [1, 2, 3, 4, 1000]
        assert median(clean) == 3.0
        assert median(with_outlier) == 3.0


class TestSpread:
    @pytest.mark.parametrize("data,expected", [
        ([5], 0.0),
        ([1, 2, 3], 2.0),
        ([-10, 10], 20.0),
        ([0, 0, 0], 0.0),
    ])
    def test_basic(self, data, expected):
        assert spread(data) == expected

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="пуст"):
            spread([])


class TestStdev:
    """Тесты стандартного отклонения (СКО) для Варианта 2."""

    @pytest.mark.parametrize("data,expected", [
        ([2, 4, 4, 4, 5, 5, 7, 9], 2.138089935299395),
        ([10, 20], 7.0710678118654755),
        ([-1, 0, 1], 1.0),
        ([42], 0.0),
    ])
    def test_basic(self, data, expected):
        assert stdev(data) == pytest.approx(expected)

    def test_constant_series_zero_stdev(self):
        """Краевой кейс Варианта 2: одинаковые значения -> СКО = 0.0."""
        assert stdev([5.0, 5.0, 5.0, 5.0, 5.0]) == 0.0
        assert stdev([0, 0, 0]) == 0.0

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="пуст"):
            stdev([])


class TestMode:
    """Тесты моды ряда для Варианта 2."""

    @pytest.mark.parametrize("data,expected", [
        ([1, 2, 2, 3], [2.0]),
        ([3, 1, 3, 1, 2], [1.0, 3.0]),
        ([5], [5.0]),
        ([1, 2, 3], [1.0, 2.0, 3.0]),
    ])
    def test_basic(self, data, expected):
        assert mode(data) == expected

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="пуст"):
            mode([])


class TestSummarize:
    def test_keys(self):
        s = summarize([1, 2, 3, 4, 5])
        assert set(s) == {
            "count",
            "mean",
            "median",
            "spread",
            "stdev",
            "mode",
            "min",
            "max",
        }

    def test_values(self):
        s = summarize([1, 2, 2, 3, 4])
        assert s["count"] == 5
        assert s["mean"] == pytest.approx(2.4)
        assert s["median"] == 2.0
        assert s["spread"] == 3.0
        assert s["stdev"] == pytest.approx(1.140175425099138)
        assert s["mode"] == [2.0]
        assert s["min"] == 1.0
        assert s["max"] == 4.0

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="пуст"):
            summarize([])
