'''
Stamina.py by Eryk Banatt


mainfile which actually runs things
'''
from stamina import *

def main():
	#win_tournament_by_round, win_round_by_round, lose_round_by_round, all_winners = tournament(1)
	#win_tourn, win_round, lose_round, aggregate, round_prob, tourn_prob = prep_batcher(win_tournament_by_round, win_round_by_round, lose_round_by_round)
	#visualize(tourn_prob, "Test", "Probability")
	#visualize(zz, "Test", "Probability")
	
	y = find_max_densities(2, 15)
	print y
	x = range(1, 15+1)

	coeffs = np.polyfit(np.log(x), y, 1, w=np.sqrt(y))
	print coeffs
	poly = np.polyval(coeffs, np.log(x))

	plt.plot(poly)
	plt.scatter(x, y)
	plt.title("Mode spent by Winner, mean=50")
	plt.xlabel("Round")
	plt.ylabel("Points")
	plt.xlim(1, 15)
	plt.show()



main()
