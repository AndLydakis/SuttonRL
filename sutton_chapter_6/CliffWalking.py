from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import math


class CliffWalking:

    rewQ = []
    rewS = []
    def is_final(self, r, c):
        return r == 0 and c == 11

    def pick_action(self, e, q, r, c):
        if np.random.rand() > e:
            return np.argmax(q[r, c])
        else:
            return np.random.randint(4)

    def take_action(self, ac, row, col):
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
        if col < 0:
            col = 0
        if row > 3:
            row = 3
        if col > 11:
            col = 11
        return [row, col]

    def sarsa(self, episodes, alpha, epislon, gamma):
        Q = np.zeros(4 * 12 * 4).reshape((4, 12, 4))
        R = np.zeros(4 * 12).reshape((4, 12))
        R.fill(-1.0)
        R[0, 1:11] = -100.0
        # R[2, 1:11, 1] = -100.0
        # R[0, 1:11, 0] = -100.0
        print(R)
        AS = ["UP", "DOWN", "RIGHT", "LEFT"]
        ASS = ["^", "V", ">", "<"]
        A = [0, 1, 2, 3]
        rew = []
        for e in range(episodes):
            rewards = 0
            row = 0
            col = 0
            steps = 0
            while not self.is_final(row, col):
                a_ = self.pick_action(epislon, Q, row, col)
                row_, col_ = self.take_action(a_, row, col)
                # print(Q[row, col, A])
                reward = R[row_, col_]
                rewards += reward
                if row_ == 0 and 0 < col_ < 11:
                    row_ = 0
                    col_ = 0
                new_ac = self.pick_action(epislon, Q, row_, col_)
                Q[row, col, a_] = \
                    Q[row, col, a_] + alpha * (reward +
                                               gamma * Q[row_, col_, new_ac]
                                               - Q[row, col, a_])
                # print("S:[{} {}], A:{}, S':[{} {}], R:{}, Q(S,a)={}".format(row, col, AS[a_], row_, col_, reward,
                #                                                             Q[row, col, a_]))
                row = row_
                col = col_
                steps += 1
            rew.append(rewards)
        plt.figure()
        plt.plot(np.arange(len(rew)), rew)
        plt.show()

    def qlearning(self, episodes, alpha, epislon, gamma):
        Q = np.zeros(4 * 12 * 4).reshape((4, 12, 4))
        R = np.zeros(4 * 12).reshape((4, 12))
        R.fill(-1.0)
        R[0, 1:11] = -100.0
        # R[2, 1:11, 1] = -100.0
        # R[0, 1:11, 0] = -100.0
        print(R)
        AS = ["UP", "DOWN", "RIGHT", "LEFT"]
        ASS = ["^", "V", ">", "<"]
        A = [0, 1, 2, 3]
        rew = []
        for e in range(episodes):
            rewards = 0
            row = 0
            col = 0
            steps = 0
            while not self.is_final(row, col):
                a_ = self.pick_action(epislon, Q, row, col)
                row_, col_ = self.take_action(a_, row, col)
                # print(Q[row, col, A])
                reward = R[row_, col_]
                rewards += reward
                if row_ == 0 and 0 < col_ < 11:
                    row_ = 0
                    col_ = 0
                Q[row, col, a_] = \
                    Q[row, col, a_] + alpha * (reward +
                                               gamma * Q[row_, col_, [np.argmax(Q[row_, col_])]]
                                               - Q[row, col, a_])
                # print("S:[{} {}], A:{}, S':[{} {}], R:{}, Q(S,a)={}".format(row, col, AS[a_], row_, col_, reward,
                #                                                             Q[row, col, a_]))
                row = row_
                col = col_
                steps += 1
            rew.append(rewards)
        plt.figure()
        plt.plot(np.arange(len(rew)), rew)
        plt.show()

    def __init__(self, q, episodes=500, alpha=0.5, epsilon=0.1, gamma=1.0):
        if q:
            self.qlearning(episodes, alpha, epsilon, gamma)
        else:
            self.sarsa(episodes, alpha, epsilon, gamma)




if __name__ == '__main__':
    rewq = CliffWalking(True)
    rews = CliffWalking(False)



