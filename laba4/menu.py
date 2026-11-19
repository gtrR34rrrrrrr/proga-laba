#Меню типов передач и маршрутизация выбора через match-case.

from constants import ETA_CYLINDRICAL, ETA_CONICAL, ETA_WORM


def show_menu() -> None:
    """Вывести меню типов передач."""
    print("\nМеню типов передач:")
    print("1 - цилиндрическая передача (eta = 0.97)")
    print("2 - коническая (eta = 0.95)")
    print("3 - червячная (eta = 0.80)")
    print("0 - выход из меню")


def select_mode() -> float | None:
    """Выбор типа передачи через match-case. Возвращает eta или None при выходе."""
    while True:
        choice = input("Выберите пункт меню (0, 1, 2 или 3): ").strip()
        match choice:
            case "1":
                return ETA_CYLINDRICAL
            case "2":
                return ETA_CONICAL
            case "3":
                return ETA_WORM
            case "0":
                return None
            case _:
                print("Неверный пункт меню. Пожалуйста, выберите 0, 1, 2 или 3.")


def mode_name(eta: float) -> str:
    """Вернуть название передачи по КПД eta через match-case."""
    match eta:
        case 0.97:
            return "цилиндрическая"
        case 0.95:
            return "коническая"
        case 0.80:
            return "червячная"
        case _:
            return "неизвестная"