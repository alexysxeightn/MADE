NUMBERS = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
OPERANDS = ('+', '-', '*', '(', ')', '.')

flag_of_wrong = False

def is_number(s):
    if s == '0':
        return True
    if s[0] not in NUMBERS[1:]:
        return False
    for symbol in s[1:]:
        if symbol not in NUMBERS:
            return False
    return True

class Lexer:
    def __init__(self, s):
        global flag_of_wrong
        self.tokens = []
        
        if s.count('(') != s.count(')'):
            flag_of_wrong = True
        
        s = s.replace(' ', '')
        
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
                flag_of_wrong = True
                break
        
    def token_generator(self):
        for token in self.tokens:
            yield token

class Parser:
    def __init__(self, Lexer):
        self.tokens = Lexer.token_generator()
        self.cur_token = None
    
    def next_token(self):
        self.cur_token = next(self.tokens)
    
    def parse_expr(self):
        result = self.parse_sum()
        while self.cur_token == '+' or self.cur_token == '-':
            c = self.cur_token
            self.next_token()
            if c == '+':
                result = result + self.parse_sum()
            else:
                result = result - self.parse_sum()
        return result
            
    def parse_sum(self):
        result = self.parse_product()
        while self.cur_token == '*':
            self.next_token()
            result = result * self.parse_product()
        return result
        
    def parse_product(self):
        if is_number(self.cur_token):
            number = self.cur_token
            self.next_token()
            if self.cur_token == '(':
                raise Exception()
            return int(number)
        elif self.cur_token == '(':
            self.next_token()
            answer = self.parse_expr()
            assert self.cur_token == ')'
            self.next_token()
            return answer
        else:
            raise Exception()

    def parse(self):
        if flag_of_wrong:
            return 'WRONG'
        else:
            self.next_token()
            return self.parse_expr()

s = str(input())
lexer = Lexer(s)
parser = Parser(lexer)

try:
    print(parser.parse())
except:
    print('WRONG')
