class Settings:
	"""A class to store all the settings for Alien Invasion"""

	def __init__(self):
		"""Initialize the game settings"""
		#screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230,230,230)
		#ship setting
		self.ship_speed = 1.5
		#bullet settings
		self.bullet_speed = 1.5
		self.bullet_width = 10000

		self.bullet_height = 15
		self.bullet_color = (60,60,60)
		self.bullets_allowed = 90
		self.alien_speed = 1.0
		self.fleet_drop_speed = 100
		#fleet direction 1 equals right, -1 equals left
		self.fleet_direction = 1
		self.ship_limit = 3