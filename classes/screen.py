#screen.py
import pygame
import sys
from classes.background import Background
from classes.flyer import Flyer
from classes.obstacle_layer import Obstacle_Layer

class Screen:


	pygame.init()
	pygame.mixer.init()

	
	crash_sound = pygame.mixer.Sound('audio/crash.wav')
	flip_sound = pygame.mixer.Sound('audio/flip.wav')
	fan_sound = pygame.mixer.Sound('audio/fan.wav')
	point_sound = pygame.mixer.Sound('audio/point.wav')
	
	crash_sound.set_volume(1.0)
	flip_sound.set_volume(0.5)
	point_sound.set_volume(0.5)

	width, height = 380 , 550 

	score = 0

	font = pygame.font.Font(None, 50)
	WHITE = (255, 255, 255)
	BLACK = (0, 0, 0)

	# Create a text surface


	# Set window title
	pygame.display.set_caption("Swing Copters")

	clock = pygame.time.Clock()

	scroll_speed = 2.5

	
	# Main game loop
	running = True
	start = False
	dead = False

	def __init__(self):
		self.win = pygame.display.set_mode((Screen.width, Screen.height))
		self.flyers = [Flyer(self.win)]
		self.reset()
		self.draw()

	def reset(self):
		self.background = Background(self.win)
		self.background.randomize_color()
		self.obstacle_layer = Obstacle_Layer(self.win)

	def tick(self):
		Screen.clock.tick(60)
		if Screen.start:
			self.background.scroll(Screen.scroll_speed)
			my_obstacle_layer.scroll(Screen.scroll_speed)
			for flyer in self.flyers:
				flyer.move()
				if self.obstacle_layer.check_collision(flyer):
					self.flyers.remove(flyer)
		self.obstacle_layer.swing()
		self.draw()
		

	def draw(self):
		self.background.draw()
		self.obstacle_layer.draw()
		for flyer in self.flyers:
			flyer.draw()
		pygame.display.update()
