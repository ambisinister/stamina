'''
Stamina.py by Eryk Banatt


TODO:

rewrite single_match to work for both single and double elim
explore seeds for tournament 2

'''

import numpy as np
from collections import Counter
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from functions import *

### Tournaments

## Tournaments only currently work for powers of 2 (just use 64)

# Runs a Single Elimination tournament
# 	output: winning players match record, 
#			every rounds winning picks, 
#			every rounds losing picks
def single_elim(n, playerlist, wins=[], losses=[], raw_values=True):

	win_round = {}
	lose_round = {}

	if(n == 1):
		all_enters = []
		winner_sum = 0
		for x in playerlist[n].record: winner_sum += x.keys()[0]
		return playerlist[n].record, wins, losses, winner_sum
	else:
		for x in range(0,n/2):
			single_match(playerlist, n, x, wins, losses, win_round, lose_round, raw_values)

		wins.append(win_round)
		losses.append(lose_round)

		return single_elim(n/2, playerlist, wins, losses, raw_values)

# as far as I can tell this is actually completed, but still doesn't work because the single_match logic doesn't
def double_elim(n, playerlist, wins=[], losses=[], rnd=0, raw_values=True):
	if(n == 1):
		all_enters = []
		winner_sum = 0
		for x in playerlist[n].record: winner_sum += x.keys()[0]
		return playerlist[n].record, wins, losses, winner_sum
	else:
		#winners bracket
		for x in range(0,n/2):
			single_match(playerlist, n, x, wins, losses, raw_values)
		#losers bracket
		if(rnd == 0):
			#losers vs losers
			for x in range(n/2, 3*n/4):
				single_match(playerlist, n, x, wins, losses, raw_values)
		else:
			#winners vs losers
			for x in range(n/2, n):
				single_match(playerlist, n, x, wins, losses, raw_values)

			#losers vs losers
			for x in range(n/2, 3*n/4):
				single_match(playerlist, n, x, wins, losses, raw_values)
		double_elim(n/2, playerlist, wins, losses, rnd+1, raw_values)

# Stuck working for single_elim
# Consult double elim paircheck and see if there's a clever way to pass a value
def single_match(playerlist, n, x, wins, losses, win_round, lose_round, raw_values):
	#print("{} vs {}".format(playerlist[x+1].ID, playerlist[n-x].ID))
	try:
		p1_roll = np.random.randint(0, playerlist[x+1].stam + 1)
	except ValueError: #np.random.randint(0, 0) returns an error instead of 0
		p1_roll = 0

	try:
		p2_roll = np.random.randint(0, playerlist[n-x].stam + 1)
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
		p1rec[pctof(p1_roll, playerlist[x+1].stam)] = 1
		p2rec[pctof(p2_roll, playerlist[n-x].stam)] = 1

	playerlist[x+1].record.append(p1rec)
	playerlist[n-x].record.append(p2rec)

	# Evaluate which player won
	if(p1_roll < p2_roll): # P2 wins, swaps IDs
		swapPlayersInDict(playerlist[x+1], playerlist[n-x], playerlist)
		winroll = p2_roll
		loseroll = p1_roll
	elif(p1_roll == p2_roll): # Tie, Randomly decided
		winner = np.random.rand()
		if(winner > .5): # I suppose this is still infinitesimally weighted towards p2 but whatever 
			winroll = p1_roll
			loseroll = p2_roll
		else: #P2 wins requires swap
			swapPlayersInDict(playerlist[x+1], playerlist[n-x], playerlist)
			winroll = p2_roll
			loseroll = p1_roll
	else: #P1 wins, no swaps
		winroll = p1_roll
		loseroll = p2_roll

	## Add winning roll to win record (winner will always be x+1 due to swaps)
	# Raw Values or Percentages
	if raw_values == 1:
		if(winroll in win_round): win_round[winroll] += 1
		else: win_round[winroll] = 1
	else:
		pctofwinroll = pctof(winroll, playerlist[x+1].stam)
		if(pctofwinroll in win_round): win_round[pctofwinroll] += 1
		else: win_round[pctofwinroll] = 1

	# Add losing roll to loss record
	# Raw Values or Percentages
	if raw_values:
		if(loseroll in lose_round): lose_round[loseroll] += 1
		else: lose_round[loseroll] = 1
	else:
		pctofloseroll = pctof(loseroll, playerlist[n-x].stam)
		if(pctofloseroll in lose_round): lose_round[pctofloseroll] += 1
		else: lose_round[pctofloseroll] = 1

	# Deduct spent stamina from winner 
	playerlist[x+1].stam -= winroll

#Simulated Tournaments
def tournament(variant, simulations=100000, raw_values=True, PLAYERS=64):

	playerlist = {}

	# These are lists of dictionaries, one dictionary per round
	# each round win/lose_round odds updates n/2 times (each)
	# each tournament win_tournament updates x times where x = matches played by round
	# each round 
	win_tournament_by_round = []
	win_round_by_round = []
	lose_tournament_by_round = []
	lose_round_by_round = []
	all_winners = []

	# "Zero out" lists
	if(variant in [1, 2]):
		for z in range(0, int(np.log2(PLAYERS))): # number of stages in single elim is repeated div by 2
			win_tournament_by_round.append({})
			win_round_by_round.append({})
			lose_tournament_by_round.append({})
			lose_round_by_round.append({})
	else:
		for z in range(0, (2*PLAYERS-1)): # number of stages
			win_tournament_by_round.append({})
			win_round_by_round.append({})
			lose_tournament_by_round.append({})
			lose_round_by_round.append({})

	#Simulations
	for x in range(0, simulations):

		# reroll points for random assign every simulation
		if(variant in [1, 3]):
			roll_points_uniform(PLAYERS, playerlist)
		else:
			roll_points_normal(PLAYERS, playerlist)
			
		if(variant <= 2): #1-2: Single Elim Variants
			# ok real talk I have no clue why this fixed the problem, something to look into
			winner, roundwin, roundlose, winner_sum = single_elim(PLAYERS, playerlist, [], [], raw_values)
		else: #3-4: Double Elim Variants
			winner, roundwin, roundlose, winner_sum = double_elim(PLAYERS, playerlist, [], [], raw_values)

		playerlist = {} # Erase list of players to reroll

		# Add tournament info to collections of data
		incorporate(winner, win_tournament_by_round)
		incorporate(roundwin, win_round_by_round)
		incorporate(roundlose, lose_round_by_round)
		all_winners.append(winner_sum)

	return win_tournament_by_round, win_round_by_round, lose_round_by_round, all_winners

# Sort of niche function to generate a plot of the top of the normal distribution for successively larger tournaments
# 	more mainfile-ish code but I want to refer back to it later without deleting it
def find_max_densities(variant, power, sims=10000, raw_values=True):
	tops = []
	for x in range(1, power+1):
		print x
		players = 2 ** x
		W, WR, LR, WS = tournament(variant, sims, raw_values, players)
		tops.append(max(WS, key=WS.count))
	return tops