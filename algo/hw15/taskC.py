NEW_YEAR_TOKENS = ('Ded Moroz', 'Moroz', 'Snegurochka', 'Podarok(')

NEW_YEAR_CONSTANTS = {
    'Ded Moroz': 2020,
    'Moroz': -30,
    'Snegurochka': 10
}

def function_podarok(x):
    return x + 5 if x > 0 else abs(x)

def is_digit(c):
    return 0 <= ord(c) - ord('0') <= 9 

def is_operand(c):
    return c in '+-*().'

def is_space(c):
    return ' ' == c

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
            
        elif token in NEW_YEAR_TOKENS:
            self.type = 'function_podarok' if 'Podarok(' == token else 'new_year_constant'
            self.subtype = self.type
        
        else:
            self.type = 'unknown'

class Lexer:
    def __init__(self, s):
        self.flag_of_wrong = False
        self.tokens = []
        
        i, n = 0, len(s)
        
        while i < n:
            if is_digit(s[i]):
                num_str = ''
                while i < n and is_digit(s[i]):
                    num_str += s[i]
                    i += 1
                self.tokens.append(Token(num_str))
            elif i < n and is_operand(s[i]):
                self.tokens.append(Token(s[i]))
                i += 1
            elif is_space(s[i]):
                i += 1
            else:
                for token in NEW_YEAR_TOKENS:
                    if i+len(token) < n and s[i:i+len(token)] == token:
                        self.tokens.append(Token(token))
                        i += len(token)
                        break
                else:
                    self.flag_of_wrong = True
                    break

    def token_generator(self):
        for token in self.tokens:
            yield token

class Parser(Lexer):
    def __init__(self, s):
        super().__init__(s)
        self.cur_token = None
        self.tokens_gen = self.token_generator()
    
    def next_token(self):
        self.cur_token = next(self.tokens_gen)
    
    def parse_expr(self):
        result = self.parse_sum()
        while 'sum' == self.cur_token.type:
            c = self.cur_token
            self.next_token()
            if 'plus' == c.subtype:
                result += self.parse_sum()
            else:
                result -= self.parse_sum()
        return result
            
    def parse_sum(self):
        result = self.parse_product()
        while 'multiplication' == self.cur_token.subtype:
            self.next_token()
            result *= self.parse_product()
        return result
        
    def parse_product(self):
        if self.cur_token.type in ('number', 'new_year_constant'):
            if 'number' == self.cur_token.type:
                number = self.cur_token.value
            else:
                number = NEW_YEAR_CONSTANTS[self.cur_token.value]
            self.next_token()
            assert self.cur_token.subtype != 'left_bracket'
            return number
            
        elif self.cur_token.subtype in ('left_bracket', 'function_podarok'):
            c = self.cur_token
            self.next_token()
            if 'function_podarok' == c.type:
                result = function_podarok(self.parse_expr())
            else:
                result = self.parse_expr()
            assert 'right_bracket' == self.cur_token.subtype
            self.next_token()
            return result
        
        else:
            raise Exception()

    def parse(self):
        try:
            assert not self.flag_of_wrong
            self.next_token()
            result = self.parse_expr()
            assert 'end_token' == self.cur_token.type
            return result
        except:
            return 'WRONG'

s = str(input())
parser = Parser(s)
print(parser.parse())
