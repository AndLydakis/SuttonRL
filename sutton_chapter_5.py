from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import random
import math

class Deck:
    def draw(self):
        return (random.choice(self.cards)
        
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
    def draw(self, deck):
        card = deck.draw()
        if card == 1:
            self.aces +=1
        else:
            self.sum +=1
            
    def c_safe_sum(self):
        self.safe_sum = self.sum + self.aces*11
        if(self.safe_sum > 21):
            for i in range(self.aces):
                self.safe_sum -= 10
                if self.safe_sum<21 :
                    break
        return self.safe_sum
                            
    def __init__(self, dealer=False):
        self.dealer = dealer
        self.sum = 0
        self.aces = 0
        self.safe_sum = 0
        
class BlackJack:
    
    def isOver:
        if self.player.aces==1 and self.player.sum==10:
            if self.dealer.aces==1 and self.dealer.sum==10:
                self.winner = 0
            else:
                self.winner = 1
            return True
        if self.player.c_safe_sum() > 21:
            self.winner = -1
            return True
        if self.dealer.c_safe_sum() > 21:
            self.winner = 1
            return True
    
    def game_round(pp, dp):
        draws = 0
        if pp[self.player.c_safe_sum()]==1:
            self.player.draw()
            draws += 1
        if dp[self.dealer.c_safe_sum()]==1:
            self.dealer.draw()
            draws += 1
        if draws == 0:
            self.winner = 0
            return 0
        else:
            return -1
            
    def __init__(self):
        self.winner = 0
        self.player = Player(False)
        self.dealer = Player(True)
        self.deck = Deck()
        self.dealer.draw(deck)
        self.dealer.draw(deck)
        self.player.draw(deck)
        self.player.draw(deck)
        
    
class BlackJackMC:
    def __init__(self, episodes):
        player_policy = ones(22)
        player_policy[20] = 0
        player_policy[21] = 0
        dealer_policy = ones(22)
        dealer_policy[17] = 0
        dealer_policy[18] = 0
        dealer_policy[19] = 0
        dealer_policy[20] = 0
        dealer_policy[21] = 0
        for i in range(episodes):
            game = BlackJack()
            while game not isOver():
                if game.game_round(player_policy, dealer_policy) == 0:
                    break
            print(game.winner)
        
        
if __name__ == "__main__":
    BlackJackMC(1000)
