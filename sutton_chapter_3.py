from __future__ import print_function
import numpy as np
import matplotlib as plt
import random
import math


class GridWorldState:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.prob = {"NORTH":0.25, "EAST":0.25, "SOUTH":0.25, "WEST":0.25}
        self.reward = {}
        self.move = {}
        self.terminal = False
        self.special = False
        
        if self.y==0:
            self.reward["NORTH"] = -1.0
            self.move["NORTH"] = [self.x, self.y]
        else:
            self.reward["NORTH"] = 0.0
            self.move["NORTH"] = [self.x, self.y-1]
            
        if self.y==size-1 :
            self.reward["SOUTH"] = -1.0
            self.move["SOUTH"] = [self.x, self.y]
        else:
            self.reward["SOUTH"] = 0.0
            self.move["SOUTH"] = [self.x, self.y+1]
        
        if self.x==0:
            self.reward["WEST"] = -1.0
            self.move["WEST"] = [self.x, self.y]
        else:
            self.reward["WEST"] = 0.0
            self.move["WEST"] = [self.x-1, self.y]
            
        if self.x==size-1 :
            self.reward["EAST"] = -1.0
            self.move["EAST"] = [self.x, self.y]
        else:
            self.reward["EAST"] = 0.0
            self.move["EAST"] = [self.x+1, self.y]
            
        
class MDPTestbed:
        
    def __init__(self, gamma=0.9, iterations=1000, error = 1e-5, size = 5, random=False, optimal=False):
        self.gamma = gamma
        self.iterations = iterations
        self.error = error
        self.size = size
        self.random = random
        self.optimal = optimal
        self.gridworld = [[GridWorldState(0, 0 ,0) for x in range(size)] for y in range(size)]
        self.actions = {"NORTH":0, "EAST":1, "SOUTH":2, "WEST":3}
        
        for x in range(size):
            for y in range(size):
                self.gridworld[x][y] = GridWorldState(x, y, size)
                
        self.gridworld[0][1].reward = {"NORTH":10.0, "EAST":10.0, "SOUTH":10.0, "WEST":10.0}
        self.gridworld[0][1].move = {"NORTH":[self.gridworld[0][1].x, size-1], "EAST":[self.gridworld[0][1].x, size-1], "SOUTH":[self.gridworld[0][1].x, size-1], "WEST":[self.gridworld[0][1].x, size-1]}
        self.gridworld[0][3].reward = {"NORTH":5.0, "EAST":5.0, "SOUTH":5.0, "WEST":5.0}
        self.gridworld[0][3].move = {"NORTH":[self.gridworld[0][3].x, 2], "EAST":[self.gridworld[0][3].x, 2], "SOUTH":[self.gridworld[0][3].x, 2], "WEST":[self.gridworld[0][3].x, 2]}
        
        init_values = np.zeros((self.size,self.size))
        
        if self.random:
            print("Random Policy - Error Threshold")
            while True:
                values = np.zeros((self.size, self.size))
                for x in range(self.size):
                    for y in range(self.size):
                        for ac in self.actions:
                            new_pos = self.gridworld[x][y].move[ac]
                            # print("["+str(self.gridworld[x][y].x)+", "+str(self.gridworld[x][y].y)+"] -->" +ac+"--> "+str(new_pos)+" "+str(self.gridworld[x][y].reward[ac]))
                            # print("----------------")
                            values[x][y] += self.gridworld[x][y].prob[ac] * (self.gridworld[x][y].reward[ac] + self.gamma*init_values[new_pos[0]][new_pos[1]])
                sum_ = np.sum(np.abs(init_values - values))
                if(sum_ < self.error) or (math.isnan(sum_)):
                    print(values)
                    break
                init_values = values
            return
        
        if not self.optimal:
            print("Random Policy - Iterations")
            for i in range(self.iterations):
                values = np.zeros((self.size, self.size))
                for x in range(self.size):
                    for y in range(self.size):
                        for ac in self.actions:
                            new_pos = self.gridworld[x][y].move[ac]
                            # print("["+str(self.gridworld[x][y].x)+", "+str(self.gridworld[x][y].y)+"] -->" +ac+"--> "+str(new_pos)+" "+str(self.gridworld[x][y].reward[ac]))
                            # print("----------------")
                            values[x][y] += self.gridworld[x][y].prob[ac] * (self.gridworld[x][y].reward[ac] + self.gamma*init_values[new_pos[0]][new_pos[1]])
                sum_ = np.sum(np.abs(init_values - values))
                if(sum_ < self.error) or (math.isnan(sum_)):
                    print(values)
                    print("Iteration " +str(i))
                    return
                init_values = values
            print(values)
            print("Iteration " +str(i))
            return
            
        if self.optimal:
            print("Optimal Policy")
            for i in range(self.iterations):
                values = np.zeros((self.size, self.size))
                for x in range(self.size):
                    for y in range(self.size):
                        max_val = -9999999
                        for ac in self.actions:
                            new_pos = self.gridworld[x][y].move[ac]
                            # print("["+str(self.gridworld[x][y].x)+", "+str(self.gridworld[x][y].y)+"] -->" +ac+"--> "+str(new_pos)+" "+str(self.gridworld[x][y].reward[ac]))
                            # print("----------------")
                            cur_val = self.gridworld[x][y].reward[ac] + self.gamma*init_values[new_pos[0]][new_pos[1]]
                            if cur_val > max_val:
                                max_val = cur_val
                        values[x][y] = max_val
                sum_ = np.sum(np.abs(init_values - values))
                if(sum_ < self.error) or (math.isnan(sum_)):
                    print(values)
                    print("Iteration " +str(i))
                    return
                init_values = values
            return
            
if __name__ =="__main__":
    MDPTestbed(0.9, 1000, 1e-6, 5, True, False)
    MDPTestbed(0.9, 1000, 1e-6, 5, False, False)
    MDPTestbed(0.9, 1000, 1e-6, 5, False, True)
