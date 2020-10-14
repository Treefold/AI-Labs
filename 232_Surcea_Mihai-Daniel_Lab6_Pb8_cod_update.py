import time
from keyboard import is_pressed

valueOf = {"i": 1, "g": 0, "d": -1} # where "i" = lock one more time, "g" = does not modify it, "d" = unlock it once if it in not unlocked

def readKeys (inputFileName):
  
    outputFileName = inputFileName.replace("input", "output")
    assert outputFileName != inputFileName, "Incorrect input file name, must include 'input'"
    try:
        inputFile  = open (inputFileName, "r")
    except IOError:
        raise Exception("Problem with input file " + inputFileName)
        
    global outputFile, keys, n, startInfo, scopInfo
    outputFile = open (outputFileName, "w")

    startInfo = []
    for x in inputFile.readline().replace('\n', '').split(' '):
        startInfo.append(int(x))
    keys = inputFile.read().replace('\n', '').split(" ") 
    inputFile.close()

    n = len(startInfo)
    assert n > 0, "The number of locks cannot be 0"
    assert len(keys) > 0, "No keys were given"
    openable  = [False] * n
    scopInfo  = [0] * n # I want to unlock all the locks

    # validate input
    for key in keys:
        assert len(key) == n, f"Incorrect length of key: {key}"
        spareKey = key.replace("i", "").replace("g", "").replace("d", "")
        assert len(spareKey) == 0, f"The key '{key}' shoudn't contain '{spareKey}''"
        for i in range(n):
            if key[i] == 'd': 
                openable[i] = True
    assert sum(openable) == n, f"The locks that cannot be oppend are marked with false: {openable}"

"""
    In some cases the keys are strongly connected and there is no solution
    Example: ["idgdgii", "idgidid", "gidddii", "idggiig", "dgigidd"]
    In that example, the program might never stop (or ran out of memory)
    A solution that might work (not implemented in this code, not sure it will work):
        Create a graph for each lockA where the nodes are the keys and there is an edge from key1 to key2 if key1 locks lockA and key2 unlocks it
        Then we should find intergraphs dependencies and before we decide to add a node in the open, to test for starvation or deadlock
    Simple examples: 
        1. keys=[0:'id', 1:'di']
            Graph lock0 dependecies: key0->key1 
            Graph lock1 dependecies: key1->key0
        2. keys=[0:'idg', 1:'gid', 2:'dgi']
            Graph lock0 dependecies: key0->key2 
            Graph lock1 dependecies: key1->key0
            Graph lock1 dependecies: key2->key1
        Those examples are small and all posibilites will be exhausted fast, but on more complex ones it will take a while
    A multiple graph is needed because it is important on which lock 2 keys are dependent
"""

def Hmax (arr): return max(arr) # the times we need to unlocked de most locked lock (doesn't care about the other locks) - does not overestimate 
def Hsum (arr): return sum(arr) # takes into account all locks - overestimates, but it a lot better than the Hmax
def Hlocked (arr): return sum(1 for k in arr if k != 0) # the number of not unlocked locks - overestimates, but not as much as Hsum
def HH (arr): 
    s = m = 0
    for x in arr:
        s += x
        if x > m: m = x
    return [m, s]

'''
    The problem with Hmax is that if the lock state is the following [0, 1, 2, 0, 100, 2, 0, 4] or [0, 10, 20, 0, 100, 20, 0, 40], it will evaluate them the same (100)
        - even if it does not overestimates
        - the other locks are important too and should be taken into account (not only the maximum)
    The problem with Hlocked is that if the lock state is the following [0, 1, 2, 0, 100, 2, 0, 4] or [0, 10, 20, 0, 100, 20, 0, 40] or [0, 1, 1, 0, 1, 1, 0, 1], it will evaluate them the same (5)
        - it overestimates the solution because after using the key 'gddgddgd' on [0, 1, 1, 0, 1, 1, 0, 1] it is in the final state after one key used, not 5
        - the number of how many times a lock is locked is important too and should be taken into account (not only if it is unlocked or not)
        - the range of values is limited to [0, n]
    The problem with Hsum is that it overestimates the solution because after using the key 'gddgddgd' on [0, 1, 1, 0, 1, 1, 0, 1] it is in the final state after one key used, not 5
    BUT it knows the huge difference between [0, 1, 2, 0, 100, 2, 0, 4] or [0, 10, 20, 0, 100, 20, 0, 40] or [0, 1, 1, 0, 1, 1, 0, 1]

    Best solution that does not overestimates: the combination of Hmax and Hsum
        we will sort them after Hmax which does not overestimates and if two Hmax are the same, after Hsum

'''

def UseKey (arr, key): # returns None if the current lock was better without using this key (if all unlocked locks were already unlocked)
    newKey = [0] * n
    alLeastOneUnlocked = False
    for keyPoz in range (n): # len(key) = n for any key in keys
        newKey[keyPoz] = arr[keyPoz] + valueOf[key[keyPoz]]
        if (newKey[keyPoz] < 0): newKey[keyPoz] = 0 # tried to unlock the unlocked lock
        else: alLeastOneUnlocked = True # at least one lock was truthly unlocked once
    return newKey if alLeastOneUnlocked else None

