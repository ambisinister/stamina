
'''
Stamina.py by Eryk Banatt


mainfile which actually runs things
'''
from stamina import *

def main():
	#double_elim_paircheck(64, 0)
        
	allrounds, all_winners, every_player_ever = tournament(1, 1000)
	win_tourn, win_round, lose_round, aggregate, round_prob, tourn_prob = prep_batcher(allrounds[c_WINNERS], allrounds[WINNERS_WINS], allrounds[WINNERS_LOSSES])
        find_best_path(every_player_ever)        
	#visualize(win_tourn, "Test", "Probability")

# in progress
def find_best_path(every_player_ever, rnd=0):
        bestpath = []
        winners = [0] * 101
        all_p = [0] * 101 
        t_len = len(every_player_ever[0].get(1).record)-1
        
        for tourney in every_player_ever:
                for playerID in range(1, len(tourney)):
                        
                        p = tourney[playerID]
                        if len(p.record) > rnd:
                                choice = p.record[rnd].keys()[0]
                                if playerID is 1:
                                        winners[choice] += 1
                                        all_p[choice] += 1
                                else:
                                        all_p[choice] += 1

        print winners
        print all_p
        print ""
        if rnd < t_len: return find_best_path(every_player_ever, rnd+1)
        
main()
