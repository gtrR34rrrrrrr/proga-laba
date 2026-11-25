"""Тесты модуля num_series.stats (включая std_dev и skewness_pearson Варианта 9)."""
import pytest
from num_series.stats import (
    mean,
    median,
    spread,
    std_dev,
    skewness_pearson,
    summarize,
)


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
        ([1], 1),
        ([1, 2, 3], 2),
        ([3, 1, 2], 2),
        ([1, 2, 3, 4], 2.5),
        ([4, 1, 3, 2], 2.5),
        ([-3, -1, -2], -2),
        ([0, 0, 0, 0], 0),
    ])
    def test_basic(self, data, expected):
        assert median(data) == pytest.approx(expected)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            median([])

    def test_resistant_to_outlier(self):
        clean = [1, 2, 3, 4, 5]
        with_outlier = [1, 2, 3, 4, 1000]
        assert median(clean) == 3
        assert median(with_outlier) == 3


class TestSpread:
    @pytest.mark.parametrize("data,expected", [
        ([5], 0),
        ([1, 2, 3], 2),
        ([-10, 10], 20),
        ([0, 0, 0], 0),
    ])
    def test_basic(self, data, expected):
        assert spread(data) == expected

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            spread([])


class TestSkewnessPearson:
    """Тесты коэффициента асимметрии по Пирсону: 3 * (mean - median) / std_dev."""

    @pytest.mark.parametrize("data,expected", [
        #Симметричный ряд: mean=3, median=3 -> skewness=0.0
        ([1, 2, 3, 4, 5], 0.0),
        #Правосторонняя асимметрия: [1, 2, 2, 3, 7]
        # mean = 3.0, median = 2.0, var = (4+1+1+0+16)/4 = 5.5, sd = sqrt(5.5)
        ([1, 2, 2, 3, 7], 3.0 * (3.0 - 2.0) / (5.5 ** 0.5)),
        #Левосторонняя асимметрия: [1, 5, 6, 6, 7]
        #mean = 5.0, median = 6.0, sd = sqrt(5.5)
        ([1, 5, 6, 6, 7], 3.0 * (5.0 - 6.0) / (5.5 ** 0.5)),
    ])
    def test_manual_cases(self, data, expected):
        assert skewness_pearson(data) == pytest.approx(expected)

    def test_constant_series_zero_std_dev(self):
        assert std_dev([4.0, 4.0, 4.0]) == 0.0
        assert skewness_pearson([4.0, 4.0, 4.0]) == 0.0

    def test_single_element_returns_zero(self):
        assert std_dev([10.0]) == 0.0
        assert skewness_pearson([10.0]) == 0.0

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            skewness_pearson([])


class TestSummarize:
    def test_keys(self):
        s = summarize([1, 2, 3, 4, 5])
        assert set(s) == {
            "count",
            "mean",
            "median",
            "spread",
            "min",
            "max",
            "skewness_person",
        }

    def test_values(self):
        s = summarize([1, 2, 3, 4, 5])
        assert s["count"] == 5
        assert s["mean"] == pytest.approx(3.0)
        assert s["median"] == 3
        assert s["spread"] == 4
        assert s["min"] == 1
        assert s["max"] == 5
        assert s["skewness_person"] == pytest.approx(0.0)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            summarize([])