class Nod:
    nodes = []
    heuristic = Hsum
    def __init__(self, info, key = None, g = 0, p = None):
        self.id = len(Nod.nodes)
        self.key = key
        self.info = info # unique
        self.p = p
        self.g = g
        self.h = Nod.heuristic(info)
        if isinstance(self.h, list): # only when you use HH
            self.f = [x+self.g for x in self.h]
        else: # Hmax, Hsum, Hlocked
            self.f = self.g + self.h # for Hmax, Hsum, Hlocked

        Nod.nodes.append(self)
        
    def __str__ (self):
        return (f"(Info={self.info}; UsedKey='{self.key}'; h={self.h}; g={self.g}; f={self.f})")
    def __repr__ (self):
        return (f"(Info={self.info}; UsedKey='{self.key}'; h={self.h}; g={self.g}; f={self.f})")

    def Succ (self):
        succ = []
        
        for key in keys:
            info = UseKey(self.info, key)
            if info: # all the keys that unlocks at least one lock
                succ.append (Nod(info, key, self.g + 1, self.id))

        return succ
    
    def HasPred (self, nod): # checks if self has nod as a predecesor
        predId = self.p
        while predId is not None:
            if Nod.nodes[predId].info == nod.info: return True
            predId = Nod.nodes[predId].p
        return False

    def IsInList (self, nods):
        for nodPoz in range(len(nods)):
            
            # if nods[nodPoz].info == self.info: 
            #     return nodPoz

            atLeastOneBetter = False
            for i in range(n):
                if self.info[i] < nods[nodPoz].info[i]:
                    atLeastOneBetter = True        
                    break
            if not atLeastOneBetter: 
                return nodPoz
        return None

    def PrintPath (self):
        if self.p is not None: Nod.nodes[self.p].PrintPath()
        else: print ("Path:", file=outputFile)
        print (self, file=outputFile)

# this function is the impementaiton from the course of A*, any comments will be redundant
def solve(h = Hsum): # h is the used heuristic function
    Nod.heuristic = h   
    opened = [Nod (startInfo)]
    closed = []
    done = False
    if startInfo == scopInfo:
        opened[0].PrintPath()
        done = True
    print ("\tpress q to stop the current execution")
    startTime = time.time()
    while len(opened) != 0 and not done:
        currNod = opened.pop(0)
        closed.append (currNod)
        # if I was the final state I should have already stopped
        for s in currNod.Succ():
            if s.info == scopInfo:
                done = True
                s.PrintPath()
                break

            if currNod.HasPred(s): continue
            if s.IsInList(closed) or s.IsInList(opened): continue
            alLeastOneBetter = False
            for i in range(n):
                if currNod.info[i] > s.info[i]:
                    alLeastOneBetter = True
            
            if not alLeastOneBetter: continue

            poz = len(opened)
            opened.append (s)

            while poz > 0 and opened[poz-1].f > opened[poz].f:
                opened[poz-1], opened[poz] = opened[poz], opened[poz-1]
                poz -= 1

            while poz > 0 and opened[poz-1].f == opened[poz].f and opened[poz-1].g > opened[poz].g:
                opened[poz-1], opened[poz] = opened[poz], opened[poz-1]
                poz -= 1

            if is_pressed('q'): # if it takes too long and you want to stop it
                invalidRsp = True
                while invalidRsp:
                    try:
                        rsp = int(input("Press 0 to exit or 1 to continue"))
                        if rsp == 1:
                            break
                        if rsp == 0:
                            done = True
                            print ("\tForce exit")
                            print ("Force exit", file=outputFile)
                            break
                        print(f'Invalid choice (choose between 0 and 1).')                            
                    except ValueError:
                            print(f'Invalid choice (choose between 0 and 1).')

    print (f"Duration: {time.time() - startTime}", file=outputFile)    
    if not done:
        print("Unsolvable", file=outputFile)

def main():
    inputFilesName = ["232_Surcea_Mihai-Daniel_Lab6_Pb8_input1.txt", "232_Surcea_Mihai-Daniel_Lab6_Pb8_input2.txt", "232_Surcea_Mihai-Daniel_Lab6_Pb8_input3.txt", "232_Surcea_Mihai-Daniel_Lab6_Pb8_input4.txt"]
    for inputFileName in inputFilesName:
        print ("\nUsing", inputFileName)
        readKeys(inputFileName)
        print ("\n\tUsing Hlocked")
        print ("\nUsing Hlocked", file=outputFile)
        solve (Hlocked)
        print ("\n\tUsing Hsum")
        print ("\nUsing Hsum", file=outputFile)
        solve (Hsum)
        print ("\n\tUsing Hmax")
        print ("\nUsing Hmax", file=outputFile)
        solve (Hmax)
        print ("\n\tUsing HH")
        print ("\nUsing HH", file=outputFile)
        solve (HH)
        outputFile.close()
    print("\nDone")

if __name__ == "__main__":
    main()
