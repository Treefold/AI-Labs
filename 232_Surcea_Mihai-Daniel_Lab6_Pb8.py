#232 Surcea Mihai-Daniel

import time

n = 7 # 3
startInfo = [1] * n
scopInfo  = [0] * n

valueOf = {"i": 1, "g": 0, "d": -1}
keys = ["idddgii", "idiidid", "iidddii", "iddgiig", "dgggiid", "didiigg", "gigddgg", "gdggggg", "gggiggd", "dgggddg"] # ["iid", "did", "gdg"]

# validate input
for key in keys:
    assert len(key) == n, f"Incorrect length of key: {key}"
    spareKey = key.replace("i", "").replace("g", "").replace("d", "")
    assert len(spareKey) == 0, f"The key '{key}' shoudn't contain '{spareKey}''"

def H (arr): return sum(arr)

def UseKey (arr, key):
    newKey = [0] * n
    for keyPoz in range (n): # len(key) = n for any key in keys
        newKey[keyPoz] = arr[keyPoz] + valueOf[key[keyPoz]]
        if (newKey[keyPoz] < 0): newKey[keyPoz] = 0 # tried to unlock the opened lock
    return newKey

class Nod:
    nodes = []
    def __init__(self, info, key = None, g = 0, p = None):
        self.id = len(Nod.nodes)
        self.key = key
        self.info = info # unique
        self.p = p
        self.g = g
        self.h = H(info)
        self.f = self.g + self.h
        Nod.nodes.append(self)
        
    def __str__ (self):
        return (f"(Info={self.info}; UsedKey='{self.key}'; h={self.h}; g={self.g}; f={self.f})")
    def __repr__ (self):
        return (f"(Info={self.info}; UsedKey='{self.key}'; h={self.h}; g={self.g}; f={self.f})")

    def Succ (self):
        succ = []
        
        for key in keys:
            succ.append (Nod(UseKey(self.info, key), key, self.g + 1, self.id))

        return succ
    
    def HasPred (self, nod): # checks if self has nod as a predecesor
        predId = self.p
        while predId is not None:
            if Nod.nodes[predId].info == nod.info: return True
            predId = Nod.nodes[predId].p
        return False

    def IsInList (self, nods):
        for nodPoz in range(len(nods)):
            if nods[nodPoz].info == self.info: 
                return nodPoz
        return None

    def PrintPath (self):
        if self.p is not None: Nod.nodes[self.p].PrintPath()
        else: print ("Path:")
        print (self)

open = [Nod (startInfo)]
closed = []
done = False
startTime = time.time()
while len(open) != 0 and not done:
    currNod = open.pop(0)
    closed.append (currNod)
    # if I was the final state I should have already stopped
    for s in currNod.Succ():
        if s.info == scopInfo:
            done = True
            s.PrintPath()
            break

        if currNod.HasPred(s): continue
        if s.IsInList(closed) or s.IsInList(open): continue

        poz = len(open)
        open.append (s)

        while poz > 0 and open[poz-1].f > open[poz].f:
            open[poz-1], open[poz] = open[poz], open[poz-1]
            poz -= 1

        while poz > 0 and open[poz-1].f == open[poz].f and open[poz-1].g > open[poz].g:
            open[poz-1], open[poz] = open[poz], open[poz-1]
            poz -= 1

print (f"Duration: {time.time() - startTime}")    
if not done:
    print("Lista open e vida, nu avem drum de la nodul start la nodul scop")