from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from mpl_toolkits.mplot3d import Axes3D

figureIndex = 0
def prettyPrint(data, tile, zlabel='reward'):
    global figureIndex
    fig = plt.figure(figureIndex)
    figureIndex += 1
    fig.suptitle(tile)
    ax = fig.add_subplot(111, projection='3d')
    axisX = []
    axisY = []
    axisZ = []
    for i in range(12, 22):
        for j in range(1, 11):
            axisX.append(i)
            axisY.append(j)
            axisZ.append(data[i - 12, j - 1])
    ax.scatter(axisX, axisY, axisZ)
    ax.set_xlabel('player sum')
    ax.set_ylabel('dealer showing')
    ax.set_zlabel(zlabel)
    
class Deck:
    def draw(self):
        return (random.choice(self.cards))
        
    def __init__(self):
        self.cards = []
        for i in range(1, 11):
            self.cards.append(i)
            self.cards.append(i)
            self.cards.append(i)
            self.cards.append(i)
        for i in range(3):
            self.cards.append(10)
            self.cards.append(10)
            self.cards.append(10)
        
class Player:
    
    def has_usable_ace(self):
        if self.sum > 21 and self.aces>0:
            return True
        return False
        
    def draw(self, deck):
        card = deck.draw()
        if card == 1:
            self.aces +=1
        else:
            self.sum += card
        return card
            
    def c_safe_sum(self):
        self.safe_sum = self.sum + self.aces*11
        if(self.safe_sum > 21):
            for i in range(self.aces):
                self.safe_sum -= 10
                if self.safe_sum<21 :
                    break
        return self.safe_sum
             
    @classmethod
    def empty(pl, dealer=False):
        pl = Player(dealer)
    
    @classmethod
    def fromState(pl, aces, sum, dealer=False):
        pl = Player(dealer)
        pl.aces = aces
        pl.sum = sum
        
    def __init__(self, dealer=False):
        self.dealer = dealer
        self.sum = 0
        self.aces = 0
        self.safe_sum = 0
        self.trajectory = []
        
class BlackJack:
    
    def play(self, pp, dp):
        while not self.isOver():
            if self.game_round(pp, dp) == 0:
                break
            self.status()
        print(str(self.player.c_safe_sum())+" "+str(self.dealer.c_safe_sum())+" "+str(self.winner))
            
    def isOver(self):
        if self.player.aces==1 and self.player.sum==10:
            if self.dealer.aces==1 and self.dealer.sum==10:
                print("Draw")
                self.winner = 0
            else:
                print("Player Wins")
                self.winner = 1
            return True
        if self.dealer.c_safe_sum == 21:
            print("Dealer Wins")
            self.winner = -1
            return True
            
        if self.player.c_safe_sum() > 21:
            self.winner = -1
            print("Dealer Wins")
            return True
            
        if self.dealer.c_safe_sum() > 21:
            self.winner = 1
            print("Player Wins")
            return True
    
    def status(self):
        print("---------")
        print(str(self.p_sum)+" "+str(self.p_aces)+" "+str(self.d_show)+" "+str(self.init_action))
        print("Player ["+str(self.player.sum)+","+str(self.player.aces)+","+str(self.player.c_safe_sum())+"]")
        print("Dealer ["+str(self.dealer.sum)+","+str(self.dealer.aces)+","+str(self.dealer.c_safe_sum())+"]")
        print(self.player.trajectory)
        
    def game_round(self, pp, dp):
        draws = 0
        
        while True:
            if self.init_action == 0:
                self.init_action = -1
                print("Player Draws "+str(self.player.draw(self.deck)))
                self.player.trajectory.append(1)
                draws += 1
            elif self.init_action == 1:
                self.init_action = -1
                print("Player Stands")
                self.player.trajectory.append(0)
                break
            else:
                if pp[self.player.c_safe_sum()] == 1:
                    print("Player Draws "+str(self.player.draw(self.deck)))
                    self.player.trajectory.append(1)
                    draws += 1
                else:
                    # pass
                    print("Player Stands")
                    self.player.trajectory.append(0)
                    break
            if self.player.c_safe_sum() > 21:
                print("Player Busts, Dealer Wins")
                self.winner = -1
                return 0
        
        while True:    
            if dp[self.dealer.c_safe_sum()] == 1:
                print("Dealer Draws "+str(self.dealer.draw(self.deck)))
                draws += 1
            else:
                print("Dealer Stands")
                break
            if self.dealer.c_safe_sum() > 21:
                print("Dealer Busts, Player Wins")
                self.winner = -1
                return 0
            
        
        if(self.player.c_safe_sum() > self.dealer.c_safe_sum()):
            print("Player Wins")
            self.winner = 1
        elif(self.player.c_safe_sum() < self.dealer.c_safe_sum()):
            print("Dealer Wins")
            self.winner = -1
        else:
            print("Draw")
            self.winner = 0
        return 0
            
    def __init__(self, p_sum=-1, p_aces=-1, d_show=-1, init_action=-1):
        self.winner = 0
        self.player = Player(False)
        self.dealer = Player(True)
        self.deck = Deck()
        self.showed = 0
        self.p_sum = p_sum
        self.p_aces = p_aces
        self.d_show = d_show
        self.init_action = init_action
        
        if d_show == -1:
            self.dealer.draw(self.deck) 
            if self.dealer.aces == 1:
                self.showed = 1
            else:
                self.showed = self.dealer.sum
            self.dealer.draw(self.deck)
        else:
            self.showed = d_show
            if d_show == 1:
                self.dealer.aces += 1
            else:
                self.dealer.sum += d_show
        
        self.dealer.c_safe_sum()
        
        if p_sum ==-1:
            self.player.draw(self.deck)
            self.player.draw(self.deck)
        else:
            self.player.sum = p_sum
            self.player.aces = p_aces
            if(p_aces == 1) and (p_sum == 12):
                self.player.aces = 2
                self.player.sum = 0
        self.player.c_safe_sum()
            

    
