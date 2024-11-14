import numpy as np

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
    grid = create_grid(N, seed)
    N += 2 #edges
    x = N // 2
    y = N // 2
    moves = 0
    score = 0
    if grid[x][y] == 1:
        score += 1
    grid[x][y] -= 1
    while moves < 2*N and score > 0 and score < N:
        view = grid[max(0, x - m):min(N, x + m + 1), max(0, y - m):min(N, y + m + 1)]
        
        
        

def create_games(N, m, seed):
    scores = ""
    for i in range(10):
        fn = f"./game{i}"
        total_score = ant_rec(N, m, fn, seed)
        scores += f"{total_score},"
    fn = f"scores_m{m}"
    with open(fn, "w") as f:
        f.write(scores)

N = 10
m = 1
seed = 0
create_games(N, m, seed)
m = 2
create_games(N, m, seed)

# dataset1game = game1
with open("./dataset5games", "w") as f1, open("./dataset10games", "w") as f2:
    for i in range(10):
        file = f"./game{i}"
        with open(file, "r") as f0:
            if i < 5:
                f1.write(f0.read())
                f1.write("\n")

            f2.write(f0.read())
            f2.write("\n")
