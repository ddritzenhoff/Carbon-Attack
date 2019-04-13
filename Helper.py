import os, sys
import pygame
from pygame.locals import *


def load_image(name, colorkey=None):  # The =None is the equivalent of setting the variable to 'null'

	# This specifies the path to the image that you want to get.
	fullname = os.path.join('/home/dominic/PycharmProjects/pacmanFinal/Data/', 'Images')
	fullname = os.path.join(fullname, name)  # This resigns the 'fullname' variable to the image
	# fullname = os.path.join(os.getcwd(), name)

	# os.getcwd()

	try:
		image = pygame.image.load(fullname)
		print(fullname)
	except pygame.error:  # message: #not sure how this syntax works [HELP]
		print("Cannot load image: " + fullname)
		return

	image = image.convert()

	if colorkey is not None:  # if colorkey is not equal to null, then continue.
		if colorkey is -1:  # not sure if this is proper syntax. -1 is usually the value that is associated with an error.
			colorkey = image.get_at((0, 0))  # not exactly sure what is happening here [HELP]
		"""This will make it so that when blitting the surface onto a destination, any pixels that have the same 
		color scheme as first input will be rendered invisible."""
		image.set_colorkey(colorkey, RLEACCEL)

	return image, image.get_rect()  # constructs a tuple which will return both values.

