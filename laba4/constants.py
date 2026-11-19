import math

#---Константы проекта для расчёта параметров редуктора (Вариант 9).--0

ETA_CYLINDRICAL: float = 0.97   # цилиндрическая передача
ETA_CONICAL: float = 0.95       # коническая передача
ETA_WORM: float = 0.80          # червячная передача

Z1_MIN: int = 10
Z1_MAX: int = 100
Z2_MIN: int = 10
Z2_MAX: int = 200

P_MIN: float = 0.1
P_MAX: float = 100.0
N1_MIN: float = 100.0
N1_MAX: float = 3000.0

U_SMALL_LIMIT: float = 2.0
U_LARGE_LIMIT: float = 8.0
TORQUE_COEFF: float = 9550.0

LOG_FILE: str = "input_errors.log"