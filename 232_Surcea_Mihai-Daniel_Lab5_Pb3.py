# 232 Surcea Mihai-Daniel

import time

cMalI = 0
mMalI = 1
cMalF = 2
mMalF = 3
malBarca = 4
malI =  1
malF = -1

n, m = 3, 2
startInfo = (n, n, 0, 0, malI)
scopInfo  = (0, 0, n, n, malF)

def IsAValidMove (cI, mI, cF, mF, cB, mB):
    if cI > mI and mI != 0: return False
    if cF > mF and mF != 0: return False
    if cB > mB and mB != 0: return False
    if cB + mB == 0 or cB + mB > m: return False
    return True

class Nod:
    nodes = []
    def __init__(self, info, g = 0, p = None):
        self.id = len(Nod.nodes)
        self.info = info # unique
        self.p = p
        self.g = g
        self.h = (info[cMalI] + info[mMalI]) // 2
        self.f = self.g + self.h
        Nod.nodes.append(self)
        
    def __str__ (self):
        return (f"(Info={self.info}; h={self.h}; g={self.g}; f={self.f})")
    def __repr__ (self):
        return (f"(Info={self.info}; h={self.h}; g={self.g}; f={self.f})")

    def Succ (self):
        succ = []
        maxNrC = self.info[cMalI if self.info[malBarca] == malI else cMalF]
        maxNrM = self.info[mMalI if self.info[malBarca] == malI else mMalF]

        nrC = 1
        while nrC <= maxNrC and nrC <= m: # mutam doar canibali
            if IsAValidMove(self.info[cMalI] - self.info[malBarca] * nrC, self.info[mMalI], self.info[cMalF] + self.info[malBarca] * nrC, self.info[mMalF], nrC, 0):
                info = (self.info[cMalI] - self.info[malBarca] * nrC, self.info[mMalI], self.info[cMalF] + self.info[malBarca] * nrC, self.info[mMalF], -self.info[malBarca])
                succ.append (Nod(info, self.g + 1, self.id))
            nrC += 1

        nrM = 1
        while nrM <= maxNrM and nrM <= m:
            nrC = 0
            while nrC <= nrM and nrC <= maxNrC and nrM + nrC <= m:
                if IsAValidMove(self.info[cMalI] - self.info[malBarca] * nrC, self.info[mMalI] - self.info[malBarca] * nrM, self.info[cMalF] + self.info[malBarca] * nrC, self.info[mMalF] + self.info[malBarca] * nrM, nrC, nrM):
                    info = (self.info[cMalI] - self.info[malBarca] * nrC, self.info[mMalI] - self.info[malBarca] * nrM, self.info[cMalF] + self.info[malBarca] * nrC, self.info[mMalF] + self.info[malBarca] * nrM, -self.info[malBarca])
                    succ.append (Nod(info, self.g + 1, self.id))
                nrC += 1
            nrM += 1

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

        while poz > 0 and open[poz-1].f < open[poz].f:
            open[poz-1], open[poz] = open[poz], open[poz-1]
            poz -= 1

        while poz > 0 and open[poz-1].f == open[poz].f and open[poz-1].g > open[poz].g:
            open[poz-1], open[poz] = open[poz], open[poz-1]
            poz -= 1

print (f"Duration: {time.time() - startTime}")    
if not done:
    print("Lista open e vida, nu avem drum de la nodul start la nodul scop")