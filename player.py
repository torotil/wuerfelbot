
class Player:
	def __init__(self, aim):
		self.aim = aim
		self.my_points = 0
		self.op_points = 0
		self.op_round_points = 0
		
	def beginGame(self):
		pass
	
	def name(self):
		return self.__class__.__name__
	
	def beginTurn(self, my, op):
		if self.op_points < op:
			self.op_took(op - self.op_points)
		self.my_points = my
		self.op_points = op
		self.tmp_points = my
		self.op_round_points = 0
	
	def thrown(self, n):
		if n <= 6:
			self.tmp_points += n
			
	def op_threw(self, n):
		if n < 6:
			self.op_round_points += n
		else:
			self.op_left(self.op_round_points)
	
	def decide(self):
		return self._decide(self.aim, self.my_points, self.tmp_points, self.op_points)
	
	def op_took(self, n):
		pass
	
	def op_left(self, n):
		pass
	
	def immediate_decision(self, old, mine, opp):
		self.beginTurn(old, opp)
		return self._decide(self.aim, old, mine, opp)


