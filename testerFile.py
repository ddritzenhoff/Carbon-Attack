import pygame
import sys
from pygame.locals import *
import os
import serial
from PIL import Image
from Helper import load_image


class Runner:

	def __init__(self, height=640, width=600):
		self.height = height
		self.width = width

		# self.screen = pygame.display.set_mode((self.width, self.height))
		self.screen = pygame.display.set_mode((800, 600))
		self.screen.fill((0, 10, 0))

		# self.background = pygame.Surface(self.screen.get_size())  # This doesn't do anything. Why?
		# self.background = self.background.convert()
		# self.background.fill((255, 0, 255))

		# Loading the pacman image into the object.
		self.image = pygame.image.load("/home/dominic/PycharmProjects/pacmanFinal/Data/Images/block.png").convert()
		self.image.set_colorkey((0, 0, 0))
		self.rect = self.image.get_rect()

		self.screen.blit(self.image, self.rect)
		pygame.draw.rect(self.screen, (255, 0, 0), [400, 300, 40, 40])  # Third and fourth params control size of rect.



	def main_loop(self):

		pygame.init()

		running = True
		while running:
			# pygame.event.get() gets all the events from the event queue and removes them.
			for event in pygame.event.get():
				# Checks to see whether a key has been pressed down.
				if event.type == KEYDOWN:
					# Checks to see if the key that has been pressed down is the escape key.
					if event.key == K_ESCAPE:
						# If so, set the boolean variable running to false.
						running = False
				# Checks to see if the key that has been pressed down is the exit key.
				elif event.type == QUIT:
					# If so, set the boolean variable running to false.
					running = False

			pygame.display.update()


class Pacman:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.canEatGhosts = False

class Jared:

	def main_loop(self):
		path1 = os.path.normpath("Data/Images/Slide1.jpg")
		path2 = os.path.normpath("Data/Images/Slide2.jpg")
		path3 = os.path.normpath("Data/Images/Slide3.jpg")
		path4 = os.path.normpath("Data/Images/Slide4.jpg")
		path5 = os.path.normpath("Data/Images/Slide5.jpg")
		path6 = os.path.normpath("Data/Images/Slide6.jpg")
		path7 = os.path.normpath("Data/Images/Slide7.jpg")
		path8 = os.path.normpath("Data/Images/Slide8.jpg")
		image1 = Image.open(path1)
		image2 = Image.open(path2)
		image3 = Image.open(path3)
		image4 = Image.open(path4)
		image5 = Image.open(path5)
		image6 = Image.open(path6)
		image7 = Image.open(path7)
		image8 = Image.open(path8)

		arduinostate = serial.Serial('/dev/ttyUSB0', 9600)
		timespressed = 0
		buttondelay = 0
		while (1 == 1):
			if (arduinostate.inWaiting() > 0):
				myData = arduinostate.readline()
				# print(myData)
				if (myData == b'1\r\n'):
					print("up")
				elif (myData == b'2\r\n'):
					print("right")
				elif (myData == b'3\r\n'):
					print("left")
				elif (myData == b'4\r\n'):
					print("down")
				elif (myData == b'5\r\n'):
					print("nothing")
					buttondelay = 1
				elif (myData == b'6\r\n'):
					print("up and to the left")
				elif (myData == b'7\r\n'):
					print("up and to the right")
				elif (myData == b'8\r\n'):
					print("down and to the left")
				elif (myData == b'9\r\n'):
					print("down and to the right")
				if (myData == b'10\r\n') and (buttondelay == 1):
					print("Button pressed")
					buttondelay = 0
					timespressed = timespressed + 0.5
			while (timespressed == 0):
				image1.show()
				timespressed = timespressed + 0.5
			while timespressed == 1:
				image2.show()
				timespressed = timespressed + 0.5
			while timespressed == 2:
				image3.show()
				timespressed = timespressed + 0.5
			while timespressed == 3:
				image4.show()
				timespressed = timespressed + 0.5
			while timespressed == 4:
				image5.show()
				timespressed = timespressed + 0.5
			while timespressed == 5:
				image6.show()
				timespressed = timespressed + 0.5
			while timespressed == 6:
				image7.show()
				timespressed = timespressed + 0.5
			while timespressed == 7:
				image8.show()
				timespressed = timespressed + 0.5
	def test2(self):

		self.screen = pygame.display.set_mode((1300, 1000))
		slide1, slide1Rect = load_image('Slide1.v1.jpg')
		slide2, slide2Rect = load_image('Slide2.v1.jpg')
		slide3, slide3Rect = load_image('Slide3.v1.jpg')
		slide4, slide4Rect = load_image('Slide4.v1.jpg')
		slide5, slide5Rect = load_image('Slide5.v1.jpg')
		slide6, slide6Rect = load_image('Slide6.v1.jpg')
		slide7, slide7Rect = load_image('Slide7.v1.jpg')
		slide8, slide8Rect = load_image('Slide8.v1.jpg')

		slideArray = [slide1, slide2, slide3, slide4, slide5, slide6, slide7, slide8]
		slideArrayRect = [slide1Rect, slide2Rect, slide3Rect, slide4Rect, slide5Rect, slide6Rect, slide7Rect, slide8Rect]
		running = True
		# Serial stuff
		arduinostate = serial.Serial('/dev/ttyUSB0', 9600)
		buttonPress = 0
		buttondelay = 0
		self.timespressed = 0
		self.num = 0
		while running:
			if (arduinostate.inWaiting() > 0):
				myData = arduinostate.readline()
				print(myData)
				if (myData == b'5\r\n'):
					print("nothing")
					buttondelay = 1
				elif (myData == b'10\r\n') and (buttondelay == 1):
					print("Button pressed")
					buttondelay = 0
					self.timespressed += 0.5
			if self.num < 8:
				while self.timespressed == self.num:
					self.screen.fill((0, 0, 0))
					self.screen.blit(slideArray[self.num], slideArrayRect[self.num])
					pygame.display.update()
					self.timespressed += 0.5
					self.num += 1



			# pygame.event.get() gets all the events from the event queue and removes them.
			for event in pygame.event.get():
				# Checks to see whether a key has been pressed down.
				if event.type == KEYDOWN:
					# Checks to see if the key that has been pressed down is the escape key.
					if event.key == K_ESCAPE:
						# If so, set the boolean variable running to false.
						running = False
				# Checks to see if the key that has been pressed down is the exit key.
				elif event.type == QUIT:
					# If so, set the boolean variable running to false.
					running = False




if __name__ == "__main__":
	# run = Runner()
	# run.main_loop()
	jaredTest = Jared()
	jaredTest.test2()


