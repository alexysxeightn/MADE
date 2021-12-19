NUMBERS = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

class Lexer:
    def __init__(self, s):
        self.tokens = []
        
        num_str = ''
        for symbol in s:
            if symbol in NUMBERS:
                num_str += symbol
            else:
                if num_str:
                    self.tokens.append(num_str)
                    num_str = ''
                self.tokens.append(symbol)
        
    def token_generator(self):
        for token in self.tokens:
            yield token

s = str(input())
lexer = Lexer(s)
token_generator = lexer.token_generator()

token = next(token_generator)
while token != '.':
    print(token)
    token = next(token_generator)
