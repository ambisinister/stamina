#Basic pairing numbers for single elimination tournaments
def single_elim(n):
	if(n == 1):
		print("tournament complete")
	else:
		for x in range(0,n/2):
			print("{} vs {}".format(x+1, n-x))
		single_elim(n/2)

#Basic pairing numbers for double elimination tournaments
def double_elim(n, round):
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

#single_elim(64)
#double_elim(64, 0)

# Each individual player
#	At some point need to add match record? maybe tag too idk
class Player:
	def __init__(self, stamina, currentID, OriginalSeed):
		self.stam = stamina
		self.ID = currentID
		self.seed = OriginalSeed

# Swaps currentID of both players, keeps seed the same
# 	This is used for pairing players even when they get upset
#		(Tested and confirmed working)
def SwapPlayersInDict(player1, player2, dic):
	p1_cID = player1.ID
	p2_cID = player2.ID

	dic[p1_cID] = player2
	dic[p2_cID] = player1
	player1.ID = p2_cID
	player2.ID = p1_cID

playerlist = {}

'''
for x in range(0, 64):
	print(x+1)
	plyr = Player(100, x+1, x+1)
	playerlist[plyr.ID] = plyr
'''
