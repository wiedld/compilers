import utils
import string
import re


ascii_letters = string.ascii_letters


###################################################
# Abstract class for python "compiled" languages

class AbstractParseNode(object):
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

class CalculatorNode(AbstractParseNode):
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
        # 3+5 and (3+5)
        num_op_num = [('^(\(*([0-9]+)(\%s)([0-9]+)\)*)' % op) for op in cls.operators.keys()]
        # 3+  and (3+(  and  (3+   and  3+(
            # since the num_op_num is added first, will be checked as matches first
        num_op = [('^(\(*([0-9]+)(\%s)\(*)' % op) for op in cls.operators.keys()]
        # +5  and )+5)  and )+5    and +5)
        op_num = [('^(\)*(\%s)([0-9]+)\)*)' % op) for op in cls.operators.keys()]
        regex_expns = num_op_num + num_op + op_num

        return tuple(regex_expns)


    @classmethod
    def parse_tree(cls, tokens_list):
        root = cls()
        root.recursive_parse(tokens_list)

        # test is working
        root.print_parse_tree()


    def recursive_parse(self, tokens_list):
        # base case = if no more tokens
        if tokens_list == []:
            return

        # for each token, make operator=parent and left/right children
        token = tokens_list[0]

        # if only num (subtree from num_op_num)
        if re.match('^(\(*([0-9]*)\)*)$', token):
            self.data = re.search('([0-9]*)', token).group(0)
            return

        # if num_op_num
        if re.match('^(\(*([0-9]+)([\+\-\/\*\%\^\!\e]{1})([0-9]+)\)*)', token):
            self.data = "result"
            self.left = CalculatorNode()
            num_op = re.search('^(\(*([0-9]+)([\+\-\/\*\%\^\!\e]{1}))', token).group(0)
            num = token[len(num_op):].replace(")", "")
            # make subtree to use num_op_num, with token_list = [num_op, num]
            self.left.recursive_parse([num_op, num])

        # if num_op = left(num) + parent(op)
        # if op_num, still also do = left(num) + parent(op)
        else:
            self.data = re.search('([\+\-\/\*\%\^\!\e]{1})', token).group(0)
            num = re.search('([0-9]*)', token).group(0)    # greedy, match all the nums
            self.left = CalculatorNode(num)

        # continuing building parse tree to the right
        self.right = CalculatorNode()
        return self.right.recursive_parse(tokens_list[1:])


    def print_parse_tree(self):
        if self.data == None:
            return

        print "node.data = ", self.data

        if self.left:
            self.left.print_parse_tree()
        if self.right:
            self.right.print_parse_tree()



    # def bind(self):
    #         if self.data in self.operators:
    #             self.data = None

