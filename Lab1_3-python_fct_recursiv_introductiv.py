#python_fct_recursiv_introductiv

import random
nr = random.randint(0,10)

def tries (st = 0, dr = 9, leftTries = 3):
    if leftTries < 0:
        print ("Not found, the number was {}".format(nr))
        return 0
    else:
        tr = int(input ("The number is between {} and {}\nYou have {} tries left\nYour guess is ".format(st, dr, leftTries)))
        if nr > tr:
            tries (tr+1, dr, leftTries - 1)
        elif nr < tr:
            tries (st, tr-1, leftTries - 1)
        else:
            print ("You got it")

tries ()