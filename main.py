import remote
from pickled import Player

server = ('wettbewerb.linuxmagazin.de', 3333)
player_name = 'zwirbeltier'

b = Player(50, 'pickled/zwirbeltier4.pickle')
g = remote.Game(server, b, player_name)
g.play()
