# 232 Surcea Mihai-Daniel

import time
from copy import deepcopy

startInfo = [['a'],['c', 'b'],['d']]
scopInfo  = [['b', 'c'],[],['d', 'a']]

def H(stive):
    dist = 0
    for indStiva in range(len(scopInfo)):
        for indEl in range(len(scopInfo[indStiva])):
            try:
                if stive[indStiva][indEl] != scopInfo[indStiva][indEl]:
                    dist += 1
            except IndexError: # exists in the final version, but not in the current one
                dist += 1
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
        for stivaInitInd in range(len(self.info)):
            if len(self.info[stivaInitInd]) == 0: continue
            for stivaFinInd in range(stivaInitInd):
                cInfo = deepcopy(self.info)
                cInfo[stivaFinInd].append (cInfo[stivaInitInd].pop())
                succ.append (Nod(cInfo, self.g + 1, self.id))
            for stivaFinInd in range(stivaInitInd+1, len(self.info)):
                cInfo = deepcopy(self.info)
                cInfo[stivaFinInd].append (cInfo[stivaInitInd].pop())
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
# no need for closed
done = False
startTime = time.time()
while len(open) != 0 and not done:
    currNod = open.pop(0)
    # if I was the final state I should have already stopped
    for s in currNod.Succ():
        if s.h == 0:
            done = True
            s.PrintPath()
            break

        if currNod.HasPred(s): continue

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