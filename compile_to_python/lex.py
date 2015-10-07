import nodes
import string

ascii_letters = string.ascii_letters

# def make_nested_arrays(string, output=None):
#     if output is None:      # on first function in stack
#         output = []
#     ## use regex to tokenize
#     return output


def tokenize(cls, string, output=None):
    """takes input string, returns list of tokens"""

    if output is None:      # on first function in stack
        output = []

    if len(string) == 0:    # base case
        return output

    token = ""
    types = {("(", ")"): 0,
             cls.get_operators(): 0,
             ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"): 0,
             tuple(ascii_letters): 0}

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


def lexical_analysis(raw, cls):
    print "RAW", raw
    tokenize_without_nesting = tokenize(cls, raw)
    return tokenize_without_nesting

    # nested_statements = make_nested_arrays(raw)
    # print nested_statements

    # tokens_list = [lexical.tokenize(CalculatorNode, statement) for statement in nested_statements]
    # print tokens_list
    # return tokens_list