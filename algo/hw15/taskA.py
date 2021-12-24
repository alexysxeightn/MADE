class Token:
    def __init__(self, s, type):
        self.value = s
        self.type = type
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        print(self.value, end=' ')

class Number_Token(Token):
    def __init__(self, s):
        super().__init__(int(s), 'number')

class Operand_Token(Token):
    def __init__(self, s):
        super().__init__(s, 'operand')

class Lexer:
    def __init__(self, s):
        self.tokens = []
        
        num_str = ''
        for symbol in s:
            if is_digit(symbol):
                num_str += symbol
            else:
                if num_str:
                    self.tokens.append(Number_Token(num_str))
                    num_str = ''
                self.tokens.append(Operand_Token(symbol))

def is_digit(c):
    return 0 <= ord(c) - ord('0') <= 9 

def main():
    s = input()
    lexer = Lexer(s)
    print(*lexer.tokens[:-1], sep='\n')
    
if __name__ == '__main__':
    main()
