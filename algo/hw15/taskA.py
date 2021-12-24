def is_digit(c):
    return 0 <= ord(c) - ord('0') <= 9 

def is_number(s):
    if '0' == s:
        return True
    if is_digit(s[0]) and ord(s[0]) != ord('0'):
        for symbol in s[1:]:
            if not is_digit(symbol):
                return False
    else:
        return False
    return True

class Token:
    def __init__(self, token):
        self.type = None
        self.subtype = None
        self.value = token
        
        if token in '+-':
            self.type = 'sum'
            self.subtype = 'plus' if '+' == token else 'minus'

        elif '*' == token:
            self.type = 'product'
            self.subtype = 'multiplication'
    
        elif token in '()':
            self.type = 'bracket'
            self.subtype = 'left_bracket' if '(' == token else 'right_bracket'
    
        elif '.' == token:
            self.type = 'end_token'
    
        elif is_number(token):
            self.type, self.value = 'number', int(token)

        else:
            self.type = 'unknown'

class Lexer:
    def __init__(self, s):
        self.tokens = []
        
        num_str = ''
        for symbol in s:
            if is_digit(symbol):
                num_str += symbol
            else:
                if num_str:
                    self.tokens.append(Token(num_str))
                    num_str = ''
                self.tokens.append(Token(symbol))

s = input()
lexer = Lexer(s)
for token in lexer.tokens[:-1]:
    print(token.value)
