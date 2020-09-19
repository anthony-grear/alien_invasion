import pygame

class Ship:
	"""a class to manage a ship."""

	def __init__(self, ai_game):
		"""Initialize the ship and set it's starting position"""
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()

		#load the ship image and it's rect
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()

		#start each new ship at the bottom middle of the screen
		self.x = float(self.rect.x)
		self.rect.midbottom = self.screen_rect.midbottom

		#movement flag
		self.moving_right = False
		self.moving_left = False

	def update(self):
		"""Update the ships position based on the movement flag"""
		#update the ships rect value, not the flags

		if self.moving_right:
			self.x += self.settings.ship_speed
		if self.moving_left:
			self.x -=self.settings.ship_speed

		#update rect object from self.x
		self.rect.x = self.x



	def blitme(self):
		"""draw the ship at it's current location"""
		self.screen.blit(self.image, self.rect)

