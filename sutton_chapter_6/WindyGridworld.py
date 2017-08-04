import math
import numpy as np
import matplotlib as plt


class WindyGridworld:
    S = np.zeros((10, 7))
    R = np.zeros((10, 7))
    R.fill(-1.0)
    R[7, 3] = 1
    W = np.zeros((7, 10))
    W[3, :] = 1
    W[4, 4] = 1
    W[:, 5] = 1
    W[:, 6] = 2
    W[:, 7] = 2
    W[:, 8] = 1
    ACTION_UP = 0
    ACTION_DOWN = 1
    ACTION_RIGHT = 2
    ACTION_LEFT = 3
    ACTION_UP_RIGHT = 4
    ACTION_UP_LEFT = 5
    ACTION_DOWN_RIGHT = 6
    ACTION_DOWN_LEFT = 7
    ACST = ["UP", "DOWN", "RIGHT", "LEFT", "UP RIGHT", "UP LEFT", "DOWN RIGHT", "DOWN LEFT"]
    A = [ACTION_UP, ACTION_DOWN, ACTION_RIGHT, ACTION_LEFT]
    AK = [ACTION_UP, ACTION_DOWN, ACTION_RIGHT, ACTION_LEFT, ACTION_UP_RIGHT, ACTION_UP_LEFT, ACTION_DOWN_RIGHT,
          ACTION_DOWN_LEFT]
    Q = np.zeros(7 * 10 * 4).reshape(7, 10, 4)
    # Q = [np.zeros((7, 10, 4))]
    QK = [np.zeros((7, 10, 8))]

    def take_action(self, action, sx, sy):
        AK_ = self.AK
        W = self.W
        if action == AK_[0]:
            sy -= (1 + W[sx, sy])
        elif action == AK_[1]:
            sy += (1 + W[sx, sy])
        elif action == AK_[2]:
            sx += (1 + W[sx, sy])
        elif action == AK_[3]:
            sx -= (1 + W[sx, sy])
        elif action == AK_[4]:
            sy -= (1 + W[sx, sy])
            sx += 1
        elif action == AK_[5]:
            sy -= (1 + W[sx, sy])
            sx -= 1
        elif action == AK_[6]:
            sy += (1 + W[sx, sy])
            sx += 1
        elif action == AK_[7]:
            sy += (1 + W[sx, sy])
            sx -= 1
        if sx < 0:
            sx = 0
        if sy < 0:
            sy = 0
        if sx > 9:
            sx = 9
        if sy > 10:
            sy = 10
        return [int(sx), int(sy)]

    def is_terminal(self, sx, sy):
        return sx == 7 and sy == 3

    def pick_action(self, q, x, y, e, k):
        if np.random.rand() > e:
            print(x, y)
            print(q[x][y])
            return np.argmax(q[x][y])
        else:
            if k:
                return np.random.randint(7)
            else:
                return np.random.randint(3)

    def __init__(self, alpha=0.01, gamma=0.01, epsilon=0.1, episodes=100, kings=False):

        for e in range(episodes):
            Sx = 0
            Sy = 0
            Sx_ = 0
            Sy_ = 0
            if kings:
                Q = self.QK
                A = self.AK
            else:
                Q = self.Q
                A = self.A
            ac = self.pick_action(Q, Sx, Sy, epsilon, kings)
            while not self.is_terminal(Sx, Sy):
                [Sx_, Sy_] = self.take_action(ac, Sx, Sy)
                ac_ = self.pick_action(Q, Sx_, Sy_, epsilon, kings)
                print(
                    "S = [{} {}], a = {}, S' = [{} {}], a' = {}".format(Sx, Sy, self.ACST[ac], Sx_, Sy_,
                                                                        self.ACST[ac_]))
                Q[Sx, Sy, ac] = (Q[Sx, Sy, ac] + alpha * (-1 + gamma * Q[Sx_, Sy_, ac_] - Q[Sx, Sy, ac]))
                Sx = Sx_
                Sy = Sy_
                ac = ac_
        return


if __name__ == '__main__':
    WindyGridworld()
