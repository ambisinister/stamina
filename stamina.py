'''
Stamina.py by Eryk Banatt


TODO:

Test Tournament function, run Tournament 1 test trial 
Write matplotlib animation functions for 3D graphs, test on tournament 1
Write Double Elimination Function
Write probability-to-win function 
Run all the tournaments
'''

import numpy as np
from collections import Counter

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
		plyr = Player(sample[x], x+1, x+1)
		playerlist[plyr.ID] = plyr

# Takes two lists of dictionaries and adds the first list to the second list
# 	Note that I can't just zip to y.update(x) because that will replace all common
#	values of x and y with the new value, deleting all the previous data
def incorporate(newlist, oldlist):
	for x, y in zip(newlist, oldlist):
		c1 = Counter(x)
		c2 = Counter(y)
		y.update(c1+c2)

# Tournaments only currently work for powers of 2, since I'll just be using 64 every time

# Runs a Single Elimination tournament
# 	output: winning players match record, 
#			every rounds winning picks, 
#			every rounds losing picks
def single_elim(n, playerlist, wins=[], losses=[]):

	win_round = {}
	lose_round = {}
	p1rec = {}
	p2rec = {}

	if(n == 1):
		print("tournament complete")
		return playerlist[n].record, wins, losses
	else:
		for x in range(0,n/2):
			print("{} vs {}".format(x+1, n-x))

			# Both players roll some number between 0 and their current max stamina
			p1_roll = np.random.randint(0, playerlist[x+1].stam)
			p2_roll = np.random.randint(0, playerlist[n-x].stam)

			# Rolls saved in each player's record
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
			else #P1 wins, no swaps
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
				
		single_elim(n/2, playerlist, win_round, lose_round)

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

#Simulated Tournaments
def tournament(n, simulations=10000, PLAYERS=64):

	#Generate P players, give them points, place them into a dictionary
	playerlist = {}

	#Tournaments that give 100 points to every player equally
	# Might be nicer as it's own function but it only needs to be called once and saved
	if(n in [1, 3, 5, 7]):
		for x in range(0, n):
			plyr = Player(100, x+1, x+1)
			playerlist[plyr.ID] = plyr
		default_playerlist = playerlist # Saves this profile in a temp variable

	# These are lists of dictionaries, one dictionary per round
	# each round win/lose_round odds updates n/2 times (each)
	# each tournament win_tournament updates x times where x = matches played by round
	# each round 
	win_tournament_by_round = []
	win_round_by_round = []
	lose_tournament_by_round = []
	lose_round_by_round = []

	# "Zero out" lists in single elimination
	if(n in [1, 2, 3, 4]):
		for z in range(0, PLAYERS-1):
			win_tournament_by_round.append({})
			win_round_by_round.append({})
			lose_tournament_by_round.append({})
			lose_round_by_round.append({})
	else:
		for z in range(0, (2*PLAYERS-1)):
			win_tournament_by_round.append({})
			win_round_by_round.append({})
			lose_tournament_by_round.append({})
			lose_round_by_round.append({})


	#Simulations
	for x in range(0, simulations):

		# reroll points for random assign every simulation
		if(n in [2, 4, 6, 8]):
			roll_points_normal(n, playerlist)
			
		if(n >= 4): #1-4: Single Elim Variants
			winner, roundwin, roundlose = single_elim(n, playerlist)
		else: #5-8: Double Elim Variants
			winner, roundwin, roundlose = double_elim(n, playerlist)

		if(n in [1, 3, 5, 7]):
			playerlist = default_playerlist # Keep 100 for each player
		else:
			playerlist = {} # Erase list of players to reroll

		# Add tournament info to collections of data
		incorporate(winner, win_tournament_by_round)
		incorporate(roundwin, win_round_by_round)
		incorporate(roundlose, lose_round_by_round)



