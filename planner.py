import sys
import copy
from copy import deepcopy


def create_world_from_file(file: str) -> (int, int, list[list]):
    with open(file, "r") as file:
        cols = int(file.readline().strip())
        rows = int(file.readline().strip())
        world = [list(row.strip()) for row in file]
        return rows, cols, world

def _depth_first_search(rows: int, cols: int, world: list[list], start: list[int]) -> (int, int, str, list[int]):
    stack = [[start[0], start[1], ""]]
    checked = dict()
    nodes_generated = 1
    nodes_expanded = 0

    while len(stack) > 0:
        cur_x, cur_y, cur_path = stack.pop()
        nodes_expanded += 1

        for a, b in [[0,1], [1,0], [-1,0], [0,-1]]:
            new_x = cur_x + a
            new_y = cur_y + b
            if 0 > new_x or new_x >= rows or 0 > new_y or new_y >= cols or world[new_x][new_y] == "#" or (new_x, new_y) in checked:
                continue
            else:
                if a == 0 and b == 1:
                    new_path = cur_path + "E"
                elif a == 0 and b == -1:
                    new_path = cur_path + "W"
                elif a == 1 and b == 0:
                    new_path = cur_path + "S"
                else:
                    new_path = cur_path + "N"

                if world[new_x][new_y] == "*":
                    return nodes_generated, nodes_expanded, new_path, [new_x, new_y]
                else:
                    checked[(new_x, new_y)] = 1
                    stack.append([new_x, new_y, new_path])
                    nodes_generated += 1

    print("Not possible")
    return None, None, None, None

def depth_first_search(rows:int, cols:int, world: list[list]):
    count, start = find_important_info(world)
    nodes_generated = 0
    nodes_expanded = 0

    path = ""
    while count > 0:
        new_generated, new_expanded, new_path, new_start = _depth_first_search(rows, cols, world, start)

        if new_path is None:
            return None

        nodes_generated += new_generated
        nodes_expanded += new_expanded

        world[start[0]][start[1]] = "-"
        world[new_start[0]][new_start[1]] = "@"
        path += new_path
        path += "V"
        count -= 1
        start = new_start

    print_output(path, nodes_generated, nodes_expanded)

def uniform_cost_search(rows: int, cols: int, world: list[list]):
    count, start = find_important_info(world)
    queue = dict()
    queue[0] = (world, start[0], start[1], "", count)
    checked = dict()
    output_id = 0
    input_id = 1
    nodes_generated = 1
    nodes_expanded = 0

    while input_id > output_id:
        cur_world, cur_x, cur_y, path, rem_spots = queue[output_id]
        nodes_expanded += 1
        output_id += 1

        for a, b in [[0,1], [1,0], [-1,0], [0,-1]]:
            new_world = deepcopy(cur_world)
            new_rem_spots = rem_spots
            new_x = cur_x + a
            new_y = cur_y + b
            if 0 > new_x or new_x >= rows or 0 > new_y or new_y >= cols or world[new_x][new_y] == "#" or (tuple(tuple(row) for row in cur_world), new_x, new_y) in checked:
                continue
            else:
                if a == 0 and b == 1:
                    new_path = path + "E"
                elif a == 0 and b == -1:
                    new_path = path + "W"
                elif a == 1 and b == 0:
                    new_path = path + "S"
                else:
                    new_path = path + "N"

                if new_world[new_x][new_y] == "*":
                    checked[(tuple(tuple(row) for row in new_world), new_x, new_y)] = 0
                    new_path += "V"
                    new_world[new_x][new_y] = "-"
                    new_rem_spots = rem_spots - 1
                    if new_rem_spots == 0:
                        print_output(new_path, nodes_generated, nodes_expanded)
                        return

                checked[(tuple(tuple(row) for row in new_world), new_x, new_y)] = 0
                nodes_generated += 1
                queue[input_id] = (new_world, new_x, new_y, new_path, new_rem_spots)
                input_id += 1


    print("Not possible")
    return

def find_important_info(world: list[list]) -> (int, list[int]):
    count = 0
    start = []

    for i in range(len(world)):
        for j in range(len(world[0])):
            if world[i][j] == "@":
                start = [i, j]
            elif world[i][j] == "*":
                count += 1

    return count, start

def print_output(path: str, nodes_generated: int, nodes_expanded: int):
    for char in path:
        print(char)
    print(f"{nodes_generated} nodes generated\n{nodes_expanded} nodes expanded")

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 planner.py <algorithm> <worldfile>")
        sys.exit(1)

    alg = sys.argv[1]
    file = sys.argv[2]

    rows, cols, world = create_world_from_file(file)

    if alg == "depth-first":
        depth_first_search(rows, cols, world)
    elif alg == "uniform-cost":
        uniform_cost_search(rows, cols, world)

if "__main__" == __name__:
    main()

