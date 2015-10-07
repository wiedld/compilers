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




