import math
w = float(input("Введите переменную w (по условию 3.994): "))
a = (math.sqrt(17) * w) / (2 * math.pi)
x = math.pow(a, -1.61)
y = x + math.sqrt(math.fabs(math.pow(a, 2) - math.pow(x, 2)) + 1)
print("Результаты:")
print("a = {0:.4f}".format(a))
print("x = {0:.4f}".format(x))
print("y = {0:.2f}".format(y))
