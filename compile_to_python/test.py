import re

expr = "b = 2 + a*10"

pos = 0

pattern = re.compile("\s*(?:(\d+)|(\w+)|(.))")

while 1:
    m = pattern.match(expr, pos)
    if not m:
        break
    print m.lastindex
    print repr(m.group(m.lastindex))
    print "\n"
    pos = m.end()

