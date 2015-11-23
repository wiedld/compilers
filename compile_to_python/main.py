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
#     - nums are left children of operators
# - semantic analysis:
#     - type checking/conversion
#     - bind math operator symbols to functions
#     - issue any warnings



###########################
# TODO:
# - handle spaces in input.
# "**": utils.power screws up regex

# NEXT:
# - read tree, and do computation/operations to return result
# - should be in parser file. put helper functs in utils file?
# - handle no parans. 23 + 234 - 234

###########################

import lexer
import parser


def calculator():
    while True:
        raw = raw_input("> ")

        if raw == "q":
            break

        tokens = lexer.lexical_analysis(raw, parser.CalculatorNode)
        print tokens

        parse_tree = parser.CalculatorNode.parse_into_tree(tokens)
        parse_tree.print_parse_tree()

        parse_tree.semantic_analysis()
        parse_tree.print_parse_tree()

        print "DID NOT BREAK PYTHON....but still need to see if worked correctly"


if __name__ == "__main__":
    calculator()
