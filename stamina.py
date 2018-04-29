'''
Stamina.py by Eryk Banatt


TODO:

you fixed this but you should link it in the links page this month because it was helpful
http://docs.python-guide.org/en/latest/writing/gotchas/

explore seeds for tournament 2
explore difficulty rating in typical brackets and in actual brackets
clean up shit, make sure its all good and readable
      figure out wtf you did with the arrays and make constants that make it legible
      make this all readable so you can embed it in the actual writeup and have the code be relatively clean
'''

import numpy as np
from collections import Counter
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from functions import *

#GLOBAL CONSTANTS
WINNERS_WINS = 0
WINNERS_LOSSES = 1
LOSERS_WINS = 2
LOSERS_LOSSES = 3

### Tournaments

## Tournaments only currently work for powers of 2 (just use 64)

# Runs a Single Elimination Tournamement
#       output: winning players match record,
#                       every rounds winning picks,
#                       every rounds losing picks
def single_elim(n, playerlist, matchhistory, raw_values=True):

        roundhistory = [{}, {}, {}, {}]

        if(n == 1):
                winner_sum = 0
                for x in playerlist[n].record: winner_sum += x.keys()[0]
                return playerlist[n].record, matchhistory, winner_sum
        else:
                for x in range(0,n/2):
                        single_match(playerlist, x+1, n-x, matchhistory, roundhistory, 1, raw_values)

                matchhistory[WINNERS_WINS].append(roundhistory[WINNERS_WINS])
                matchhistory[WINNERS_LOSSES].append(roundhistory[WINNERS_LOSSES])

                return single_elim(n/2, playerlist, matchhistory, raw_values)

# in process of being rewritten for readability
def double_elim(n, playerlist, matchhistory, rnd, raw_values=True):

        # dicts containing what occurs during this round
        roundhistory = [{}, {}, {}, {}]

        if(n == 1):
                #Grand Finals set 1
                bracket_L_bracket = playerlist[n+1].seed
                single_match(playerlist, 2, 1, matchhistory, roundhistory, 1, raw_values)

                #Grand Finals set 2
                if playerlist[n+1].seed != bracket_L_bracket:
                        single_match(playerlist, 2, 1, matchhistory, roundhistory, 1, raw_values)

                #sum points spent
                winner_sum = 0
                for x in playerlist[n].record: #winners
                        if(x != {}): winner_sum += x.keys()[0]
                for x in playerlist[n].record_L: #losers
                        if(x != {}): winner_sum += x.keys()[0]

                #return victory information, please consolidate
                return playerlist[n].record, playerlist[n].record_L, matchhistory, winner_sum
        else:
                #winners bracket
                for x in range(0,n/2):
                        single_match(playerlist, x+1, n-x, matchhistory, roundhistory, 1, raw_values)

                matchhistory[WINNERS_WINS].append(roundhistory[WINNERS_WINS])
                matchhistory[WINNERS_LOSSES].append(roundhistory[WINNERS_LOSSES])

                #losers bracket
                if(rnd == 0):
                        #losers vs losers
                        for x in range(n/2, 3*n/4):
                                single_match(playerlist, x+1,
                                             ((3*n)/2)-x, matchhistory,
                                             roundhistory, 3, raw_values)

                        matchhistory[LOSERS_WINS].append(roundhistory[LOSERS_WINS])
                        matchhistory[LOSERS_LOSSES].append(roundhistory[LOSERS_LOSSES])

                else:
                        #winners vs losers
                        for x in range(n/2, n):
                                single_match(playerlist, x+1, (2*n)-x,
                                             matchhistory, roundhistory, 2,
                                             raw_values)

                        matchhistory[LOSERS_WINS].append(roundhistory[LOSERS_WINS])
                        matchhistory[LOSERS_LOSSES].append(roundhistory[LOSERS_LOSSES])

                        #losers vs losers
                        for x in range(n/2, 3*n/4):
                                single_match(playerlist, x+1,
                                             ((3*n)/2)-x, matchhistory,
                                             roundhistory, 3, raw_values)

                        matchhistory[LOSERS_WINS].append(roundhistory[LOSERS_WINS])
                        matchhistory[LOSERS_LOSSES].append(roundhistory[LOSERS_LOSSES])

                return double_elim(n/2, playerlist, matchhistory, rnd+1, raw_values)

