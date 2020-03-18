import time
h = {'a': float('inf'), 'b': 10, 'c': 3, 'd': 7, 'e': 8, 'f': 0, 'g': 14, 'i': 3, 'j': 1, 'k': 2 }
g = {}
f = {}
p = {}
for key in h.keys():
    g[key] = 0
    f[key] = float('inf')
    p[key] = None
succ = {
    'a': {'b': 3, 'c': 9, 'd': 7}, 
    'b': {'f': 100, 'e': 4}, 
    'c': {'e': 10, 'g': 6}, 
    'd': {'i':4},
    'e': {'f': 8, 'c': 1}, 
    'f': {}, 
    'g': {'e': 7}, 
    'h': {}, 
    'i': {'k': 1, 'j': 2}, 
    'j': {}, 
    'k': {}
}
start = 'a'
scop  = 'f'

def drum(curr, p):
    if curr is not None:
        drum(p[curr], p)
        print (curr + " ", end='')

def isPred(curr, p, toFind):
    if curr is None:   return False
    if curr == toFind: return True
    return isPred (p[curr], p, toFind)

finished = False
open     = [start]
closed   = []


startTime = time.time()
while len(open):
    curr = open.pop(0)
    if curr == scop:
        finished = True
        drum (scop, p)
        break
    closed.append(curr)
    for s, c in succ[curr].items():
        if isPred(curr, p, s): continue
        try:
            poz = open.index(s)
        except ValueError:
            
            try:
                poz = closed.index(s)
                if g[curr] + c < g[s]: closed.pop(poz)
                else: continue
            except ValueError:
                poz = 0 # it's ok

            poz = len (open)
            open.append (s)

        p[s] = curr
        g[s] = g[curr] + c
        f[s] = g[s] + h[s]
        while poz > 0 and f[open[poz-1]] > f[open[poz]]:
            open[poz-1], open[poz] = open[poz], open[poz-1]
            poz -= 1

        while poz > 0 and f[open[poz-1]] == f[open[poz]] and g[open[poz-1]] < g[open[poz]]:
            open[poz-1], open[poz] = open[poz], open[poz-1]
            poz -= 1

print (f"Duration: {time.time() - startTime}")    
if len(open) == 0 and not finished:
    print("Lista open e vida, nu avem drum de la nodul start la nodul scop")
else:
    print ("\nf = {}, g = {}".format(f[scop], g[scop]))