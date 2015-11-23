

ops = {
    "+": (lambda a,b: a+b),
    "-": (lambda a,b: a-b),
    "*": (lambda a,b: a*b)
}


def num(s):
    try:
        return int(s)
    except:
        return None


########################################

def LR0_eval(tokens):
    """LR(0), postfix.
        - Left-to-right through tokens.
        - Parsing is right derivation, (a post-order traversal of a tree with op as parent nodes).
        - Rule assessment starts on the right side (doesn't require lookahead).
        Done with shift reduce."""

    stack = []

    for t in tokens:
        print "current stack:", stack
        if t in ops:
            arg2 = stack.pop()
            arg1 = stack.pop()

            # shift-reduce
            result = ops[t](arg1, arg2)
            stack.append(result)

        else:
            stack.append(int(t))

    return stack.pop()


test = '7 2 3 + -'
print LR0_eval(test.split())
print

########################################

def LL1_eval(tokens):
    """LL(2), prefix.
        - Left-to-right through tokens.
        - Parsing is left derivation, (a pre-order traversal of a tree with op as parent nodes).
        - Rule assessment starts on the left side (therefore, must have lookahead).
        Done with prediction."""

    # # RULES
    #     S -> op int int | op int E | op E E
    #     E -> op E E | op int E | op E int

    stack = []
    i = 0

    while True:
        print "current stack:", stack

        # exit
        if i == len(tokens):
            if len(stack) > 1:
                tokens = stack
                stack, i = [], 0
                continue
            elif len(stack) == 1 and num(stack[-1])!=None:
                return stack.pop()
            else:
                return "Invalid input"


        curr = tokens[i]
        # lookahead, predictive
        ahead = tokens[i+1:i+2]

        # E -> op E E
        if curr in ops:
            stack.append(curr)
            i += 1
            continue

        # E -> (op on stack) (int on stack) int
        elif ahead == []:
            stack.append(curr)
            i += 1
            continue

        # E -> (op on stack) int int
        elif num(curr)!=None and num(ahead[0])!=None:
            top = stack.pop()
            result = ops[top](num(curr), num(ahead[0]))
            stack.append(result)
            i += 2
            continue

        # E -> (op on stack) int E
        elif num(curr)!=None and ahead[0] in ops:
            stack.append(curr)
            i += 1
            continue

        # invalid
        else:
            return "Input is not valid"



test1 = '+ 7 * 2 3 '        # 13
test2 = '+ * 1 7 * 2 3 '    # 13
test3 = '+ * 2 3 7'         # 13
#   * + 1 2 3 == ( * ( + 2 ) 3 )
print LL1_eval(test1.split())
print
print LL1_eval(test2.split())
print
print LL1_eval(test3.split())

########################################

# def LL_eval(tokens):
#     """LL(k), prefix. Left-to-right, left derivation."""
#     stack = []

#     return

# test2 = '+ 7 2 - 3'
# #   * + 1 2 3 == ( * ( + 2 ) 3 )
# print LL_eval(test2.split())