# Runs a single match between two players
def single_match(playerlist, firstplayer, secondplayer, matchhistory, roundhistory, ratio = 1, raw_values=True):

        # Generates roll for each player
        #       (could I make this shorter?)
        try:
                p1_roll = np.random.randint(0, playerlist[firstplayer].stam + 1)
        except ValueError: #np.random.randint(0, 0) returns an error instead of 0
                p1_roll = 0
        try:
                p2_roll = np.random.randint(0, playerlist[secondplayer].stam + 1)
        except ValueError:
                p2_roll = 0

        ## Rolls saved in each player's record
        p1rec = {}
        p2rec = {}

        # Raw Values or Percentages
        if raw_values:
                p1rec[p1_roll] = 1
                p2rec[p2_roll] = 1
        else:
                p1rec[pctof(p1_roll, playerlist[firstplayer].stam)] = 1
                p2rec[pctof(p2_roll, playerlist[secondplayer].stam)] = 1

        #hackathony way to save these to the correct dict to the correct spot
        phase_rec1 = [{}, {}]
        phase_rec2 = [{}, {}]

        #Place this round into the correct index        
        phase_rec1[min(ratio-1, 1)] = p1rec
        phase_rec2[min(ratio-1, 1)] = p2rec

        #Updates winning and losing records:
        #       if it's in winners, it publishes the result into their winners record, and a blank dict for phase 1 of the losers record
        #               since losing in winners places you into losers phase 2, and you'll never reach losers phase 1
        #       if it's in losers phase 1, it publishes a blank dict into the winners record for record keeping purposes, and the result
        #               into their losers record
        #       if it's in losers phase 2, it publishes just the result into their losers record, since the winners dict for this round
        #               was already included in either the winners phase or the losers phase 1
        if(ratio in [1, 2]):
                playerlist[firstplayer].record.append(phase_rec1[0])
                playerlist[secondplayer].record.append(phase_rec2[0])
                playerlist[firstplayer].record_L.append(phase_rec1[1])
                playerlist[secondplayer].record_L.append(phase_rec2[1])

        # Evaluate which player won
        if(p1_roll < p2_roll): # P2 wins, swaps IDs
                swapPlayersInDict(playerlist[firstplayer], playerlist[secondplayer], playerlist)
                winroll = p2_roll
                loseroll = p1_roll
        elif(p1_roll == p2_roll): # Tie, Randomly decided
                winner = np.random.rand()
                if(winner > .5):
                        winroll = p1_roll
                        loseroll = p2_roll
                else: #P2 wins requires swap
                        swapPlayersInDict(playerlist[firstplayer], playerlist[secondplayer], playerlist)
                        winroll = p2_roll
                        loseroll = p1_roll
        else: #P1 wins, no swaps
                winroll = p1_roll
                loseroll = p2_roll

        # if it's in winners, the winner will never enter that round's losers phase 2, so a blank dict is appended to only that player
        if(ratio is 1): playerlist[firstplayer].record_L.append(phase_rec1[1])

        ## Add winning roll to win record
        #       winner will always be x+1 due to swaps
        #       adds to x_round if in winners, adds to x_round_L if in losers
        if(ratio is 1):
                add_to_recordbook(roundhistory[WINNERS_WINS], winroll, playerlist, firstplayer, raw_values)
                add_to_recordbook(roundhistory[WINNERS_LOSSES], loseroll, playerlist, secondplayer, raw_values)
        else:
                add_to_recordbook(roundhistory[LOSERS_WINS], winroll, playerlist, firstplayer, raw_values)
                add_to_recordbook(roundhistory[LOSERS_LOSSES], loseroll, playerlist, secondplayer, raw_values)

        # Deduct spent stamina from winner
        playerlist[firstplayer].stam -= winroll

        # Deduct spent stamina from loser
        playerlist[secondplayer].stam -= loseroll

#Simulated Tournaments, temporarily broken for single elim
def tournament(variant, simulations=100000, raw_values=True, PLAYERS=64):

        playerlist = {}

        # These are lists of dictionaries, one dictionary per round
        # each round win/lose_round odds updates n/2 times (each)
        # each tournament win_tournament updates x times where x = matches played by round
        # each round
        # and losers variants
        # I wanna consolidate this later into an array with multiple indices to look nicer but this works for now
        allrounds = [[], [], [], [], [], [], [], []]
        all_winners = []

        # "Zero out" lists ((needs to be slightly adjusted for double elim))
        for z in range(0, int(np.log2(PLAYERS))): # number of stages in an elim tournament is repeated div by 2
                for a in allrounds: a.append({})
                for y in range(4, 8):
                        allrounds[y].append({})
                        allrounds[y].append({})

        #Simulations
        for x in range(0, simulations):

                # reroll points for random assign every simulation
                if(variant in [1, 3]):
                        roll_points_uniform(PLAYERS, playerlist)
                else:
                        roll_points_normal(PLAYERS, playerlist)

                if(variant <= 2): #1-2: Single Elim Variants
                        winner, roundhistory, winner_sum = single_elim(PLAYERS, playerlist, [[], [], [], []], raw_values)
                else: #3-4: Double Elim Variants
                        winner, winner_L, roundhistory, winner_sum = double_elim(PLAYERS, playerlist, [[], [], [], []], 0, raw_values)

                playerlist = {} # Erase list of players to reroll

                # Add tournament info to collections of data

                
                for new, old in zip(roundhistory, allrounds):
                    incorporate(new, old)
                incorporate(winner, allrounds[6])
                if (variant > 2): incorporate(winner_L, allrounds[7])
                        
                all_winners.append(winner_sum)

        return allrounds, all_winners

# Sort of niche function to generate a plot of the top of the normal distribution for successively larger tournaments
#       more mainfile-ish code but I want to refer back to it later without deleting it
def find_max_densities(variant, power, sims=10000, raw_values=True):
        tops = []
        for x in range(1, power+1):
                print x
                players = 2 ** x
                W, WR, LR, WS = tournament(variant, sims, raw_values, players)
                tops.append(max(WS, key=WS.count))
        return tops
