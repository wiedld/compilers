import abstractParsers
import lexers
import string
import re


###################################################
###################################################

class CalcParserLR(abstractParsers.CalculatorParser):
    """Handles postfix notation.
    Rule applied once the righthand op is read
        (right derivation, right hand recursive call).
    Precedence determined by parans.
    Utilizes a stack."""


    def __init__(self):
        self.stack = []


    @classmethod
    def parse(cls, input_string):
        lexer = lexers.Lexer()
        tokens = lexer.tokenize(cls, input_string)
        print "TOKENS:", tokens

        parser = cls()
        parser.tokens = tokens
        return parser._LR_parse()


    def _LR_parse(self, i=0):

        if len(self.tokens) <= i:
            return self.stack.pop()

        tok = self.tokens[i]

        if tok == ")":
            # reduce
            self._tok_close(i)
            # right recurse
            return self._LR_parse(i)

        elif tok == "(":
            # shift
            self.stack.append(tok)
            # right recurse
            return self._LR_parse(i+1)

        elif self._num(tok):
            # shift
            self.stack.append(self._num(tok))
            # righ recurse
            return self._LR_parse(i+1)

        elif tok in self.operators.keys():
            # reduce
            term2 = self.stack.pop()
            term1 = self.stack.pop()
            result = self.operators[tok](term1, term2)
            self.stack.append(result)
            # right recurse
            return self._LR_parse(i+1)

        else:
            return SyntaxError("Token not recognized by parser.")


    def _tok_close(self, i):
        # (int op int) --> but the int op int will already be reduced.
        # stack = ["(",int]
            # --> remove the open_tok, and place int at front of tokens
            # so any expr prior to open_tok will now be eval
        try:
            reduced_term = self.stack.pop()
            matching_open = self.stack.pop()

            if not self._num(reduced_term):
                return TypeError("Token before tok_close must be integer.")
            if matching_open != "(":
                return SyntaxError("Unmatched parans.")

            self.tokens[i] = reduced_term
            return
        except:
            raise SyntaxError("Incorrect syntax preceeding tok_close.")


###################################################
###################################################


class CalcParserRD(abstractParsers.CalculatorParser):
    """Handles infix notation.
    Rule checking, results in recursive call on the left side as well as right.
    Precedence determined by parans.
    Requires 1 lookahead = LL(1).
    No stack. Utilizes recursion and a passed state variable (tracking left term, as right recurse)."""


    def __init__(self):
        self.i = 0


    @classmethod
    def parse(cls, input_string):
        lexer = lexers.Lexer()
        tokens = lexer.tokenize(cls, input_string)
        print "TOKENS:", tokens

        parser = cls()
        parser.tokens = tokens
        return parser._RD_parse()


    def _RD_parse(self, left_term=None):

        if len(self.tokens) <= self.i:
            return left_term

        tok = self.tokens[self.i]

        # base case: closing paran:
        if tok == ")":
            self.i += 1
            return left_term

        elif tok == "(":
            self.i += 1
            # recurse to right
            return self._RD_parse(left_term)

        elif tok in self.operators.keys():
            try:
                self.i += 1
                # recurse to right
                numb = self._RD_parse(left_term)
                # apply rule to left
                left_term = self.operators[tok](left_term, numb)
                return left_term
            except:
                return SyntaxError

        elif self._num(tok):
            ahead = self.tokens[self.i+1:self.i+2]
            if ahead != [] and ahead[0] in self.operators.keys():
                # recursive call with left_term as current tok
                self.i += 1
                left_term = self._RD_parse(self._num(tok))
                return left_term
            else:
                return self._num(tok)


###################################################
###################################################

# test1 = '- + 7 * 2 3 26'        # -13
# test2 = '- + * 1 7 * 2 3 26'    # -13
# test3 = '- + * 2 3 7 26'         # -13


class CalcParserLL(abstractParsers.CalculatorParser):
    """Handles prefix notation.
    Rule applied once the lefthand op is read
        (left derivation, left hand recursive call).
    Precedence determined by parans. count parans up/down.
    Utilizes lookahead k=2."""


    def __init__(self):
        self.count_parans = 0


    @classmethod
    def parse(cls, input_string):
        lexer = lexers.Lexer()
        tokens = lexer.tokenize(cls, input_string)
        print "TOKENS:", tokens

        parser = cls()
        parser.tokens = tokens
        return parser._LL_parse()[0]


    def _LL_parse(self, i=0):
        print

        tok = self.tokens[i]

        if len(self.tokens) <= i:
            return tok, i

        print "TOK:", tok

        # if tok == ")":
        #     self._tok_close()
        #     self.i += 1
        #     return left_term

        # elif tok == "(":
        #     self.count_parans += 1
        #     self.i += 1
        #     return self._LL_parse()

        if tok in self.operators.keys():
            print "line 208"
            # k=2
            try:
                ahead1 = self.tokens[i+1]
                ahead2 = self.tokens[i+2]
                print "ahead1", ahead1, "ahead2", ahead2

                # op num num
                if self._num(ahead1) and self._num(ahead2):
                    print "line 216"
                    print "tok", tok, "ahead1", ahead1, "ahead2", ahead2
                    result = self.operators[tok](self._num(ahead1), self._num(ahead2))
                    print "result", result
                    print "new i", i + 2
                    return result, i+2
                # op E ?
                elif ahead1 in self.operators.keys():
                    print "line 220"
                    # expand left derivation
                    ahead1, i = self._LL_parse(i+1)
                    print "ahead1 redefined", ahead1
                    ahead2 = self.tokens[i+1]
                    print "ahead2 rededined", ahead2
                    # op E int
                    if self._num(ahead2):
                        print "line 226"
                        print "new i", i + 1
                        return self.operators[tok](ahead1, self._num(ahead2)), i+1
                    # op E E
                    elif ahead2 in self.operators.keys():
                        print "line 230"
                        ahead2, i = self._LL_parse(i+1)
                        return self.operators[tok](ahead1, ahead2), i

                # op int E
                elif ahead2 in self.operators.keys():
                    print "line 244"
                    ahead2, i = self._LL_parse(i+2)
                    return self.operators[tok](self._num(ahead1), ahead2), i

            except:
                return SyntaxError("Unmatched operator.")

        return SyntaxError("Expected operator.")


    def _tok_close(self):
        # confirm tok_close is matched
        if self.count_parans%2 != 0:
            self.count -= 1
        else:
            return SyntaxError("Unmatched tok_close.")


