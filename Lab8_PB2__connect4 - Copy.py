import time
from copy import deepcopy

def TestFinal (diag):
    last = None
    leng = None
    for x in diag:
        if x == Joc.GOL:
            last = None
        elif x == last:
            leng += 1
        else:
            leng = 1
            last = x
        if leng == Joc.NR_CONNECT: return last # someone won
    return None  

def nr_intervale_deschise(arr, jucator): 
    nr = 0  
    leng = 0
    for x in arr:
        if x == Joc.GOL or x == jucator:
            leng += 1
        else:
            leng = 0
        if leng >= Joc.NR_CONNECT: nr += 1
    return nr

class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 7
    NR_LINII = 6
    NR_CONNECT = 4  # cu cate simboluri adiacente se castiga
    SIMBOLURI_JUC = ['X', '0']  # ['G', 'R'] sau ['X', '0']
    JMIN = None  # 'R'
    JMAX = None  # 'G'
    GOL = '.'
    def __init__(self, tabla=None, lastMovePoz = None):
        self.matr = tabla or [Joc.GOL]*(Joc.NR_COLOANE * Joc.NR_LINII)
        self.lastMovePoz = lastMovePoz
    
    def __str__(self):
        sir = ''
        for nr_col in range(self.NR_COLOANE):
            sir += str(nr_col) + ' '
        sir += '\n'

        for lin in range(self.NR_LINII):
            k = lin * self.NR_COLOANE
            sir += (" ".join([str(x) for x in self.matr[k : k+self.NR_COLOANE]])+"\n")
        return sir

    def final(self):
        # returnam simbolul jucatorului castigator daca are 4 piese adiacente
        #	pe linie, coloana, diagonala \ sau diagonala /
        # sau returnam 'remiza'
        # sau 'False' daca nu s-a terminat jocul


        # Verificarea inainte sa citesc ca trebuie facuta doar ultima pozitie (ultima mutare) care nu exista in configuratia actuala 
        # (asa voiam sa fac de la inceput, doar ca am presupus ca nu am voie sa modific configuratia actuala <=> sa adaug pozitia ultimei mutari)
        rez = False

        # verificam linii
        # TO DO ..................
        for row in range (self.NR_LINII):
            last = None
            leng = None
            for x in self.matr[row*self.NR_COLOANE:(row+1)*self.NR_COLOANE]: #select row elements
                if x == self.GOL:
                    last = None
                elif x == last:
                    leng += 1
                else:
                    leng = 1
                    last = x
                if leng == self.NR_CONNECT: return last # someone won
            if leng == None: break # after a free row, the next ones are also free

        # verificam coloane
        # TO DO ..........
        for col in range (self.NR_COLOANE):
            last = None
            leng = None
            for x in self.matr[col::self.NR_COLOANE]: # select column elements
                if x == self.GOL:
                    break # end of column (cannot have more elements)
                elif x == last:
                    leng += 1
                else:
                    leng = 1
                    last = x
                if leng == self.NR_CONNECT: return last # someone won

        # verificam diagonale \
        # TO DO..........

        # Case Row == Col
        #  1111
        # 3 111
        # 33 11
        # 333 1
        # 3333

        # Case Col > Row 
        # 3 2222 1111
        # 33 2222 111
        # 333 2222 11
        # 3333 2222 1

        # Case Row > Col
        #   1111
        #  2 111
        #  22 11
        #  222 1
        #  2222
        # 3 222
        # 33 22
        # 333 2
        # 3333

        # bottom triangle: 1
        for i in range (Joc.NR_CONNECT-1, min(Joc.NR_LINII, Joc.NR_COLOANE)):
            rez = TestFinal(self.matr[Joc.NR_COLOANE-i-1:(Joc.NR_CONNECT+i-2)*Joc.NR_COLOANE:Joc.NR_COLOANE+1])
            if rez != None: return rez
        # middle part if Col > Row: 2 (doesn't enter if Col <= Row)
        for i in range (Joc.NR_LINII-Joc.NR_COLOANE-1):
            rez = TestFinal(self.matr[(i+1)*Joc.NR_COLOANE:(Joc.NR_COLOANE+i+1)*Joc.NR_COLOANE:Joc.NR_COLOANE+1])
            if rez != None: return rez
        # middle part if Row > Col: 2 (doesn't enter if Row <= Col)
        for i in range (Joc.NR_COLOANE-Joc.NR_LINII-1):
            rez = TestFinal(self.matr[Joc.NR_COLOANE*Joc.NR_LINII-i-2::-Joc.NR_COLOANE-1])
            if rez != None: return rez
        # top triangle: 3
        for i in range (max(1 if Joc.NR_COLOANE == Joc.NR_LINII else 0, Joc.NR_LINII-Joc.NR_COLOANE), Joc.NR_LINII-Joc.NR_CONNECT+1):
            rez = TestFinal(self.matr[i*Joc.NR_COLOANE::Joc.NR_COLOANE+1])
            if rez != None: return rez

        # verificam diagonale /
        # TO DO..........

        # Case Row == Col
        # 1111
        # 111 3
        # 11 33
        # 1 333
        #  3333

        # Case Col > Row 
        # 1111 2222 3
        # 111 2222 33
        # 11 2222 333
        # 1 2222 3333

        # Case Row > Col
        # 1111
        # 111 2
        # 11 22
        # 1 222
        #  2222
        #  222 3
        #  22 33
        #  2 333
        #   3333

        # bottom triangle: 1
        for i in range (Joc.NR_CONNECT-1, min(Joc.NR_LINII, Joc.NR_COLOANE)):
            rez = TestFinal(self.matr[i*Joc.NR_COLOANE:i-1:-Joc.NR_COLOANE+1])
            if rez != None: return rez
        # middle part if Col > Row: 2 (doesn't enter if Col <= Row)
        for i in range (Joc.NR_COLOANE-Joc.NR_LINII-1):
            rez = TestFinal(self.matr[Joc.NR_LINII+i::Joc.NR_COLOANE-1])
            if rez != None: return rez
        # middle part if Row > Col: 2 (doesn't enter if Row <= Col)
        for i in range (Joc.NR_LINII-Joc.NR_COLOANE-1):
            rez = TestFinal(self.matr[(Joc.NR_COLOANE + i) * Joc.NR_COLOANE:(i+1) * Joc.NR_COLOANE:-Joc.NR_COLOANE+1])
            if rez != None: return rez
        # top triangle: 3
        for i in range (max(1 if Joc.NR_COLOANE == Joc.NR_LINII else 0, Joc.NR_COLOANE - Joc.NR_LINII), Joc.NR_COLOANE-Joc.NR_CONNECT+1):
            rez = TestFinal(self.matr[max(i, (Joc.NR_LINII+i-Joc.NR_COLOANE+1)*Joc.NR_COLOANE-1):(Joc.NR_LINII-1)*Joc.NR_COLOANE+i+1:Joc.NR_COLOANE-1])
            if rez != None: return rez

        if Joc.GOL not in self.matr:
            return 'remiza'
        else:
            return False
     
    def mutari(self, jucator_opus):
        l_mutari=[]

        # TO DO..........
        # folosim:
        # matr_tabla_noua = list(self.matr)
        # .... "jucator_opus" (parametrul functiei) adauga o mutare in "matr_tabla_noua"
        # l_mutari.append(Joc(matr_tabla_noua))

        # mutarea se face alegand o coloana care nu e plina
        for nrCol in range (self.NR_COLOANE):
            try:
                poz = self.matr[nrCol::self.NR_COLOANE].index(self.GOL) * self.NR_COLOANE + nrCol
                matr_tabla_noua = deepcopy(self.matr)
                matr_tabla_noua[poz] = jucator_opus
                l_mutari.append(Joc(matr_tabla_noua), poz)
            except ValueError: continue # this column is full
        return l_mutari  

    def nr_intervale_deschise(self, jucator):
        # un interval de 4 pozitii adiacente (pe linie, coloana, diag \ sau diag /)
        # este deschis pt "jucator" daca nu contine "juc_opus"
        # sau daca contine doar "jucator" si "GOL"
        # juc_opus = Joc.JMIN if jucator == Joc.JMAX else Joc.JMAX
        rez = 0

        # linii
        # TO DO ..................
        for row in range (self.NR_LINII):
            rez += nr_intervale_deschise(self.matr[row*self.NR_COLOANE:(row+1)*self.NR_COLOANE], jucator)

        # coloane
        # TO DO ..........
        for col in range (self.NR_COLOANE):
            rez += nr_intervale_deschise(self.matr[col::self.NR_COLOANE], jucator)

        # diagonale \
        # TO DO..........
        # bottom triangle
        for i in range (Joc.NR_CONNECT-1, min(Joc.NR_LINII, Joc.NR_COLOANE)):
            rez += nr_intervale_deschise(self.matr[Joc.NR_COLOANE-i-1:(Joc.NR_CONNECT+i-2)*Joc.NR_COLOANE:Joc.NR_COLOANE+1], jucator)
        # middle part if Col > Row
        for i in range (Joc.NR_LINII-Joc.NR_COLOANE-1):
            rez += nr_intervale_deschise(self.matr[(i+1)*Joc.NR_COLOANE:(Joc.NR_COLOANE+i+1)*Joc.NR_COLOANE:Joc.NR_COLOANE+1], jucator)
        # middle part if Row > Col
        for i in range (Joc.NR_COLOANE-Joc.NR_LINII-1):
            rez += nr_intervale_deschise(self.matr[Joc.NR_COLOANE*Joc.NR_LINII-i-2::-Joc.NR_COLOANE-1], jucator)
        # top triangle
        for i in range (max(1 if Joc.NR_COLOANE == Joc.NR_LINII else 0, Joc.NR_LINII-Joc.NR_COLOANE), Joc.NR_LINII-Joc.NR_CONNECT+1):
            rez += nr_intervale_deschise(self.matr[i*Joc.NR_COLOANE::Joc.NR_COLOANE+1], jucator)

        # diagonale /
        # TO DO..........
        # bottom triangle
        for i in range (Joc.NR_CONNECT-1, min(Joc.NR_LINII, Joc.NR_COLOANE)):
            rez += nr_intervale_deschise(self.matr[i*Joc.NR_COLOANE:i-1:-Joc.NR_COLOANE+1], jucator)
        # middle part if Col > Row
        for i in range (Joc.NR_COLOANE-Joc.NR_LINII-1):
            rez += nr_intervale_deschise(self.matr[Joc.NR_LINII+i::Joc.NR_COLOANE-1], jucator)
        # middle part if Row > Col
        for i in range (Joc.NR_LINII-Joc.NR_COLOANE-1):
            rez += nr_intervale_deschise(self.matr[(Joc.NR_COLOANE + i) * Joc.NR_COLOANE:(i+1) * Joc.NR_COLOANE:-Joc.NR_COLOANE+1], jucator)
        # top triangle
        for i in range (max(1 if Joc.NR_COLOANE == Joc.NR_LINII else 0, Joc.NR_COLOANE - Joc.NR_LINII), Joc.NR_COLOANE-Joc.NR_CONNECT+1):
            rez += nr_intervale_deschise(self.matr[max(i, (Joc.NR_LINII+i-Joc.NR_COLOANE+1)*Joc.NR_COLOANE-1):(Joc.NR_LINII-1)*Joc.NR_COLOANE+i+1:Joc.NR_COLOANE-1], jucator)

        return rez

    def fct_euristica(self):
        # TO DO: alte variante de euristici? ..... pare destul de buna, la alta nu m+am putut gandi

        # (pe linii, coloane, diagonale) 
        # intervale_deschisa(juc) = cate intervale de 4 pozitii nu contin juc_opus
        # <=> contin doar juc_current si GOL
        return self.nr_intervale_deschise(Joc.JMAX) - self.nr_intervale_deschise(Joc.JMIN)

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
    # ?? TO DO:
    # de adagat parametru "pozitie", ca sa nu verifice mereu toata tabla,
    # ci doar linia, coloana, 2 diagonale pt elementul nou, de pe "pozitie"
    # => trebuie sa retinem "pozitia" ultimei mutari din aceasta configuratie

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
        Joc.JMIN = str(input("Doriti sa jucati cu {} sau cu {}? ".format(s1, s2))).upper()
        if (Joc.JMIN in Joc.SIMBOLURI_JUC):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie {} sau {}.".format(s1, s2))
    Joc.JMAX = s1 if Joc.JMIN == s2 else s2

    #initializare tabla
    tabla_curenta = Joc()
    print("Tabla initiala")
    print(str(tabla_curenta))

    #creare stare initiala
    stare_curenta = Stare(tabla_curenta, Joc.SIMBOLURI_JUC[0], Stare.ADANCIME_MAX)

    linie = -1
    coloana = -1
    while True :
        if (stare_curenta.j_curent == Joc.JMIN):
            #muta jucatorul
            raspuns_valid=False
            while not raspuns_valid:
                try:
                    coloana = int(input("coloana = "))

                    # TO DO......
                    # de verificat daca "coloana" este in intervalul corect,
                    # apoi de gasit pe ce "linie" este cea mai de jos
                    # casuta goala de pe acea "coloana"

                    #if ........
                        # ..........

                        #if ......
                        #    print("Toata coloana este ocupata.")
                    #else:
                    #    print("Coloana invalida (trebuie sa fie un numar intre 0 si {}).".format(Joc.NR_COLOANE - 1))
                    if coloana >= Joc.NR_COLOANE:
                        print("Coloana invalida (trebuie sa fie un numar intre 0 si {}).".format(Joc.NR_COLOANE - 1))
                        continue
                    try:
                        linie = stare_curenta.tabla_joc.matr[coloana::Joc.NR_COLOANE].index(Joc.GOL)
                        raspuns_valid = True
                    except ValueError: 
                         print("Coloana Plina (trebuie aleasa o coloana unde se mai poate pune o piesa).")                     
                except ValueError:
                    print("Coloana trebuie sa fie un numar intreg.")

            #dupa iesirea din while sigur am valida coloana
            #deci pot plasa simbolul pe "tabla de joc"
            pozitie = linie * Joc.NR_COLOANE + coloana
            stare_curenta.tabla_joc.matr[pozitie] = Joc.JMIN

            #afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))

            #testez daca jocul a ajuns intr-o stare finala
            #si afisez un mesaj corespunzator in caz ca da
            if (afis_daca_final(stare_curenta)):
                break

            #S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()

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
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            #preiau timpul in milisecunde de dupa mutare
            t_dupa=int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de "+str(t_dupa-t_inainte)+" milisecunde.")

            if (afis_daca_final(stare_curenta)):
                break

            #S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()

if __name__ == "__main__" :
        main()