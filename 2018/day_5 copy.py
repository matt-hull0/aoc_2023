import sys

line = [line for line in sys.stdin][0].strip()


def are_opp(a, b):
    return (a.lower() == b.lower() and
            ((a.isupper() and b.islower()) or
             (a.islower() and b.isupper())))


def react(line):
    buf = []
    for c in line:
        if buf and are_opp(c, buf[-1]):
            buf.pop()
        else:
            buf.append(c)
    return len(buf)


agents = set([c.lower() for c in line])

# part 1
print(react(line))

# part 2
print(min([react(line.replace(a, '').replace(a.upper(), ''))
           for a in agents]))

