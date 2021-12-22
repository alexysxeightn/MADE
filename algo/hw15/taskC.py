NUMBERS = '0123456789'
OPERANDS = '+-*().'
NEW_YEAR_TOKENS = ('Ded Moroz', 'Moroz', 'Snegurochka', 'Podarok(')

NEW_YEAR_CONSTANTS = {
    'Ded Moroz': 2020,
    'Moroz': -30,
    'Snegurochka': 10
}

def function_podarok(x):
    return x + 5 if x > 0 else abs(x)
    
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
        
        i, n = 0, len(s)
        
        while i < n:
            if s[i] in NUMBERS:
                num_str = ''
                while i < n and s[i] in NUMBERS:
                    num_str += s[i]
                    i += 1
                self.tokens.append(num_str)
            elif i < n and s[i] in OPERANDS:
                self.tokens.append(s[i])
                i += 1
            else:
                for token in NEW_YEAR_TOKENS:
                    if i+len(token) < n and s[i:i+len(token)] == token:
                        self.tokens.append(token)
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
            
        elif self.cur_token in NEW_YEAR_CONSTANTS.keys():
            number = NEW_YEAR_CONSTANTS[self.cur_token]
            self.next_token()
            assert self.cur_token != '('
            return number
            
        elif 'Podarok(' == self.cur_token:
            self.next_token()
            result = function_podarok(self.parse_expr())
            assert ')' == self.cur_token
            self.next_token()
            return result
            
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
