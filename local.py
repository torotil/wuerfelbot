# -*- coding: utf-8 -*-

from random import randint
from common import m

class SingleGame:
	def __init__(self, player, aim):
		self.p = player
		self.aim = aim
	
	def play(self):
		score = 0
		round = 0
		self.p.beginGame()
		while True:
			round += 1
			old_score = score
			self.p.beginTurn(old_score, 0)
			m('BEGIN TURN')
			while self.p.decide():
				x = self.roll()
				if x == 6:
					score = old_score
					break
				self.p.thrown(x)
				score += x
				if score >= self.aim:
					return round
		
	def roll(self):
		return randint(1, 6)


class Game:
	def __init__(self, player1, player2, target):
		self.p = [player1, player2]
		self.target = target
		self.turns = [[0,0], [0,0]]
		self.games = [0, 0]
	
	def killBots(self):
		del self.p
	
	def turn(self, p):
		self.game_turns[p] += 1
		player = self.p[p]
		opponent = self.p[(p+1)%2]
		m('begin turn of player "%s"' % player.__class__.__name__)
		m('current scores: %s' % self.points)
		player.beginTurn(self.points[p], self.points[(p+1)%2])
		n = 0
		s = self.points[p]
		while n != 6:
			s += n
			if s >= self.target:
				self.points[p] = s
				return False
			if not player.decide():
				m('SAVE')
				self.points[p] = s
				break
			n = self.roll()
			m('ROLL: %d -> %d' % (n, n+s))
			player.thrown(n)
			opponent.op_threw(n)
		return True
	
	def play(self, beginner):
		m("----------")
		for p in self.p:
			p.beginGame()
		self.points = [0, 0]
		self.game_turns = [0, 0]
		p = beginner
		while self.turn(p):
			p = (p+1)%2
		m("%s won the game" % self.p[p].__class__.__name__)
		self.turns[p][0] += self.game_turns[0]
		self.turns[p][1] += self.game_turns[1]
		self.games[p] += 1
		return p
		
	def stats(self):
		print self.games
		print [[float(t)/g for t in turns] for turns,g in zip(self.turns, self.games)]
	
	def roll(self):
		return randint(1, 6)