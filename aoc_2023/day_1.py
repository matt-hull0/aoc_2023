with open("day_1.txt") as f:
    doc = [line.strip() for line in f.readlines()]

calibration_values = []
    
for line in doc:
    nums_in_line = [int(char) for char in line if char.isnumeric()]
    
    calibration_values.append(int(str(nums_in_line[0]) + str(nums_in_line[-1])))
    
print(f"Part 1: {sum(calibration_values)}")

# Part 2

with open("day_1.txt") as f:
    doc = [line.strip() for line in f.readlines()]
    
d = { 0 : 'zero', 1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four', 5 : 'five',
          6 : 'six', 7 : 'seven', 8 : 'eight', 9 : 'nine'
}

calibration_values = []
    
for line in doc:
    
    updated_line = []
    i = 0
    matched = False

    while i < len(line):
        for num, spelled_num in d.items():
            # if i+len(spelled_num) <= len(line):
            if line[i:i+len(spelled_num)] == spelled_num:
                updated_line.append(str(num))
                i+= len(spelled_num)-1
                matched = True
                
        if matched:
            matched = False
        else:
            updated_line.append(line[i])
            i+=1

    # print(''.join(updated_line))
    nums_in_line = [int(char) for char in updated_line if char.isnumeric()]
    
    calibration_values.append(int(str(nums_in_line[0]) + str(nums_in_line[-1])))
# print(calibration_values)
print(f"Part 2: {sum(calibration_values)}")

# 54251 too high - had to change eighthree to 83 not 8hree
# 54249
