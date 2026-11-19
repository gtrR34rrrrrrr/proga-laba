"""Точка входа приложения «Расчёт параметров редуктора» (Вариант 9)."""

from validation import input_z1, input_z2, input_power, input_n1
from menu import show_menu, select_mode, mode_name
from operations import gear_ratio, output_speed, input_torque, output_torque, ratio_class


def main() -> None:
    """Главный цикл программы."""
    while True:
        show_menu()
        eta = select_mode()
        if eta is None:
            print("Работа завершена.")
            break

        z1 = input_z1()
        z2 = input_z2(z1)
        p = input_power()
        n1 = input_n1()

        u = gear_ratio(z1, z2)
        n2 = output_speed(n1, u)
        t1 = input_torque(p, n1)
        t2 = output_torque(t1, u, eta)
        u_class = ratio_class(u)

        print("==================== Результаты расчёта ====================")
        print(f"Тип выбранной передачи: {mode_name(eta)}")
        print(f"Коэффициент полезного действия: eta = {eta}")
        print(f"Передаточное отношение: u = {u:.2f} ( {u_class} передача )")
        print(f"Частота выходного вала: n2 = {n2:.2f} об/мин")
        print(f"Крутящий момент на входе: T1 = {t1:.2f} Н*м")
        print(f"Крутящий момент на выходе: T2 = {t2:.2f} Н*м")
        print("============================================================")


if __name__ == "__main__":
    main()