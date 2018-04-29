
'''
Stamina.py by Eryk Banatt


mainfile which actually runs things
'''
from stamina import *

def main():
	#double_elim_paircheck(64, 0)
        
	allrounds, all_winners = tournament(1, 1000)
	#win_tourn, win_round, lose_round, aggregate, round_prob, tourn_prob = prep_batcher(allrounds[6], allrounds[0], allrounds[1])
	#visualize(win_tourn, "Test", "Probability")
	#visualize(win_tourn, "Test", "Probability")



main()
