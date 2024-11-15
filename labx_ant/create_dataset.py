import numpy as np
import random

def create_grid(N, seed):
    np.random.seed(seed)
    grid = np.zeros((N + 2, N + 2), dtype=int)
    grid[0, :] = -N-2
    grid[-1, :] = -N-2
    grid[:, 0] = -N-2
    grid[:, -1] = -N-2
    positions = np.random.choice(N * N, N, replace=False)
    row_idxs, col_idxs = np.unravel_index(positions, (N, N))
    grid[row_idxs + 1, col_idxs + 1] = 1
    return grid

def ant_rec(N, m, filename, seed):
    #random.seed(seed)
    grid = create_grid(N, seed)
    x = (N + 2) // 2
    y = (N + 2) // 2
    moves = 0
    score = 0
    move = ""
    if grid[x][y] == 1:
        score += 1
    grid[x][y] -= 1
    while moves < 2*N and score > -N-2 and score < N:
        x_min, x_max = max(0, x - m), min(N, x + m + 1)
        y_min, y_max = max(0, y - m), min(N, y + m + 1)
        view = grid[x_min:x_max, y_min:y_max]
        ones_positions = np.argwhere(view == 1)
        ones_positions = [(x_min + pos[0], y_min + pos[1]) for pos in ones_positions]
        if ones_positions:
            first_near = [(x-1, y), (x, y-1), (x, y+1), (x+1, y)]
            first_ones = [pos for pos in ones_positions if pos in first_near]
            if first_ones: # if-elif-else all cases m=1
                x_mov, y_mov = random.choice(first_ones)
                if (x_mov, y_mov) == (x-1, y):
                    x -= 1
                    move = "up"
                elif (x_mov, y_mov) == (x, y-1):
                    y -= 1
                    move = "left"
                elif (x_mov, y_mov) == (x, y+1):
                    y += 1
                    move = "right"
                elif (x_mov, y_mov) == (x+1, y):
                    x += 1
                    move = "down"
            else:
                first_corsers = [(x-1, y-1), (x+1, y+1), (x-1, y-1), (x-1, y+1)]
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
                    second_near = [(x-2, y), (x, y-2), (x, y+2), (x+2, y)]
                    second_ones = [pos for pos in ones_positions if pos in second_near]
                    if second_ones:
                        x_mov, y_mov = random.choice(second_ones)
                        if (x_mov, y_mov) == (x-2, y):
                            x -= 1
                            move = "up"
                        elif (x_mov, y_mov) == (x, y-2):
                            y -= 1
                            move = "left"
                        elif (x_mov, y_mov) == (x, y+2):
                            y += 1
                            move = "right"
                        elif (x_mov, y_mov) == (x+2, y):
                            x += 1
                            move = "down"
                    else:
                        second_corsers = [(x-2, y-2), (x+2, y+2), (x-2, y-2), (x-2, y+2),
                                          (x-2, y-1), (x-1, y-2), (x-2, y+1), (x-1, y+2),
                                          (x+2, y-1), (x+1, y-2), (x+2, y+1), (x+1, y+2)]
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
        line = ",".join(map(str, view.flatten())) + f",{move}\n"
        with open(filename, "a") as f:
            f.write(line)
    return score

def create_games(N, m, seed):
    scores = ""
    for i in range(10):
        fn = f"./data/m{m}_game{i}.txt"
        print(fn)
        total_score = ant_rec(N, m, fn, seed)
        scores += f"{total_score},"
    fn = f"./data/scores_m{m}.txt"
    with open(fn, "w") as f:
        f.write(scores)

_N = 10
_m = 1
_seed = 0
create_games(_N, _m, _seed)
_m = 2
create_games(_N, _m, _seed)
# dataset1game = game1
for j in range(1, 3):
    with open(f"./data/dataset5games_m{j}.txt", "w") as f1, open(f"./data/dataset10games_m{j}.txt", "w") as f2:
        for i in range(10):
            file = f"./data/m{j}_game{i}.txt"
            with open(file, "r") as f0:
                line = f0.read()
                if i < 5:
                    f1.write(line)
                    f1.write("\n")
                f2.write(line)
                f2.write("\n")
