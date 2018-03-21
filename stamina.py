'''
Stamina.py by Eryk Banatt


TODO:

Write RNG RNG function
Write Double Elimination Function
Run all the tournaments
'''

import numpy as np
from collections import Counter
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt

# Each individual player
#	all ints except record, which is a list of dicts
#		record is of format [{15: 1}, {66: 1}, {49: 1}]
class Player:
	def __init__(self, stamina, currentID, OriginalSeed):
		self.stam = stamina
		self.ID = currentID
		self.seed = OriginalSeed
		self.record = []

# Swaps currentID of both players, keeps seed the same
# 	This is used for pairing players even when they get upset
#		(Tested and confirmed working)
def swapPlayersInDict(player1, player2, dic):
	p1_cID = player1.ID
	p2_cID = player2.ID

	dic[p1_cID] = player2
	dic[p2_cID] = player1
	player1.ID = p2_cID
	player2.ID = p1_cID

# Creates n players in playerlist with random, normally distributed stamina values
# 	Will need to be rerolled every simulation, since 64 won't get every value
# 		(tested and looks good)
def roll_points_normal(n, playerlist):
	mu, sigma = 75, 25 #mean 75, SD 25; might need tuning
	sample = np.random.normal(mu, sigma, n)
	sample.sort()
	sample = sample[::-1] # feels gross doing this instead of reverse=True but it's not behaving with numpy
	sample = np.round(sample)

	for x in range(0, n):
		if(sample[x] < 0): sample[x] = 0
		plyr = Player(sample[x], x+1, x+1)
		playerlist[plyr.ID] = plyr

def roll_points_uniform(n, playerlist):
	for x in range(0, n):
		plyr = Player(100, x+1, x+1)
		playerlist[plyr.ID] = plyr

# Takes two lists of dictionaries and adds the first list to the second list
# 	Note that I can't just zip to y.update(x) because that will replace all common
#	values of x and y with the new value, deleting all the previous data
def incorporate(newlist, oldlist):
	for x, y in zip(newlist, oldlist):
		c1 = Counter(x)
		c2 = Counter(y)
		y.update(c1+c2)

# Prepares a dictionary for visualization w/ matplotlib
# 	sorts / puts values into even multidimensional array
#	not very efficient but only used once for a demonstrably small use
def prep_dict_for_viz(borges):
	ar = []

	for rnd in borges:
		ar_rnd = []
		for x in range(0, len(borges[0])):
			if x in rnd:
				ar_rnd.append(rnd[x])
			else:
				ar_rnd.append(0)
		ar.append(ar_rnd)

	return ar

# Plots a 2d array as a 3d surface
def visualize(arr, TL="", XL="Round in Tournament", YL="Points Chosen", ZL=""):
	z = np.transpose(np.array(arr))
	x = range(1, len(arr)+1)
	y = range(len(arr[0]))
	X, Y = np.meshgrid(x, y)
	print arr[0]
	hf = plt.figure()
	ha = hf.gca(projection='3d')
	ha.plot_surface(X, Y ,z,rstride=1,cstride=1, cmap=cm.terrain, 
		linewidth=1, antialiased=False)
	ha.set_title(TL, y=1.08)
	ha.set_xlabel(XL)
	ha.set_ylabel(YL)
	ha.set_zlabel(ZL)

	plt.show()

# adds together two 2d arrays of the same dimensions
#	(works fine)
def combine(a, b):
	c = []
	for x, y in zip(a, b):
		c_temp = []
		for x1, y1 in zip(x, y):
			c_temp.append(x1+y1)
		c.append(c_temp)
	return c

# divide every element by its respective pair in a second array
#
def divout(a, b):
	c = []
	for x, y in zip(a, b):
		c_temp = []
		for x1, y1 in zip(x, y):
			if(y1 == 0):
				c_temp.append(1)
			else:
				c_temp.append(x1 / (y1 * 1.0))
		c.append(c_temp)
	return c

### Tournaments

## Tournaments only currently work for powers of 2 (just use 64)

