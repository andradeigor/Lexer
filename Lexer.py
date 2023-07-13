import re
import sys
from Token import Token
from collections import deque
from Parser import Parser
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
            token = Token(type_name, Valor)
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



def printRaiz(raiz):
  if(raiz.tag):
    vars = raiz.vars
    prints = raiz.prints
    for var in vars:
      print(var.tag, var.nome, var.valor.e1)
    for pri in prints:
      print(pri.e1)
printRaiz(raiz)
