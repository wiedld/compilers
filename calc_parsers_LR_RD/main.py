# Objective #1:
# - build infix calculator which takes in heavily nested input strings
#     e.g. (5+((12*123/234)-124))**(234/(23+234))
# - returns the math result
# - make sure is constructed in a generalized fashion!

# Steps:
# - tokenize
# - parse:
#     - LR
#     - RD
# - semantic analysis:
#     - type checking/conversion
#     - bind math operator symbols to functions
#     - issue any warnings


###########################

from parsers import CalcParserLR, CalcParserRD


def calculator():
    while True:
        raw = raw_input("> ")

        if raw == "q":
            break

        # POSTFIX
        print CalcParserLR.parse(raw)

        # # PREFIX
        # print CalcParserLL.parse(raw)

        # INFIX
        # print CalcParserRD.parse(raw)


if __name__ == "__main__":
    calculator()
