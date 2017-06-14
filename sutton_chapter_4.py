from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import random
import math


class Gambler:
    
    class state:
        def __init__(self, cap):
            self.cap = cap
            if cap == 100:
                self.terminal = True
                self.rew = 1
            else:
                self.rew = 0
                self.terminal = False
                
    def __init__(self, gamma, theta, method="VI", pheads = 0.4, num_sweeps = -4):
        self.gamma = gamma
        self.theta = theta
        self.pheads = pheads
        S = []
        V = []
        P = []
        for i in range(101):
            S.append(i)
            V.append(0.0)
            P.append(0)
        V[100]=1
        sweep = 0 
        if method=="PI":
            while True:
                # Policy Evaluation
                print(sweep)
                sweep +=1
                while True:
                    Delta = 0
                    for s in S:
                        v = V[s]
                        V[s] = self.pheads*(V[s+P[s]])+(1-self.pheads)*(V[s-P[s]])
                        Delta = max(Delta, np.abs(v - V[s]))
                    if Delta<self.theta:
                        break
                # Policy Improvement
                while True:
                    policy_stable = True
                    for s in S:
                        old_action = P[s]
                        max_a = -999
                        max_idx = 0
                        for a in range(min(s, 100)):
                            temp = self.pheads*(V[s+P[s]])+(1-self.pheads)*(V[s-P[s]])
                            if temp>max_a:
                                max_a = temp
                                max_idx = a
                            P[s] = a
                        if old_action != P[s]:
                            policy_stable = False
                    if policy_stable:
                        print(V)
                        # plt.plot(V)
                        # plt.show()
                        print(P)
                        return
                    else:
                        break
        else:
            while True:
                Delta = 0
                for s in S:
                    max_a = -999
                    max_idx = 0
                    for a in range(min(s, 100-s)+1):
                        temp = self.pheads*V[s+a]+(1-self.pheads)*V[s-a]
                        if temp>max_a:
                            max_a = temp
                            max_idx = a
                    Delta += np.abs(temp - V[s])
                    V[s] = temp
                    print(Delta)
                if Delta < self.theta:
                    print(V)
                    plt.plot(V)
                    plt.show()
                    print(P)
                    break
            for s in S:
                max_a = -999
                max_idx = 0
                for a in range(min(s, 100-s)+1):
                    temp = self.pheads*V[s+a]+(1-self.pheads)*V[s-a]
                    if temp>max_a:
                        max_a = temp
                        max_idx = a
                P[s] = S[a]
            plt.plot(P)
            plt.show()
            print(P)


