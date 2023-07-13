import re
import sys
from Token import Token
from collections import deque
from Parser import Parser, ExpAdd,ExpNum, ExpNeg, ExpMul, ExpDiv, ExpPar, ExpSub, ExpRaiz
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
    "NOME" : "[a-zA-Z_][a-zA-Z_0-9]*",
    "NUMERO" : "[0-9][0-9]*",
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
        print("ERRO!")
        break


read_file(sys.stdin)
tokens.append(Token("EOF",None))
parse = Parser(tokens)
raiz = parse.parseS()

exp = ExpMul(ExpAdd(ExpNeg(ExpNum(5)), ExpNum(8)), ExpSub(ExpRaiz(ExpNum(25)), ExpPar(ExpMul(ExpNum(3),ExpNum(3))))) 


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
    print(exp)
    assert(False)


def printRaiz(raiz):
  env = {}
  calcula(raiz,env)
    
  
    
printRaiz(raiz)
