import player
import pickled
from common import m

class Nemesis(player.Player):
	def __init__(self, goal, opp_probabilities):
		player.Player.__init__(self, goal)
		self.goal = goal
		self.cache_win_save_depth = [[0 for i in range(goal)] for mine in range(goal+5)]
		self.cache_win_save = [[0.0 for i in range(goal)] for mine in range(goal+5)]
		self.cache_win_roll_depth = [[[0 for i in range(goal)] for mine in range(old, goal+5)] for old in range(goal)]
		self.cache_win_roll = [[[0.0 for i in range(goal)] for mine in range(old, goal+5)] for old in range(goal)]
		self.cache_win_depth = [[[0 for i in range(goal)] for mine in range(old, goal+5)] for old in range(goal)]
		self.cache_win = [[[0.0 for i in range(goal)] for mine in range(old, goal+5)] for old in range(goal)]
		self.cache_opp_gets = opp_probabilities
		self.cache_decide = [[[2 for i in range(goal)] for mine in range(old, goal)] for old in range(goal)]
	
	def p_i_win_save(self, depth, mine, opp):
		if self.cache_win_save_depth[mine][opp] < depth:
			self.cache_win_save[mine][opp] = self._p_i_win_save(depth, mine, opp)
			self.cache_win_save_depth[mine][opp] = depth
		return self.cache_win_save[mine][opp]
	
	def p_i_win_roll(self, depth, old, mine, opp):
		d = mine - old
		if self.cache_win_roll_depth[old][d][opp] < depth:
			self.cache_win_roll[old][d][opp] = self._p_i_win_roll(depth, old, mine, opp)
			self.cache_win_roll_depth[old][d][opp] = depth
		return self.cache_win_roll[old][d][opp]
	
	def p_i_win(self, depth, old, mine, opp):
		d = mine - old
		if self.cache_win_depth[old][d][opp] < depth:
			self.cache_win[old][d][opp] = self._p_i_win(depth, old, mine, opp)
			self.cache_win_depth[old][d][opp] = depth
		return self.cache_win[old][d][opp]
	
	def p_opp_gets(self, opp_base, opp_res, mine):
		return self.cache_opp_gets[opp_base][opp_res - opp_base][mine]
	
	def _p_i_win_save(self, depth, mine, opp):
		if depth <= 0: return 0
		save = 0.0
		fsum = 0.0
		for opp_new in range(opp, self.goal):
			f = self.p_opp_gets(opp, opp_new, mine)
			if f > 0:
				fsum += f
				save += f*self.p_i_win(depth-1, mine, mine, opp_new)
		if save > 1:
			m('p_i_win_save(%s) -> ' % ((depth, mine, opp),), save, fsum)
		return save
	
	def _p_i_win_roll(self, depth, old, mine, opp):
		#print 'p_i_win_roll(%s)' % ((depth, mine),)
		if depth <= 0: return 0
		s = [self.p_i_win(depth, old, new_mine, opp) for new_mine in range(mine+1, mine+6)]+[self.p_i_win_save(depth, old, opp)]
		#print s
		return sum(s)/6.0
	
	def _p_i_win(self, depth, old, mine, opp):
		#print 'p_i_win(%s)' % ((depth, old, mine, opp),)
		if mine >= self.goal: return 1
		return max(self.p_i_win_save(depth, mine, opp), self.p_i_win_roll(depth, old, mine, opp))
	
	def _decide(self, goal, old, mine, opp):
		#print 'decide: ---- %s' % ((old, mine),)
		d = mine - old
		if self.cache_decide[old][d][opp] == 2:
			self.cache_decide [old][d][opp] = self._decide_(old, mine, opp)
		return self.cache_decide[old][d][opp]
	
	depth = 30
	def _decide_(self, old, mine, opp):
		self.prepare_saved(old, opp)
		roll = self.p_i_win_roll(self.depth, old, mine, opp)
		save = self.p_i_win_save(self.depth, mine, opp)
		if abs(roll - save) < 0.001:
			m('close decision %f at %s' % (abs(roll - save), (old, mine, opp)))
		if old == mine and save >= roll:
			m('obviously wrong decision at %s' % ((old, mine, opp),))
			m('(%d -> %d) roll > save == %f > %f' % (old, mine, roll, save))
		return roll > save
		
	def prepare_saved(self, old, opp):
		for i in range(self.depth + 1):
			self.p_i_win_save(i, old, opp)
	
	def chances_to_win(self):
		win_first = self.p_i_win_roll(self.depth, 0, 0, 0)
		win_secnd = self.p_i_win_save(self.depth, 0, 0)
		print 'my chances are:\n\twin beginning: %f\n\twin as second: %f\n\twin overall: %f\n' % (win_first, win_secnd, 0.5*(win_first+win_secnd))
		

class MultiNemesis(Nemesis):
	def __init__(self, goal, enemy_probs, weights = False):
		Nemesis.__init__(self, goal, [])
		self.weights = weights
		if weights == False:
			self.weights = [1 for x in enemy_probs]
		self.nems = [(Nemesis(goal, e), w) for e, w in zip(enemy_probs, self.weights)]
	def _p_i_win_save(self, depth, mine, opp):
		return sum([n.p_i_win_save(depth, mine, opp)*w for n, w in self.nems])
	def _p_i_win_roll(self, depth, old, mine, opp):
		return sum([n.p_i_win_roll(depth, old, mine, opp)*w for n, w in self.nems])
		


class Player(Nemesis):
	def __init__(self, goal, player):
		Nemesis.__init__(self, goal, self.bot_to_probabilities(player))
	
	@staticmethod
	def bot_to_probabilities(bot, goal = 50):
		p_matrix = [[[0.0 for i in range(goal)] for mine in range(old, goal)] for old in range(goal)]
		for old in reversed(range(0, goal)):
			for opp in reversed(range(0, goal)):
				decision = [bot.immediate_decision(old, mine, opp) for mine in range(old, goal)]
				p_matrix[old][0][opp] = 1.0
				for d in range(0, goal-old):
					if decision[d]:
						p = p_matrix[old][d][opp]
						p_matrix[old][d][opp] = 0
						for dn in range(d+1, min(d+6, goal-old)):
							p_matrix[old][dn][opp] += p/6.0
						p_matrix[old][0][opp] += p/6.0
		return p_matrix

class Pickled(Player):
	def __init__(self, goal, file_name):
		Player.__init__(self, goal, pickled.Player(goal, file_name))

if __name__ == '__main__':
	#print 'create nemesis of zwirbeltier and save it'
	#p = Pickled(50, 'pickled/nemesis_roll25.pickle')
	#pickled.save(p, 'pickled/nemesis_nemesis_roll25.pickle')
	
	print 'create zwirbeltier5'
	import bots
	a = Player.bot_to_probabilities(bots.Roll25(50), 50)
	b = Player.bot_to_probabilities(bots.AlwaysRoll(50), 50)
	c = Player.bot_to_probabilities(pickled.Player(50, 'pickled/nemesis_alwaysroll.pickle'), 50)
	d = Player.bot_to_probabilities(pickled.Player(50, 'pickled/nemesis_roll25.pickle'), 50)
	e = Player.bot_to_probabilities(bots.OptiRoll(50), 50)
	
	mn = MultiNemesis(50, [a, b, c, d, e], (7, 1, 2, 2, 3))
	pickled.save(mn, 'pickled/zwirbeltier5.pickle')
