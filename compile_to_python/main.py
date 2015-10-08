# Objective #1:
# - build a calculator which takes in heavily nested input strings
#     e.g. (5+((12*123/234)-124))**(234/(23+234))
# - returns the math result
# - make sure is constructed in a generalized fashion!

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
# TODO:
# - handle spaces in input.
# "**": utils.power screws up regex
###########################

import lex
import parser


def calculator():
    while True:
        raw = raw_input("> ")

        if raw == "q":
            break

        tokens = lex.lexical_analysis(raw, parser.CalculatorNode)
        print tokens

        # root = CalculatorNode(tokens_list)
        # parse(root)


if __name__ == "__main__":
    calculator()
