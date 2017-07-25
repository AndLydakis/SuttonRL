import numpy as np

states = [.5, .5, .5, .5, .5, .5, 1]
svalues = [0.0, 1 / 6.0, 2 / 6.0, 3 / 6.0, 4 / 6.0, 5 / 6.0, 1.0]


class RWalk:
    def __init__(self, nepisodes=100, alpha=0.1):
        self.states = states[:]
        self.values = svalues[:]
        self.ep = nepisodes
        self.alpha = alpha
        for i in range(self.ep):
            self.td_zero(3)
            self.const_a_markov(3)
        pass

    def td_zero(self, cs):
        cur_state = cs
        history = [cur_state]
        s = states[:]
        v = svalues[:]
        r = 0.0
        while True:
            previous = cur_state
            if np.random.randint(2) == 0:
                cur_state -= 1
            else:
                cur_state += 1
            s[previous] += self.alpha * (s[cur_state] - s[previous])
            history.append(cur_state)
            if cur_state == 0:
                break
            if cur_state == 6:
                break
        return r, history

    def const_a_markov(self, cs):
        cur_state = cs
        s = states[:]
        v = svalues[:]
        history = [cs]
        while True:
            if np.random.randint(2) == 0:
                cur_state -= 1
            else:
                cur_state += 1
            if cur_state == 0:
                r = 0.0
                break
            if cur_state == 6:
                r = 1.0
            for h in history:
                s[h] += self.alpha * (r - s[h])
        return r * (len(history) - 1), history


if __name__ == '__main__':
    RWalk(100, 0.1)
