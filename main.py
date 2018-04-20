'''
Stamina.py by Eryk Banatt


mainfile which actually runs things
'''
from stamina import *

def main():
	win_tournament_by_round, win_round_by_round, lose_round_by_round, all_winners = tournament(1)
	win_tourn, win_round, lose_round, aggregate, round_prob, tourn_prob = prep_batcher(win_tournament_by_round, win_round_by_round, lose_round_by_round)
	visualize(win_tourn, "Test", "Probability")
	#visualize(zz, "Test", "Probability")
	




main()
