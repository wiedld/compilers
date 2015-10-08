import utils
import string

ascii_letters = string.ascii_letters


##############################
# classes for each parse tree

class ParsedTreeNode(object):
    operators = {}  # key=operator, value=function_name
    valid_ascii = []    # enter valid ascii alphanumeric

    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    @classmethod
    def get_ascii(cls):
        """return tuple (hashable type) containing valid ascii"""
        return tuple(cls.valid_ascii)

    @classmethod
    def get_operators(cls):
        """return tuple (hashable type) containing operators"""
        return None

    @classmethod
    def token_patterns(cls):
        """return tuple containing valid regex expressions."""
        return None

    def bind(self):
        """bind the opcode (python = opcode here) to the operator"""
        return None


class CalculatorNode(ParsedTreeNode):
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

    valid_ascii = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")

    @classmethod
    def get_operators(cls):
        return tuple(cls.operators.keys())

    @classmethod
    def token_patterns(cls):
        """return tuple containing valid regex expressions."""
        regex_expns = [('^(\(*([0-9]*)(\%s)([0-9]*)\)*)' % op) for op in cls.operators.keys()]

        return tuple(regex_expns)

    def bind(self):
        if self.data in self.operators:
            self.data = None


##############################
# parsing function

def parse(node):

    if len(node.data) <= 1:
        return

    # # find the next "(", and the last ")"
    # paran_start = tokens_list.index("(")
    # paran_end = (len(tokens_list) - 1) - tokens_list[::-1].index(")")

    node.left = CalculatorNode(node.data[:paran_start])
    node.right = CalculatorNode(node.data[paran_start:])

    # recursive call
    parse(node.left)
    parse(node.right)




