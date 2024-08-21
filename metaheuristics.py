import random
from math import e
import time

# ogr_sc_idx, ogr_sc_war, kolumny, wiersze, polaczenia, meta_plansza,

# limitwall_idx, limitwall_val, columns, rows, connections, meta_board


def metaheuristics(limitwall_idx, limitwall_val, columns, rows, connections, meta_board, T = 100, alpha = 0.95, iter = 500000, stop = 500):
    start_time = time.perf_counter()
    idx = indexes(meta_board)
    current_board = reshuffle(meta_board.copy(), idx)
    current_value = f(limitwall_idx, limitwall_val, columns, rows, connections, current_board)

    repeated = 0
    for i in range(iter):
        temp_board = reshuffle(current_board.copy(), idx)
        temp_value = f(limitwall_idx, limitwall_val, columns, rows, connections, temp_board)

        if temp_value >= current_value:
            current_board = temp_board
            current_value = temp_value
            repeated = 0
        else:
            try:
                if e ** (- abs((temp_value - current_value) / T)) > random.random():
                    current_board = temp_board
                    current_value = temp_value
                    repeated = 0
                else:
                    repeated += 1
            except OverflowError:
                # print('error')
                repeated += 1

        T = T * alpha

        if repeated > stop:
            print(f'at T = {T} there was no change in too many tries')
            end_time = time.perf_counter()
            time_meta = end_time - start_time
            return current_board, current_value, time_meta
    end_time = time.perf_counter()
    time_meta = end_time - start_time
    return current_board, current_value, time_meta





def f(limitwall_idx, limitwall_val, columns, rows, connections, board):
    score_is_light = [0 for _ in range(len(board))]
    for i in range(len(connections)):
        if type(board[i]) != str:
            temp = 0
            for j in range(len(connections)):
                if type(board[j]) != str:
                    temp += board[j] * connections[i][j]
            score_is_light[i] = min(1, temp)

    score_walls = limitwall_val.copy()
    for i in range(len(limitwall_val)):
        for j in limitwall_idx[i]:
            if board[j - 1] == 1:
                score_walls[i] -= 1
    score_walls = [abs(i) for i in score_walls]

    score_columns = []
    for i in columns:
        temp = 0
        for j in i:
            if board[j - 1] == 1:
                temp += 1
        if temp <= 1:
            temp = 0
        score_columns.append(temp)

    score_rows = []
    for i in rows:
        temp = 0
        for j in i:
            if board[j - 1] == 1:
                temp += 1
        if temp <= 1:
            temp = 0
        score_rows.append(temp)


    score = sum(score_is_light)
    score -= sum(score_walls) * 0.3
    score -= sum(score_columns) * 0.5
    score -= sum(score_rows) * 0.5

    return score


def max_score(board):
    score = 0
    for i in board:
        if i == 0:
            score += 1
    return score


def indexes(board):
    indexes = []
    for i in range(len(board)):
        if type(board[i]) == int:
            indexes.append(i)
    return indexes


def reshuffle(board, indexes):
    temp = (random.sample(indexes, random.randint(1, int(len(indexes) * 0.25))))
    for i in temp:
        board[i] = 1 - board[i]

    return board




