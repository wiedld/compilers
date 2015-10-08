import nodes
import re


def tokenize(cls, string):
    valid_patterns = cls.token_patterns()

    r_list = [re.compile(pattern) for pattern in valid_patterns]

    tokens = []
    pos = 0
    while string != "" and pos < 5:
        found = False
        for r in r_list:
            if r.search(string):
                matched_token = r.search(string).group(0)
                tokens.append(matched_token)
                string = string[len(matched_token):]
                found = True
                break       # break out of for loop
        if found == False:
            return "TokenError: invalid language syntax."
        pos = pos + 1

    return tokens


def lexical_analysis(raw, cls):
    tokens = tokenize(cls, raw)
    return tokens
