import utils


##############################
# classes for each parse tree

class ParsedTreeNode(object):
    operators = {}  # key=operator, value=function_name


    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    @classmethod
    def get_operators(cls):
        """return tuple (hashable type) containing operators"""
        return None


class CalculatorNode(ParsedTreeNode):
    operators = {"+": utils.add,
                 "-": utils.subtract,
                 "/": utils.division,
                 "*": utils.multiply,
                 "%": utils.mod,
                 "^": utils.power,
                 "!": utils.factorial,
                 "e": utils.natural_exp}

    @classmethod
    def get_operators(cls):
        return tuple(cls.operators.keys())

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




