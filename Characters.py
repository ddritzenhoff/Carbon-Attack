# import the pygame module
import pygame
# import random for random numbers!
import random
# import pygame.locals for easier access to key coordinates
from pygame.locals import *
from Helper import load_image
import Sprite
import random


class Pacman(pygame.sprite.Sprite):

	# This function is called when an instance of the class is created.
	def __init__(self, centerPoint, image, size):

		pygame.sprite.Sprite.__init__(self)

		self.pacman_image_rect = pygame.Rect(centerPoint[0] - (size/2), centerPoint[1] - (size/2), size, size)
		# self.rect = self.pacman_image_rect
		self.food_items_eaten = 0
		self.image = image
		self.rect = image.get_rect()
		self.rect.x = centerPoint[0] - (size/2)
		self.rect.y = centerPoint[1] - (size/2)
		self.first_direction = 0
		self.nextdir = 0
		self.dx = 0
		self.dy = 0
		self.speed = 3
		self.counter = 0
		self.choice = 0
		# Matrix that determines speed.
		self.directionX = [0, -self.speed, self.speed, 0, 0]
		self.directionY = [0, 0, 0, -self.speed, self.speed]

		# Loading for the four orientations of the pacman.
		self.LeftOrientation, self.LeftOrientationRect = load_image("algae40Left.png")
		self.RightOrientation, self.RightOrientationRect = load_image("algae40.png")
		self.UpOrientation, self.UpOrientationRect = load_image("algae40Up.png")
		self.DownOrientation, self.DownOrientationRect = load_image("algae40Down.png")

	def keyPress(self, key):

		# Saving key input to the next desired movement
		# print("First pass")
		if self.first_direction is not self.nextdir:
			self.first_direction = self.nextdir
		if key == K_RIGHT:
			self.nextdir = 2
			self.image = self.RightOrientation
		elif key == K_LEFT:
			self.nextdir = 1
			self.image = self.LeftOrientation
		elif key == K_UP:
			self.nextdir = 3
			self.image = self.UpOrientation
		elif key == K_DOWN:
			self.nextdir = 4
			self.image = self.DownOrientation

	def update(self, block_group):
		# Updating the change in positions.
		self.dx = self.directionX[self.nextdir]
		self.dy = self.directionY[self.nextdir]
		# Moving the player
		self.rect.move_ip(self.dx, self.dy)
		# Checking to see if the two sprites collided. Self refers to the object of the Pacman
		if pygame.sprite.spritecollide(self, block_group, False):
			# If collision, reverse the movement.
			self.rect.move_ip(-self.dx, -self.dy)
			# Continue in old direction
			self.dx = self.directionX[self.first_direction]
			self.dy = self.directionY[self.first_direction]
			# Move in old direction
			self.rect.move_ip(self.dx, self.dy)

			if pygame.sprite.spritecollide(self, block_group, False):
				# If that did not work, reverse the move and bring the object to a stand still.
				self.rect.move_ip(-self.dx, -self.dy)
				self.dx = 0
				self.dy = 0
				self.first_direction = 0
				self.nextdir = 0
		# else:
		# 	self.first_direction = 0


class Ghost(pygame.sprite.Sprite):

	# This function is called when an instance of the class is created.
	def __init__(self, centerPoint, image, size):

		pygame.sprite.Sprite.__init__(self)

		self.ghost_image_rect = pygame.Rect(centerPoint[0] - (size / 2), centerPoint[1] - (size / 2), size, size)
		self.rect = self.ghost_image_rect
		self.image = image
		self.ghost_image_rect.x = centerPoint[0] - (size/2)
		self.ghost_image_rect.y = centerPoint[1] - (size/2)

		# Updated variables
		self.dx = 0
		self.dy = 0
		self.speed = 2
		# These two instantiations are special because there is only ever movement in one direction or none at all.
		self.directionX = [0, -self.speed, self.speed, 0, 0]
		self.directionY = [0, 0, 0, -self.speed, self.speed]
		self.nextDir = 3
		self.direction = 1
	def update(self, block_group):

		# Determining the first axis movement.
		self.dx = self.directionX[self.nextDir]
		self.dy = self.directionY[self.nextDir]

		# moving the rect
		self.rect.move_ip(self.dx, self.dy)

		# If there is a collision, reverse the action and find a new direction.
		if pygame.sprite.spritecollide(self, block_group, False):
			# reversing the move
			self.rect.move_ip(-self.dx, -self.dy)

			self.dx = self.directionX[self.direction]
			self.dy = self.directionY[self.direction]
			self.rect.move_ip(self.dx, self.dy)

			if pygame.sprite.spritecollide(self, block_group, False):
				self.rect.move_ip(-self.dx, -self.dy)
				if self.nextDir < 3:
					self.nextDir = random.randint(3, 4)
				else:
					self.nextDir = random.randint(1, 2)
			else:
				self.direction = self.nextDir
				if self.nextDir < 3:
					self.nextDir = random.randint(3, 4)
				else:
					self.nextDir = random.randint(1, 2)


