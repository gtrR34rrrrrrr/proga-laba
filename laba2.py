import math

print("\nМеню типов передач:")
print("1 - цилиндрическая передача (eta = 0.97)")
print("2 - коническая (eta = 0.95)")
print("3 - червячная (eta = 0.80)")

valid = False
while not valid:
    try:
        choice = int(input("Выберите пункт меню (1, 2 или 3): "))
        
        if choice == 1:
            type_name = "цилиндрическая"
            eta = 0.97
            valid = True
        elif choice == 2:
            type_name = "коническая"
            eta = 0.95
            valid = True
        elif choice == 3:
            type_name = "червячная"
            eta = 0.80
            valid = True
        else:
            print("Неверный пункт меню. Пожалуйста, выберите 1, 2 или 3.")
            
    except ValueError:
        print("Ошибка ввода! Пожалуйста, введите целое число.")


valid = False
while not valid:
    try:
        z1 = int(input("Введите число зубьев ведущего z1 (10..100): "))
        if z1 >= 10 and z1 <= 100:
            valid = True
        else:
            print("Ошибка! Значение должно быть от 10 до 100.")
    except ValueError:
        print("Ошибка ввода! Введите целое число.")

valid = False
while not valid:
    try:
        z2 = int(input("Введите число зубьев ведомого z2 (10..200): "))
        if z2 >= 10 and z2 <= 200:
            if z2 > z1:
                valid = True
            else:
                print("Технологическая ошибка! Число z2 должно быть строго больше z1 (" + str(z1) + ").")
        else:
            print("Ошибка! Значение должно быть от 10 до 200.")
    except ValueError:
        print("Ошибка ввода! Введите целое число.")

valid = False
while not valid:
    try:
        P = float(input("Введите мощность на входе P, кВт (0.1..100): "))
        if P >= 0.1 and P <= 100.0:
            valid = True
        else:
            print("Ошибка! Значение должно быть от 0.1 до 100.")
    except ValueError:
        print("Ошибка ввода! Введите число.")

valid = False
while not valid:
    try:
        n1 = float(input("Введите частоту входного вала n1, об/мин (100..3000): "))
        if n1 >= 100.0 and n1 <= 3000.0:
            valid = True
        else:
            print("Ошибка! Значение должно быть от 100 до 3000.")
    except ValueError:
        print("Ошибка ввода! Введите число.")

u = z2 / z1
n2 = n1 / u
T1 = 9550 * P / n1
T2 = T1 * u * eta

if u < 2:
    u_class = "малая"
elif u >= 2 and u <= 8:
    u_class = "нормальная"
else:
    u_class = "большая"

print("==================== Результаты расчёта ====================")
print("Тип выбранной передачи: ", type_name)
print("Коэффициент полезного действия: eta =", eta)
print("Передаточное отношение: u =", round(u, 2), "(", u_class, "передача )")
print("Частота выходного вала: n2 =", round(n2, 2), "об/мин")
print("Крутящий момент на входе: T1 =", round(T1, 2), "Н*м")
print("Крутящий момент на выходе: T2 =", round(T2, 2), "Н*м")
print("============================================================")