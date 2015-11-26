from __future__ import print_function
import string
import re


ascii_letters = string.ascii_letters


###################################################
###################################################
# Abstract class for python "compiled" languages

class AbstractParseNode(object):
    operators = {}  # key=operator, value=function_name
    valid_types = []    # enter valid types

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
    def parse_into_tree(cls, tokens_list):
        """take a token list and root, and creates parsed tree"""
        return None


    def iterate_tree(self, funct):
        """generalized function to iterate through tree, performing function on each node."""

        if self.data == None:
            return

        funct(self)

        if self.left:
            self.left.iterate_tree(funct)
        if self.right:
            self.right.iterate_tree(funct)


    def print_parse_tree(self):
        """print data from each node. for debugging."""

        funct = lambda x: print (x.data)
        self.iterate_tree(funct)


    def semantic_analysis(self):
        """type checking/conversation, and binding of functions to operators"""

        # def type_convert_func(x):
        #     pass

        # self.iterate_tree(type_convert_func)

        def bind_op_function(x):
            if x.operators.get(x.data):
                x.data = x.operators.get(x.data)

        self.iterate_tree(bind_op_function)


###################################################
###################################################
# calculator language

class CalculatorNode(AbstractParseNode):
    operators = {"+": (lambda a,b: a+b),
                    "-": (lambda a,b: a-b),
                    "*": (lambda a,b: a*b),
                    "/": (lambda a,b: a/b),
                    "%": (lambda a,b: a%b),
                    "^": (lambda a,b: a**b),
                    "!": (lambda a: reduce(lambda x,y:x*y,[1]+range(1,n+1)))
                }
    valid_types = [int, float]


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
    def parse_into_tree(cls, tokens_list):
        root = cls()
        root.recursive_parse(tokens_list)

        return root


    def recursive_parse(self, tokens_list):
        """grammar rules:
                num_op
                op_num
                num_op_num -->  num ("result")
        """
        # base case = if no more tokens
        if tokens_list == []:
            return

        # for each token, make operator=parent and left/right children
        token = tokens_list[0]

        # if only num (subtree from num_op_num)
        if re.match('^(\(*([0-9]*)\)*)$', token):
            # print "line 94", token
            self.data = re.search('(\d+)', token).group(0)
            return

        # if num_op_num
        if re.match('^(\(*([0-9]+)([\+\-\/\*\%\^\!\e]{1})([0-9]+)\)*)', token):
            # print "line 100", token
            self.data = "result"
            self.left = CalculatorNode()
            num_op = re.search('^(\(*([0-9]+)([\+\-\/\*\%\^\!\e]{1}))', token).group(0)
            num = token[len(num_op):].replace(")", "")
            # make subtree to use num_op_num, with token_list = [num_op, num]
            self.left.recursive_parse([num_op, num])

        # if num_op = left(num) + parent(op)
        # if op_num, still also do = left(num) + parent(op)
        else:
            # print "line 111", token
            self.data = re.search('([\+\-\/\*\%\^\!\e]{1})', token).group(0)
            num = re.search('(\d+)', token).group(0)    # greedy, match all the nums
            self.left = CalculatorNode(num)

        # continuing building parse tree to the right
        self.right = CalculatorNode()
        return self.right.recursive_parse(tokens_list[1:])

