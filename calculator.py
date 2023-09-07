from curses.ascii import isdigit
from operator import pos


class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__
                          
class Stack:
    '''
        >>> x=Stack()
        >>> x.pop()
        >>> x.push(2)
        >>> x.push(4)
        >>> x.push(6)
        >>> x
        Top:Node(6)
        Stack:
        6
        4
        2
        >>> x.pop()
        6
        >>> x
        Top:Node(4)
        Stack:
        4
        2
        >>> len(x)
        2
        >>> x.peek()
        4
    '''
    def __init__(self):
        self.top:Node = None
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__

    def isEmpty(self):

        return self.top == None

    def __len__(self): 

        count = 0
        current = self.top
        while current is not None:
            count += 1
            current = current.next
        return count

    def push(self,value):

        new = Node(value)
        new.next = self.top
        self.top = new

    def pop(self):

        top_node = self.top
        if top_node is not None:
            self.top = self.top.next
            return top_node.value
        return None

    def peek(self):

        if self.isEmpty():
            return None
        return self.top.value
        

class Calculator:
    def __init__(self):
        self.__expr = None


    @property
    def getExpr(self):
        return self.__expr

    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr=new_expr
        else:
            print('setExpr error: Invalid expression')
            return None

    def _isNumber(self, txt):
        '''
            >>> x=Calculator()
            >>> x._isNumber(' 2.560 ')
            True
            >>> x._isNumber('7 56')
            False
            >>> x._isNumber('2.56p')
            False
            >>> x._isNumber('-3')
            True
        '''

        num = txt.strip()
        try:
            float(num)
            return True
        except:
            return False


    def _cleanExpr(self, expr:str):
        """
        Clean an expression by removing trailing whitespaces and consequtive spacing

        >>> calc = Calculator()
        >>> calc._cleanExpr(" 3    + 2 -   0 *    5    +  6")
        '3 + 2 - 0 * 5 + 6'
        >>> calc._cleanExpr("   2 + (2   -     -3)    *   5")
        '2 + ( 2 - -3 ) * 5'
        >>> calc._cleanExpr("   3 *     9      +  2   - 1     + 7     + 8")
        '3 * 9 + 2 - 1 + 7 + 8'
        >>> calc._cleanExpr("3 *-3 + 9")
        '3 * -3 + 9'
        >>> calc._cleanExpr("3.23 + 5.04 - 7.04")
        '3.23 + 5.04 - 7.04'
        >>> calc._cleanExpr(" 2.5 +         3 * (2 + ( 3.0) * ( 5^2-2 * 3 ^ ( 2 )         ) * ( 4 ) ) * ( 2 / 8 + 2 * ( 3 - 1 /3 ) ) - 2 / 3^ 2")
        '2.5 + 3 * ( 2 + ( 3.0 ) * ( 5 ^ 2 - 2 * 3 ^ ( 2 ) ) * ( 4 ) ) * ( 2 / 8 + 2 * ( 3 - 1 / 3 ) ) - 2 / 3 ^ 2'
        >>> calc._cleanExpr("7^2^3")
        '7 ^ 2 ^ 3'
        """
        if not isinstance(expr, str):
            print("Invalid Expression")
            return None

        allowed_ops = "+-*/^()"
        # Split according to whitespace
        expr = expr.split()
        mutated = []

        # Although expr was split, some operators may be conjoined to numbers
        for sub in expr:
            # Sub is not an operator and not a number... meaning it is a mix of both
            # A negative number will not match this if statement
            if not (self._isNumber(sub) and len(sub) > 1) or sub.startswith("+"):
                # Loop through str
                # Keep var that adds ch iteratively
                # append on operator or end of str
                term = ""
                for ch in sub:
                    # `ch in allowed_ops` --> Check if operator
                    # `not (term == "" and ch == "-")` --> handles negative number
                    if ch in allowed_ops and not (term == "" and ch == "-" and (mutated[-1] in allowed_ops[:-2])):
                        if term != "":
                            mutated.append(term)
                        mutated.append(ch)
                        term = ""
                    else:
                        if ch != " ":
                            term += ch
                if term != "":
                    mutated.append(term)
            else:
                mutated.append(sub)

        return " ".join(mutated)


    def _isValidExpr(self, expr):
        """
        Check if an expression is valid given the following criteria:
            - No unsupported operators
            - No consecutive operators (exception: operator followed by - sign)
            - No missing operands/operators
            - Parenthesis must be balanced
            - No implied multiplication
        
        >>> c = Calculator()
        >>> c._isValidExpr("5 + -5")
        True
        >>> c._isValidExpr("(5 + 6))")
        False
        >>> c._isValidExpr("5(6)")
        False
        >>> c._isValidExpr("2 + 2 / 2")
        True
        >>> c._isValidExpr("4 3 2 + 1")
        False
        >>> c._isValidExpr("( .5 )")
        True
        >>> c._isValidExpr("((2))")
        True
        >>> c._isValidExpr("427.0 * 7 / 122.0")
        True
        """
        if not isinstance(expr, str):
            #print(f"Invalid expression: {expr}, Not a str")
            return False

        allowed_symbols = "+*/^.-() "
        allowed_digits = "0123456789"

        # Expression cannot start/end with an operator
        if expr[0] in allowed_symbols[:-4] or expr[-1] in allowed_symbols[:-4]:
            return False

        # Don't allow unsupported operators
        for ch in expr:
            if ch not in allowed_digits + allowed_symbols:
                return False

        # Check if missing operands
        last = 0
        for ch in expr.split(" "): # The only way we would have missing operands would be if there is a space between 2 numbers
            if self._isNumber(ch):
                last += 1
                if last > 1:
                    return False
            else:
                last = 0

        # Check for unmatched parenthesis
        total = 0
        for ch in expr:
            if ch == "(":
                total += 1
            if ch == ")":
                total -= 1
        if total != 0:
            return False

        expr = expr.replace(" ", "")
        for i in range(len(expr)-1):
            first = expr[i]
            second = expr[i+1]
            # Check for implied multiplication
            if first == ")" and self._isNumber(second) or second == "(" and self._isNumber(first):
                return False
            if first == ")" and second == "(":
                return False
            # Check for consequtive operators
            if first in allowed_symbols[:-3] and (second in allowed_symbols[:-3] and second != "-"):
                return False

        return True
                


    def _getPostfix(self, txt):
        '''
            Required: _getPostfix must create and use a Stack for expression processing
            >>> x=Calculator()
            >>> x._getPostfix('     2 ^       4')
            '2.0 4.0 ^'
            >>> x._getPostfix('          2 ')
            '2.0'
            >>> x._getPostfix('2.1        * 5        + 3       ^ 2 +         1 +             4.45')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.45 +'
            >>> x._getPostfix('2*5.34+3^2+1+4')
            '2.0 5.34 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('2.1 * 5 + 3 ^ 2 + 1 + 4')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.0 +'

            >>> x._getPostfix('( .5 )')
            '0.5'
            >>> x._getPostfix ('( ( 2 ) )')
            '2.0'
            >>> x._getPostfix ('2 * (           ( 5 +-3 ) ^ 2 + (1 + 4 ))')
            '2.0 5.0 -3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('(2 * ( ( 5 + 3) ^ 2 + (1 + 4 )))')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('((2 *((5 + 3  ) ^ 2 + (1 +4 ))    ))')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix('2* (       -5 + 3 ) ^2+ ( 1 +4 )')
            '2.0 -5.0 3.0 + 2.0 ^ * 1.0 4.0 + +'
            >>> x._getPostfix(' 2.5 +         3 * (2 + ( 3.0) * ( 5^2-2 * 3 ^ ( 2 )         ) * ( 4 ) ) * ( 2 / 8 + 2 * ( 3 - 1 /3 ) ) - 2 / 3^ 2')
            '2.5 3.0 2.0 3.0 5.0 2.0 ^ 2.0 3.0 2.0 ^ * - * 4.0 * + * 2.0 8.0 / 2.0 3.0 1.0 3.0 / - * + * + 2.0 3.0 2.0 ^ / -'
            >>> x._getPostfix('7^2^3')
            '7.0 2.0 3.0 ^ ^'
            >>> x._getPostfix('7 * 2 + 3 + 6 * (3 * 2 + 5 ^ 2)')
            '7.0 2.0 * 3.0 + 6.0 3.0 2.0 * 5.0 2.0 ^ + * +'

            # In invalid expressions, you might print an error message, adjust doctest accordingly
            # If you are veryfing the expression in calculate before passing to postfix, this cases are not necessary

            >>> x._getPostfix('2 * 5 + 3 ^ + -2 + 1 + 4')
            >>> x._getPostfix('     2 * 5 + 3  ^ * 2 + 1 + 4')
            >>> x._getPostfix('2    5')
            >>> x._getPostfix('25 +')
            >>> x._getPostfix(' 2 * ( 5      + 3 ) ^ 2 + ( 1 +4 ')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^  2 + ) 1 + 4 (')
            >>> x._getPostfix('2 *      5% + 3       ^ + -2 +1 +4')
        '''

        # Always double-check that the expression is cleaned.
        eq = self._cleanExpr(txt)

        if not self._isValidExpr(eq):
            return None

        postfixStack = Stack()  # method must use postfixStack to compute the postfix expression
        # Keep items neat in a list and concatenate at the end
        postfix_equation = []
        # Split up operands & operators and iterate
        for term in eq.split():
            # ')' signifies that stack must be popped
            if term == ")":
                while not postfixStack.isEmpty() and postfixStack.peek() != "(":
                    postfix_equation.append(postfixStack.pop())
                postfixStack.pop()
            elif term == "(":
                postfixStack.push(term)
            elif term in "*-+/^":
                # If term in stack has a higher precedence, append all higher precedence items in stack first
                # According to Order of Operations, * == / and + == -
                precedence = {"^": 2, "*": 1, "/": 1, "+": 0, "-": 0}
                # `term != "^"` was implemented to pass exponent tests like '7^2^3'... not sure if this is a proper solution, but seems to work in more than one case.
                while postfixStack.peek() != "(" and not postfixStack.isEmpty() and (precedence[postfixStack.peek()] >= precedence[term] and term != "^"):
                    postfix_equation.append(postfixStack.pop())
                postfixStack.push(term)
            else:
                # All operands are directly added to equation
                postfix_equation.append(str(float(term)))
        while not postfixStack.isEmpty():
            postfix_equation.append(postfixStack.pop())

        return " ".join(postfix_equation)


    @property
    def calculate(self):
        '''
            calculate must call _getPostfix
            calculate must create and use a Stack to compute the final result as shown in the video lecture
            
            >>> x=Calculator()
            >>> x.setExpr('4        + 3 -       2')
            >>> x.calculate
            5.0
            >>> x.setExpr('-2 +          3.5')
            >>> x.calculate
            1.5
            >>> x.setExpr('      4 +           3.65  - 2        / 2')
            >>> x.calculate
            6.65
            >>> x.setExpr('23 / 12 - 223 + 5.25      * 4 * 3423')
            >>> x.calculate
            71661.91666666667
            >>> x.setExpr('2-3*4')
            >>> x.calculate
            -10.0
            >>> x.setExpr('7^2^3')
            >>> x.calculate
            5764801.0
            >>> x.setExpr(' 3 * ((( 10 - 2*3 )) )')
            >>> x.calculate
            12.0
            >>> x.setExpr('      8 / 4 * (3 - 2.45 * ( 4   - 2 ^ 3 )       ) + 3')
            >>> x.calculate
            28.6
            >>> x.setExpr('2 * ( 4 +        2 * (         5 - 3 ^ 2 ) + 1 ) + 4')
            >>> x.calculate
            -2.0
            >>> x.setExpr(' 2.5 +         3 * (2 + ( 3.0) * ( 5^2-2 * 3 ^ ( 2 )         ) * ( 4 ) ) * ( 2 / 8 + 2 * ( 3 - 1 /3 ) ) - 2 / 3^ 2')
            >>> x.calculate
            1442.7777777777778
            >>> x.setExpr("2 + 2 * ( 3+4 ) ^ 2 + 100 - (20 * 0.5)")
            >>> x.calculate
            190.0
            

            # In invalid expressions, you might print an error message, but code must return None, adjust doctest accordingly
            >>> x.setExpr(" 4 ++ 3+ 2") 
            >>> x.calculate
            >>> x.setExpr("4  3 +2")
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 *( 2 - 3 * 2 ) )')
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 * / ( 2 - 3 * 2 )')
            >>> x.calculate
            >>> x.setExpr(' ) 2 ( *10 - 3 * ( 2 - 3 * 2 ) ')
            >>> x.calculate
            >>> x.setExpr('(    3.5 ) ( 15 )') 
            >>> x.calculate
            >>> x.setExpr('3 ( 5) - 15 + 85 ( 12)') 
            >>> x.calculate
            >>> x.setExpr("( -2/6) + ( 5 ( ( 9.4 )))") 
            >>> x.calculate
        '''

        if not isinstance(self.__expr,str) or len(self.__expr)<=0:
            print("Argument error in calculate")
            return None

        calcStack = Stack()   # method must use calcStack to compute the  expression


        postfix = self._getPostfix(self.__expr)
        # `postfix` would only be `None` if the expression is invalid
        if postfix == None:
            return None

        for term in postfix.split():
            # When encountering an operand, push it into the stack
            if term not in "+-^*/":
                calcStack.push(float(term)) # All terms are str type
            # When encountering an operator, perform a calculation
            else:
                second = calcStack.pop()
                first = calcStack.pop()
                if term == "+":
                    res = first + second
                elif term == "-":
                    res = first - second
                elif term == "/":
                    res = first / second
                elif term == "*":
                    res = first * second
                elif term == "^":
                    res = first ** second
                # Push calculation back into stack
                calcStack.push(res)

        # Item left in stack is the result
        return calcStack.pop()
            

