"""Тесты модуля num_series.generator (Вариант 2)."""
import pytest
from num_series.generator import (
    _validate_n,
    gauss_series,
    constant_series,
    random_series,
)


class TestValidateN:
    """Границы и типы входного параметра n."""

    @pytest.mark.parametrize("n", [1, 5, 100, 1000])
    def test_positive_int_passes(self, n):
        _validate_n(n)

    @pytest.mark.parametrize("n", [0, -1, -100])
    def test_zero_and_negative_rejected(self, n):
        with pytest.raises(ValueError, match="положительным целым"):
            _validate_n(n)

    @pytest.mark.parametrize("n", [3.5, -0.1, 1.0000001])
    def test_non_integer_float_rejected(self, n):
        with pytest.raises(ValueError, match="положительным целым"):
            _validate_n(n)

    @pytest.mark.parametrize("n", ["5", "abc", None, [5], {"n": 5}])
    def test_bad_types_rejected(self, n):
        with pytest.raises(ValueError, match="положительным целым"):
            _validate_n(n)

    def test_error_message_contains_repr_and_cause(self):
        with pytest.raises(ValueError) as exc_info:
            _validate_n("abc")
        msg = str(exc_info.value)
        assert "'abc'" in msg
        assert "причина" in msg

    def test_float_integral_passes(self):
        _validate_n(3.0)


class TestGaussSeries:
    """Тесты генератора нормального распределения (Вариант 2)."""

    def test_length_and_type(self):
        data = gauss_series(25, seed=1)
        assert len(data) == 25
        assert all(isinstance(x, float) for x in data)

    def test_reproducible_with_seed(self):
        assert gauss_series(30, mu=10.0, sigma=2.0, seed=42) == gauss_series(
            30, mu=10.0, sigma=2.0, seed=42
        )

    def test_different_seeds_differ(self):
        assert gauss_series(20, seed=1) != gauss_series(20, seed=2)

    def test_zero_sigma_returns_constant(self):
        data = gauss_series(10, mu=7.5, sigma=0.0, seed=0)
        assert data == [7.5] * 10

    def test_negative_sigma_raises(self):
        with pytest.raises(ValueError, match="sigma не может быть отрицательным"):
            gauss_series(10, sigma=-1.0)

    def test_invalid_n_raises(self):
        with pytest.raises(ValueError):
            gauss_series(0)


class TestConstantSeries:
    """Тесты генератора константного ряда (краевой кейс СКО = 0)."""

    def test_values_and_length(self):
        data = constant_series(5, value=42)
        assert len(data) == 5
        assert data == [42.0, 42.0, 42.0, 42.0, 42.0]
        assert all(isinstance(x, float) for x in data)

    def test_invalid_n_raises(self):
        with pytest.raises(ValueError):
            constant_series(-3)


class TestRandomSeries:
    """Тесты базового равномерного генератора."""

    def test_length(self):
        assert len(random_series(10, seed=1)) == 10

    def test_reproducible_with_seed(self):
        assert random_series(20, seed=42) == random_series(20, seed=42)

    def test_different_seeds_differ(self):
        assert random_series(20, seed=1) != random_series(20, seed=2)

    def test_within_bounds(self):
        data = random_series(100, low=-5, high=5, seed=0)
        assert all(-5 <= x <= 5 for x in data)

    def test_low_ge_high_raises(self):
        with pytest.raises(ValueError, match="low должно быть меньше high"):
            random_series(5, low=10, high=5)

    def test_invalid_n_raises(self):
        with pytest.raises(ValueError):
            random_series(0)

