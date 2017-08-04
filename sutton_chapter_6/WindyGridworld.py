import math
import numpy as np
import matplotlib as plt


class WindyGridworld:
    S = np.zeros((7, 10))
    R = np.zeros((7, 10))
    R.fill(-1.0)
    R[3, 7] = 1
    W = np.zeros((7, 10))
    W[:, 3] = 1
    W[:, 4] = 1
    W[:, 5] = 1
    W[:, 6] = 2
    W[:, 7] = 2
    W[:, 8] = 1
    print(W[6])

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
    QK = np.zeros(7 * 10 * 8).reshape(7, 10, 8)
    P = np.zeros(7 * 10).reshape(7, 10)

    def take_action(self, action, sx, sy, stoch):
        AK_ = self.AK
        W = self.W
        # UP
        if action == AK_[0]:
            sx += (1 + W[sx, sy] + self.stoch_step(stoch))
        # DOWN
        elif action == AK_[1]:
            sx = sx - 1 + W[sx, sy] + self.stoch_step(stoch)
        # RIGHT
        elif action == AK_[2]:
            sx += W[sx, sy] + self.stoch_step(stoch)
            sy += 1
        # LEFT
        elif action == AK_[3]:
            sx += W[sx, sy] + self.stoch_step(stoch)
            sy -= 1
        # UP RIGHT
        elif action == AK_[4]:
            sx += 1 + W[sx, sy] + self.stoch_step(stoch)
            sy += 1
        # UP LEFT
        elif action == AK_[5]:
            sx += 1 + W[sx, sy] + self.stoch_step(stoch)
            sy -= 1
        # DOWN RIGHT
        elif action == AK_[6]:
            sx = sx - 1 + W[sx, sy] + self.stoch_step(stoch)
            sy += 1
        # DOWN LEFT
        elif action == AK_[7]:
            sx = sx - 1 + W[sx, sy] + self.stoch_step(stoch)
            sy -= 1
        if sx < 0:
            sx = 0
        if sy < 0:
            sy = 0
        if sy > 9:
            sy = 9
        if sx > 6:
            sx = 6
        return [int(sx), int(sy)]

    def is_terminal(self, sx, sy):
        return sy == 7 and sx == 3

    def pick_action(self, q, x, y, e, k):
        if np.random.rand() > e:
            return np.argmax(q[x][y])
        else:
            if k:
                return np.random.randint(7)
            else:
                return np.random.randint(3)

    def print_policy(self, q):
        for i in range(7):
            s = ""
            for j in range(10):
                s += self.ACST[np.argmax(q[i][j])] + "\t"
            print(s)

    def stoch_step(self, stoch):
        if stoch:
            return np.random.choice([-1, 0, 1], 1)
        else:
            return 0

    def __init__(self, alpha=0.01, gamma=0.01, epsilon=0.1, episodes=8000, kings=True, stoch=False  ):

        if kings:
            Q = self.QK
            A = self.AK
        else:
            Q = self.Q
            A = self.A

        for e in range(episodes):
            Sx = 0
            Sy = 3
            Sx_ = 0
            Sy_ = 0
            ac = self.pick_action(Q, Sx, Sy, epsilon, kings)
            steps = 0
            while not self.is_terminal(Sx, Sy):
                [Sx_, Sy_] = self.take_action(ac, Sx, Sy, stoch)
                ac_ = self.pick_action(Q, Sx_, Sy_, epsilon, kings)
                # print(
                #     "S = [{} {}], a = {}, S' = [{} {}], a' = {}".format(Sy, Sx, self.ACST[ac], Sy_, Sx_,
                #                                                         self.ACST[ac_]))
                Q[Sx, Sy, ac] = (Q[Sx, Sy, ac] + alpha * (-1 + gamma * Q[Sx_, Sy_, ac_] - Q[Sx, Sy, ac]))
                Sx = Sx_
                Sy = Sy_
                ac = ac_
                steps += 1
            print(steps)
        # self.print_policy(Q)
        return


if __name__ == '__main__':
    WindyGridworld()
