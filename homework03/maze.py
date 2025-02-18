from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    pick = choice((False, True))
    row, col = coord
    if (row == 1) and (col == len(grid[0]) - 2):
        return grid
    elif row == 1:
        grid[row][col + 1] = " "
    elif col == (len(grid[0]) - 2):
        grid[row - 1][col] = " "
    else:
        if pick:
            grid[row][col + 1] = " "
        else:
            grid[row - 1][col] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    for cell in empty_cells:
        grid = remove_wall(grid, cell)

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """

    exits = list()
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "X":
                exits.append((i, j))
                if len(exits) == 2:
                    return exits
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """

    moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == k:
                for dy, dx in moves:
                    ny, nx = y + dy, x + dx
                    if len(grid) > ny >= 0 and 0 <= nx < len(grid[0]) and grid[ny][nx] == 0:
                        grid[ny][nx] = k + 1

    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    y, x = exit_coord
    path = [(y, x)]
    k = grid[y][x]
    moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    if grid[y][x] == 1:
        return path

    for dy, dx in moves:
        ny, nx = y + dy, x + dx
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] == k - 1:
            step = shortest_path(grid, (ny, nx))
            if step:
                return path + step
            grid[ny][nx] = " "

    return None


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    corners = [(0, 0), (0, len(grid) - 1), (len(grid[0]) - 1, len(grid) - 1), (len(grid[0]) - 1, 0)]
    if coord in corners:
        return True

    x, y = coord
    potential_escapes = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    for dx, dy in potential_escapes:
        nx, ny = x + dx, y + dy
        if ((0 < y < len(grid[0]) - 1) and (0 < x < len(grid) - 1)) or (
            0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == " "
        ):
            return False
    return True


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """

    exits = get_exits(grid)

    if len(set(exits)) < 2:
        return grid, exits
    for i in exits:
        if encircled_exit(grid, i):
            return grid, None

    solution = deepcopy(grid)
    y_in, x_in, y_out, x_out = exits[0][0], exits[0][1], exits[1][0], exits[1][1]

    solution[y_in][x_in] = 1

    for y in range(len(solution)):
        for x in range(len(solution[y])):
            if solution[y][x] == " " or solution[y][x] == "X":
                solution[y][x] = 0

    k = 1
    while solution[y_out][x_out] == 0:
        solution = make_step(solution, k)
        k += 1

    return solution, shortest_path(solution, (y_out, x_out))


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    # added final cleanup
    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
                elif isinstance(grid[i][j], int):
                    grid[i][j] = " "
    return grid


if __name__ == "__main__":
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    MAZE, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(MAZE, PATH)
    print(pd.DataFrame(MAZE))
