import re


class Lexer(object):


    def tokenize(self, cls, string, skip_whitespace=True):
        valid_patterns = cls._token_patterns()

        r_list = [re.compile(pattern) for pattern in valid_patterns]

        tokens = []
        pos = 0

        while string != "":
            string = self._skip_whitespace(string, skip_whitespace)

            found = False

            # identify the token
            for r in r_list:
                if r.search(string):
                    matched_token = r.search(string).group(0)
                    tokens.append(matched_token)
                    string = string[len(matched_token):]
                    found = True
                    break       # break out of for loop

            if found == False:
                return "TokenError: invalid language syntax."

        return tokens


    def _skip_whitespace(self, string, skip_status):
        """removes whitespace, based on option."""
        skip = ''

        if skip_status == True:
            m = re.match('^\s+', string)
            if m != None:
                skip = m.group(0)

        return string[len(skip):]
