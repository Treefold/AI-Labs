# 232 Surcea Mihai-Daniel

import time
from copy import deepcopy

def NrInv (mat):
    arr = []
    for row in mat:
        arr.extend (row)
    arr.pop(arr.index(0))

    sum = 0
    for i in range (len(arr)):
        for j in range (i+1, len(arr)):
            if arr[i] > arr[j]: sum += 1
    return sum

startInfo = [[5, 6, 3], [0, 1, 2], [4, 7, 8]]
scopInfo  = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

assert NrInv (startInfo) != NrInv (scopInfo), "Cannot be solved"

def H(table):
    dist = 0
    for rowPoz in range(len(table)):
        for colPoz in range(len(table[rowPoz])):
            el = table[rowPoz][colPoz]
            if el == 0: continue
            finRowPoz, finColPoz = divmod (el-1, len(table[rowPoz]))
            dist += abs(rowPoz - finRowPoz) + abs(colPoz - finColPoz)
    return dist

class Nod:
    nodes = []
    def __init__(self, info, g = 0, p = None, h = None):
        self.id = len(Nod.nodes)
        self.info = info # unique
        self.p = p
        self.g = g
        self.h = H(info) if h is None else h
        self.f = self.g + self.h
        Nod.nodes.append(self)
        
    def __str__ (self):
        return (f"(Info={self.info}; h={self.h}; g={self.g}; f={self.f})")
    def __repr__ (self):
        return (f"(Info={self.info}; h={self.h}; g={self.g}; f={self.f})")

    def Succ (self):
        succ = []
        for rowPoz in range(len(self.info)):
            try:
                spaceColPoz = self.info[rowPoz].index(0)
                spaceRowPoz = rowPoz
                break
            except ValueError: continue

        for i, j in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            if 0 <= spaceRowPoz + i and spaceRowPoz + i < len(self.info) and 0 <= spaceColPoz + j and spaceColPoz + j < len(self.info): # always true (just to validate the indexes)
                cInfo = deepcopy(self.info)
                cInfo[spaceRowPoz][spaceColPoz], cInfo[spaceRowPoz + i][spaceColPoz + j] = cInfo[spaceRowPoz + i][spaceColPoz + j], cInfo[spaceRowPoz][spaceColPoz]
                succ.append (Nod(cInfo, self.g + 1, self.id))
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

assert startInfo != scopInfo, "Already in the final state"
open = [Nod (startInfo)]
# closed = []
done = False
startTime = time.time()
while len(open) != 0 and not done:
    currNod = open.pop(0)
    # closed.append (currNod)
    # if I was in the scop state I should have already stopped
    for s in currNod.Succ():
        if s.h == 0:
            done = True
            s.PrintPath()
            break

        if currNod.HasPred(s): continue
        # if s.IsInList(closed) or s.IsInList(open): continue

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