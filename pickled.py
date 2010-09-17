import cPickle as pickle
import player

class Strategy:
	def __init__(self, file_name):
		with open(file_name, 'r') as f:
			self.decide_cache = pickle.load(f)
	def _decide(self, goal, old, mine, opp):
		return self.decide_cache[old][mine-old][opp]

class Player(player.Player, Strategy):
	def __init__(self, aim, file_name):
		player.Player.__init__(self, aim)
		Strategy.__init__(self, file_name)
		self._name = file_name
	def name(self):
		return self._name

def save(bot, file_name, aim = 50, opps = False, olds = False):
	if opps == False:
		opps = range(0, aim)
	if olds == False:
		olds = range(0, aim)
	decisions = [[[2 for i in range(aim)] for mine in range(old, aim)] for old in range(aim)]
	for old in reversed(olds):
		for mine in reversed(range(old, aim)):
			for opp in reversed(opps):
				decisions[old][mine-old][opp] = bot.immediate_decision(old, mine, opp)
	bot.chances_to_win()
	with open(file_name, 'w') as f:
		pickle.dump(decisions, f)
