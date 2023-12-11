text='dabAcCaCBAcCcaDA'

with open("2018/day_5.txt") as f:
    text = f.read().strip()

def react(text):
    for i in range(0,len(text)-1):
        char_1 = text[i]
        char_2 = text[i+1]
        
        if (char_1 != char_2) and (char_1.lower() == char_2.lower()):
            return text[:i] + text[i+2:]
    return text

def len_after_reactions(text):
        
    reacted = react(text)

    while text != reacted:
        text = reacted
        reacted = react(text)
    
    return(len(reacted))

print(f"Part 1: {len_after_reactions(text)}")

# Part 2:
# -------
min_len = len(text)

for char in set(text.lower()):
    unit_removed = text.replace(char, '')
    unit_removed = unit_removed.replace(char.upper(), '')
    min_len = min(min_len, len_after_reactions(unit_removed))
    
print(f"Part 2: {min_len}")