class Cars:
    
    def returnCars(self, l):
        return np.random.poisson(l)
        
    def requestCars(self, l):
        return np.random.poisson(l)
    
    def poisson_probability(self, actual, mean):
        # naive:   math.exp(-mean) * mean**actual / factorial(actual)

        # iterative, to keep the components from getting too large or small:
        p = math.exp(-mean)
        for i in xrange(actual):
            p *= mean
            p /= i+1
        return p
            
    def calcProf(self, state, action):
        move_cost = abs(action)*self.cars_move_cost
        sum_ = -move_cost
        profit = 0.0
        prob_total = 0.0
        for l1_req in range(self.req_bound1):
            for l2_req in range(self.req_bound2):
                for l1_ret in range(self.ret_bound1):
                    for l2_ret in range(self.ret_bound2):
                        
                        rents = 0
                        
                        preq1 = self.poisson_probability(l1_req, self.reql1)
                        preq2 = self.poisson_probability(l2_req, self.reql2)
                        pret1 = self.poisson_probability(l1_ret, self.retl1)
                        pret2 = self.poisson_probability(l2_ret, self.retl2)
                        
                        # move the cars
                        lot1_cars = min(state[0] - action, self.max_cars)
                        lot2_cars = min(state[1] + action, self.max_cars)
                        
                        # how many can be actually rented
                        if(lot1_cars >= l1_req):
                            rents += l1_req
                        else:
                            rents += lot1_cars
                            
                        
                        if(lot2_cars >= l2_req):
                            rents += l2_req
                        else:
                            rents += lot2_cars
                        
                        # cars remaining in lot after rent
                        lot1_cars = max(lot1_cars-l1_req, 0)
                        lot2_cars = max(lot2_cars-l2_req, 0)
                        
                        # cars in lot after returns
                        lot1_cars = int(min(lot1_cars+l1_ret, self.max_cars))
                        lot2_cars = int(min(lot2_cars+l2_ret, self.max_cars))
                        
                        prob = preq1*preq2*pret1*pret2
                        
                        sum_ += prob*(rents*self.cars_rent_prof + self.gamma*self.V[lot1_cars][lot2_cars])
        return(sum_)
        
    def __init__(self, gamma=0.9, theta=1e-9, reql1=3, reql2=4, retl1=3, retl2=2, method="PI"):
        
        self.gamma = gamma
        self.theta = theta
        self.reql1 = reql1
        self.reql2 = reql2    
        self.retl1 = retl1
        self.retl2 = retl2    
        p = 0
        while(self.poisson_probability(p, reql1)>0.01):
            p+=1
        # print(p)
        self.req_bound1 = p
        
        p = 0
        while(self.poisson_probability(p, reql2)>0.01):
            p+=1
        # print(p)
        self.req_bound2 = p
        
        while(self.poisson_probability(p, retl1)>0.01):
            p+=1
        # print(p)
        self.ret_bound1 = p
        
        p = 0
        while(self.poisson_probability(p, retl2)>0.01):
            p+=1
        # print(p)
        self.ret_bound2 = p
        
        # self.max_cars = 20
        self.max_cars = 10
        # self.max_cars_move = 5
        self.max_cars_move = 2
        self.cars_move_cost = 2
        self.cars_rent_prof = 10
        self.parking = 10
        
        self.A = np.arange(-self.max_cars_move, self.max_cars_move+1)
        self.S = []
        self.V = []
        self.V_ = []
        self.P = []
        for x in range(self.max_cars+1):
            self.V.append([])
            self.V_.append([])
            self.P.append([])
            for y in range(self.max_cars+1):
                self.S.append([x, y])
                self.V[x].append(0.0)
                self.V_[x].append(0.0)
                self.P[x].append(0.0)
        
        while True:
            
            # Policy Evaluation
            while True:
                Delta  = 0
                for c1, c2 in self.S:
                    v = self.V[c1][c2]
                    self.V[c1][c2] = self.calcProf([c1, c2], self.P[c1][c2])
                    Delta = max(Delta, np.abs(self.V[c1][c2] - v))
                
                print(Delta)
                if Delta < self.theta:
                    print(self.V)
                    print(self.P)
                    print(Delta)
                    break
            
            # Policy Improvement
            policy_stable = True
            for c1,c2 in self.S:
                max_val = -float("inf")
                best_action = -2
                for a in self.A:
                    if a>=0 and c1>=a:
                        # if there are enough cars in lot 1
                        temp = self.calcProf([c1, c2], a)
                    elif a<0 and c2>=(-a):
                        # if there are enough cars in lot 2
                        temp = self.calcProf([c1, c2], a)
                    else:
                        temp = -float("inf")
                    if temp > max_val:
                        max_val = temp
                        best_action = a
                print([c1, c2, best_action, max_val])
                if self.P[c1][c2]!= best_action:
                    self.P[c1][c2] = best_action
                    policy_stable = False
            if policy_stable:
                print(self.V)
                print(self.P)
                exit()
            
            
                    
if __name__ =="__main__":
    # Gambler(gamma=0.9, theta=1e-9, pheads=.4)
    Cars(gamma=0.9, theta=1e-3, reql1=3, reql2=4, retl1=3, retl2=2, method="PI")
    # Cars(gamma=0.9, theta=1e-3, reql1=1, reql2=2, retl1=1, retl2=1, method="PI")
