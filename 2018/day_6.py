from typing import List, Tuple

with open("2018/day_6.txt") as f:
    coords = [(int(x),int(y)) for x,y in [line.strip().split(',') for line in f.readlines()]]
    
print(coords)

def nearest_coord(x:int,y:int,coords:List[Tuple[int,int]]):
    dist = {}
    for i, coord in enumerate(coords, start=1):
        dist[i] = abs(x-coord[0]) + abs(y-coord[1])
        
    min_dist = min((v for v in dist.values()))
    
    min_dist_coord_nums = [k for k,v in dist.items() if v==min_dist]
    
    if len(min_dist_coord_nums)==1:
        return min_dist_coord_nums[0]
    else:
        return '.'
    
    
def coord_area(coord_num, grid):
    return sum([1 for row in grid for value in row if value==coord_num])
    
x_max, y_max = max([x for x,_ in coords]), max([y for _,y in coords])
grid = [['#' for _ in range(x_max+1)] for _ in range(y_max+1)]

for x in range(0,x_max+1):
    for y in range(0,y_max+1):
        grid[y][x] = nearest_coord(x,y,coords)
       
top_row = set(grid[0])
bottom_row = set(grid[y_max])
left_col = set([grid[y][0] for y in range(0,y_max+1)])
right_col = set([grid[y][x_max] for y in range(0,y_max+1)])
coord_inf_area =  top_row |  bottom_row | left_col | right_col

non_inf_coord_nums = set(range(1,len(coords)+1))- coord_inf_area

area = 0

for coord_num in non_inf_coord_nums:
    area = max(area, coord_area(coord_num, grid))
    
print(f"Part 1: {area}")


# Part 2

def close_enough_or_not(x,y,coords):
    limit = 10000
    
    total_dist = 0
    
    for coord in coords:
        total_dist += abs(x-coord[0]) + abs(y-coord[1])
    
    if total_dist < limit:
        return 1
    else:
        return 0
        
    
for x in range(0,x_max+1):
    for y in range(0,y_max+1):
        grid[y][x] = close_enough_or_not(x,y,coords)
        
        
print(f"Part 2: {sum(value for row in grid for value in row)}")