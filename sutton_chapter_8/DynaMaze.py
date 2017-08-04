from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt

rows = 6
cols = 9
S = np.zeros(6 * 9).reshape((6, 9))
S[2, 2] = 1
S[3, 2] = 1
S[4, 2] = 1
S[1, 5] = 1
S[4, 8] = 1
S[3, 8] = 1

start_row = 3
start_col = 0

final_row = 5
final_col = 8

A_ST = ["UP", "DOWN", "RIGHT", "LEFT"]
A_SY = ["^", "v", ">", "<"]


def is_final(r, c):
    return r == final_row and c == final_col


def create_model(M):
    for rr in range(rows):
        for cc in range(cols):
            for a in range(4):
                r = rr
                c = cc
                if a == 0:
                    if r < 5:
                        if S[r + 1, c] == 0:
                            r += 1
                elif a == 1:
                    if r > 0:
                        if S[r - 1, c] == 0:
                            r -= 1
                elif a == 2:
                    if c < 8:
                        if S[r, c + 1] == 0:
                            c += 1
                elif a == 3:
                    if c > 0:
                        if S[r, c - 1] == 0:
                            c -= 1
                if rr == final_row and cc == final_col:
                    M[rr, cc, a] = [r, c, 1]
                else:
                    M[rr, cc, a] = [r, c, 0]
                    # print("[{}, {}] -> {} -> [{}, {}]".format(rr, cc, A_ST[a], r, c))


def take_action(r, c, a):
    if a == 0:
        if r < 5:
            if S[r + 1, c] == 0:
                r += 1
    elif a == 1:
        if r > 0:
            if S[r - 1, c] == 0:
                r -= 1
    elif a == 2:
        if c < 8:
            if S[r, c + 1] == 0:
                c += 1
    elif a == 3:
        if c > 0:
            if S[r, c - 1] == 0:
                c -= 1
    return [r, c]


def pick_action(e, r, c, q):
    if np.random.rand() > e:
        return np.argmax(q[r, c])
    else:
        return np.random.randint(4)


def dynaQ(episodes=80, epsilon=.1, gamma=.95, alpha=.1, n=50):
    Q = np.zeros(6 * 9 * 4).reshape((6, 9, 4))
    # Q.fill(float('-inf'))
    R = np.zeros(6 * 9).reshape(6, 9)
    R[final_row, final_col] = 1.0
    M = np.empty(6 * 9 * 4, dtype=np.object_).reshape((6, 9, 4))
    M.fill([])
    # create_model(M)
    history = []
    for e in range(episodes):
        print('Episode: {}'.format(e))
        row = np.random.randint(rows)
        col = np.random.randint(cols)
        while not is_final(row, col):
            a = pick_action(epsilon, row, col, Q)
            if [row, col, a] not in history:
                history.append([row, col, a])
            row_, col_ = take_action(row, col, a)
            reward = R[row_, col_]
            Q[row, col, a] += alpha * (reward + gamma * np.argmax(Q[row_, col_]) - Q[row, col, a])
            M[row, col, a] = [row_, col_, reward]

            # print("S:[{} {}], A:{}, S':[{} {}], R:{}, Q(S,a)={} Q(S)={}".format(row, col, A_ST[a], row_, col_,
            #                                                                     reward, Q[row, col, a], Q[row, col]))

            for nn in range(n):
                # print(history)
                ns = history[np.random.randint(len(history))]
                row = ns[0]
                col = ns[1]
                a_ = ns[2]
                nr_, nc_ = take_action(row, col, a_)  # [row, col, a_]
                rew = R[nr_, nc_]
                Q[row, col, a_] += alpha * (rew + gamma * np.argmax(Q[nr_, nc_]) - Q[row, col, a_])
            row = row_
            col = col_
    print('---------------------------------')
    for r in range(rows):
        s = ""
        for c in range(cols):
            s += A_SY[np.argmax(Q[r, c])] + "\t"
        print(s + "\n")

    print(R)


dynaQ()
