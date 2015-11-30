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
            self.tok_close(i)
            return self._LR_parse(i)

        elif tok == "(":
            self.stack.append(tok)
            return self._LR_parse(i+1)

        elif self._num(tok):
            self.stack.append(self._num(tok))
            return self._LR_parse(i+1)

        elif tok in self.operators.keys():
            term2 = self.stack.pop()
            term1 = self.stack.pop()
            result = self.operators[tok](term1, term2)
            self.stack.append(result)
            return self._LR_parse(i+1)

        else:
            return SyntaxError("Token not recognized by parser.")


    def tok_close(self, i):
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
    No stack. Utilizes recursion and a single passed state variable."""


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
        # base case: finished all tokens
        if len(self.tokens) <= self.i:
            return left_term

        tok = self.tokens[self.i]

        # base case: closing paran:
        if tok == ")":
            self.i += 1
            return left_term

        # start recursive descent
        if tok == "(":
            self.i += 1
            return self._RD_parse(left_term)

        elif tok in self.operators.keys():
            try:
                self.i += 1
                numb = self._RD_parse(left_term)
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



