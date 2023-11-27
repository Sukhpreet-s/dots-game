class Room:

	def __init__(self, player_name):
		self.players = {} # list of player and their points
		self.game = None
		self.add_player(player_name)


	def add_player(self, player_name):
		# Initialize entry of new player with 0 points 
		self.players[player_name] = 0

	def init_game(self, game):
		self.game = game

	def add_player_points(self, points, player_name):
		self.players[player_name] += points 

	def get_players_list(self):
		return list(self.players.keys())

	def get_player_index(self, player_name):
		return list(self.players.keys()).index(player_name)

	def get_winner(self):
		# Player with max points is the winner.
		# DS is a list because multiple players can have the same highest score for draw
		current_max_point_player_name = []
		current_max_points = 0

		for player_name in self.players:
			if self.players[player_name] > current_max_points:
				# Reset the winner player name list 
				current_max_point_player_name = []
				current_max_point_player_name.append(player_name)
				current_max_points = self.players[player_name]
			elif self.players[player_name] == current_max_points:
				current_max_point_player_name.append(player_name)

		return { 
			'player_name': current_max_point_player_name,
			'points': current_max_points 
		}
