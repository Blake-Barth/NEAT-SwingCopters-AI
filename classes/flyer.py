#flyer.py
import pygame
from classes.collision_box import Collision_Box

class Flyer:
	flyer_width = 35
	flyer_height = 40
	copter_width = 50
	copter_height = 14

	left_flyer_image = pygame.image.load("images/left_flyer.png")
	right_flyer_image = pygame.image.load("images/right_flyer.png")
	left_flyer_image = pygame.transform.scale(left_flyer_image, (flyer_width, flyer_height))
	right_flyer_image = pygame.transform.scale(right_flyer_image, (flyer_width, flyer_height))

	copter_images = []
	copter_images.append(pygame.image.load("images/copter_one.png"))
	copter_images.append(pygame.image.load("images/copter_two.png"))
	copter_images.append(pygame.image.load("images/copter_three.png"))
	copter_images.append(pygame.image.load("images/copter_four.png"))
	for i in range(4):
		copter_images[i] = pygame.transform.scale(copter_images[i], (copter_width, copter_height))
	acceleration = 0.75
	terminal_velocity = 7
	initial_velocity = -5

	rotation_velocity = 3
	max_angle = 30
	initial_angle = 25

	def __init__(self, window):
		self.win = window
		self.velocity = 0
		self.horizantal_position = 50
		self.vertical_pos = 333
		self.orientation = 1 # 1 = right, -1 = left
		self.copter_state = 0 # for copter animation
		self.image_angle = 0
		self.is_dead = False
		self.AI_cooldown = 0

		self.copter_collision_box = Collision_Box(self.horizantal_position - Flyer.copter_width/2, 358, Flyer.copter_width, Flyer.copter_height)
		self.body_collision_box = Collision_Box(self.horizantal_position - (Flyer.flyer_width * 1.2)/2, 375, Flyer.flyer_width * 1.2, Flyer.flyer_height)

	def draw(self):
		
		"""
		self.copter_collision_box.draw(self.win, "green")
		self.body_collision_box.draw(self.win, "yellow")
		"""
	
		if self.orientation == 1:
			image = self.__class__.right_flyer_image
		elif self.orientation == -1:
			image = self.__class__.left_flyer_image
		image = pygame.transform.rotate(image, self.image_angle)
		self.win.blit(image, (self.horizantal_position - self.__class__.flyer_width/2, self.vertical_pos + self.__class__.flyer_height))
		if not self.is_dead:
			self.win.blit(self.__class__.copter_images[self.copter_state], ((self.horizantal_position - self.__class__.copter_width/2, 343 + self.__class__.copter_height)))

	def move(self):
		self.copter_state = (self.copter_state + 1) % 4
		self.horizantal_position += self.velocity
		self.velocity += self.orientation * self.__class__.acceleration
		self.image_angle +=  -1 * self.orientation * self.__class__.rotation_velocity
		self.image_angle = min(self.image_angle, self.__class__.max_angle)
		self.image_angle = max(self.image_angle, -1 * self.__class__.max_angle)
		self.velocity = min(self.velocity, self.__class__.terminal_velocity)
		self.velocity = max(self.velocity, -1 * self.__class__.terminal_velocity)
		self.horizantal_position = max(self.horizantal_position, self.__class__.flyer_width/2 - 5)
		self.horizantal_position = min(self.horizantal_position, 375 - self.__class__.flyer_width/2)
		self.copter_collision_box.set_x_pos(self.horizantal_position - Flyer.copter_width/2)
		self.body_collision_box.set_x_pos(self.horizantal_position - Flyer.flyer_width/2)
		if self.AI_cooldown != 0:
			self.AI_cooldown -= 1

	def change_direction(self):
		if self.orientation == 1:
			self.orientation = -1
		elif self.orientation == -1:
			self.orientation = 1
		self.image_angle = self.orientation * self.__class__.initial_angle
		self.velocity = self.orientation * self.__class__.initial_velocity

	def death_animation(self):
		self.vertical_pos += abs(self.velocity)
		self.velocity += self.orientation * self.__class__.acceleration
		self.image_angle +=  -2 * self.orientation * self.__class__.rotation_velocity
		self.velocity = min(self.velocity, self.__class__.terminal_velocity)
		self.velocity = max(self.velocity, -1 * self.__class__.terminal_velocity)
		self.vertical_pos = min(self.vertical_pos, 700)

	def hit_obstacle(self):
		if not self.is_dead:
			self.is_dead = True
			self.velocity = 0