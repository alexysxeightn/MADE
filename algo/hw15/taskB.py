NUMBERS = '0123456789'
OPERANDS = '+-*().'

def is_number(s):
    if '0' == s:
        return True
    if s[0] not in NUMBERS[1:]:
        return False
    for symbol in s[1:]:
        if symbol not in NUMBERS:
            return False
    return True

class Lexer:
    def __init__(self, s):
        self.flag_of_wrong = False
        self.tokens = []
        
        num_str = ''
        for symbol in s:
            if symbol in NUMBERS:
                num_str += symbol
            elif symbol in OPERANDS:
                if num_str:
                    self.tokens.append(num_str)
                    num_str = ''
                self.tokens.append(symbol)
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
        while self.cur_token in '+-':
            c = self.cur_token
            self.next_token()
            if '+' == c:
                result = result + self.parse_sum()
            else:
                result = result - self.parse_sum()
        return result
            
    def parse_sum(self):
        result = self.parse_product()
        while '*' == self.cur_token:
            self.next_token()
            result = result * self.parse_product()
        return result
        
    def parse_product(self):
        
        if is_number(self.cur_token):
            number = self.cur_token
            self.next_token()
            assert self.cur_token != '('
            return int(number)
            
        elif '(' == self.cur_token:
            self.next_token()
            answer = self.parse_expr()
            assert ')' == self.cur_token
            self.next_token()
            return answer
        
        else:
            raise Exception()

    def parse(self):
        try:
            assert not self.flag_of_wrong
            self.next_token()
            result = self.parse_expr()
            assert '.' == self.cur_token
            return result
        except:
            return 'WRONG'
            
s = str(input())
parser = Parser(s)
print(parser.parse())
