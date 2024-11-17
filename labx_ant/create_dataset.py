'''
@author Mqtth3w https://github.com/Mqtth3w
@license GPL-3.0
'''

import numpy as np
import random

def create_grid(N, m, seed):
    np.random.seed(seed)
    grid = np.zeros((N + m*2, N + m*2), dtype=int)
    grid[:m, :] = -N-2
    grid[-m:, :] = -N-2
    grid[:, :m] = -N-2
    grid[:, -m:] = -N-2
    positions = np.random.choice(N * N, N, replace=False)
    row_idxs, col_idxs = np.unravel_index(positions, (N, N))
    grid[row_idxs + m, col_idxs + m] = 1
    return grid

def ant_rec(N, m, filename, seed):
    grid = create_grid(N, m, seed)
    x = (N + 2) // 2
    y = (N + 2) // 2
    moves = 0
    score = 0
    move = ""
    grid[x][y] -= 1
    if grid[x][y] == 0:
        score += 1
    while x-m >= 0 and y-m >= 0 and x-m < N and y-m < N and moves < 2*N and score < N and score > -N-2:
        x_min, x_max = x - m, x + m + 1
        y_min, y_max = y - m, y + m + 1
        view = grid[x_min:x_max, y_min:y_max]
        line = ",".join(map(str, view.flatten()))
        ones_positions = np.argwhere(view == 1)
        ones_positions = [(x_min + pos[0], y_min + pos[1]) for pos in ones_positions]
        if ones_positions:
            first_near = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            first_ones = [pos for pos in ones_positions if pos in first_near]
            if first_ones: # if-elif-else all cases m=1
                x_mov, y_mov = random.choice(first_ones)
                if (x_mov, y_mov) == (x-1, y):
                    x -= 1
                    move = "up"
                elif (x_mov, y_mov) == (x+1, y):
                    x += 1
                    move = "down"
                elif (x_mov, y_mov) == (x, y-1):
                    y -= 1
                    move = "left"
                elif (x_mov, y_mov) == (x, y+1):
                    y += 1
                    move = "right"
            else:
                first_corsers = [(x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)]
                corner_ones = [pos for pos in ones_positions if pos in first_corsers]
                if corner_ones:
                    x_corner, y_corner = random.choice(corner_ones)
                    neighbors = []
                    if x_corner < x and y_corner < y:
                        neighbors = [(x, y-1, "left"), (x-1, y, "up")]
                    elif x_corner > x and y_corner > y:
                        neighbors = [(x, y+1, "right"), (x+1, y, "down")]
                    elif x_corner < x and y_corner > y:
                        neighbors = [(x-1, y, "up"), (x, y+1, "right")]
                    elif x_corner > x and y_corner < y:
                        neighbors = [(x, y-1, "left"), (x+1, y, "down")]
                    best_move = max(neighbors, key=lambda pos: grid[pos[0]][pos[1]])
                    x, y, move = best_move[0], best_move[1], best_move[2]
                else: # if-elif-else all cases m=2
                    second_near = [(x-2, y), (x+2, y), (x, y-2), (x, y+2)]
                    second_ones = [pos for pos in ones_positions if pos in second_near]
                    if second_ones:
                        x_mov, y_mov = random.choice(second_ones)
                        if (x_mov, y_mov) == (x-2, y):
                            x -= 1
                            move = "up"
                        elif (x_mov, y_mov) == (x+2, y):
                            x += 1
                            move = "down"
                        elif (x_mov, y_mov) == (x, y-2):
                            y -= 1
                            move = "left"
                        elif (x_mov, y_mov) == (x, y+2):
                            y += 1
                            move = "right"
                    else:
                        second_corsers = [(x-2, y-2), (x-2, y+2), (x+2, y-2), (x+2, y+2),
                                          (x-1, y-2), (x-1, y+2), (x-2, y-1), (x-2, y+1),
                                          (x+1, y-2), (x+1, y+2), (x+2, y-1), (x+2, y+1)]
                        corner_ones2 = [pos for pos in ones_positions if pos in second_corsers]
                        if corner_ones2:
                            x_corner, y_corner = random.choice(corner_ones2)
                            neighbors = []
                            if x_corner < x and y_corner < y:
                                neighbors = [(x, y-1, "left"), (x-1, y, "up")]
                            elif x_corner > x and y_corner > y:
                                neighbors = [(x, y+1, "right"), (x+1, y, "down")]
                            elif x_corner < x and y_corner > y:
                                neighbors = [(x-1, y, "up"), (x, y+1, "right")]
                            elif x_corner > x and y_corner < y:
                                neighbors = [(x, y-1, "left"), (x+1, y, "down")]
                            best_move = max(neighbors, key=lambda pos: grid[pos[0]][pos[1]])
                            x, y, move = best_move[0], best_move[1], best_move[2]
        else: # no ones found
            neighbors = [(x, y-1, "left"), (x-1, y, "up"), (x, y+1, "right"), (x+1, y, "down")]
            max_val = max(grid[pos[0]][pos[1]] for pos in neighbors)
            max_neighbors = [pos for pos in neighbors if grid[pos[0]][pos[1]] == max_val]
            rand_move = random.choice(max_neighbors)
            x, y, move = rand_move[0], rand_move[1], rand_move[2]
        score += grid[x][y]
        grid[x][y] -= 1
        moves += 1
        line += f",{move}\n"
        with open(filename, "a", encoding="utf-8") as f:
            f.write(line)
    return score

def create_games(N, m, seed):
    scores = ""
    for u in range(10):
        fn = f"./data/m{m}_game{u}.txt"
        print(fn)
        total_score = ant_rec(N, m, fn, (seed+u)**u)
        scores += f"{total_score},"
    fn = f"./data/scores_m{m}.txt"
    with open(fn, "w", encoding="utf-8") as f:
        f.write(scores)

if __name__ == "__main__":
    _N = 10
    _m = 1
    _seed = 0
    create_games(_N, _m, _seed)
    _m = 2
    create_games(_N, _m, _seed)
    # dataset1game = game1
    for j in range(1, 3):
        with open(f"./data/dataset5games_m{j}.txt", "w", encoding="utf-8") as f1, open(f"./data/dataset10games_m{j}.txt", "w", encoding="utf-8") as f2:
            for i in range(10):
                file = f"./data/m{j}_game{i}.txt"
                with open(file, "r", encoding="utf-8") as f0:
                    text = f0.read()
                    if i < 5:
                        f1.write(text)
                        #f1.write("\n")
                    f2.write(text)
                    #f2.write("\n")
