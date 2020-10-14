import numpy

class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 8
    NR_LINII   = 8
    SIMBOLURI_JOC = ['n', 'a']
    JMIN = None  # 'a'
    JMAX = None  # 'n'
    GOL = '#'
    POS = '.'
    def __init__(self, tabla=None, tura = None):
        if tabla == None:
            tabla =  np.full((NR_LINII, NR_COLOANE), Joc.GOL)
            stLine = (Joc.NR_LINII  -1) // 2  
            stCol  = (Joc.NR_COLOANE-1) //2
            tabla [stLine, stCol] = tabla [stLine + 1, stCol + 1] = 'a'
            tabla [stLine, stCol + 1] = tabla [stLine + 1, stCol] = 'n'
            tura = 'n'
        self.matr = tabla
        self.turn = tura
        print (self.matr)

    def oponent (self):
        return Joc.SIMBOLURI_JOC[0 if Joc.SIMBOLURI_JOC[0] != self.turn else 1]

    def __str__(self):
        maxSp = len(str(Joc.NR_LINII))
        sir = " " * (maxSp+2)
        for nr_col in range(self.NR_COLOANE):
            sir += chr(ord('a') + nr_col) + ' '
        sir += '\n' + " " * (maxSp+2) + '-' * (2 * Joc.NR_COLOANE - 1) + '\n'

        for lin in range(self.NR_LINII):
            k = lin * self.NR_COLOANE
            sir += (str(lin) + (" " * (maxSp - len(str(lin)) + 1)) + "|" + " ".join([str(x) for x in self.matr[k : k+self.NR_COLOANE]])+"\n")
        return sir

    # def mutariPos(self):


# print (Joc())
#Joc()
print ("OK")



