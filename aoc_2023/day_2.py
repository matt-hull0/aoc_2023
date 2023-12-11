from collections import defaultdict

def parse_input(fp:str) -> dict[str,dict[str,list[int]]]:
    
    games = {}
    
    with open(fp) as f:
        lines = [line.strip().split(": ") for line in f.readlines()]
        
    for line in lines:
        
        id = int(line[0].split(" ")[-1])
        
        colour_usage = defaultdict(list)
        
        subsets = line[1].split("; ")
        for subset in subsets:
            for turn in subset.split(", "):
                num, colour = turn.split(" ")
                colour_usage[colour].append(int(num))
    
        games[id] = colour_usage
    
    return games
    

def get_max_draw_per_colour(games: dict[int,dict[str,list[int]]]) -> dict[int,dict[str,int]]: 
    max_per_game_per_colour = {}
    
    for game_id, colour_count_dict in games.items():
        max_per_colour = defaultdict(lambda: 0)
        for colour, num_cubes in colour_count_dict.items():
            max_per_colour[colour] = max(max_per_colour[colour], max(num_cubes))
        max_per_game_per_colour[game_id] = max_per_colour
            
    return max_per_game_per_colour 
        
        
def is_game_possible(max_draws:dict[str,int], available:dict[str,int]):
    for colour, num_drawn in max_draws.items():
        if available[colour] < num_drawn:
            return False
    return True
    

def determine_possible_games(max_draw_per_colour: dict[int,dict[str,int]], available:dict[str,int]) -> list[int]:
    possible_ids = []
    for game_id, max_colour_draws in max_draw_per_colour.items():
        if is_game_possible(max_colour_draws, available):
            possible_ids.append(game_id)
    return possible_ids
    
           
            
games = parse_input("day_2.txt")

max_draw_per_colour = get_max_draw_per_colour(games)

available = {
    "red": 12,
    "green": 13,
    "blue": 14
}

possible_game_ids = determine_possible_games(max_draw_per_colour,available)

print(f"Part 1: {sum(possible_game_ids)}")


# Part 2

def calculate_powers(max_draw_per_colour: dict[int,dict[str,int]]) -> list[int]:
    powers = []
    
    for _, colour_usage in max_draw_per_colour.items():
        power = 1
        for _, draws in colour_usage.items():
            power *= draws
        powers.append(power)
    return powers
            

powers = calculate_powers(max_draw_per_colour)

print(f"Part 2: {sum(powers)}")
    
    
    
    
         