class BlackJackMC:
    # state variables:
    # player sum: player's total sum (the lowest is two twos, 4-21) (17 possible values))
    # dealer shown: the first card the dealer draws, 1-10 (10 possible values)
    # usable ace: player has an ace he can use (2 possible values)
    # actions:
    # 1/0 : draw/stand (2 possible values)
    def MCFirstVisit(self, ep, pp, dp):
        pass
    
    def MCExploringStarts(self, ep, pp, dp):
        Qvalues = np.zeros((18, 10, 2, 2))
        Qcount = np.ones((18, 10, 2, 2))
        player_wins = 0 
        dealer_wins = 0 
        draws = 0 
        for i in range(ep):
            # initial state
            game = BlackJack(p_sum=random.randint(4, 21), 
            p_aces=random.randint(0, 1), d_show=random.randint(1, 10))
            game.init_action = random.randint(0, 1)
            game.play(pp, dp)
            if game.winner==1:
                player_wins += 1
            elif game.winner==-1:
                dealer_wins +=1
            else:
                draws+=1
            print(game.status())
            print("----------------")
            for ac in game.player.trajectory:
                Qvalues[game.p_sum-4][game.d_show-1][game.p_aces][ac] += game.winner
                Qcount[game.p_sum-4][game.d_show-1][game.p_aces][ac] += 1
        print(str(player_wins)+" Player Wins")
        print(str(dealer_wins)+" Dealer Wins")
        print(str(draws)+" Draws")
        
        valueAce = np.zeros((18,10))
        actionAce = np.zeros((18, 10), dtype='int')
        
        valueNoAce = np.zeros((18,10))
        actionNoAce = np.zeros((18, 10), dtype='int')
        
        # print(Qvalues/Qcount)
        for i in range(18):
            for j in range(10):
                valueAce[i, j] = np.max(Qvalues[i, j, 1, :])
                actionAce[i, j] = np.argmax(Qvalues[i, j, 1, :])
                valueNoAce[i, j] = np.max(Qvalues[i, j, 0, :])
                actionNoAce[i, j] = np.argmax(Qvalues[i, j, 0, :])
        print(actionAce)
    
    def MCOnPolicyFirstVisit(self, ep, pp, dp):
        Qvalues = np.zeros((18, 10, 2))
        Qcount = np.ones((18, 10, 2))
        player_wins = 0 
        dealer_wins = 0 
        draws = 0
        aceRet = np.zeros((18, 10))
        aceRetCount = np.ones((18, 10))
        noAceRet = np.zeros((18, 10))
        noAceRetCount = np.ones((18, 10))
        for i in range(ep):
            # initial state
            game = BlackJack(p_sum=random.randint(4, 21), 
            p_aces=random.randint(0, 1), d_show=random.randint(1, 10))
            game.init_action = random.randint(0, 1)
            game.play(pp, dp)
            if game.winner == 1:
                player_wins += 1
            elif game.winner == -1:
                dealer_wins += 1
            else:
                draws+=1
            print(game.status())
            print("----------------")
            if(game.p_aces==1):
                aceRet[game.p_sum-4, game.d_show-1] += game.winner
                aceRetCount += 1
            else:
                noAceRet[game.p_sum-4, game.d_show-1] += game.winner
                noAceRetCount += 1
        
        
        print(str(player_wins)+" Player Wins")
        print(str(dealer_wins)+" Dealer Wins")
        print(str(draws)+" Draws")
        
        print(aceRet)
        print(noAceRet)
        
    def MCIncrementalOffPolicyEveryVisit(self, ep, pp, dp):
        pass
    
    def __init__(self, episodes, method="FP"):
        player_policy = np.ones(22)
        player_policy[20] = 0
        player_policy[21] = 0
        dealer_policy = np.ones(22)
        dealer_policy[17] = 0
        dealer_policy[18] = 0
        dealer_policy[19] = 0
        dealer_policy[20] = 0
        dealer_policy[21] = 0
        
        
        # self.MCExploringStarts(100000, player_policy, dealer_policy)
        self.MCOnPolicyFirstVisit(500000, player_policy, dealer_policy)
        
if __name__ == "__main__":
    BlackJackMC(500000)
