from json import dumps

result = []

for h in range(0, 500//25):
    row = [1 for _ in range(700//25)]
    row[0], row[-1] = 3, 3
    result.append(row)

result[0] = [4 for _ in range(700//25)]
result[0][0] = 6
result[0][-1] = 5

result[-1] = [4 for _ in range(700//25)]
result[-1][0] = 7
result[-1][-1] = 8

with open("map.txt", "w") as output:
    output.write(dumps(result))
