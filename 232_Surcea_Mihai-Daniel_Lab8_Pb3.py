# 232 Surcea Mihai-Daniel Lab8 Pb1: Reversi

import time
import numpy as np

class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 8
    NR_LINII   = 8
    SIMBOLURI_JUC = ['n', 'a']
    JMIN = None  # 'a'
    JMAX = None  # 'n'
    GOL = '#' # no piece here
    POS = '.' # possible pice can be placed here
    def __init__(self, tabla=[], tura = None, pas = False):
        if tabla == []:
            tabla = np.reshape(np.array([Joc.GOL] * Joc.NR_LINII * Joc.NR_COLOANE), (Joc.NR_LINII, Joc.NR_COLOANE))
            stLine = (Joc.NR_LINII  -1) // 2  
            stCol  = (Joc.NR_COLOANE-1) // 2
            tabla [stLine, stCol] = tabla [stLine + 1, stCol + 1] = 'a'
            tabla [stLine, stCol + 1] = tabla [stLine + 1, stCol] = 'n'
            tura = 'n'
        self.matr = tabla
        self.turn = tura
        self.pas  = pas # if the past turn was a pas (the openent has passed)

    def __str__(self):
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
        return Joc.SIMBOLURI_JUC[0 if Joc.SIMBOLURI_JUC[0] != me else 1]
    
    def clear (self, pos): 
        for p in pos:
            self.matr[p] = '#'

    # up (u), right (r), down (d), left (l)
    #         u      u-r     r     d-r     d     d-l      l       u-l 
    DIR = [(-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1)] 
    def mutariPos(self, me, printable = False):
        op = self.oponent(me)
        pos = []
        for lin, col in np.argwhere(self.matr == me): # pozition of this player pieces in matrix
            for diri, dirj in Joc.DIR:
                i, j = lin+diri, col+dirj
                if i < 0 or j < 0: continue
                try:
                    if self.matr[i, j] != op: continue # at least one oponent
                    while (self.matr[i, j] == op):
                        i += diri
                        j += dirj
                        if i < 0 or j < 0: raise IndexError
                    if self.matr[i, j] == Joc.GOL:
                        pos.append((i,j))
                        self.matr[i, j] = Joc.POS # mark in order not to have duplicates
                except IndexError: continue # out of matrix
        if printable: print(self)
        # else: print (pos) # debug
        self.clear (pos)
        return pos
    
    def play (self, me, lin, col): 
        op = self.oponent(me)
        self.matr[lin,col] = me
        for diri, dirj in Joc.DIR:
            i, j = lin+diri, col+dirj
            if i < 0 or j < j: continue
            try:
                if self.matr[i, j] != op: continue # at least one of my pieces
                while (self.matr[i+diri, j+dirj] == op):
                    if i < 0 or j < 0: raise IndexError
                    i += diri
                    j += dirj
                if self.matr[i+diri, j+dirj] == me:
                    while i != lin or j != col:
                        self.matr[i, j] = me                        
                        i -= diri
                        j -= dirj
            except IndexError: continue # out of matrix


    def mutari (self, me):
        op = self.oponent(me)
        pos = self.mutariPos(me)
        if len(pos) == 0:
            return [Joc(np.copy(self.matr), op, True)] # this player has to pas

        l_mutari = []
        for i, j in pos:
            nextop = Joc(np.copy(self.matr), op)
            nextop.play(me, i, j)
            l_mutari.append (nextop)
        return l_mutari
        
    def final(self):
        op = self.oponent(self.turn)
        # if oponent has passed and I don't have any other posible move (=> I also pass)
        if len(self.mutariPos(self.turn)) != 0 or len(self.mutariPos(op)) != 0: return False 
        # else: both players have passed => end of the game
        noPiecesMine = np.sum(self.matr == self.turn)
        noPiecesOp   = np.sum(self.matr == op)
        return self.turn if noPiecesMine > noPiecesOp else op if noPiecesOp > noPiecesMine else 'remiza'

    def cornersSc (self, player):
        sc = 0
        for i, j in [(0, 0), (0, Joc.NR_COLOANE-1), (Joc.NR_LINII-1, 0), (Joc.NR_LINII-1, Joc.NR_COLOANE-1)]:
            if self.matr[i, j] == player: sc += 100
        return sc

    def aprox (self, player):
        sc = self.cornersSc(player)
        
        for i, j in np.argwhere(self.matr == Joc.GOL):
            for diri, dirj in Joc.DIR:
                try:
                    if self.matr[i+diri, j+dirj] == player:
                        sc += 1
                        break
                except IndexError: continue

        return sc

    
    def fct_euristica(self):
        # HMC (Heuristic on Mobility and Corners) - http://ceur-ws.org/Vol-1107/paper2.pdf
        # this was also my idea, by in the link are some more complex aproximations

        return self.aprox(Joc.JMAX) - self.aprox(Joc.JMIN)

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        if t_final == Joc.JMAX :
            return (999+adancime)
        elif t_final == Joc.JMIN:
            return (-999-adancime)
        elif t_final == 'remiza':
            return 0
        else:
            return self.fct_euristica()

    def printWithPos (self, me):
        self.mutariPos(me, True)

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
        sir= str(self.tabla_joc) + "(Juc curent: "+self.j_curent+")\n"
        return sir

