'''
Stamina.py by Eryk Banatt

mainfile which actually runs things
'''

from stamina import *

def main():
	#double_elim_paircheck(64, 0)
        
	allrounds, all_winners, every_player_ever = tournament(1, 1000)
	win_tourn, win_round, lose_round, aggregate, round_prob, tourn_prob = prep_batcher(allrounds[c_WINNERS], allrounds[WINNERS_WINS], allrounds[WINNERS_LOSSES])
        print find_best_path(every_player_ever)        
	#visualize(win_tourn, "Test", "Probability")

# needs to filter out non-complying ones
# needs to handle length of round better
def find_best_path(every_player_ever, rnd=0, bestpath=[]):
        print ("-------{}-------".format(rnd))
        thisround = []
        winners = [0] * 101
        all_p = [0] * 101
        t_len = len(every_player_ever[0].get(1).record)-1
        
        for tourney in every_player_ever:
                for playerID in range(1, len(tourney)):
                        
                        p = tourney[playerID]

                        good = True
                        if len(p.record) > rnd:
                                if len(p.record) >= len(bestpath):
                                        for ind, best in enumerate(bestpath):
                                                if abs(best - p.record[rnd-1].keys()[0]) > 3: good = False
                                if good:
                                        choice = p.record[rnd].keys()[0]
                                        if playerID is 1:
                                                winners[choice] += 1
                                                all_p[choice] += 1
                                        else:
                                                all_p[choice] += 1
        print winners
        print all_p
        thisround = logReg([winners], [all_p], False)
        thisround = thisround[0].tolist()
        #print thisround

        taky = []
        for aa, bb in zip(winners, all_p):
                if bb is not 0: taky.append((1.0*aa)/bb)
                else: taky.append(1)

        plt.plot(taky)
        plt.plot(thisround)
        plt.show() #showing some problems with the logreg
                
        best_thisround = thisround.index(max(thisround))
        bestpath.append(best_thisround)
        if rnd < t_len: return find_best_path(every_player_ever, rnd+1, bestpath)
        else: return bestpath
        
main()
