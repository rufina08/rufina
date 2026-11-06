"""
Меню выбора материала через match-case
"""
from __future__ import annotations
from connstans import P_STEEL, P_ALUMINUM, P_COPPER

def show_menu() -> None:
    """Вывести меню материалов."""
    print("\nВыберите материал листа:")
    print("1 - сталь (p = 7850 кг/м³)")
    print("2 - алюминий (p = 2700 кг/м³)")
    print("3 - медь (p = 8900 кг/м³)")
    print("0 - выход")

def select_mode() -> float | None:
    """Циклически запрашивать материал и возвращать плотность p."""
    while True:
        choice = input("Введите номер материала (от 0 до 3): ").strip()
        match choice:
            case "1":
                return float(P_STEEL)
            case "2":
                return float(P_ALUMINUM)
            case "3":
                return float(P_COPPER)
            case "0":
                return None
            case _:
                print("Ошибка: неверный пункт меню. Повторите ввод.")
def mode_name(p:float) -> str:
    """Вернуть название материала по значению его плотности."""
    match p:
        case 7850.0:
            return "сталь"
        case 2700.0:
            return "алюминий"
        case 8900.0:
            return "медь"
        case _:
            return "неизвестный"