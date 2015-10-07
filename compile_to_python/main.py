import lex
import parser
import nodes


def calculator():
    raw = raw_input("> ")
    print lex.lexical_analysis(raw, nodes.CalculatorNode)

    # root = CalculatorNode(tokens_list)
    # parse(root)


if __name__ == "__main__":
    calculator()
