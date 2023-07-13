import re
import sys
from Token import Token
from collections import deque
tokens = deque([])


def read_file(arg_list):
  if len(arg_list) == 2:
    file=arg_list[1]
  else:
    file="lexer.py"
  with open(file, encoding="utf8") as f:
    text = f.read()
    lines = text.split("\n")
    for line in lines:
      analysis(line)

def analysis(text):
  
  len_original = len(text)

  types = {
    "IGUAL" : r"=",
    "NOME" : "[a-zA-Z_][a-zA-Z_0-9]*",
    "NÚMERO" : "[0-9][0-9]*",
    "ESPAÇO" : r"\s+",
    "MENOS": r"\-",
    "MAIS": r"\+",
    "MULTIPLICA": r"\*",
    "DIVISAO": r"\/",
    "PARENTESES":  r"\(|\)",
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
      if attemp == 7:
        print("ERRO!")
        break

read_file(sys.argv)

for token in tokens:
    print(token)