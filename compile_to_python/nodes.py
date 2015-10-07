import math_functions


class ParsedTreeNode(object):
    operators = None

    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


class CalculatorNode(ParsedTreeNode):
    operators = ("+", "-", "/", "*", "%", "^", "!", "e")

    def bind(self):
        if self.data in self.operators:
            self.data = None