# Runs a Single Elimination tournament
# 	output: winning players match record, 
#			every rounds winning picks, 
#			every rounds losing picks
def single_elim(n, playerlist, wins=[], losses=[]):

	win_round = {}
	lose_round = {}

	if(n == 1):
		all_enters = []
		return playerlist[n].record, wins, losses
	else:
		for x in range(0,n/2):
			# Both players roll some number between 0 and their current max stamina
			try:
				p1_roll = np.random.randint(0, playerlist[x+1].stam)
			except ValueError: #np.random.randint(0, 0) returns an error instead of 0
				p1_roll = 0

			try:
				p2_roll = np.random.randint(0, playerlist[n-x].stam)
			except ValueError:
				p2_roll = 0

			# Rolls saved in each player's record
			p1rec = {}
			p2rec = {}
			p1rec[p1_roll] = 1
			p2rec[p2_roll] = 1
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
			
			# Deduct spent stamina from winner (will always be x+1 due to swaps)
			playerlist[x+1].stam -= p1_roll

			# Add winning roll to win record
			if(winroll in win_round): win_round[winroll] += 1
			else: win_round[winroll] = 1

			# Add losing roll to loss record
			if(loseroll in lose_round): lose_round[loseroll] += 1
			else: lose_round[loseroll] = 1

		wins.append(win_round)
		losses.append(lose_round)

		return single_elim(n/2, playerlist, wins, losses)


# To Be Written
def double_elim(n, playerlist, wins=[], losses=[]):
	print("nah")


#Simulated Tournaments
def tournament(variant, simulations=10000, PLAYERS=64):

	playerlist = {}

	# These are lists of dictionaries, one dictionary per round
	# each round win/lose_round odds updates n/2 times (each)
	# each tournament win_tournament updates x times where x = matches played by round
	# each round 
	win_tournament_by_round = []
	win_round_by_round = []
	lose_tournament_by_round = []
	lose_round_by_round = []

	# "Zero out" lists
	if(variant in [1, 2, 3, 4]):
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
		if(variant in [1, 3, 5, 7]):
			roll_points_uniform(PLAYERS, playerlist)
		else:
			roll_points_normal(PLAYERS, playerlist)
			
		if(variant <= 4): #1-4: Single Elim Variants
			# ok real talk I have no clue why this fixed the problem, something to look into
			winner, roundwin, roundlose = single_elim(PLAYERS, playerlist, [], [])
		else: #5-8: Double Elim Variants
			winner, roundwin, roundlose = double_elim(PLAYERS, playerlist, [], [])

		playerlist = {} # Erase list of players to reroll

		# Add tournament info to collections of data
		incorporate(winner, win_tournament_by_round)
		incorporate(roundwin, win_round_by_round)
		incorporate(roundlose, lose_round_by_round)

	return win_tournament_by_round, win_round_by_round, lose_round_by_round

win_tourn_raw, win_round_raw, lose_round_raw = tournament(2)

# Simple Helper Function
def prep_batcher(win_tourn_raw, win_round_raw, lose_round_raw):
	win_tourn = prep_dict_for_viz(win_tourn_raw)
	win_round = prep_dict_for_viz(win_round_raw)
	lose_round = prep_dict_for_viz(lose_round_raw)
	aggregate = combine(win_round, lose_round)
	round_prob = divout(win_round, aggregate)
	tourn_prob = divout(win_tourn, aggregate)
	return win_tourn, win_round, lose_round, aggregate, round_prob, tourn_prob

a, b, c, d, e, f = prep_batcher(win_tourn_raw, win_round_raw, lose_round_raw)
visualize(a)

#Basic pairing numbers for single elimination tournaments
def single_elim_paircheck(n):
	if(n == 1):
		print("tournament complete")
	else:
		for x in range(0,n/2):
			print("{} vs {}".format(x+1, n-x))
		single_elim_paircheck(n/2)

#Basic pairing numbers for double elimination tournaments
def double_elim_paircheck(n, round):
	if(n == 1):
		print("tournament complete")
	else:
		#winners bracket
		for x in range(0,n/2):
			print("{} vs {}".format(x+1, n-x))

		print("....")

		#losers bracket
		if(round == 0):
			#losers vs losers
			for x in range(n/2, 3*n/4):
				print("{} vs {}".format(x+1, n-(x-n/2)))
			print("~~~~")
		else:
			#winners vs losers
			for x in range(n/2, n):
				print("{} vs {}".format(x+1, (3*n/2)-(x-(n/2))))
			print("~~~~")

			#losers vs losers
			for x in range(n/2, 3*n/4):
				print("{} vs {}".format(x+1, n-(x-n/2)))
		print("***")
		double_elim(n/2, round+1)