class AdvancedCalculator:
    '''
        >>> C = AdvancedCalculator()
        >>> C.states == {}
        True
        >>> C.setExpression('a = 5;b = 7 + a;a = 7;c = a + b;c = a * 0;return c')
        >>> C.calculateExpressions() == {'a = 5': {'a': 5.0}, 'b = 7 + a': {'a': 5.0, 'b': 12.0}, 'a = 7': {'a': 7.0, 'b': 12.0}, 'c = a + b': {'a': 7.0, 'b': 12.0, 'c': 19.0}, 'c = a * 0': {'a': 7.0, 'b': 12.0, 'c': 0.0}, '_return_': 0.0}
        True
        >>> C.states == {'a': 7.0, 'b': 12.0, 'c': 0.0}
        True
        >>> C.setExpression('x1 = 5;x2 = 7 * ( x1 - 1 );x1 = x2 - x1;return x2 + x1 ^ 3')
        >>> C.states == {}
        True
        >>> C.calculateExpressions() == {'x1 = 5': {'x1': 5.0}, 'x2 = 7 * ( x1 - 1 )': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        True
        >>> print(C.calculateExpressions())
        {'x1 = 5': {'x1': 5.0}, 'x2 = 7 * ( x1 - 1 )': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        >>> C.states == {'x1': 23.0, 'x2': 28.0}
        True
        >>> C.setExpression('x1 = 5 * 5 + 97;x2 = 7 * ( x1 / 2 );x1 = x2 * 7 / x1;return x1 * ( x2 - 5 )')
        >>> C.calculateExpressions() == {'x1 = 5 * 5 + 97': {'x1': 122.0}, 'x2 = 7 * ( x1 / 2 )': {'x1': 122.0, 'x2': 427.0}, 'x1 = x2 * 7 / x1': {'x1': 24.5, 'x2': 427.0}, '_return_': 10339.0}
        True
        >>> C.states == {'x1': 24.5, 'x2': 427.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;C = A + B;A = 20;D = A + B + C;return D - A')
        >>> C.calculateExpressions() == {'A = 1': {'A': 1.0}, 'B = A + 9': {'A': 1.0, 'B': 10.0}, 'C = A + B': {'A': 1.0, 'B': 10.0, 'C': 11.0}, 'A = 20': {'A': 20.0, 'B': 10.0, 'C': 11.0}, 'D = A + B + C': {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}, '_return_': 21.0}
        True
        >>> C.states == {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;2C = A + B;A = 20;D = A + B + C;return D + A')
        >>> C.calculateExpressions() is None
        True
        >>> C.states == {}
        True
    '''
    def __init__(self):
        self.expressions = ''
        self.states = {}

    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}

    def _isVariable(self, word):
        '''
            >>> C = AdvancedCalculator()
            >>> C._isVariable('volume')
            True
            >>> C._isVariable('4volume')
            False
            >>> C._isVariable('volume2')
            True
            >>> C._isVariable('vol%2')
            False
        '''

        if not isinstance(word, str):
            return False

        # Variables must start with a letter
        if not word[0].isalpha():
            return False

        # Variables can only contain alphanumeric characters
        for ch in word:
            if not ch.isalnum():
                return False
        
        return True


    def _replaceVariables(self, expr):
        '''
            >>> C = AdvancedCalculator()
            >>> C.states = {'x1': 23.0, 'x2': 28.0}
            >>> C._replaceVariables('1')
            '1'
            >>> C._replaceVariables('105 + x')
            >>> C._replaceVariables('7 * ( x1 - 1 )')
            '7 * ( 23.0 - 1 )'
            >>> C._replaceVariables('x2 - x1')
            '28.0 - 23.0'
        '''

        replaced = expr
        for var in self.states:
            # Only attempt replacement if `var` is a variable
            if self._isVariable(var):
                replaced = replaced.replace(var, str(self.states[var]))

        for term in replaced.split(" "):
            if self._isVariable(term):
                return None

        return replaced

    
    def calculateExpressions(self):
        self.states = {} 
        calcObj = Calculator()     # method must use calcObj to compute each expression

        steps = {}
        exprs = self.expressions.split(";")
        final_eq = exprs.pop()[7:]

        # Iterate over each expression that is setting a variable and add to state
        for expr in exprs:
            split_expr = expr.split("=")
            var = split_expr[0].strip()
            var_equals = split_expr[-1].strip()
            replaced = self._replaceVariables(var_equals)
            # Return None if variables are not defined
            if replaced is None:
                self.states = {}
                return None
            calcObj.setExpr(replaced)
            self.states[var] = calcObj.calculate

            # Create a new dict in memory to store the state of current step
            current_state = {}
            for key, value in self.states.items():
                current_state[key] = value
            steps[expr] = current_state

        # Replace variables in final expression and calculate
        final = self._replaceVariables(final_eq)
        calcObj.setExpr(final)
        calculation = calcObj.calculate
        # `calculation` returns None if there is an invalid expression
        if calculation is None:
            self.states = {}
            return None
        else:
            steps["_return_"] = calcObj.calculate
            return steps
            

if __name__ == "__main__":
    import doctest
    #doctest.run_docstring_examples(AdvancedCalculator, globals(), verbose=False)
    doctest.testmod(verbose=True)