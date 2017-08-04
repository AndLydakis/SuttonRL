import numpy as np
import matplotlib.pyplot as plt

states = [0.0, .5, .5, .5, .5, .5, 1]
svalues = [0.0, 1 / 6.0, 2 / 6.0, 3 / 6.0, 4 / 6.0, 5 / 6.0, 1.0]


class RWalk:
    def __init__(self, nepisodes=100, alpha=0.1, runs=100):
        self.states = states[:]
        self.runs = runs
        td_states = states[:]
        m_states = states[:]
        self.values = svalues[:]
        self.ep = nepisodes
        self.alpha = alpha
        # plt.figure()
        # for i in range(self.ep):
        #     tdh, tdr = self.td_zero(3, td_states, self.alpha, 0)
        #     mh, mr = self.const_a_markov(3, m_states, self.alpha, 0)
        #     if i % 20 == 0 or i == 0 or i == 1:
        #         plt.plot(np.arange(len(self.states)), td_states, label=str(i) + ' episodes')
        # plt.plot(np.arange(len(self.states)), svalues, label="True values")
        # plt.xlabel("STATES")
        # plt.ylabel("Episodes")
        # plt.title("Figure 6.2")
        # plt.legend(loc="best")
        # plt.show()
        # plt.close()

        # plt.figure()
        # for a in [0.1, 0.05, 0.02, 0.01]:
        #     total_td_sq_errors = np.zeros(self.ep)
        #     total_mc_sq_errors = np.zeros(self.ep)
        #     for r in range(self.runs):
        #         td_states = self.states[:]
        #         td_sq_errors = []
        #         mc_states = self.states[:]
        #         mc_sq_errors = []
        #         for e in range(self.ep):
        #             # print(str(r) + " " + str(e))
        #             td_sq_errors.append(np.sqrt(np.sum(np.power(np.array(svalues) - np.array(td_states), 2)) / 7.0))
        #             mc_sq_errors.append(np.sqrt(np.sum(np.power(np.array(svalues) - np.array(mc_states), 2)) / 7.0))
        #             tdh, tdr = self.td_zero(3, td_states, self.alpha, 0)
        #             mh, mr = self.const_a_markov(3, mc_states, self.alpha, 0)
        #         total_td_sq_errors += td_sq_errors
        #         total_mc_sq_errors += mc_sq_errors
        #     total_td_sq_errors /= self.runs
        #     total_mc_sq_errors /= self.runs
        #     plt.plot(np.arange(self.ep), td_sq_errors, label='TD, alpha: ' + str(a))
        #     plt.plot(np.arange(self.ep), mc_sq_errors, label='MC, alpha: ' + str(a))
        # plt.ylabel("RMS ERROR")
        # plt.xlabel("Walks/Episodes")
        # plt.title("Figure 6.3")
        # plt.legend(loc="best")
        # plt.show()
        # plt.close()

        total_td_sq_errors = np.zeros(self.ep)
        total_mc_sq_errors = np.zeros(self.ep)
        for r in range(self.runs):
            td_histories = []
            td_rewards = []
            td_sq_errors = []
            mc_histories = []
            mc_rewards = []
            mc_sq_errors = []
            for e in range(self.ep):
                td_conv = 999999.0
                mc_conv = 999999.0
                td_states = states[:]
                mc_states = states[:]
                tdr, tdh = self.td_zero(3, td_states, 0.001, 1)
                mcr, mch = self.const_a_markov(3, mc_states, 0.001, 1)
                td_histories.append(tdh)
                td_rewards.append(tdr)
                mc_histories.append(mch)
                mc_rewards.append(mcr)
                while True:
                    if td_conv > 1e-3:
                        td_new_values = np.zeros(len(states))
                        for h in range(len(td_histories)):
                            for hh in range(len(td_histories[h]) - 1):
                                td_new_values[td_histories[h][hh]] += \
                                    td_rewards[h] - td_states[td_histories[h][hh]] + td_states[td_histories[h][hh + 1]]
                        td_new_values *= 0.001
                        td_conv = sum(np.abs(td_new_values))
                        td_states += td_new_values[:]
                    else:
                        print("TD " + str(r) + " " + str(e) + " " + str(td_conv))
                        td_sq_errors.append(
                            np.sqrt(np.sum(np.power((np.array(td_states) - np.array(self.values)), 2)) / 7.0))
                        break

                while True:
                    mc_new_values = np.zeros(len(states))
                    if mc_conv > 1e-3:
                        for h in range(len(mc_histories)):
                            for hh in range(len(mc_histories[h])):
                                mc_new_values[mc_histories[h][hh]] += \
                                    mc_rewards[h] - mc_states[mc_histories[h][hh]]
                        mc_new_values *= 0.001
                        mc_conv = sum(np.abs(mc_new_values))
                        mc_states += mc_new_values[:]
                    else:
                        print("MC " + str(r) + " " + str(e) + " " + str(mc_conv))
                        mc_sq_errors.append(
                            np.sqrt(np.sum(np.power((np.array(mc_states) - np.array(self.values)), 2)) / 7.0))
                        break
            total_td_sq_errors += td_sq_errors
            total_mc_sq_errors += mc_sq_errors
        total_td_sq_errors /= runs
        total_mc_sq_errors /= runs
        plt.figure()
        plt.plot(np.arange(self.ep), total_td_sq_errors, label="TD")
        plt.plot(np.arange(self.ep), total_mc_sq_errors, label="MC")
        plt.plot(label="MC")
        plt.xlabel("Walks/Episodes")
        plt.ylabel("RMS Error")
        plt.legend(loc="best")
        plt.show()
        plt.close()

    def td_zero(self, cs, states_, a, batch=0):
        cur_state = cs
        history = [cur_state]
        v = svalues[:]
        r = 0.0
        while True:
            previous = cur_state
            if np.random.randint(2) == 0:
                cur_state -= 1
            else:
                cur_state += 1
            if batch == 0:
                states_[previous] += a * (states_[cur_state] - states_[previous])
            history.append(cur_state)
            if cur_state == 0:
                break
            if cur_state == 6:
                break
        return r, history

    def const_a_markov(self, cs, states_, a, batch):
        cur_state = cs
        v = svalues[:]
        history = [cs]
        r = 0.0
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
                break
        if batch == 0:
            for h in history:
                states_[h] += a * (r - states_[h])
        return r * (len(history) - 1), history


if __name__ == '__main__':
    RWalk(100, 0.1)
