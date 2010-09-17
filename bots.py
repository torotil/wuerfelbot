from common import m
from player import Player

class AlwaysRoll(Player):
	def _decide(self, aim, old, mine, opp):
		return True

class RollN(Player):
	@classmethod
	def _decide(self, aim, old, mine, opp):
		return (mine - old < self.take)

class Roll16(RollN):
	take = 16

class Roll25(RollN):
	take = 25

class Roll17(RollN):
	take = 17

class OptiRoll(Player):
	targets = [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 12, 13, 13, 13, 14, 15, 15, 15, 16, 17, 17, 17, 18, 18, 19, 20, 20, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16, 17]
	def beginTurn(self, my, o):
		Player.beginTurn(self, my, o)
		self.take = self.targets[self.aim - my]
		m('begin turn: difference to goal is %d so take is %d' % (self.aim - my, self.take))
		
	def _decide(self, aim, old, mine, opp):
		return (mine - old < self.take)

