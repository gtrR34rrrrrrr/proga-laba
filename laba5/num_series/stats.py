"""Модуль расчёта базовых статистических показателей без сторонних библиотек."""

import math

from typing import Dict, Sequence


def _ensure_not_empty(data: Sequence[float]) -> None:
    """Проверяет, что последовательность не пуста."""
    if not data:
        raise ValueError("Ряд пуст: расчёт статистики невозможен")


def mean(data: Sequence[float]) -> float:
    """Среднее арифметическое."""
    _ensure_not_empty(data)
    return sum(data) / len(data)


def median(data: Sequence[float]) -> float:
    """Медиана (устойчива к выбросам)."""
    _ensure_not_empty(data)
    s = sorted(data)
    k = len(s) // 2
    if len(s) % 2:
        return float(s[k])
    return (s[k - 1] + s[k]) / 2.0


def spread(data: Sequence[float]) -> float:
    """Размах ряда: max - min."""
    _ensure_not_empty(data)
    return float(max(data) - min(data))


def summarize(data: Sequence[float]) -> Dict[str, float]:
    """Сводный отчёт: count, mean, median, spread, min, max."""
    _ensure_not_empty(data)
    return {
        "count": len(data),
        "mean": mean(data),
        "median": median(data),
        "spread": spread(data),
        "min": float(min(data)),
        "max": float(max(data)),
        "skewness_person": skewness_pearson(data)
    }

def std_dev(data: Sequence[float]) -> float:
    """Выборочное стандартное отклонение."""
    _ensure_not_empty(data)
    if len(data) < 2:
        return 0.0
    m = mean(data)
    variance = sum((x - m) ** 2 for x in data) / (len(data) - 1)
    return math.sqrt(variance)


def skewness_pearson(data: Sequence[float]) -> float:
    """Коэффициент асимметрии по Пирсону: 3 * (mean - median) / std_dev."""
    _ensure_not_empty(data)
    sd = std_dev(data)
    if sd == 0:
        return 0.0
    return 3.0 * (mean(data) - median(data)) / sd           