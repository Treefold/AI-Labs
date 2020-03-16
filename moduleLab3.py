def citire ():
    n = int(input("n = "))
    assert n > 0, "n must be greater than"
    v = [0 for i in range(n)]
    for i in range (n):
        v[i] = int(input("v[{}] = ".format(i+1)))
    return v

def afisare (v):
    if len(v) == 0:
        print ("Not found")
        return
    for i in v:
        print (i, end=' ')
    print()

def valpoz (v):
    w = []
    for val in v:
        if (val > 0): # 0 won't be taken into account
            w.append (val)
    return w

def semn (v):
    for i in range(len(v)):
        v[i] *= -1
    return v