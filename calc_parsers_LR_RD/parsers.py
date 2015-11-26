import abstractParsers
import lexers
import string
import re


###################################################
###################################################

class CalcParserLR(abstractParsers.CalculatorParser):

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
        print "STACK IS:", self.stack

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
            self.tok_num(tok)
            return self._LR_parse(i+1)

        elif tok in self.operators.keys():
            self.stack.append(tok)
            return self._LR_parse(i+1)

        else:
            return SyntaxError("Token not recognized by parser.")


    def tok_close(self, i):
        # (int op int) --> but the int op int will already be reduced.
        # stack = [(,int]
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


    def tok_num(self, tok):
        # case #1: stack=[int op], tok=int
        # case #2: stack= [] | ["("]
        if self.stack == []:
            self.stack.append(tok)
            return

        elif self.stack[-1] == "(":
            self.stack.append(tok)
            return

        else:
            try:
                op = self.stack.pop()
                term = self.stack.pop()
                result = self.operators[op](self._num(term), self._num(tok))
                self.stack.append(result)
                return
            except:
                raise SyntaxError("Terminal breaks production rules.")


###################################################
###################################################


# class CalcParser_RD(CalculatorParser):

#     @classmethod
#     def parse(cls, tokens_list):
#         parser = cls()

#         return parser._RD_parse(tokens_list)


#     def _RD_parse(self, tokens, ops=self.operators.keys()):
#         """grammar rules:
#             (E) --> E
#             E --> E op E
#             E --> int
#         """

#         if tokens == []:
#             return

#         tok = tokens[0]

#         # "(" tok_open
#         if tok == "(":
#             return self._RD_parse(tokens[1:])

#         # E --> int
#         if len(tokens) == 1 and num(tokens[0]):
#             return tokens[0]

#         # int op  (E)|E|int
#         if num(tokens[0]) and tokens[1] in ops:
#             lam_func = self.operators[tokens[1]
#             return lam_func(num(tokens[0], self._RD_parse(tokens[2:])

#         #
#         if





