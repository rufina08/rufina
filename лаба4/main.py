from validation import input_number, input_int
from menu import show_menu, select_material, material_name
from operations import calculate_mass, thickness_class
from connstans import L_MIN, L_MAX, W_MIN, W_MAX, T_MIN, T_MAX, Q_MIN, Q_MAX

def main() -> None:
    """Главный сценарий расчета расхода материала."""
    print("=== Расчёт расхода материала при раскрое листа ===")
    
    while True:
        show_menu()
        rho = select_material()
        if rho is None:
            print("Работа завершена.")
            break
            
        # Ввод параметров с полной валидацией границ диапазонов
        l = input_number(f"Введите длину листа L, м ({L_MIN}..{L_MAX}): ", L_MIN, L_MAX)
        w = input_number(f"Введите ширину листа W, м ({W_MIN}..{W_MAX}): ", W_MIN, W_MAX)
        t = input_number(f"Введите толщину листа t, мм ({T_MIN}..{T_MAX}): ", T_MIN, T_MAX)
        q = input_int(f"Введите количество листов q ({Q_MIN}..{Q_MAX}): ", Q_MIN, Q_MAX)
      
        total_mass = calculate_mass(l, w, t, rho, q)
        t_cls = thickness_class(t)
        mat_label = material_name(rho)

        print("\n=== Результаты ===")
        print(f"Материал:       {mat_label}")
        print(f"Класс толщины:  {t_cls}")
        print(f"Масса партии:   {total_mass:.2f} кг")
        print("\n")

if __name__ == "__main__":
    main()
