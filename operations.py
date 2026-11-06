"""
Расчет расхода материала при раскрое листа
"""
from typing import Annotated
from connstans import T_SMALL_LIMIT, T_LARGE_LIMIT

def calculate_mass(
    L: Annotated[float, "Длина листа, м"],
    w: Annotated[float, "Ширина листа, м"],
    t: Annotated[float, "Толщина листа, мм"],
    p: Annotated[float, "Плотность материала, кг/м³"],
    q: Annotated[int, "Количество листов"]
) -> float:
    """Рассчитать массу партии листов m = L * w * (t / 1000) * p * q, кг."""
    return L * w * (t / 1000.0) * p * q

def thickness_class(t: Annotated[float, "Толщина, мм"]) -> str:
    """Классифицировать толщину через if-elif-else."""
    if t < T_SMALL_LIMIT:
        return "тонкий лист"
    elif t <= T_LARGE_LIMIT:
        return "нормальная толщина"
    else:
        return "толстый лист"