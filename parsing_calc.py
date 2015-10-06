# COMPILERS

# 1. frontend:
#     - Lexical analysis (identify the tokens, and categorize each)
#     - Syntax analysis (parsing into the syntax tree)
#     - Semantic analysis (type checking, object binding, issuing warnings for invalid inputs)

# 2. middle:
#     - Code optimisation done in a language other than source or machine code
#     - intermediatary layer, often used for generic optimization (shared with other compilers)

# 3. backend:
#     - additional analysis
#     - transformations
#     - tends to be specific for that computer etc.
#     - generates the actual machine code to execute

# ###########################
# ###########################

# Objective:
# - build a calculator which takes in heavily nested input strings
#     e.g. (5+((12*123/234)-124))**(234/(23+234))
# - returns the math result


# Steps:
# - tokenize
# - parse:
#     - recursive tree construction
#     - parans() denotes root of subtree
#     - nums are left/right children of operators
# - semantic analysis:
#     - type checking/conversion
#     - bind math operator symbols to functions
#     - issue any warnings

###########################
# TODO: handle spaces in input.
###########################
from nodes import CalculatorNode


def tokenize(cls, string, output=None):
    """takes input string, returns list of tokens"""

    if output is None:      # on first function in stack
        output = []

    if len(string) == 0:    # base case
        return output

    token = ""
    types = {("(", ")"): 0,
             cls(0).operators: 0,
             ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"): 0}

    while True:
        # base case 1
        if len(string) == 0:
            break

        # base case 2 = detect token edge
        type_to_add = [type_k for type_k in types.keys() if string[0] in type_k][0]
        types[type_to_add] = 1
        # break condition. stop making token when switch types (sum will = 2)
        if sum(types.values()) > 1:
            break

        # update string and token
        token = token + string[0]
        string = string[1:]

    print "TOKEN:", token
    output.append(token)
    return tokenize(cls, string, output)


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



if __name__ == "__main__":
    raw = raw_input("> ")
    tokens_list = tokenize(CalculatorNode, raw)
    print tokens_list

    root = CalculatorNode(tokens_list)
    # parse(root)


