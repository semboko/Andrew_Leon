from math import sqrt

counter = 0

for i in range(1, 1001):
    sqrt_i = sqrt(i)
    if sqrt_i - int(sqrt_i) == 0:
        print(i)
        counter = counter + 1

print("The total amount of square numbers", counter)
