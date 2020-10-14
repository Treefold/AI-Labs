# 232 Surcea Mihai-Daniel Lab9 Pb6: Queens

import time
import numpy as np

class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 8 *2
    NR_LINII = 8 *2

    assert NR_COLOANE == NR_LINII and NR_LINII % 8 == 0, "Incorrect row or colum number"
    DOWN =  1 # direction
    UP   = -1 # direction
    QUEEN = 0
    KING  = 1
    DIR   = 2
    QUEEN_DIR_INDEXES = 2
    SIMBOLURI_JUC = [('n', 'N', UP), ('a', 'A', DOWN)] # Player = (QUEEN, KING, DIR)
    JMIN = None  # 'a'
    JMAX = None  # 'n'
    SPACE = ' '
    GOL = '#' # no piece here
    POS = '.' # possible pice can be placed here
    TAKEN = '*'
    def __init__(self, tabla=[], turn = None):
        if tabla == []:
            turn = Joc.SIMBOLURI_JUC[0] # black starts
            tabla = np.reshape(np.array([Joc.SPACE ] * Joc.NR_LINII * Joc.NR_COLOANE), (Joc.NR_LINII, Joc.NR_COLOANE))
            for lineA in range (3 * Joc.NR_LINII // 8):
                lineN = Joc.NR_LINII - 1 - lineA
                for col in range (Joc.NR_COLOANE):
                    if lineA%2 != col%2: tabla [lineA, col] = Joc.SIMBOLURI_JUC[1][0]
                    if lineN%2 != col%2: tabla [lineN, col] = Joc.SIMBOLURI_JUC[0][0]

            for lineA in range (3 * Joc.NR_LINII // 8, Joc.NR_LINII // 2):
                lineN = Joc.NR_LINII - 1 - lineA
                for col in range (Joc.NR_COLOANE):
                    if lineA%2 != col%2: tabla [lineA, col] = Joc.GOL
                    if lineN%2 != col%2: tabla [lineN, col] = Joc.GOL
              
        self.matr = tabla
        self.turn = turn

    def __str__(self):
        self.fct_euristica(True)
        maxSp = len(Joc.NR_LINII.__str__())
        sir = '\n' + " " * (maxSp+2)
        for nr_col in range(self.NR_COLOANE):
            sir += chr(ord('a') + nr_col) + ' '
        sir += '\n' + " " * (maxSp+2) + '-' * (2 * Joc.NR_COLOANE - 1) + '\n'

        for lin in range(self.NR_LINII):
            #sir += '\n' + ' '.join(self.matr[lin,])
            sir += (lin.__str__() + (" " * (maxSp - len(lin.__str__()) + 1)) + "|" + ' '.join(self.matr[lin,])) + '\n'

        return sir

    def oponent (self, me):
        return Joc.SIMBOLURI_JUC[0 if Joc.SIMBOLURI_JUC[0][0] != me[0] else 1]
    
    def clear (self, pos): 
        for p in pos:
            self.matr[p] = Joc.GOL   
    
    def mark (self, pos): 
        for p in pos:
            self.matr[p] = Joc.POS   

    def piecesOfType (self, me, isKing = False):
        return np.argwhere(self.matr == me[Joc.KING if isKing else Joc.QUEEN])

    def pieces (self, me): # returns the pozition of this player's queens and kings
        return np.concatenate((self.piecesOfType(me), self.piecesOfType(me,True)), 0)

    def inList (self, lis): # lis = list of class Joc elements
        for l in lis:
            if np.sum(self.matr == l.matr) == 0: return True
        return False

    def isPieceOf (self, piece, player):
        return piece == player[Joc.QUEEN] or piece == player[Joc.KING]


    def getPoz (self, i, j = 0): # returns the position if it's valide, otherwise None
        #used wisely, this function can return if this is the last line <=> a piece has become a king
        return self.matr[i,j] if 0 <= i and i < Joc.NR_LINII and 0 <= j and j < Joc.NR_COLOANE else None

    # F - Forward / B - Backward
    # R - Right   / L - LEFT
    #         FR      FL      BR      BL
    DIRS = [(1,-1), (1,1), (-1,-1), (-1,1)]
    def mutari (self, me, startPoz = None, searchIfExists = False, pozDist1 = False, onlyJumDist1 = False):
        # me = the current playerp
        # startPoz (if not none) = the pozition we are trying to capture (returns caputes posibilities)
        # searchIfExists (if True): this function returns true if there is at leas on possible move (otherwise false)
        # pozDist1 (if True): 
        #   - startPoz is None: returns the pozition of all the movable pieces of me (this player)
        #   - startPoz is no None: returns pozition of all posible destinatoon stating from startPoz jumping at most once
        #       - if onlyJumDist1 is True: only jumping is allowed
        op = self.oponent(me)
        dir = me[Joc.DIR]
        l_mutari = []
        poz = []

        for i, j in self.pieces(me) if not startPoz else [startPoz]:
            for dirI, dirJ in Joc.DIRS[:2 if self.matr[i, j] == me[Joc.QUEEN] else 4]:
                diri = dir * dirI
                dirj = dirJ
                val = self.getPoz(i+diri, j+dirj)
                # print (i, j, i+diri, j+dirj, val)
                if val is None: continue # invalide pozition
                if val == Joc.GOL: # open space
                    # move it
                    if pozDist1:
                        if not onlyJumDist1: # not only jumping
                            if startPoz: # we have a target so we need the destination
                                poz.append((i+diri, j+dirj)) # append all possible destination
                            else: # we don't have a target
                                poz.append((i, j)) # append the possible target
                                break # only once
                            continue
                        

                    if startPoz: continue # only jumping

                    mutare = Joc(np.copy(self.matr), op)
                    mutare.matr[i+diri, j+dirj] = me[Joc.KING] if self.getPoz(i+diri+dir) is None else mutare.matr[i, j] # verify if the Queen has become a King
                    mutare.matr[i, j] = Joc.GOL
                    if searchIfExists: return True            
                    l_mutari.append (mutare)
                elif self.isPieceOf(val, op): # has something to capture
                    if self.getPoz(i+2*diri, j+2*dirj) != Joc.GOL: continue # but cannot capture
                    # else capute it
                    if pozDist1:
                        if startPoz: # we have a target so we need the destination
                            poz.append((i+2*diri, j+2*dirj)) # append all possible destination
                            continue
                        else: # we don't have a target
                            poz.append((i, j)) # append the possible target
                            break # only once
                        continue

                    mutare = Joc(np.copy(self.matr), op)
                    mutare.matr[i+2*diri, j+2*dirj] = me[Joc.KING] if self.getPoz(i+2*diri+dir) is None else mutare.matr[i, j] # verify if the Queen has become a King
                    mutare.matr[i, j] = mutare.matr[i+diri, j+dirj] = Joc.GOL # the placet that my piece and the captured piece were become empty
                    if searchIfExists: return True     
                    l_mutari.append(mutare)
                    # try to continue capturing
                    l_mutari.extend(mutare.mutari(me, (i+2*diri, j+2*dirj))) # the case when we have 2 identical tables is quite rare when caputering in your turn 
                    # this shall not be treated here (treating it is more time consumig)
                    # TODO: the duplicates should be treated in the AB or MinMax such as there aren't 2 identical tables on the same level in the tree
        return (l_mutari if not searchIfExists else False) if not pozDist1 else poz
    
        
    def final(self, me):
        # no pieces -> no more moves => we are going to check only if we have moves left
        # no ties (draws) => one must win
        # after one has done it's turn it can be decided if he has won
        # it's incorrect to decide if one has lost after its turn because he might be out of moves for the moment,
        # but the oponent turn comes next and new moves might be available (not out of moves)
        
        if Joc.SIMBOLURI_JUC[0][Joc.QUEEN] not in self.matr and Joc.SIMBOLURI_JUC[0][Joc.KING] not in self.matr:
            return Joc.SIMBOLURI_JUC[1]
        if Joc.SIMBOLURI_JUC[1][Joc.QUEEN] not in self.matr and Joc.SIMBOLURI_JUC[1][Joc.KING] not in self.matr:
            return Joc.SIMBOLURI_JUC[0]
        if not self.mutari(me, None, True):
            return self.oponent(me)
        return False
        
    def aprox(self, me):
        # +10 if it's a Queen
        # +30 if it's a King (3 * Queen)
        # +10% if a piece is protected <=> it's next to a wall <=> an the edges of the table (except the corner which, even if it's secure, it's also vulnerable)
        # +1 for each oponent piece that can be captured by it directly (in one jump) - not affected by protected
        # -1 for each oponent piece that can capture it directly (in one jump) - not affected by protected
        # TODO: take into account the number of moves before each Queen becomes King 
        # TODO: test if the score aprox becomes better 

        op = self.oponent(me)
        dir = me[Joc.DIR]
        total = 0
        for i, j in self.pieces(me):
            meKing = (self.matr[i, j] == me[Joc.KING]) # Am I a King?
            score = 30 if meKing else 10 # the score of this individual piece
            for dirIndex in range(len(Joc.DIRS)):
                dirI, dirJ = Joc.DIRS[dirIndex]
                diri = dir * dirI
                dirj = dirJ
                val = self.getPoz(i+diri, j+dirj)
                if val is None: 
                    # wall
                    if i + j != Joc.NR_COLOANE: # = Joc.NR_LINII <=> corner
                        score += 1 if self.matr[i, j] == me[Joc.QUEEN] else 3 # the score of this individual piece
                elif self.isPieceOf(val, op): # has something to capture
                    if meKing or dirIndex < Joc.QUEEN_DIR_INDEXES: # Can I even go in that direction?
                        if self.getPoz(i+2*diri, j+2*dirj) == Joc.GOL: # I can capute it :D
                            score += 1
                    if val == op[Joc.KING] or dirIndex < Joc.QUEEN_DIR_INDEXES: # Can he go in my direction?
                        if self.getPoz(i-2*diri, j-2*dirj) == Joc.GOL: # I can be captured :(
                            score -= 1
            total += score                  
        return total
    
    def fct_euristica(self, pr = False):
        jmax = self.aprox(Joc.JMAX)
        jmin = self.aprox(Joc.JMIN)
        if pr == True: # for debug to print values
            print (Joc.JMAX, "Has", jmax)
            print (Joc.JMIN, "Has", jmin)
        return jmax - jmin

    def estimeaza_scor(self, adancime):
        t_final = self.final(self.turn)
        if t_final == False:
            return self.fct_euristica()
        elif t_final[0] == Joc.JMAX[0]:
            return (9999+adancime)
        elif t_final[0] == Joc.JMIN[0]:
            return (-9999-adancime)
        else: # unknown
            return 0

class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu
    configuratiile posibile in urma mutarii unui jucator
    """

    ADANCIME_MAX = None

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        #adancimea in arborele de stari
        self.adancime=adancime

        #scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor=scor

        #lista de mutari posibile din starea curenta
        self.mutari_posibile=[]

        #cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa=None

    def jucator_opus(self):
        if self.j_curent==Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def mutari(self):
        l_mutari=self.tabla_joc.mutari(self.j_curent)
        juc_opus=self.jucator_opus()
        l_stari_mutari=[Stare(mutare, juc_opus, self.adancime-1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari


    def __str__(self):
        sir= str(self.tabla_joc) + "(Juc curent: "+self.j_curent[Joc.QUEEN]+")\n"
        return sir

""" Algoritmul MinMax """

def min_max(stare):

    if stare.adancime==0 or stare.tabla_joc.final(stare.j_curent) :
        stare.scor=stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    #calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile=stare.mutari()

    #aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor=[min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent==Joc.JMAX :
        #daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        #daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)

    stare.scor=stare.stare_aleasa.scor
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime==0 or stare.tabla_joc.final(stare.j_curent) :
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha >= beta:
        return stare #este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()
    stare.stare_aleasa = None

    if stare.j_curent[0] == Joc.JMAX[0] :
        scor_curent = float('-inf')

        for mutare in stare.mutari_posibile:
            #calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent < stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if(alpha < stare_noua.scor):
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent[0] == Joc.JMIN[0] :
        scor_curent = float('inf')

        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent > stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if(beta > stare_noua.scor):
                beta = stare_noua.scor
                if alpha >= beta:
                    break
    
    
    stare.scor = stare.stare_aleasa.scor

    return stare

def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final(stare_curenta.j_curent)
    if final:
        print("A castigat " + final[Joc.KING])
        return True
    return False

def main():
    #initializare algoritm
    raspuns_valid=False
    while not raspuns_valid:
        tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1','2']:
            raspuns_valid=True
        else:
            print("Nu ati ales o varianta corecta.")

    # initializare ADANCIME_MAX
    raspuns_valid = False
    while not raspuns_valid:
        n = input("Adancime maxima a arborelui: ")
        if n.isdigit():
            Stare.ADANCIME_MAX = int(n)
            raspuns_valid = True
        else:
            print("Trebuie sa introduceti un numar natural nenul.")


    # initializare jucatori
    [s1, s2] = Joc.SIMBOLURI_JUC.copy()  # lista de simboluri posibile
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu 1.'{}' sau cu 2.'{}'? ".format(s1[0], s2[0]))
        if (Joc.JMIN in ['1','2']):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie 1.'{}' sau 2.'{}'.".format(s1[0], s2[0]))
    if Joc.JMIN == '1':
        Joc.JMIN = s1
        Joc.JMAX = s2
    else:
        Joc.JMIN = s2
        Joc.JMAX = s1

    #initializare tabla
    tabla_curenta = Joc()
    # print("Tabla initiala")
    # print(tabla_curenta)
    #creare stare initiala
    stare_curenta = Stare(tabla_curenta, Joc.SIMBOLURI_JUC[0], Stare.ADANCIME_MAX)
    linie = -1
    coloana = -1

    def validateRsp (pos, mi = 0):
        if len(pos) == 0: return 0
        # return 1 # decomment for auto play - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        pos = sorted(pos,key=lambda x: x[0] * Joc.NR_COLOANE + x[1])
        prt = "Your possible choices:\n" + ("0. End Turn\n" if mi == 0 else "")
        for i in range(len(pos)):
            prt += (i+1).__str__() + '. (' + pos[i][0].__str__() + ', ' +  chr(ord('a') + pos[i][1]) + ')\n'
        print (prt)
        while True:
            try:
                rsp = int(input("Your choices number = "))
                if rsp < mi or rsp > len(pos):
                    print(f'Invalid choice (choose between 1 and {len(pos)}).')
                    continue 
                print ("Choice:", rsp)
                return rsp      
            except ValueError:
                    print(f'Invalid choice (choose between 1 and {len(pos)}).')

    lost = False
    while not lost:
        
        if (stare_curenta.j_curent[0] == Joc.JMIN[0]):
            #muta jucatorul
            print ("Start")
            # Choose which piece to move
            pos = stare_curenta.tabla_joc.mutari(me=stare_curenta.j_curent, pozDist1=True)
            rsp = validateRsp (pos, 1)
            src = pos[rsp-1]
            onlyJump = False # the first time get all posibilities
            # Choose where to move
            while True:
                pos = stare_curenta.tabla_joc.mutari(me=stare_curenta.j_curent, startPoz=src, pozDist1=True, onlyJumDist1=onlyJump)
                if len(pos) == 0: break # no more moves
                # show the available moves with the piece src
                stare_curenta.tabla_joc.mark(pos)
                # print(stare_curenta.tabla_joc) 
                rsp = validateRsp (pos, 0 if onlyJump else 1)
                stare_curenta.tabla_joc.clear(pos)
                if rsp == 0: break
                dest = pos[rsp-1] # valid choice
                stare_curenta.tabla_joc.matr[dest], stare_curenta.tabla_joc.matr[src] = stare_curenta.tabla_joc.matr[src], Joc.GOL
                if stare_curenta.tabla_joc.getPoz(dest[0]+stare_curenta.j_curent[Joc.DIR]) == None: # last line
                    stare_curenta.tabla_joc.matr[dest] = stare_curenta.j_curent[Joc.KING]
                if abs(dest[0] - src[0]) == 2:# 2 <=> jump
                    stare_curenta.tabla_joc.matr[((src[0]+dest[0])//2, (src[1]+dest[1])//2)] = Joc.GOL
                    onlyJump = True # after this capture, you can continue your turn only by capturing
                    src = dest
                else: break # did not capture <=> end of the turn
                
            print(stare_curenta.tabla_joc) 
            print("End of your turn")

        #--------------------------------
        else: #jucatorul e JMAX (calculatorul)
        #Mutare calculator

            #preiau timpul in milisecunde de dinainte de mutare
            t_inainte=int(round(time.time() * 1000))
            if tip_algoritm=='1':
                stare_actualizata = min_max(stare_curenta)
            else: #tip_algoritm==2
                stare_actualizata = alpha_beta(-50000, 50000, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            #preiau timpul in milisecunde de dupa mutare
            t_dupa=int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de "+str(t_dupa-t_inainte)+" milisecunde.")
            

            print("Tabla dupa mutarea calculatorului")
            print(stare_curenta.tabla_joc)
        
        #S-a realizat o mutare. Schimb jucatorul cu cel opus
        stare_curenta.j_curent = stare_curenta.jucator_opus()
        #testez daca jocul a ajuns intr-o stare finala
        #si afisez un mesaj corespunzator in caz ca da
        if (afis_daca_final(stare_curenta)):
            break

if __name__ == "__main__" :
        main()
# try the "auto function" in validateRsp in order to see it work
# it also works for any multiple of 8 (for 16 use depth 2, it wins in a few seconds in auto)