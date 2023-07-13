from ExpNum import ExpNum


class ComandoAtribuicao:
    def __init__(self,nome,valor):
        self.nome = nome
        self.valor = valor


class Parser:
    def __init__(self, Tokens):
        self.Tokens = Tokens

    def peek(self, tag):
        return self.Tokens[0] == tag
    
    def consome(self, tag):
        if(not self.nextToken.tag == tag):
            return SyntaxError
        token = self.Tokens.popleft()
        return token
    
    #def parserS(self):
    
    def parseE(self):
        e = self.parseT()
        while(True):
            if(self.peek("MAIS")):
                self.consome("MAIS")
                temp = self.parseT()
                e = expAdd(e, temp)
            elif(self.peek("MENOS")):
                self.consome("MENOS")
                temp = self.parseT()
                e = expSub(e, temp)
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

