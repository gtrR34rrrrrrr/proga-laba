"""Модуль расчёта скользящих средних (SMA, CMA, EMA)."""

from typing import List, Sequence


def check_window(window: int, n: int) -> None:
    """Проверяет корректность размера окна: целое 1 <= window <= n."""
    if isinstance(window, bool) or not isinstance(window, int):
        raise ValueError(f"Окно должно быть целым числом (получено: {window!r})")
    if window < 1:
        raise ValueError(f"Окно должно быть >= 1 (получено: {window})")
    if window > n:
        raise ValueError(f"Окно ({window}) не может быть больше длины ряда ({n})")


def simple_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Простая скользящая средняя (SMA) через бегущую сумму за O(n)."""
    if not data:
        raise ValueError("Ряд пуст: расчёт SMA невозможен")
    check_window(window, len(data))

    running = float(sum(data[:window]))
    result = [running / window]
    for i in range(window, len(data)):
        running += data[i] - data[i - window]
        result.append(running / window)
    return result


def centered_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Центрированная скользящая средняя (CMA) для нечётного окна."""
    if not data:
        raise ValueError("Ряд пуст: расчёт CMA невозможен")
    check_window(window, len(data))
    if window % 2 == 0:
        raise ValueError(
            f"Для центрированной МА окно должно быть нечётным (получено: {window})"
        )

    half = window // 2
    running = float(sum(data[:window]))
    result = [running / window]
    for center in range(half + 1, len(data) - half):
        running += data[center + half] - data[center - half - 1]
        result.append(running / window)
    return result


def exponential_moving_average(data: Sequence[float], alpha: float) -> List[float]:
    """Экспоненциальная скользящая средняя (EMA), 0 < alpha <= 1."""
    if not data:
        raise ValueError("Ряд пуст: расчёт EMA невозможен")
    if isinstance(alpha, bool) or not isinstance(alpha, (int, float)):
        raise ValueError(f"alpha должно быть числом (получено: {alpha!r})")
    if not (0 < alpha <= 1):
        raise ValueError(f"Коэффициент alpha должен быть в (0, 1] (получено: {alpha})")

    result = [float(data[0])]
    for i in range(1, len(data)):
        ema_val = alpha * data[i] + (1.0 - alpha) * result[-1]
        result.append(ema_val)
    return result