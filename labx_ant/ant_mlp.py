'''
@author Mqtth3w https://github.com/Mqtth3w
@license GPL-3.0
'''

import pandas as pd
from create_dataset import create_grid
from sklearn.neural_network import MLPClassifier


label2id = {"up": 11, "down": 26, "left": 17, "right": 9}
id2label = {11: "up", 26: "down", 17: "left", 9: "right"}


def ant_train(model, m, dataset):
    dataset = pd.read_csv(dataset, header=None)
    X = dataset.iloc[:,:(2*m+1)**2].values
    y = dataset.iloc[:,(2*m+1)**2].values
    y = [label2id[label] for label in y]
    #print("X=", X)
    #print("y=", y)
    model.fit(X, y)
    print("model trained.")

def ant_play_game(model, grid, N, m):
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
        print("Board:\n", grid, "\nant view:\n", view)
        y_pred = model.predict([view.flatten()])
        move = id2label[y_pred[0]]
        print(f"ant grid pos: ({x}, {y}). model move: {move}.")
        if move == "up":
            x -= 1
        elif move == "down":
            x += 1
        elif move == "left":
            y -= 1
        elif move == "right":
            y += 1
        score += grid[x][y]
        grid[x][y] -= 1
        moves += 1
        print(f"score: {score}. moves: {moves}.")
        #input("press any key to proced or remove this line to automate the process.")
    return score

if __name__ == "__main__":
    _N = 10
    _seed = 0
    _m = 2
    clf_mxm = MLPClassifier(hidden_layer_sizes=((2*_m+1)**2-_m, ((2*_m+1)**2-2*_m)), max_iter=500, early_stopping=False, random_state=_seed)
    ant_train(clf_mxm, _m, f"./data/dataset5games_m{_m}.txt")
    for i in range(5):
        print(f"\n\nGame number {i} of 5.\n\n")
        _grid = create_grid(_N, _m, (_seed+i)**i)
        _score = ant_play_game(clf_mxm, _grid, _N, _m)
        with open(f"./mlp_game_scores/m{_m}_game_scores.txt", "a", encoding="utf-8") as f:
            f.write(f"{_score}\n")
    
    