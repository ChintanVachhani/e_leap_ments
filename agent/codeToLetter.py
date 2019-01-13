map = dict()
for i in range(1, 5):
    map[i] = chr(i + 64)


# print(map)

def codeToLetter(code):
    res = str()
    for i in code:
        res += map[i]
    return res
# print(codeToLetter([1,3,2,4]))
