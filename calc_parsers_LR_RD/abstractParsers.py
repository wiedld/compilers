import string
import re


###################################################
###################################################
# Abstract class for Parsers.

class AbstractParser(object):
    operators = {}  # key=operator, value=function_name
    valid_types = []    # enter valid types

    @classmethod
    def _get_operators(cls):
        """Take class, return tuple (hashable type) containing operators"""
        return None

    @classmethod
    def _token_patterns(cls):
        """Take class, return tuple containing valid tok expressions."""
        return None

    def parse(self, tokens_list):
        """take a token list. return output."""
        return None

###################################################
###################################################
# Abstract class for Calculators.


class CalculatorParser(AbstractParser):
    operators = {"+": (lambda a,b: a+b),
                    "-": (lambda a,b: a-b),
                    "*": (lambda a,b: a*b),
                    "/": (lambda a,b: a/b),
                    "%": (lambda a,b: a%b),
                    "^": (lambda a,b: a**b)
                }
    valid_types = [int, float]


    @classmethod
    def _get_operators(cls):
        return tuple(cls.operators.keys())


    @classmethod
    def _token_patterns(cls):
        tok_open = ['^\(']
        tok_close = ['^\)']
        tok_num = ['^(\d+)']
        tok_op = [('^(\%s)' % op) for op in cls._get_operators()]
        regex_expns = tok_open + tok_close + tok_num + tok_op

        return tuple(regex_expns)


    def _num(self, tok):
        try:
            return int(tok)
        except:
            return None

