import os, sys
import pygame
import Map
import Sprite
from pygame.locals import *
from pygame import mixer
from Helper import *
from Characters import Pacman, Ghost
import serial
import time

class Runner:

	def runnerLoop(self):
		runner = 0
		while runner < 1:
			print("new game")
			print("New window")
			gameWindow = Controller(1300, 1000)
			print("Start main loop")
			gameWindow.mainLoop()


class Controller:

	def __init__(self, width=640, height=480):

		# Starting the game
		pygame.init()

		# Setting the window size
		self.width = width
		self.height = height
		# Setting the dimensions of the screen.
		self.screen = pygame.display.set_mode((self.width, self.height))
		# Filling screen with black.
		self.screen.fill((0, 0, 0))
		# Setting caption of the newly created screen.
		pygame.display.set_caption("Carboman - Northwestern Design Team")
		# Creating an array which stores the location of the walls in this class. This is ghetto rigging.
		self.walls = []
		"""Defining the pygame groups that are needed to print everything to the screen"""
		self.block_sprites = pygame.sprite.Group()
		# create a food group
		self.food_sprites = pygame.sprite.Group()
		# Creating a pacman Sprite group
		self.pacman_sprite_group = pygame.sprite.Group()
		# Creating a clock object which will keep the frame rate consistent.
		self.clock = pygame.time.Clock()
		# first time
		self.firstTime = pygame.time.get_ticks()
		self.timeTest = 0
		# Declaring the pacman object here.
		self.pacman = None
		# Declaring the ghost1 object here.
		self.ghost1 = None
		# Declaring the score variable.
		self.score = None
		# Create a list which saves the position of the score.
		self.score_position = (1050, 538)
		# Determine joystick positive speed
		self.joystick_positive_go_speed = 6
		# Determine joystick negative speed
		self.joystick_negative_go_speed = -6
		# Determine joystick stop speed
		self.joystick_stop_speed = 0
		# Declare lose message.
		self.lose_text = "Ay cuh, you lose mother fucker"
		# Declaring lose function
		self.lose_background = None
		# Declare buttonDelay variable to make sure that the pictures don't fly by
		self.buttondelay = 0
		# Instantiate times pressed variable to make sure button is pressed in moderation.
		self.timespressed = 0
		# Counter for beginning of game
		self.counter = 0
		# Counter for the end of the game.
		self.counterEnd = 0
		# Counter for number of pictures
		self.num = 0
		# Determine font size
		self.fontSize = 55
		# instantiate max time
		self.max_time = 44900
		# reset the game variable
		self.gameReset = 0
		# initial time
		self.firstTimeTracker = pygame.time.get_ticks()

		#Loading pictures
		self.slide1, self.slide1Rect = load_image('Slides1A.v1.jpg')
		self.slide2, self.slide2Rect = load_image('Slides2A.v1.jpg')
		self.slide3, self.slide3Rect = load_image('Slides3A.v1.jpg')
		self.slide4, self.slide4Rect = load_image('Slides4A.v1.jpg')
		self.slide5, self.slide5Rect = load_image('Slides5A.v1.jpg')
		self.slide6, self.slide6Rect = load_image('Slides6A.v1.jpg')
		self.slide7, self.slide7Rect = load_image('Slides7A.v1.jpg')
		self.slide8, self.slide8Rect = load_image('Slides8A.v1.jpg')

		self.slideArray = [self.slide1, self.slide2, self.slide3, self.slide4, self.slide5, self.slide6, self.slide7, self.slide8]
		self.slideArrayRect = [self.slide1Rect, self.slide2Rect, self.slide3Rect, self.slide4Rect, self.slide5Rect, self.slide6Rect, self.slide7Rect, self.slide8Rect]
		# Declare arduino state
		try:
			self.arduinostate = serial.Serial('/dev/ttyUSB0', 9600)
		except:
			print("Arduino state was unable to be read.")


	def mainLoop(self):

		# Run this at the very beginning of the game.
		try:
			while self.counter < 1:
				if self.arduinostate.inWaiting() > 0:
					myData = self.arduinostate.readline()
					print(myData)
					if (myData == b'5\r\n'):
						print("nothing start sequence")
						buttondelay = 1
					elif (myData == b'10\r\n') and (buttondelay == 1):
						print("Button pressed")
						buttondelay = 0
						self.timespressed += 0.5
				if self.num < 8:
					while self.timespressed == self.num:
						self.screen.fill((0, 0, 0))
						self.screen.blit(self.slideArray[self.num], self.slideArrayRect[self.num])
						# time.sleep(3)
						pygame.display.update()
						self.timespressed += 0.5
						self.num += 1
				# Breaking out of while loop
				else:
					self.counter += 1
		except:
			pass
		# keep track of time
		# self.start_time = pygame.time.get_ticks()
		# Loads all of the sprites into their respective sprite groups.
		self.loadSprites()
		self.timeTest = pygame.time.get_ticks()
		# Create an infinite loop
		running = True
		while running:
			# Keep the frame rate at a constant 60 FPS
			self.clock.tick(60)
			# pygame.event.get() gets all the events from the event queue and removes them.
			for event in pygame.event.get():
				# Checks to see whether a key has been pressed down.
				if event.type == KEYDOWN:
					# Checks to see if the key that has been pressed down is the escape key.
					if event.key == K_ESCAPE:
						# If so, set the boolean variable running to false.
						running = False
						pygame.quit()
					if ((event.key == K_RIGHT) or (event.key == K_LEFT) or (event.key == K_DOWN) or (
							event.key == K_UP)):
						self.pacman.keyPress(event.key)
				# Checks to see if the key that has been pressed down is the exit key.
				elif event.type == QUIT:
					# If so, set the boolean variable running to false.
					running = False

			try:
				if self.arduinostate.inWaiting() > 0:
					myData = self.arduinostate.readline()
					# myData.decode("utf-8")
					if myData == b'1\r\n':
						print("up")
						self.pacman.keyPress(K_UP)
					elif myData == b'2\r\n':
						print("right")
						self.pacman.keyPress(K_RIGHT)
					elif myData == b'3\r\n':
						print("left")
						self.pacman.keyPress(K_LEFT)
					elif myData == b'4\r\n':
						print("down")
						self.pacman.keyPress(K_DOWN)
					elif myData == b'5\r\n':
						print("nothing")
					elif myData == b'6\r\n':
						pass
					elif myData == b'7\r\n':
						pass
					elif myData == b'8\r\n':
						pass
					elif myData == b'9\r\n':
						pass
			except:
				pass
				# print("Arduino state in main loop has not been able to be read.")

			# Uncomment to enable pellet eating function.
			collisons = pygame.sprite.spritecollide(self.pacman, self.food_sprites, True)
			self.pacman.food_items_eaten = self.pacman.food_items_eaten + len(collisons)
			self.score = self.pacman.food_items_eaten*10

			# Get time
			self.start_time = pygame.time.get_ticks()

			# The first parameter for the font object is whether an image should be used. The second is the font size.
			font = pygame.font.Font(None, self.fontSize)
			# rendering the text.
			score_text = font.render("SCORE: %s" % self.score, 1, (255, 255, 255))

			# Updating section
			self.food_sprites.update()
			self.ghost1.update(self.block_sprites)
			self.ghost2.update(self.block_sprites)
			self.ghost3.update(self.block_sprites)
			self.pacman.update(self.block_sprites)

			# Drawing section
			pygame.time.set_timer(USEREVENT, 30000)
			print(self.start_time)
			print((self.start_time - self.timeTest) % 45000)

			if pygame.sprite.collide_rect(self.ghost1, self.pacman) or pygame.sprite.collide_rect(self.ghost2, self.pacman) or pygame.sprite.collide_rect(self.ghost3, self.pacman) or ((self.start_time - self.timeTest) % 45000) > self.max_time: # or (self.score < 1820): # or TALK ABOUT TIME
				print("you lose")
				self.screen.fill((0, 0, 0))
				if self.num < 9:
					while self.gameReset < 1:
						randoNum = 7
						self.screen.blit(self.slideArray[randoNum], self.slideArrayRect[randoNum])
						pygame.display.update()
						myData = self.arduinostate.readline()
						if myData == b'10\r\n':
							return

							# Arduino probably not plugged in.

			# Redrawing the background and filling it in with the color black.
			self.screen.fill((0, 0, 0))
			# Drawing the blocks on top of the background
			self.block_sprites.draw(self.screen)
			# Drawing the food pellets to the background
			self.food_sprites.draw(self.screen)
			# Draw score on board.
			self.screen.blit(score_text, self.score_position)
			# Draw time on board.
			# self.start_time = pygame.time.get_ticks()
			timeTest1 = font.render("TIME: %s" % str((self.max_time - (self.start_time - self.timeTest))/1000), 1, (255, 255, 255))
			self.screen.blit(timeTest1, (20, 538))
			# Draw the ghost
			# pygame.draw.rect(self.screen, (0, 255, 0), self.ghost1.ghost_image_rect)
			self.screen.blit(self.ghost1.image, self.ghost1.rect)
			self.screen.blit(self.ghost2.image, self.ghost2.rect)
			self.screen.blit(self.ghost3.image, self.ghost3.rect)
			# Updating position of pacman to the screen. This is the current problem child.
			self.screen.blit(self.pacman.image, self.pacman.rect)
			# Updating the screen.
			pygame.display.update()

	# This function loads all of the sprites into their respective sprite groups.
	def loadSprites(self):

		# Creating an instance of the map class. level1 is now a Map object.
		level1 = Map.Map()
		# Calling the layout function from the Map class. Returns a double matrix full of numbers.
		layout = level1.getLayout()
		# Calling the getSprites function from the Map class. Returns a list full of images with their respective paths.
		img_list = level1.getSprites()

		# Calculating the centers of each block size.
		x_offset = (level1.BLOCK_SIZE / 2) + 220
		y_offset = (level1.BLOCK_SIZE / 2)

		# Creating a double matrix that goes through the double matrix from layout. Should go column by column.
		for row in range(len(layout)):
			for col in range(len(layout[row])):

				# Calculating the center point of each rect.
				center_point = [(col*level1.BLOCK_SIZE)+x_offset, (row*level1.BLOCK_SIZE)+y_offset]
				# center_point = [(col * level1.BLOCK_SIZE), (row * level1.BLOCK_SIZE)]
				# Checking to see if the index variable is equal to the saved block variable.
				if layout[row][col] == level1.BLOCK:
					# Create a block sprite and add it to a sprite group.
					self.block_sprites.add(Sprite.Sprite(center_point, img_list[0]))  # Hard coding 0 into this. Should be level1.BLOCK
					# Create an equivalent rect of the wall and add it to an array.
					self.walls.append(pygame.Rect(center_point[0] - (level1.BLOCK_SIZE/2), center_point[1] - (level1.BLOCK_SIZE/2), level1.BLOCK_SIZE, level1.BLOCK_SIZE))
				# Checking to see if the index variable is equal to the saved PACMAN variable.
				elif layout[row][col] == level1.PACMAN:
					# Create an object of the Pacman class and save it to the pacman variable.
					self.pacman = Pacman(center_point, img_list[1], level1.BLOCK_SIZE)
					# Adding an equivalent Sprite to a sprite group. THIS MAY NOT BE NECESSARY
					self.pacman_sprite_group.add(Sprite.Sprite(center_point, img_list[1]))
				# Checking to see if the index variable is equal to the saved FOOD variable.
				elif layout[row][col] == level1.FOOD:
					# Creating sprites and adding them to a sprite group.
					self.food_sprites.add(Sprite.Sprite(center_point, img_list[2]))
				elif layout[row][col] == level1.Ghost1:
					# Create an object of the Ghost class and save it to the ghost1 variable.
					self.ghost1 = Ghost(center_point, img_list[3], level1.BLOCK_SIZE)
				elif layout[row][col] == level1.Ghost2:
					self.ghost2 = Ghost(center_point, img_list[4], level1.BLOCK_SIZE)
				elif layout[row][col] == level1.Ghost3:
					self.ghost3 = Ghost(center_point, img_list[5], level1.BLOCK_SIZE)


# If this function is called as the main function, then the game initiates.
if __name__ == "__main__":
	gameWindow = Runner()
	gameWindow.runnerLoop()

