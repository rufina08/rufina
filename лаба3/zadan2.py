total_sum = 0.0
count = 0
while True:
    try:
        num = float(input("Введите число: "))
    except ValueError:
        print("Ошибка: пожалуйста, введите корректное число.")
        continue
    if num >= 0:
        break
    total_sum += num
    count += 1
if count > 0:
    avg = total_sum / count
    print(f"\nКоличество отрицательных чисел: {count}")
    print(f"Сумма чисел: {total_sum}")
    print(f"Среднее арифметическое: {avg:.2f}")
else:
    print("Сразу введено положительное число (или ноль)")
