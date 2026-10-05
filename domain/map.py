map_matrix = []

def map_make():
    with open("map", encoding="utf-8") as file_in:
        for line in file_in:
            map_matrix.append(list(line.rstrip("\n")))

map_make()