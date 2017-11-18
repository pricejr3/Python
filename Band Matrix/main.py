from bandMatrix import bandMatrix

b1 = bandMatrix(100)
b2 = bandMatrix(10)
b3 = b1 + b1

print(b1.get(0,0))
print(b2.get(0,0))
print(b3.get(0,0))

b1.set(3,4,-123.9)
b2.set(3,4,-123.9)
b3.set(3,4,-123.9)
