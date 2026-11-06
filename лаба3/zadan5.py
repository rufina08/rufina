source_arr = []
is_valid = False

while not is_valid:
    user_input = input("Введите элементы массива через пробел: ").split()
    
    if len(user_input) > 0:
        is_current_input_valid = True
        temp_arr = []
        i = 0
        
        while i < len(user_input) and is_current_input_valid:
            try:
                num = int(user_input[i])
                temp_arr.append(num)
            except ValueError:
                is_current_input_valid = False
            i += 1

        if is_current_input_valid:
            source_arr = temp_arr
            is_valid = True
        else:
            print("Ошибка: все элементы должны быть целыми числами. Попробуйте снова.")
    else:
        print("Ошибка: вы ничего не ввели.")
positive_arr = []  # Положительные (> 0)
other_arr = []     # Остальные (<= 0)

for num in source_arr:
    if num > 0:
        positive_arr.append(num)
    else:
        other_arr.append(num)

print("Исходный массив:", source_arr)
print("Второй массив (положительные элементы):", positive_arr)
print("Третий массив (остальные элементы):", other_arr)
