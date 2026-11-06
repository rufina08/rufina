print("Расчёт расхода материала при раскрое листа")
# Выбор материала
f1 = True
while f1:
    try:
        print("\n1 — сталь")
        print("2 — алюминий")
        print("3 — медь")
        number = int(input("Выберите материал: "))
        if number < 1 or number > 3:
            print("Ошибка: выберите число от 1 до 3.")
        else:
            f1 = False
    except ValueError:
        print("Ошибка: введите целое число.")
match number:
    case 1:
        material = "сталь"
        density = 7850
    case 2:
        material = "алюминий"
        density = 2700
    case 3:
        material = "медь"
        density = 8900
# Длина листа
f1 = True
while f1:
    try:
        length = float(input("Длина листа L, м (0.1–5): "))
        if length < 0.1 or length > 5:
            print("Ошибка: длина должна быть от 0.1 до 5 м.")
        else:
            f1 = False
    except ValueError:
        print("Ошибка: введите число.")
# Ширина листа
f1 = True
while f1:
    try:
        width = float(input("Ширина листа W, м (0.1–3): "))
        if width < 0.1 or width > 3:
            print("Ошибка: ширина должна быть от 0.1 до 3 м.")
        else:
            f1 = False
    except ValueError:
        print("Ошибка: введите число.")
# Толщина листа
f1 = True
while f1:
    try:
        thickness = float(input("Толщина листа t, мм (0.1–20): "))
        if thickness < 0.1 or thickness > 20:
            print("Ошибка: толщина должна быть от 0.1 до 20 мм.")
        else:
            f1 = False
    except ValueError:
        print("Ошибка: введите число.")
# Количество листов
f1 = True
while f1:
    try:
        quantity = int(input("Количество листов q (1–1000): "))

        if quantity < 1 or quantity > 1000:
            print("Ошибка: количество должно быть от 1 до 1000.")
        else:
            f1 = False
    except ValueError:
        print("Ошибка: введите целое число.")
# Расчёт массы
mass = length * width * (thickness / 1000) * density * quantity
# Классификация толщины
if thickness < 0.5:
    thickness_class = "тонкий лист"
elif thickness <= 5:
    thickness_class = "нормальная толщина"
else:
    thickness_class = "толстый лист"
print("\nРезультаты расчёта:")
print("Материал:", material)
print("Плотность:", density, "кг/м³")
print("Класс толщины:", thickness_class)
print("Масса партии:", round(mass, 3), "кг")
