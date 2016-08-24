import random

class Player:
	"""
	A player in a Swiss system; has an ID (fixed), a skill level (integer, fixed at creation, goes from 0-100),
	plus a score (integer) and a list of opponents played so far (list of integers). There is also a boolean variable isdummy,
	used to mark a player as a dummy created for the purpose of resolving byes with odd player counts.
	"""

	def ___init___(self, ID, skill, isdummy):
		self.ID = ID
		self.skill = skill
		self.score = 0
		self.opponents = []
		self.SoS = 0
		self.isdummy = isdummy

	def log_opponent(opponent):
		self.opponents.append(player2.ID)


def create_tourney(skills):
	"""
	Initial tourney setup. The setup simply creates a dictionary consisting of n players, with player IDs being the keys.
	Each has a skill defined by the passed variable skills, which should be a list of integers. While these can be arranged
	in any order in the passed list, descending order means that the best player will be player 1, the second best player 2,
	etc, which makes analysing the results more intuitive later.
	"""

	numplayers = len(skills)
	tourney = {}
	#Create players
	for i in range(numplayers):
		tourney[i+1] = Player(i+1, skills[i], False)
	#Adds a dummy player if needed for byes
	if numplayers%2 == 1:
		tourney[numplayers+1] = Player(numplayers+1, 0, True)
	return tourney



def resolve_matchup(player1, player2):
	"""
	Takes two players, and calculates the result of a match between them. Two equally matched players will have a
	50 percent chance of winning each, side so 1/4 sweep for player 1, 1/2 split, 1/4 sweep for player 2. For each point of
	skill difference, the better player has a 0.5 percent greater chance to win each game.
	Outcomes are recorded by directly manipulating the score variables of the player objects.
	"""

	###TODO: Add code to account for intentional draws.
	#Checks if either player is a dummy to allow instant resolution of those matches
	if player1.isdummy = True:
		player1wins = 0
	elif player2.isdummy = True:
		player1wins = 2
	#Below is code for actual resolution of a match
	else:
		player1winchance = 0.5 + 0.005 * (player1.skill - player2.skill)
		#Split 0 to 1 into sections delineated by the following variables, so that each section is proportional to the relevant
		#win chance. (e.g. for equal players, p1sweep is 0.25, and split is 0.75) Then take a random number and see which section
		#it falls into to decide result.
		p1sweep = player1winchance**2
		split = p1sweep + player1winchance*(1-player1winchance)
		result = random.random()
		if result < p1sweep:
			player1wins = 2
		elif result < split:
			player1wins = 1
		else:
			player1wins = 0
	#Update player objects with results (+3 score for each win) and log them as opponents of each other
	player1.score += 3*player1wins
	player2.score += 3*(2-player1wins)
	player1.log_opponent(player2)
	player2.log_opponent(player1)

