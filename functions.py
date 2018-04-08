'''
Stamina.py by Eryk Banatt


File full of helper functions
'''

import numpy as np
from collections import Counter
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import itertools
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

# Each individual player
#	all ints except record, which is a list of dicts
#		record is of format [{15: 1}, {66: 1}, {49: 1}]
class Player:
	def __init__(self, stamina, currentID, OriginalSeed):
		self.stam = stamina
		self.ID = currentID
		self.seed = OriginalSeed
		self.record = []

# Generates a logistic-compatible dataset from the aggregates
#	This is insanely slow and I should think about optimizing this in a not stupid way
def make_data(wins, losses):
	features = []
	targets = []
	for point, quant in enumerate(wins):
		for z in range(0, quant):
			features.append([point])
			targets.append(1)
	for point, quant in enumerate(losses):
		for z in range(0, quant):
			features.append([point])
			targets.append(0)
	return features, targets

# Generates a logistic-compatible dataset and also subtracts one from the other
#	Used for arriving at "Lose This Tournament" from "Win Tournament" and "All"
#	(((((Unfinished)))))
def make_data_subtract(x, y):
	wins_pad = []
	all_pad = []

	diff = len(x) - len(y)
	if diff >= 0:
		all_pad = np.pad(y, (0, diff), 'constant')
		wins_pad = x
	else:
		all_pad = y
		wins_pad = np.pad(x, (0, -1 * diff), 'constant')

	losses = np.subtract(all_pad, wins_pad)

	return losses

# Runs a Logistic Regression Analysis
#	I honestly have no idea what I'm doing here
def logReg(wins, losses, dont_subtract=True):
	regression = []

	for win_this_round, lose_this_round in zip(wins, losses):
		if(dont_subtract):
			X, Y = make_data(win_this_round, lose_this_round)
		else:
			X, Y = make_data(win_this_round, make_data_subtract(win_this_round, lose_this_round))
		logistic_regression = LogisticRegression()
		logistic_regression.fit(X, Y)
		zz = np.array(range(max(len(win_this_round), len(lose_this_round))))
		regression.append(logistic_regression.predict_proba(zz.reshape(-1, 1))[:,1])

	return regression

### Might want to run a "validate" on this regression on another, second trial of more data to assess goodness of fit

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
	mu, sigma = 50, 25 #mean 75, SD 25; might need tuning
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
def visualize(arr, TL="", ZL="", YL="Points Chosen", XL="Round in Tournament"):
	z = np.transpose(np.array(arr))
	x = range(1, len(arr)+1)
	y = range(len(arr[0]))
	X, Y = np.meshgrid(x, y)
	hf = plt.figure()
	ha = hf.gca(projection='3d')
	ha.plot_surface(X, Y ,z,rstride=1,cstride=1, cmap=cm.terrain, 
		linewidth=1, antialiased=False)
	ha.set_title(TL, y=1.08)
	ha.set_xlabel(XL)
	ha.set_ylabel(YL)
	ha.set_zlabel(ZL)

	plt.show()

# Builds a histogram with things I want in it
def histogram_a(arr):
	plt.hist(arr, density=False, facecolor='g')
	plt.xlabel('Points Spent')
	plt.ylabel('Count')
	plt.title('Points Distribution of Tournament Winner')
	#plt.axis([75, 150])
	plt.grid(True)
	plt.show()

# adds together two 2d arrays of equivalent or unequivalent shapes
# 	(changed from zip to izip longest because needed to handle diff lengths)
def combine(a, b):
	c = []
	for x, y in itertools.izip_longest(a, b):
		c_temp = []
		for x1, y1 in itertools.izip_longest(x, y):
			if x1 is not None:
				if y1 is not None:
					c_temp.append(x1+y1)
				else:
					c_temp.append(x1)
			else:
				c_temp.append(y1)
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

def divout2(a, b):
	c = []
	for x, y in zip(a, b):
		diff = len(x) - len(y)
		if diff >= 0:
			all_pad = np.pad(y, (0, diff), 'constant')
			wins_pad = x
		else:
			all_pad = y
			wins_pad = np.pad(x, (0, -1 * diff), 'constant')
		c.append(np.absolute(np.true_divide(wins_pad, all_pad)).tolist())
	return c

# Simple Helper Function
def prep_batcher(win_tourn_raw, win_round_raw, lose_round_raw):
	win_tourn = prep_dict_for_viz(win_tourn_raw)
	win_round = prep_dict_for_viz(win_round_raw)
	lose_round = prep_dict_for_viz(lose_round_raw)
	aggregate = combine(win_round, lose_round)
	round_prob = divout(win_round, aggregate)
	tourn_prob = divout(win_tourn, aggregate)
	return win_tourn, win_round, lose_round, aggregate, round_prob, tourn_prob

# Returns nearest integer percent of two numbers as an int
def pctof(numer, denom):
	if denom <= 0:
		return 100
	else:
		return np.rint((numer / (denom * 1.0)) * 100).astype(int)

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