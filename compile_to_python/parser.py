import utils
import string
import re


ascii_letters = string.ascii_letters


###################################################
# Abstract class for python "compiled" languages

class AbstractParsedNode(object):
    operators = {}  # key=operator, value=function_name
    valid_ascii = []    # enter valid ascii alphanumeric

    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    @classmethod
    def get_operators(cls):
        """return tuple (hashable type) containing operators"""
        return None

    @classmethod
    def token_patterns(cls):
        """return tuple containing valid regex expressions."""
        return None

    @classmethod
    def parse_tree(cls, tokens_list):
        """take list of tokens, and return root of parsed tree."""
        return None

    def bind(self):
        """bind the opcode function (python = opcode here) to the operator"""
        return None


###################################################
# calculator language

class CalculatorNode(AbstractParsedNode):
    operators = {"+": utils.add,
                 "-": utils.subtract,
                 "/": utils.division,
                 "*": utils.multiply,
                 "%": utils.mod,
                 "^": utils.power,
                 "!": utils.factorial,
                 "e": utils.natural_exp,
                 # "**": utils.power
                 }

    @classmethod
    def get_operators(cls):
        return tuple(cls.operators.keys())

    @classmethod
    def token_patterns(cls):
        regex_expns = [('^(([0-9]*)(\%s)([0-9]*))' % op) for op in cls.operators.keys()]
        return tuple(regex_expns)


    @classmethod
    def parse_tree(cls, tokens_list):
        root = cls()
        root.recursive_parse(tokens_list)

    # def recursive_parse(self, tokens_list):
    #     # base case = if no more tokens
    #     if tokens_list == []:
    #         return

    #     # for each token, make operator=parent and left/right children
    #     statement = self.data[0]
    #     # if a left child + parent operator
    #     if re.match('^\(*[0-9]+[\+\-\/\*\%\^\!\e]{1}$', statement):
    #         left_data = re.match('^[0-9]*', statement).group(0)
    #         self.left = CalculatorNode(left_data)
    #         self.data = re.match('[\+\-\/\*\%\^\!\e]{1}', statement).group(0)
    #     # if a parent + right child, or left + parent + right
    #     data = re.match('[\+\-\/\*\%\^\!\e]{1}', statement).group(0)
    #     self.data = CalculatorNode(data)
    #     # if a right child -- then it's off the next root


    #     # recursive call to the right (lopsided tree?)

    #     if re.match('[\+\-\/\*\%\^\!\e]{1}[0-9]*', statement):







    def bind(self):
            if self.data in self.operators:
                self.data = None




