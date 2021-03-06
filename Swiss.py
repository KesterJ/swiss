import random
import networkx as nx
from operator import itemgetter, attrgetter
import matplotlib.pyplot as plt


class Player(object):
	"""
	A player in a Swiss system; has an ID (fixed), a skill level (integer, fixed at creation, goes from 0-100),
	plus a score (integer) and a list of opponents played so far (list of integers). There is also a boolean variable isdummy,
	used to mark a player as a dummy created for the purpose of resolving byes with odd player counts.
	"""

	def __init__(self, id, skill, isdummy):
		self.id = id
		self.skill = skill
		self.score = 0
		self.opponents = []
		self.sos = 0
		self.isdummy = isdummy
		self.roundsplayed = 0


	def log_opponent(self, opponent):
		self.opponents.append(opponent)

	def pointsperround(self):
		if roundsplayed>0:
			return float(self.score)/self.roundsplayed
		else:
			return 0
	#Done? Could still add more though.

def create_tourney(skills):
	"""
	Initial tourney setup. The setup simply creates a dictionary consisting of n players, with player IDs being the keys.
	Each has a skill defined by the passed variable skills, which should be a list of integers. While these can be arranged
	in any order in the passed list, descending order means that the best player will be player 1, the second best player 2,
	etc, which makes analysing the results more intuitive later.
	This should be used to create a global variable, as the tourney list will be accessed by various other functions.
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
	#Done


def resolve_matchup(player1, player2, draw):
	"""
	Takes two players, and calculates the result of a match between them. Two equally matched players will have a
	50 percent chance of winning each, side so 1/4 sweep for player 1, 1/2 split, 1/4 sweep for player 2. For each point of
	skill difference, the better player has a 0.5 percent greater chance to win each game.
	Outcomes are recorded by directly manipulating the score variables of the player objects.
	"""

	###TODO: Add code to account for intentional draws.
	#Checks if either player is a dummy to allow instant resolution of those matches
	if player1.isdummy == True:
		player1wins = 0
	elif player2.isdummy == True:
		player1wins = 2
	#This is if an Intentional Draw happens
	elif draw:
		player1wins = 1
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
	player1.log_opponent(player2.id)
	player2.log_opponent(player1.id)
	player1.roundsplayed += 1
	player2.roundsplayed += 1
	#Done


def update_sos(player, tourney):
	"""
	This is passed a Player object, and directly updates their Strength of Schedule by modifying the variable.
	Used by rank_players function.
	"""
	strength = 0
	if player.roundsplayed != 0:
		for item in player.opponents:
			strength += tourney[item].score
		strength = float(strength)/player.roundsplayed
	player.sos = strength
	#Done


def rank_players(tourney):
	"""
	Returns a list of the IDs of all the players in the tournament, sorted by points, then by strength of schedule.
	"""
	#Update strength of schedule first; done here to save time because ranking is the only place it's relevant.
	for player in tourney:
		update_sos(tourney[player], tourney)
	playerlist = [tourney[x] for x in tourney]
	#Not done
	rankedlist = [y.id for y in sorted(playerlist, key=attrgetter('score', 'sos'), reverse=True)]
	return rankedlist


def pair_players(tourney):
	"""
	This looks at the points players have, and then analyses a cost function which minimises for the sum of within-pair
	score differentials. Needs to check byes too, but this can be on the todo list for now.
	"""
	###TODO: Implement making sure lowest ranked player who has not yet had a bye is the one who gets the bye.
	###TODO: Implement handling byes at all
	pairgraph = nx.Graph()
	#Build graph
	pairgraph.add_nodes_from(tourney.keys())
	#Add edges one by one with a weight based on score
	for player in tourney:
		for playerid in tourney.keys():
			if playerid not in tourney[player].opponents and not pairgraph.has_edge(playerid, player):
				#Subtracted from 1000 so we can calc max weight matching when we really want a minimum, and square it so that 
				#higher weight is put on keeping more different scores apart
				scoreweight = 1000 - abs(tourney[player].score - tourney[playerid].score)**2 + random.random()*0.25
				pairgraph.add_edge(player, playerid, weight = scoreweight)
	#Create pairings
	pairings = nx.max_weight_matching(pairgraph)
	###TODO: Return pairings and translate
	return pairings


def do_round(tourney, currentround):
	global idcount
	ranks = rank_players(tourney)
	top8 = ranks[:8]
	#Temp solution for displaying results as we go
	#ranklist = [tourney[playerid] for playerid in ranks]
	#display_results(ranklist)
	#End of temp solution
	pairs = pair_players(tourney)
	#print('Pairings for round:', pairs)
	while pairs:
		pair = random.choice(list(pairs.keys()))
		if tourney[pair].id in top8 and tourney[pairs[pair]].id in top8 and currentround >= 3:
			resolve_matchup(tourney[pair], tourney[pairs[pair]], True)
			idcount += 1
		else:
			resolve_matchup(tourney[pair], tourney[pairs[pair]], False)
		del pairs[pairs[pair]]
		del pairs[pair]


def run_tourney(tourney, totalrounds):
	currentround = 1
	while currentround <= totalrounds:
		#print('Round', currentround)
		do_round(tourney, currentround)
		currentround += 1
		###TODO: Maybe log some results here too for use later.
	finalranks = rank_players(tourney)
	#This next loop is just to get players skills as well, which are not provided by rank_players.
	results = [tourney[playerid] for playerid in finalranks]
	return results


def display_results(resultslist):
	for i in range(len(resultslist)):
		print(i+1,'. ',resultslist[i].id,' ',resultslist[i].skill,' ',resultslist[i].score,' ',resultslist[i].sos,'\n')


def display_cuts(cutslist):
	xaxis = []
	yaxis = []
	for playerid in range(1,33):
		xaxis.append(str(playerid))
		yaxis.append(cutslist.count(playerid))
	plt.bar(xaxis, yaxis)
	plt.show()


def main():
	global idcount
	idcount = 0
	cuts = []
	for i in range(10000):
		print('On tourney',i)
		skills = range(1,97,3)
		tourney = create_tourney(skills)
		results = run_tourney(tourney, 5)
		#display_results(results)
		for j in range(8):
			cuts.append(results[j].id)
	print('Total number of intentional draws:',idcount)
	display_cuts(cuts)

main()
