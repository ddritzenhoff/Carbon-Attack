import pygame
from Helper import *


class Sprite(pygame.sprite.Sprite):  # inheriting the methods from the pygame.Sprite class.

	def __init__(self, centerPoint, image):
		pygame.sprite.Sprite.__init__(self)  # calling the super class's .__init__ method.
		self.image = image  # assigning the object's image
		self.rect = image.get_rect()  # making a rectangle out of the image.
		self.rect.center = centerPoint  # find the center point.
