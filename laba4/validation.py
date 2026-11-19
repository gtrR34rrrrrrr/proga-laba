#Валидация пользовательского ввода (проверка типа и диапазона).

from constants import (
    Z1_MIN, Z1_MAX,
    Z2_MIN, Z2_MAX,
    P_MIN, P_MAX,
    N1_MIN, N1_MAX,
)
from logger import log_error


def validate_range(value: float, low: float, high: float) -> tuple[bool, str]:
    """Проверка границ через if-elif-else."""
    if value < low:
        return False, f"Ошибка! Значение меньше нижней границы ({low})."
    elif value > high:
        return False, f"Ошибка! Значение больше верхней границы ({high})."
    else:
        return True, ""


def input_number(prompt: str, low: float, high: float) -> float:
    """Циклический ввод вещественного числа с флагом is_valid."""
    is_valid = False
    result = 0.0

    while not is_valid:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            msg = "Ошибка ввода! Введите число."
            print(msg)
            log_error(msg)
            continue

        ok, msg = validate_range(value, low, high)
        if ok:
            result = value
            is_valid = True
        else:
            print(msg)
            log_error(msg)

    return result


def input_int(prompt: str, low: int, high: int) -> int:
    """Циклический ввод целого числа с флагом is_valid."""
    is_valid = False
    result = 0

    while not is_valid:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            msg = "Ошибка ввода! Введите целое число."
            print(msg)
            log_error(msg)
            continue

        ok, msg = validate_range(float(value), float(low), float(high))
        if ok:
            result = value
            is_valid = True
        else:
            print(msg)
            log_error(msg)

    return result


def input_z1() -> int:
    """Ввод числа зубьев ведущего z1 (10..100)."""
    return input_int(
        "Введите число зубьев ведущего z1 (10..100): ",
        Z1_MIN, Z1_MAX)


def input_z2(z1: int) -> int:
    """Ввод числа зубьев ведомого z2 (10..200) с проверкой z2 > z1."""
    is_valid = False
    result = 0

    while not is_valid:
        z2 = input_int("Введите число зубьев ведомого z2 (10..200): ", Z2_MIN, Z2_MAX)
        if z2 > z1:
            result = z2
            is_valid = True
        else:
            msg = f"Технологическая ошибка! Число z2 должно быть строго больше z1 ({z1})."
            print(msg)
            log_error(msg)

    return result


def input_power() -> float:
    """Ввод мощности на входе P, кВт (0.1..100)."""
    return input_number(
        "Введите мощность на входе P, кВт (0.1..100): ",
        P_MIN, P_MAX)


def input_n1() -> float:
    """Ввод частоты входного вала n1, об/мин (100..3000)."""
    return input_number(
        "Введите частоту входного вала n1, об/мин (100..3000): ",
        N1_MIN, N1_MAX)