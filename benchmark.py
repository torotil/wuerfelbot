from nemesis import Player

class BotComparator(Player):
	def __init__(self, goal, player1, player2):
		Player.__init__(self, goal, player2)
		self.player = player1
		
	def _p_i_win(self, depth, old, mine, opp):
		if mine >= self.goal: return 1
		if self.player.immediate_decision(old, mine, opp):
			return self.p_i_win_roll(depth, old, mine, opp)
		else:
			return self.p_i_win_save(depth, mine, opp)
	
class Benchmark:
	def __init__(self):
		self.bots = []
	def __call__(self, bot):
		print 'Benchmarking', bot.name()
		for enemy in self.bots:
			print 'enemy:', enemy.name()
			c = BotComparator(50, bot, enemy)
			for old in reversed(range(50)):
				for opp in reversed(range(50)):
					c.prepare_saved(old, opp)
			c.chances_to_win()

def compare(A, B, aim = 50, opps = False, olds = False):
	if opps == False:
		opps = range(0, aim)
	if olds == False:
		olds = range(0, aim)
	
	diffs = 0
	a = [[[2 for y in range(50)] for x in range(old, 50)] for old in range(50)]
	b = [[[2 for y in range(50)] for x in range(old, 50)] for old in range(50)]
	for decisions, bot in [(a, A), (b, B)]:
		for old in reversed(olds):
			for mine in reversed(range(old, aim)):
				for opp in reversed(opps):
					decisions[old][mine-old][opp] = bot.immediate_decision(old, mine, opp)
	for old in olds:
		for opp in opps:
			all_False = 0 
			for mine in range(old, aim):
				x, y = a[old][mine-old][opp], b[old][mine-old][opp]
				if all_False >= 5:
					break # We can never reach the rest - differences don't matter
				if (x == y == False):
					all_False += 1
				else:
					all_False = 0
				if (x != y):
					print 'difference at (old, mine, opp) = (%d, %d, %d) -> %s vs. %s' % (old, mine, opp, x, y)
					diffs += 1
	print 'found %d differences' % diffs

if __name__ == '__main__':
	import bots
	import pickled
	
	benchmark = Benchmark()
	benchmark.bots += [
  	bots.AlwaysRoll(50), bots.Roll16(50), bots.Roll25(50), bots.OptiRoll(50),
		pickled.Player(50, 'pickled/nemesis_alwaysroll.pickle'), pickled.Player(50, 'pickled/nemesis_roll25.pickle')]
	#benchmark.bots = [
  #	bots.Roll25(50),
	#	pickled.Player(50, 'pickled/nemesis_roll25.pickle')]
	
	benchmark(pickled.Player(50, 'pickled/zwirbeltier5.pickle'))
