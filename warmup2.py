x = 10
y = 3

print(id(x))
print(id(y))

x = y

print(id(x))
print(id(y))

z = x + y

print(z)
print(id(z))