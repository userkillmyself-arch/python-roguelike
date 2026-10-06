import os

def load_map(level=1):
    path = f"map{level}.txt"
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return [list(line.rstrip("\n")) for line in f]