def map_read(map_file_name):
    import os
    script_dir = os.path.dirname(__file__)

    map_file = open(f"{script_dir}/maps/{map_file_name}", 'r')
    lines = map_file.readlines()
    line_count = 0
    global a_line
    a_line = []
    global whole_line
    whole_line = []
    global count_line
    count_line = []

    global map_coordinate
    map_coordinate = []

    for line in lines:
        line = line.strip()
        line_count += 1
        count_line.append(len(line))
        for char in range(len(line)):
            a_line.append(line[char:char + 1])
        whole_line.append(a_line)
        a_line = []
    for line in range(line_count):
            for char in range(count_line[line]):
                map_line = whole_line[line]
                map_char = map_line[char]
                if map_char == '_':
                    pass
                elif map_char == 'b':
                    map_coordinate.append(("block",-500 + char * 50, line * 50))
                elif map_char == 'e':
                    map_coordinate.append(("enemy",-500 + char * 50, line * 50))
                elif map_char == 's':
                    map_coordinate.append(("savepoint",-500 + char * 50, line * 50))
                elif map_char == 'P':
                    map_coordinate.append(("player",-500 + char * 50, line * 50))
                elif map_char == "g":
                    map_coordinate.append(("goal",-500 + char * 50, line * 50))

    map_file.close()
    return map_coordinate