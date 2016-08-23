

class Player:
	"""
	A player in a Swiss system; has an ID (fixed), a skill level (integer, fixed at creation, goes from 0-100),
	plus a score (integer) and a list of opponents played so far (list of integers).
	"""

	def ___init___(self, ID, skill):
		self.ID = ID
		self.skill = skill
		self.score = 0
		self.opponents = []
		self.SoS = 0



def create_tourney(skills):
	numplayers = len(skills)
	tourney = []
	for i in range(numplayers):
		tourney.append(Player(i, skills[i]))

