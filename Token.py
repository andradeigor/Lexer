class Token:
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value

    def __str__(self):
        return f'Token: {self.tag} Valor: {self.value} '
    