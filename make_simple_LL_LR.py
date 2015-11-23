

ops = {
    "+": (lambda a,b: a+b),
    "-": (lambda a,b: a-b)
}

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

def LL2_eval(tokens):
    """LL(2), prefix.
        - Left-to-right through tokens.
        - Parsing is left derivation, (a pre-order traversal of a tree with op as parent nodes).
        - Rule assessment starts on the left side (therefore, must have lookahead).
        Done with prediction."""

    stack = []

    i = 0
    while i < len(tokens):
        print "current stack:", stack

        curr = tokens[i]

        if curr in ops:
            # lookahead, predictive
            ahead1, ahead2 = tokens[i+1:i+2], tokens[i+2:i+3]

            try:
                ahead1, ahead2 = int(ahead1[0]), int(ahead2[0])
                result = ops[curr](ahead1, ahead2)
                stack.append(result)
                i += 3

            except:
                ahead1 = int(ahead1[0])
                prev = stack.pop()
                result = ops[curr](prev, ahead1)
                stack.append(result)
                i += 2

    return stack.pop()


test2 = '+ 7 2 - 3'
#   * + 1 2 3 == ( * ( + 2 ) 3 )
print LL2_eval(test2.split())

########################################

# def LL_eval(tokens):
#     """LL(k), prefix. Left-to-right, left derivation."""
#     stack = []

#     return

# test2 = '+ 7 2 - 3'
# #   * + 1 2 3 == ( * ( + 2 ) 3 )
# print LL_eval(test2.split())