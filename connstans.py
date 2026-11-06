import math
# --- Плотность материалов ---
P_STEEL = 7850      # 1 - сталь, кг/м³
P_ALUMINUM = 2700   # 2 - алюминий, кг/м³
P_COPPER = 8900     # 3 - медь, кг/м³

# --- Допустимые диапазоны входных данных ---
L_MIN: float = 0.1
L_MAX: float = 5.0

W_MIN: float = 0.1
W_MAX: float = 3.0

T_MIN: float = 0.1
T_MAX: float = 20.0

Q_MIN: int = 1
Q_MAX: int = 1000

# --- Пороговые значения для классификации толщины ---
T_SMALL_LIMIT: float = 0.5
T_LARGE_LIMIT: float = 5.0

# --- Файл журнала ошибок ---
LOG_FILE: str = "input_errors.log"
