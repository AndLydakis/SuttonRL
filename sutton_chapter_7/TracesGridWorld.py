from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import math

rows = 8
columns = 10

start_row = 3
start_col = 1

final_row = 3
final_col = 6

A_ST = ["UP", "DOWN", "RIGHT", "LEFT"]
A_SY = ["^", "v", ">", "<"]


def is_final(r, c):
    return r == final_row and c == final_col


def pick_action(e, q, r, c):
    roll = np.random.rand()
    print("Roll: {}".format(roll))
    if roll > e:
        # print(q[r, c])
        # print(np.argmax(q[r, c]))
        # print(q[r, c, np.argmax(q[r, c])])
        return np.argmax(q[r, c])
    else:
        return np.random.randint(4)


def take_action(ac, row, col):
    if ac == 0:
        row += 1
    elif ac == 1:
        row -= 1
    elif ac == 2:
        col += 1
    else:
        col -= 1

    if row < 0:
        row = 0
    if row > 7:
        row = 7

    if col < 0:
        col = 0
    if col > 9:
        col = 9
    return [row, col]


def sarsa_lambda(episodes, lam, epsilon, gamma, alpha):
    Q = np.zeros(rows * columns * 4).reshape((rows, columns, 4))
    R = np.zeros(rows * columns).reshape((rows, columns))
    R[final_row, final_row] = 100.0
    for e in range(episodes):
        Z = np.zeros(rows * columns * 4).reshape((rows, columns, 4))
        row = start_row
        col = start_col
        action = np.random.randint(4)
        while not is_final(row, col):
            row_, col_ = take_action(action, row, col)
            action_ = pick_action(epsilon, Q, row_, col_)
            reward = R[row_, col_]
            delta = reward + gamma * Q[row_, col_, action_] - Q[row, col, action]
            Z[row, col, action] += 1
            print("S:[{} {}], A:{}, S':[{} {}], R:{}, Q(S,a)={}, delta={}".format(row, col, A_ST[action], row_, col_,
                                                                                  reward, Q[row, col, action_], delta))
            for r in range(rows):
                for c in range(columns):
                    for a in range(4):
                        Q[r, c, a] += alpha * delta * Z[r, c, a]
                        Z[r, c, a] += gamma * lam * Z[r, c, a]
                        print(Q[r, c, a])
                        print(Z[r, c, a])

            row = row_
            col = col_
            action = action_


sarsa_lambda(episodes=1, lam=0.9, epsilon=.1, gamma=1, alpha=1)
