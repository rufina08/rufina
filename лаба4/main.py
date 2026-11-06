from validation import input_length, input_width, input_thickness, input_quantity
from menu import show_menu, select_mode, mode_name
from operations import calculate_mass, thickness_class

def main() -> None:
    """Главный сценарий."""
    print("=== Расчёт расхода материала при раскрое листа ===")
    
    while True:
        show_menu()
        p = select_mode()
        if p is None:
            print("Работа завершена.")
            break
            
        L = input_length()
        w = input_width()
        t = input_thickness()
        q = input_quantity()
        
        # Вычисление результатов
        m = calculate_mass(L, w, t, p, q)
        t_cls = thickness_class(t)
        mat_title = mode_name(p)
        
        # Вывод результатов
        print("\n=== Результаты ===")
        print(f"Материал:              {mat_title} (p = {int(p)} кг/м³)")
        print(f"Масса партии листов m: {m:.2f} кг")
        print(f"Класс толщины:         {t_cls}")
        print("\n")

if __name__ == "__main__":
    main()
