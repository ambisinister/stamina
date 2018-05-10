
'''
Stamina.py by Eryk Banatt


mainfile which actually runs things
'''
from stamina import *

def main():
	#double_elim_paircheck(64, 0)
        
	allrounds, all_winners, every_player_ever = tournament(2, 100, True, 64, 100)
	win_tourn, win_round, lose_round, aggregate, round_prob, tourn_prob = prep_batcher(allrounds[c_WINNERS], allrounds[WINNERS_WINS], allrounds[WINNERS_LOSSES])
        #visualize(lose_round, "Test", "Probability")
	visualize(win_tourn, "Test", "Probability")



main()