""" Algoritmul MinMax """

def min_max(stare):

    if stare.adancime==0 or stare.tabla_joc.final() :
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
    if stare.adancime==0 or stare.tabla_joc.final() :
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha >= beta:
        return stare #este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX :
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

    elif stare.j_curent == Joc.JMIN :
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
    final = stare_curenta.tabla_joc.final()
    if(final):
        if (final=="remiza"):
            print("Remiza!")
        else:
            print("A castigat "+final)
        return True
    return False

def main():
    #initializare algoritm
    raspuns_valid=False
    while not raspuns_valid:
        tip_algoritm=input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
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
        Joc.JMIN = input("Doriti sa jucati cu {} sau cu {}? ".format(s1, s2))
        if (Joc.JMIN in Joc.SIMBOLURI_JUC):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie {} sau {}.".format(s1, s2))
    Joc.JMAX = s1 if Joc.JMIN == s2 else s2

    #initializare tabla
    tabla_curenta = Joc()
    print("Tabla initiala")
    tabla_curenta.printWithPos(Joc.SIMBOLURI_JUC[0])

    #creare stare initiala
    stare_curenta = Stare(tabla_curenta, Joc.SIMBOLURI_JUC[0], Stare.ADANCIME_MAX)

    linie = -1
    coloana = -1
    while True :

        pos = stare_curenta.tabla_joc.mutariPos(stare_curenta.j_curent)
        if len(pos) == 0:
            print ("No available moves")
            stare_curenta.j_curent = stare_curenta.jucator_opus()
            continue 

        if (stare_curenta.j_curent == Joc.JMIN):
            #muta jucatorul

            pos = sorted(pos,key=lambda x: x[0] * Joc.NR_COLOANE + x[1])
            prt = "Your possible choices:\n"
            for i in range(len(pos)):
                prt += (i+1).__str__() + '. (' + pos[i][0].__str__() + ', ' +  chr(ord('a') + pos[i][1]) + ')\n'
            print (prt)
            raspuns_valid = False
            while not raspuns_valid:
                try:
                    rsp = int(input("Your choices number = "))
                    if rsp < 1 or rsp > len(pos):
                        print(f'Invalid choice (choose between 1 and {len(pos)}).')
                        continue 
                    print ("Choice:", rsp)
                    linie, coloana = pos[rsp-1] # valid choice
                    raspuns_valid = True       
                except ValueError:
                        print(f'Invalid choice (choose between 1 and {len(pos)}).')

            #dupa iesirea din while sigur am valida coloana
            #deci pot plasa simbolul pe "tabla de joc"
            stare_curenta.tabla_joc.play(stare_curenta.j_curent, linie, coloana)


            #S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus() # I change the player in order to show it's posible moves
            #afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            stare_curenta.tabla_joc.printWithPos(stare_curenta.j_curent)

            #testez daca jocul a ajuns intr-o stare finala
            #si afisez un mesaj corespunzator in caz ca da
            if (afis_daca_final(stare_curenta)):
                break

        #--------------------------------
        else: #jucatorul e JMAX (calculatorul)
        #Mutare calculator

            #preiau timpul in milisecunde de dinainte de mutare
            t_inainte=int(round(time.time() * 1000))
            if tip_algoritm=='1':
                stare_actualizata = min_max(stare_curenta)
            else: #tip_algoritm==2
                stare_actualizata = alpha_beta(-5000, 5000, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc

            #preiau timpul in milisecunde de dupa mutare
            t_dupa=int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de "+str(t_dupa-t_inainte)+" milisecunde.")
            

            #S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()
            print("Tabla dupa mutarea calculatorului")
            stare_curenta.tabla_joc.printWithPos(stare_curenta.j_curent)

            if (afis_daca_final(stare_curenta)):
                break

if __name__ == "__main__" :
        main()

