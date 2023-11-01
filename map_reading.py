import os
script_dir = os.path.dirname(__file__)

map_file = open(f"{script_dir}/jump_game_map.txt", 'r')
lines = map_file.readlines()
line_count = 0
global a_line
a_line = []
global whole_line
whole_line = []
global count_line
count_line = []
for line in lines:
    line = line.strip()
    line_count += 1
    count_line.append(len(line))
    for char in range(len(line)):
        a_line.append(line[char:char + 1])
    whole_line.append(a_line)
    a_line = []

map_file.close()