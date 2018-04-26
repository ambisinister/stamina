'''
Stamina.py by Eryk Banatt


TODO:

read this and fix shit
http://docs.python-guide.org/en/latest/writing/gotchas/

explore seeds for tournament 2
explore difficulty rating in typical brackets and in actual brackets
clean up shit, make sure its all good and readable
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
def single_elim(n, playerlist, wins, losses, raw_values=True):

	win_round = {}
	lose_round = {}

	if(n == 1):
		winner_sum = 0
		for x in playerlist[n].record: winner_sum += x.keys()[0]
		return playerlist[n].record, wins, losses, winner_sum
	else:
		for x in range(0,n/2):
			single_match(playerlist, n, x, wins, losses, win_round, lose_round, 1, raw_values)

		wins.append(win_round)
		losses.append(lose_round)

		return single_elim(n/2, playerlist, wins, losses, raw_values)

# as far as I can tell this is actually completed, but still doesn't work because the single_match logic doesn't
def double_elim(n, playerlist, wins, losses, wins_L, losses_L, rnd, raw_values=True):
	#Might be useful to eventually rewrite this to be a list of two dictionaries each, rather than four dicts
	win_round = {}
	lose_round = {}
	win_round_L = {}
	lose_round_L = {}

	if(n == 1):
		#Grand Finals set 1
		bracket_L_bracket = playerlist[n+1].seed
		single_match(playerlist, 2, 0, wins, losses, win_round, lose_round, wins_L, losses_L, win_round_L, lose_round_L, 1, raw_values)
		
		#Grand Finals set 2
		if playerlist[n+1].seed != bracket_L_bracket: 
			single_match(playerlist, 2, 0, wins, losses, win_round, lose_round, wins_L, losses_L, win_round_L, lose_round_L, 1, raw_values)
		
		#sum points spent
		winner_sum = 0
		for x in playerlist[n].record: #winners
			if(x != {}): winner_sum += x.keys()[0]
		for x in playerlist[n].record_L: #losers
			if(x != {}): winner_sum += x.keys()[0]

		#return victory information
		return playerlist[n].record, playerlist[n].record_L, wins, losses, wins_L, losses_L, winner_sum
	else:
		#winners bracket
		for x in range(0,n/2):
			single_match(playerlist, n, x, wins, losses, win_round, lose_round, wins_L, losses_L, win_round_L, lose_round_L, 1, raw_values)
		
		wins.append(win_round)
		losses.append(lose_round)

		#losers bracket
		if(rnd == 0):
			#losers vs losers
			for x in range(n/2, 3*n/4):
				single_match(playerlist, n, x, wins, losses, win_round, lose_round, wins_L, losses_L, win_round_L, lose_round_L, 3, raw_values)
			
			wins_L.append(win_round_L)
			losses_L.append(lose_round_L)
		else:
			#winners vs losers
			for x in range(n/2, n):
				single_match(playerlist, n, x, wins, losses, win_round, lose_round, wins_L, losses_L, win_round_L, lose_round_L, 2, raw_values)
			
			wins_L.append(win_round_L)
			losses_L.append(lose_round_L)

			#losers vs losers
			for x in range(n/2, 3*n/4):
				single_match(playerlist, n, x, wins, losses, win_round, lose_round, wins_L, losses_L, win_round_L, lose_round_L, 3, raw_values)
			
			wins_L.append(win_round_L)
			losses_L.append(lose_round_L)

		return double_elim(n/2, playerlist, wins, losses, wins_L, losses_L, rnd+1, raw_values)

# Works for single elimination, working on getting it working for double elimintation
def single_match(playerlist, n, x, wins, losses, win_round, lose_round, wins_L=[], losses_L=[], win_round_L=[], lose_round_L=[], ratio = 1, raw_values=True):
	#print("{} vs {}".format(playerlist[x+1].ID, playerlist[n-x].ID))
	# Constants for readability
	PHASE_WINNERS = 0
	PHASE_LOSERS = 1
	
	# Create variables to point at correct indicies
	# 	This is gonna be different when I fix the paircheck / double elim params 
	firstplayer = x+1

	if(ratio == 1):
		secondplayer = n-x
		phase = PHASE_WINNERS
	elif(ratio == 2):
		secondplayer = (2*n) - x #fix
		phase = PHASE_LOSERS
	elif(ratio == 3):
		secondplayer = ((3*n)/2) - x
		phase = PHASE_LOSERS
	#secondplayer = ??

	# Generates roll for each player
	# 	(could I make this shorter?)
	try:
		p1_roll = np.random.randint(0, playerlist[firstplayer].stam + 1)
	except ValueError: #np.random.randint(0, 0) returns an error instead of 0
		p1_roll = 0
	except KeyError: #remove me
		print firstplayer
		print secondplayer
		print "a"

	try:
		p2_roll = np.random.randint(0, playerlist[secondplayer].stam + 1)
	except ValueError:
		p2_roll = 0
	except KeyError:
		print firstplayer
		print secondplayer
		print "b"

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
	phase_rec1[phase] = p1rec
	phase_rec2[phase] = p2rec

	#Updates winning and losing records:
	#	if it's in winners, it publishes the result into their winners record, and a blank dict for phase 1 of the losers record
	#		since losing in winners places you into losers phase 2, and you'll never reach losers phase 1
	#	if it's in losers phase 1, it publishes a blank dict into the winners record for record keeping purposes, and the result  
	#		into their losers record
	#	if it's in losers phase 2, it publishes just the result into their losers record, since the winners dict for this round  
	#		was already included in either the winners phase or the losers phase 1 
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
		if(winner > .5): # I suppose this is still infinitesimally weighted towards p2 but whatever 
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
	if(phase == PHASE_WINNERS): playerlist[firstplayer].record_L.append(phase_rec1[1])

	## Add winning roll to win record 
	#	winner will always be x+1 due to swaps
	#	adds to x_round if in winners, adds to x_round_L if in losers
	if(phase == PHASE_WINNERS):
		add_to_recordbook(win_round, winroll, playerlist, firstplayer, raw_values)
		add_to_recordbook(lose_round, loseroll, playerlist, secondplayer, raw_values)
	else:
		add_to_recordbook(win_round_L, winroll, playerlist, firstplayer, raw_values)
		add_to_recordbook(lose_round_L, loseroll, playerlist, secondplayer, raw_values)

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
	win_tournament_by_round = []
	win_round_by_round = []
	lose_tournament_by_round = []
	lose_round_by_round = []

	win_tournament_by_round_L = []
	win_round_by_round_L = []
	lose_tournament_by_round_L = []
	lose_round_by_round_L = []

	all_winners = []

	# "Zero out" lists ((needs to be slightly adjusted for double elim))
	for z in range(0, int(np.log2(PLAYERS))): # number of stages in an elim tournament is repeated div by 2
		win_tournament_by_round.append({})
		win_round_by_round.append({})
		lose_tournament_by_round.append({})
		lose_round_by_round.append({})

		for y in range(0, 2):
			win_tournament_by_round_L.append({})
			win_round_by_round_L.append({})
			lose_tournament_by_round_L.append({})
			lose_round_by_round_L.append({})

	#Simulations
	for x in range(0, simulations):

		# reroll points for random assign every simulation
		if(variant in [1, 3]):
			roll_points_uniform(PLAYERS, playerlist)
		else:
			roll_points_normal(PLAYERS, playerlist)
			
		if(variant <= 2): #1-2: Single Elim Variants
			winner, roundwin, roundlose, winner_sum = single_elim(PLAYERS, playerlist, [], [], raw_values)
		else: #3-4: Double Elim Variants
			winner, winner_L, roundwin, roundlose, roundwin_L, roundlose_L, winner_sum = double_elim(PLAYERS, playerlist, [], [], [], [], 0, raw_values)

		playerlist = {} # Erase list of players to reroll

		# Add tournament info to collections of data
		incorporate(winner, win_tournament_by_round)
		incorporate(roundwin, win_round_by_round)
		incorporate(roundlose, lose_round_by_round)
		# Need these to only happen in double elim lmao
		if (variant > 2):
			incorporate(winner_L, win_tournament_by_round_L)
			incorporate(roundwin_L, win_round_by_round_L)
			incorporate(roundlose_L, lose_round_by_round_L)
		all_winners.append(winner_sum)

	return win_tournament_by_round, win_round_by_round, lose_round_by_round, win_tournament_by_round_L, win_round_by_round_L, lose_round_by_round_L, all_winners

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