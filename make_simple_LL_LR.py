
########################################

ops = {
    "+": (lambda a,b: a+b),
    "-": (lambda a,b: a-b),
    "*": (lambda a,b: a*b),
    "/": (lambda a,b: a/b)
}


def num(s):
    try:
        return int(s)
    except:
        return None

########################################

# S|E --> E E op
# E --> int

# therefore, determine each E and reduce to a term int, before moving forward


def LR0_eval(tokens):
    """LR(0), postfix.
        - Left-to-right through tokens.
        - Parsing is right derivation, (a post-order traversal of a tree with op as parent nodes).
        - Rule assessment starts on the right side (doesn't require lookahead).
        Done with shift reduce."""

    stack = []

    for t in tokens:
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

#    S|E  ->  op E E
#    E -> int


def LL1_eval(tokens):
    """LL(1), prefix.
        - Left-to-right through tokens.
        - Parsing is left derivation, (a pre-order traversal of a tree with op as parent nodes).
        - Rule assessment starts on the left side (therefore, must have lookahead).
        Done with prediction. If statements expecting certain tokens."""

    stack = []
    i = 0

    while True:
        # only 1 item in input stream. should==int
        if stack == [] and len(tokens[i:]) == 1:
            try:
                stack.append(num(tokens[i]))
                break
            except:
                raise TypeError

        curr = tokens[i:i+1]    # avoid indexing error

        # finished input stream
        if curr == []:
            break

        if curr[0] in ops:
            stack.append(curr[0])
            i += 1
            continue

        if num(curr[0]):
            # if curr==int, stack[-2:0] == [op,int]
            if num(stack[-1]):
                try:
                    top = stack.pop()
                    op = stack.pop()
                    result = ops[op](num(top), num(curr[0]))
                    # stack.append(result)
                    tokens[i] = result
                    # i += 1
                    continue
                except:
                    raise TypeError

            # lookahead
            ahead = tokens[i+1:i+2]
            # if curr==int and ahead==int, then top stack must == op
            if num(ahead[0]):
                try:
                    top = stack.pop()
                    result = ops[top](num(curr[0]), num(ahead[0]))
                    # stack.append(result)
                    i += 1
                    tokens[i] = result
                    continue
                except:
                    raise TypeError

            # ahead != int, move forward
            stack.append(curr[0])
            i += 1
            continue

        return TypeError  # curr != (num | op)

    return stack.pop()


test1 = '- + 7 * 2 3 26'        # -13
test2 = '- + * 1 7 * 2 3 26'    # -13
test3 = '- + * 2 3 7 26'         # -13

print LL1_eval(test1.split())
print LL1_eval(test2.split())
print LL1_eval(test3.split())

########################################

