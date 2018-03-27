'''
Stamina.py by Eryk Banatt


mainfile which actually runs things
'''
from stamina import *

def main():

	win_tourn_raw, win_round_raw, lose_round_raw = tournament(1)
	win_tourn, win_round, lose_round, aggregate, round_prob, tourn_prob = prep_batcher(win_tourn_raw, win_round_raw, lose_round_raw)

	visualize(win_round, "Count of Points Spent By Round Winner", "Quantity")
	visualize(win_tourn, "Count of Points Spent By Eventual Tournament Winner", "Quantity")
	visualize(aggregate, "Count of Points Spent By All Players", "Quantity")
	visualize(round_prob, "Probability of Round Win", "Probability")
	visualize(tourn_prob, "Probability of Eventual Tournament Win", "Probability")


	'''
	visualize(win_round, "Percentage of Remaining Points Spent By Winner By Round", "Quantity", "Percentage Chosen")
	visualize(aggregate, "All Players' Percentage of Remaining Points Spent By Round", "Quantity", "Percentage Chosen")
	visualize(round_prob, "Probability of Round Win By Round Given Percentage Spent", "Probability", "Percentage Chosen")
	visualize(tourn_prob, "Probability of Eventual Tournament Win Given Percentage Spent", "Probability", "Percentage Chosen")
	'''
	

main()