
'''
Stamina.py by Eryk Banatt


mainfile which actually runs things
'''
from stamina import *

def main():
	#double_elim_paircheck(64, 0)

	
	win_tournament_by_round, win_round_by_round, lose_round_by_round, win_tournament_by_round_L, win_round_by_round_L, lose_round_by_round_L, all_winners = tournament(1, 1000)
	win_tourn, win_round, lose_round, aggregate, round_prob, tourn_prob = prep_batcher(win_tournament_by_round, win_round_by_round, lose_round_by_round)
	#visualize(win_tourn, "Test", "Probability")
	visualize(win_tourn, "Test", "Probability")



main()
