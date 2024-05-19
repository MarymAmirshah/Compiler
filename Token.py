class Tokens:
    def __init__(self, lexeme, token, index):
        self.lexeme = lexeme
        self.token = token
        self.index = index

    def lt(self, other):
        return self.index < other.index

    def str(self):
        if self.token == 'T_Whitespace':
            representation_string = f"{self.index - len(self.lexeme)}: whitespace -> {self.token}"
        else:
            representation_string = f"{self.index - len(self.lexeme)}: {self.lexeme} -> {self.token}"

        return representation_string
