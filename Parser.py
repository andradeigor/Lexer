from ExpNum import ExpNum


class ExpRaiz:
    def __init__(self,e1):
        self.tag = "RAIZQUADRADA"
        self.e1 = e1

class ExpPar:
    def __init__(self,e1):
        self.tag = "PARENTESES"
        self.e1 = e1


class ComandoAtribuicao:
    def __init__(self,nome,valor):
        self.tag = "ATRIBUICAO"
        self.nome = nome
        self.valor = valor

class ComandoPrint:
    def __init__(self,e1):
        self.tag = "PRINT"
        self.e1 = e1

class ExpMul:
    def __init__(self,e1, e2):
        self.tag = "MULTIPLICACAO"
        self.e1 = e1
        self.e2 = e2

class ExpDiv:
    def __init__(self,e1, e2):
        self.tag = "DIVISAO"
        self.e1 = e1
        self.e2 = e2
class ExpAdd:
    def __init__(self,e1, e2):
        self.tag = "ADICAO"
        self.e1 = e1
        self.e2 = e2
class ExpSub:
    def __init__(self,e1, e2):
        self.tag = "SUBTRACAO"
        self.e1 = e1
        self.e2 = e2
class ExpNeg:
    def __init__(self,e1):
        self.tag = "NEGATIVO"
        self.e1 = e1

class ExpVar:
    def __init__(self,nome):
        self.tag = "VAR"
        self.nome = nome

class expRaizDaArvore:
    def __init__(self,vars,prints):
        self.tag = "RAIZARVORE"
        self.vars = vars
        self.prints = prints
    

class Parser:
    def __init__(self, Tokens):
        self.Tokens = Tokens

    def peek(self, tag):
        return self.Tokens[0].tag == tag
    
    def consome(self, tag):
        if(not self.Tokens[0].tag == tag):
            return SyntaxError
        token = self.Tokens.popleft().value
        return token
    
    def parseS(self):
        e = self.parseVS()
        p = self.parsePS()
        raiz = expRaizDaArvore(e,p)
        return raiz
    
    def parseF(self):
        if(self.peek("NUMERO")):
            num = self.consome("NUMERO")
            return ExpNum(num)
        elif(self.peek("NOME")):
            nome = self.consome("NOME")
            return ExpVar(nome)
        elif(self.peek("KEYWORD")):
            self.consome("KEYWORD")
            self.consome("PARENTESESABRE")
            e = self.parseE()
            self.consome("PARENTESESFECHA")
            return ExpRaiz(e)
        elif(self.peek("PARENTESESABRE")):
            self.consome("PARENTESESABRE")
            e = self.parseE()
            self.consome("PARENTESESFECHA")
            return ExpPar(e)
        elif(self.peek("MENOS")):
            self.consome("MENOS")
            e = self.parseF()
            return ExpNeg(e)
    def parseT(self):
        e = self.parseF()
        while(True):
            if(self.peek("MULTIPLICA")):
                self.consome("MULTIPLICA")
                temp = self.parseF()
                e = ExpMul(e, temp)
            elif(self.peek("DIVISAO")):
                self.consome("DIVISAO")
                temp = self.parseF()
                e = ExpDiv(e, temp)
            else:
                break
        return e  

    def parseE(self):
        e = self.parseT()
        while(True):
            if(self.peek("MAIS")):
                self.consome("MAIS")
                temp = self.parseT()
                e = ExpAdd(e, temp)
            elif(self.peek("MENOS")):
                self.consome("MENOS")
                temp = self.parseT()
                e = ExpSub(e, temp)
            else:
                break
        return e                


    def parseVS(self):
        variaveis = []
        while self.peek("NOME"):
            var = self.consome("NOME")
            self.consome("IGUAL")
            exp = self.parseE()
            variaveis.append(ComandoAtribuicao(var,exp))
        return variaveis
    def parsePS(self):
        prints = [] 
        while self.peek("ARROBA"):
            self.consome("ARROBA")
            exp = self.parseE()
            prints.append(ComandoPrint(exp))  
        return prints


