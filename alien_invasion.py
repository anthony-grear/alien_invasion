import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from aliens import Alien
from time import sleep
from game_stats import GameStats
from button import Button

class AlienInvasion:
	"""Overall class to manage game assets and behavior"""

	def __init__(self):
		"""Initialize the game and create game resources"""
		pygame.init()
		self.settings = Settings()
		self.screen = pygame.display.set_mode((self.settings.screen_width,
			self.settings.screen_height))
		pygame.display.set_caption("Alien Invasion")
		self.stats = GameStats(self)
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()
		self._create_fleet()
		#make the play button
		self.play_button = Button(self, "Play")



	
			
	def _create_alien(self, alien_number, row_number):
		#create an alien and place it in a row
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 * alien.rect.height*row_number  
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""respond if the alien has reached the edge of the screen"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""drop the fleet and change the direction"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *=-1
	#self.aliens.add(alien)


	

	def _check_events(self):
		"""Respond to kep presses and mouse events"""
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					self._check_keydown_events(event)
				elif event.type == pygame.KEYUP:
					self._check_keyup_events(event)
					
	def _check_keydown_events(self, event):
		"""respond to keypresses"""
		if event.key == pygame.K_RIGHT: #move the ship to the right
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_events(self,event):
		"""respond to key releases"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _fire_bullet(self):
		"""create a new bullet and add it to the bullets group"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)
	
	def _update_bullets(self):
		"""update position of bullets and get rid of old bullets"""
		#update bullet positions
		self.bullets.update()
		#get rid of bullets that have disappeared
		# 
		self._check_bullet_alien_collisions()
		"""check for any bullets that have hit aliens
		if so, get rid of the bullet and the alien"""
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True )
		if not self.aliens:
			#destroy existing bullets and create new fleet
			self.bullets.empty()
			self._create_fleet()

	def _check_bullet_alien_collisions(self):
		"""respond to bullet-alien collisions"""
		#remove and bullets and aliens that have collided
		for bullet in self.bullets.copy():
		 	if bullet.rect.bottom <= 0:
		 		self.bullets.remove(bullet)

	def _ship_hit(self):
		"""respons to the ship being hit by an alien"""
		if self.stats.ships_left > 0:
			#decrement ships left
			self.stats.ships_left -=1
			#get rid of any remaining bullets and aliens
			self.aliens.empty()
			self.bullets.empty()

			#create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()

			#pause
			sleep(0.5)
		else:
			self.stats.game_active = False

	def _check_aliens_bottom(self):
		"""check if any aliens have reached the bottom of the screen"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				#treat this the same as if the ship got hit
				self._ship_hit()
				break

	def _update_aliens(self):
		"""check if aliens at the edge then 
		update aliens positions of the whole fleet"""
		self._check_fleet_edges()
		self.aliens.update()
		#look for alien-ship collisions
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()
		#look for aliens hitting the bottom of the screen
		self._check_aliens_bottom()
	
	def _create_fleet(self):
		"""Create the fleet of aliens."""
		#create an alien and find the number of aliens
		#in each row
		#spacing between equals the width of one alien 

		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2*alien_width)
		number_aliens_x = available_space_x // (2*alien_width)

		#Determine the number of rows of aliens that fit on the screen
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height-
								(3*alien_height)-ship_height)
		number_rows = available_space_y//(2*alien_height)
		#create a fleet full of aliens
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)


	def _update_screen(self):
		"""update images on the screen, and flip to a new screen"""
		self.screen.fill(self.settings.bg_color)
			#make the most recently drawn screen visible
		
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)
		#draw the play button if the game is inactive
		if not self.stats.game_active:
			self.play_button.draw_button()
		pygame.display.flip()

	def run_game(self):
		"""Start the main loop for the game"""
		while True:
			#watch for keyboard and mouse events"""
			self._check_events()
			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			self._update_screen()

if __name__ == '__main__':
	#Make a game instance, and run the game
	ai = AlienInvasion()
	ai.run_game()