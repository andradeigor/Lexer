import re
import sys
from collections import deque

class Token:
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value

    def __str__(self):
        return f'Token: {self.tag} Valor: {self.value} '


class ExpNum:
    def __init__(self, num):
        self.tag = "NUMERO"
        self.num = num

class ExpRaiz:
    def __init__(self,e1):
        self.tag = "RAIZQUADRADA"
        self.e1 = e1

class ExpPar:
    def __init__(self,e1):
        self.tag = "PARENTESES"
        self.e1 = e1


class ComandoAtribuicao:
    def __init__(self,nome,e1):
        self.tag = "ATRIBUICAO"
        self.nome = nome
        self.e1 = e1

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

class ExpRaizDaArvore:
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
            return SyntaxError()
        token = self.Tokens.popleft().value
        return token
    
    def parseS(self):
        e = self.parseVS()
        p = self.parsePS()
        raiz = ExpRaizDaArvore(e,p)
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
        else:
            return SyntaxError()
        

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
                #aqui a verificação não pode ocorrer pq a quebra do while está condicionada a um caso não coberto acima
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
        while not self.peek("EOF"):
            self.consome("ARROBA")
            exp = self.parseE()
            prints.append(ComandoPrint(exp))  
        return prints

 

tokens = deque([])



def read_file(input):
  text = input.read()
  lines = text.split("\n")
  for line in lines:
    analysis(line)

def analysis(text):
  
  len_original = len(text)

  types = {
    "IGUAL" : r"=",
    "NOME" : r"[a-zA-Z_][a-zA-Z_0-9]*",
    "NUMERO" : r"[0-9][0-9]*",
    "ESPAÇO" : r"\s+",
    "MENOS": r"\-",
    "MAIS": r"\+",
    "MULTIPLICA": r"\*",
    "DIVISAO": r"\/",
    "PARENTESESABRE":  r"\(",
    "PARENTESESFECHA":  r"\)",
    "ARROBA": r"@"
  }



  keywords = ["sqrt"]

  while(len(text)):
    attemp = 0
    for type_name, type_regex in types.items():
      attemp += 1
      type = re.compile(type_regex)
      match_result = type.match(text)
      if match_result:
        Valor = match_result.group(0)
        end_match = match_result.end()
        if type_name == "ESPAÇO" and len(text) == len_original:
          type_name = "TABULAÇÃO"
        elif type_name == "NOME" and Valor in keywords:
          type_name = "KEYWORD"
        if(type_name != "ESPAÇO"):
            token = Token(type_name, Valor) if type_name!="NUMERO" else Token(type_name, float(Valor))
            tokens.append(token)
        text = text[end_match:]
        break
      if attemp == 11:
        assert(False)



def calcula(exp,env):
  if(exp.tag == "ADICAO"):
    return calcula(exp.e1,env) + calcula(exp.e2,env)
  elif(exp.tag == "NUMERO"):
    return exp.num
  elif(exp.tag == "SUBTRACAO"):
    return calcula(exp.e1,env) - calcula(exp.e2,env)
  elif(exp.tag == "MULTIPLICACAO"):
    return calcula(exp.e1,env) * calcula(exp.e2,env)
  elif(exp.tag == "DIVISAO"):
    return calcula(exp.e1,env) / calcula(exp.e2,env)
  elif(exp.tag == "NEGATIVO"):
    return -calcula(exp.e1,env)
  elif(exp.tag =="VAR"):
    return env[exp.nome]
  elif(exp.tag == "PARENTESES"):
    return calcula(exp.e1,env)
  elif(exp.tag == "RAIZQUADRADA"):
    return (calcula(exp.e1,env))**(1/2)
  elif(exp.tag == "ATRIBUICAO"):
    env[exp.nome] = calcula(exp.e1,env)
    return env[exp.nome]
  elif(exp.tag == "PRINT"):
    print(calcula(exp.e1, env))
  elif(exp.tag=="RAIZARVORE"):
    for var in exp.vars:
      calcula(var, env)
    for pri in exp.prints:
      calcula(pri, env)
  else:
    SystemError()
    assert(False)

def main():
  read_file(sys.stdin)
  tokens.append(Token("EOF",None))
  parse = Parser(tokens)
  raiz = parse.parseS()

  env = {}
  calcula(raiz,env)

if __name__=="__main__":
   main()