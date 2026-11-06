n = 0
is_valid = False

while not is_valid:
    try:
        n = int(input("Введите количество элементов N: "))
        if n > 0:
            is_valid = True
        else:
            print("Ошибка: количество элементов должно быть больше 0.")
    except ValueError:
        print("Ошибка: пожалуйста, введите целое число.")
arr = []
print("Введите элементы массива:")
for i in range(n):
    is_element_valid = False
    while not is_element_valid:
        try:
            element = int(input(f"Элемент [{i}]: "))
            arr.append(element)
            is_element_valid = True
        except ValueError:
            print("Ошибка: элемент должен быть целым числом. Попробуйте снова.")
min_val = arr[0]
min_index = 0
for i in range(1, n):
    if arr[i] < min_val:
        min_val = arr[i]
        min_index = i
print(f"\nМинимальный элемент: {min_val}")
print(f"Индекс минимального элемента: {min_index}")
