import re 
from collections import Counter, defaultdict


with open("2018/day_4.txt") as f:
    lines = f.read().split("\n")
    
lines = sorted(lines, key=lambda x: x[15:17])
lines = sorted(lines, key=lambda x: x[12:14])
lines = sorted(lines, key=lambda x: x[9:11])
lines = sorted(lines, key=lambda x: x[6:8])
lines = sorted(lines, key=lambda x: x[1:3])

print('\n'.join(lines))

guards_sleep_minutes = defaultdict(Counter)

for line in lines:
    
    last_word = line.split(' ')[-1]
    
    if last_word == "shift":
        guard_num = int(re.search(r"#(\d+)", line).groups()[0])
    
    elif last_word == "asleep":
        asleep_min = int(line[15:17])
        
    
    elif last_word == "up":
        wake_up_min = int(line[15:17])
        
        print(f"Guard {guard_num} slept {asleep_min} -> {wake_up_min}")
        guards_sleep_minutes[guard_num].update(range(asleep_min,wake_up_min))
        
    else:
        raise UnboundLocalError
        
    
print(guards_sleep_minutes)

total_minutes_asleep_per_guard = [(k,sum(v.values())) for k,v in guards_sleep_minutes.items()]
most_asleep_guard = sorted(total_minutes_asleep_per_guard, key=lambda x: x[1], reverse=True)[0][0]

minute_most_asleep_guard_sleeps_most = guards_sleep_minutes[most_asleep_guard].most_common(1)[0][0]
    
print(f"Part 1: {minute_most_asleep_guard_sleeps_most * most_asleep_guard}")

# Part 2
# ------

most_frequent_minute_asleep = [(k,v.most_common(1)[0]) for k,v in guards_sleep_minutes.items()]
most_frequent_minute_asleep = sorted(most_frequent_minute_asleep, key=lambda x: x[1][1], reverse=True)[0]
print(f"Part 2: {most_frequent_minute_asleep[0] * most_frequent_minute_asleep[1][0]}")