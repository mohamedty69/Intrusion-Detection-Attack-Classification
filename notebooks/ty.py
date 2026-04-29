string = "LIECHTENSTEIN"
key = "TWO"
res = ""
y = 0
for i in string:
    if i == ' ':
        res+= ' '
    else :
        y = y % len(key)
        k = ord(key[y]) - ord('A')
        convert = ((ord(i) - ord('A')) + k ) % 26
        res += chr(convert + ord('A'))
        y+=1 
print(res)