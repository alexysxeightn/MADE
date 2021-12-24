def is_digit(c):
    return 0 <= ord(c) - ord('0') <= 9 

def is_operand(c):
    return c in '+-*().'

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
        self.flag_of_wrong = False
        self.tokens = []
        
        num_str = ''
        for symbol in s:
            if is_digit(symbol):
                num_str += symbol
            elif is_operand(symbol):
                if num_str:
                    self.tokens.append(Token(num_str))
                    num_str = ''
                self.tokens.append(Token(symbol))
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
        
        if 'number' == self.cur_token.type:
            number = self.cur_token.value
            self.next_token()
            assert self.cur_token.subtype != 'left_bracket'
            return number
            
        elif 'left_bracket' == self.cur_token.subtype:
            self.next_token()
            answer = self.parse_expr()
            assert 'right_bracket' == self.cur_token.subtype
            self.next_token()
            return answer
        
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
