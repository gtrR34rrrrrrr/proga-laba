"""Расчёты параметров редуктора и классификация передаточного отношения."""

from typing import Annotated
from constants import TORQUE_COEFF, U_SMALL_LIMIT, U_LARGE_LIMIT


def gear_ratio(
    z1: Annotated[int, "Число зубьев ведущего колеса"],
    z2: Annotated[int, "Число зубьев ведомого колеса"],
) -> float:
    """Рассчитать передаточное отношение u = z2 / z1.

    Args:
        z1: число зубьев ведущего колеса.
        z2: число зубьев ведомого колеса.

    Returns:
        Передаточное отношение u.
    """
    return z2 / z1


def output_speed(
    n1: Annotated[float, "Частота входного вала, об/мин"],
    u: Annotated[float, "Передаточное отношение"],
) -> float:
    """Рассчитать частоту выходного вала n2 = n1 / u.

    Args:
        n1: частота входного вала, об/мин.
        u: передаточное отношение.

    Returns:
        Частота выходного вала n2, об/мин.
    """
    return n1 / u


def input_torque(
    p: Annotated[float, "Мощность на входе, кВт"],
    n1: Annotated[float, "Частота входного вала, об/мин"],
) -> float:
    """Рассчитать крутящий момент на входе T1 = 9550 * P / n1.

    Args:
        p: мощность на входе, кВт.
        n1: частота входного вала, об/мин.

    Returns:
        Крутящий момент T1, Н·м.
    """
    return TORQUE_COEFF * p / n1


def output_torque(
    t1: Annotated[float, "Крутящий момент на входе, Н·м"],
    u: Annotated[float, "Передаточное отношение"],
    eta: Annotated[float, "КПД передачи"],
) -> float:
    """Рассчитать крутящий момент на выходе T2 = T1 * u * eta.

    Args:
        t1: крутящий момент на входе, Н·м.
        u: передаточное отношение.
        eta: КПД передачи.

    Returns:
        Крутящий момент T2, Н·м.
    """
    return t1 * u * eta


def ratio_class(
    u: Annotated[float, "Передаточное отношение"],
) -> str:
    """Классифицировать передаточное отношение через if-elif-else.

    Args:
        u: передаточное отношение.

    Returns:
        Класс передачи: «малая», «нормальная» или «большая».
    """
    if u < U_SMALL_LIMIT:
        return "малая"
    elif u <= U_LARGE_LIMIT:
        return "нормальная"
    else:
        return "большая"