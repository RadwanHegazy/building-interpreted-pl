import sys, os

class Interpreter : 

    def printkeyword(self, val): 
        res = self.evaluate(val)
        print(res)

    def inputkeyword (self, val) : 
        var_name,screen = val.split('&')
        input_value = input(screen.strip()[1:-1])
        self.__vars[var_name.strip()] = self.evaluate(input_value)

    def calckeyword(self, val) : 
        print(eval(val.strip()))

    def oskeyword(self, val) : 
        res = os.system(val.strip())
        if res:
            print(res)

    def __init__(self, code : str):
        code_lines = code.split('\n')
        self.__vars = {}
        self.__keywords = {
            'print' : self.printkeyword,
            'input' : self.inputkeyword,
            'calc' : self.calckeyword,
            'os' : self.oskeyword
        }
        for line in code_lines : 
            if line.startswith('#') or line == "" : 
                continue
            
            if '=>' in line:
                keyword,expr = line.split('=>')
                keyword = keyword.strip()

                try:
                    self.__keywords[keyword](expr)
                except KeyError:
                    print("Error: Invalid Keyword : ", keyword)
            elif '=' in line:
                (var_name, _,val_str) = line.split(maxsplit=2)
                if var_name.endswith('[]') : 
                    var_name = var_name.replace('[]','')
                    data_list = val_str.split(',')
                    for i in range(len(data_list)):
                        self.__vars[f'{var_name}[{i}]'] = self.evaluate(data_list[i])
                else:
                    self.__vars[var_name.strip()] = self.evaluate(val_str)


    def evaluate(self, line : str) : 
        tokens = line.split()
        stack = []
        for token in tokens:
            if token.isnumeric():
                stack.append(int(token))
            elif token in self.__vars:
                stack.append(self.__vars[token])
            elif self.isfloat(token) : 
                stack.append(float(token))
            elif token.startswith('"') or token.startswith("'") :
                stack.append(token[1:-1])
            else:
                # implement arthimetic operations
                rhs = stack.pop()
                lhs = stack.pop()

                if token == '+' : 
                    stack.append(lhs + rhs)
                elif token == '*' : 
                    stack.append(lhs * rhs)

        return stack[0]        

    def isfloat(self, val : str) : 
        isfloat = True
        if '.' in val:
            for i in val.split('.'): # 1.1 -> ['1','1']
                if not i.isnumeric() :
                    isfloat = False
        else:
            isfloat = False
        return isfloat

# python interpreter.py filename


if __name__ == "__main__" : 
    filename = sys.argv[1]
    inter = Interpreter(
        code = open(filename, 'r').read()
    )