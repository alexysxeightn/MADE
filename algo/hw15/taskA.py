NUMBERS = '0123456789'

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

s = input()
lexer = Lexer(s)
print(*lexer.tokens[:-1], sep='\n')
