#obstacle.py
import pygame
import math
import random
from classes.collision_box import Collision_Box

class Obstacle:
	arm_width = 359
	arm_height = 29
	hammer_width = 53
	hammer_height = 96

	arm_image = pygame.image.load("images/obstacle_arm.png")
	hammer_image = pygame.image.load("images/obstacle_hammer.png")

	arm_image = pygame.transform.scale(arm_image, (arm_width, arm_height))
	hammer_image = pygame.transform.scale(hammer_image, (hammer_width, hammer_height))


	gap = 170
	max_shift = 60
	hammer_shift_x = 22
	hammer_shift_y = 63

	max_initial_hammer_angle = 40 # change to 20

	swing_acceleration = 0.02
	max_swing_velocity = 1.25

	hammer_mallet_height = 20
	hammer_collision_box_width = 10

	def __init__(self, vertical_pos):
		self.vertical_pos = vertical_pos
		random_shift = random.randint(-1 * Obstacle.max_shift, Obstacle.max_shift)
		random_hammer_angle = random.randint(-1 * Obstacle.max_initial_hammer_angle, Obstacle.max_initial_hammer_angle)
		random_start_direction = random.choice([-1, 1])
		if random_hammer_angle != 0:
			random_start_direction = -1 * random_hammer_angle/abs(random_hammer_angle)
		if random_start_direction == 1:
			direction = 1
		else:
			direction = -1
		self.hammer_angle = random_hammer_angle
		self.hammer_velocity = random_start_direction * Obstacle.max_swing_velocity
		self.horizontal_shift = random_shift

		self.left_arm_collision_box = Collision_Box(380/2 + self.__class__.gap/2 + self.horizontal_shift, 550 - self.vertical_pos, Obstacle.arm_width, Obstacle.arm_height)
		self.right_arm_collision_box = Collision_Box(380/2 - self.__class__.arm_width - self.__class__.gap/2 + self.horizontal_shift, 550 - self.vertical_pos, Obstacle.arm_width, Obstacle.arm_height)

		self.left_hammer_collision_boxes = [] #topleft, topright, bottomleft, bottomright
		self.right_hammer_collision_boxes = [] #topleft, topright, bottomleft, bottomright

		for _ in range(3):
			self.left_hammer_collision_boxes.append(Collision_Box(0, 0, Obstacle.hammer_collision_box_width, Obstacle.hammer_mallet_height))
			self.right_hammer_collision_boxes.append(Collision_Box(0, 0, Obstacle.hammer_collision_box_width, Obstacle.hammer_mallet_height))

		self.callibrate_hammer_collison_boxes()

	def draw(self, win):
		width, height = win.get_size()

		hammer_image = Obstacle.hammer_image
		hammer_image = pygame.transform.rotate(hammer_image, self.hammer_angle)
		"""
		self.left_arm_collision_box.draw(win, "red")
		self.right_arm_collision_box.draw(win, "red")
		"""

		win.blit(self.__class__.arm_image, (width/2 + self.__class__.gap/2 + self.horizontal_shift, height - self.vertical_pos))
		win.blit(self.__class__.arm_image, (width/2 - self.__class__.arm_width - self.__class__.gap/2 + self.horizontal_shift, height - self.vertical_pos))
		rotational_offset_x = math.sin(math.radians(self.hammer_angle)) * Obstacle.hammer_height/2
		rotational_offset_y = Obstacle.hammer_height/2 - math.cos(math.radians(self.hammer_angle)) * Obstacle.hammer_height/2
		hammer_width, hammer_height = hammer_image.get_size()
		win.blit(hammer_image, (width/2 - hammer_width/2 + self.horizontal_shift + Obstacle.gap/2 + Obstacle.hammer_shift_x + 1 + rotational_offset_x, height - self.vertical_pos - hammer_height/2 + Obstacle.hammer_shift_y - rotational_offset_y))
		win.blit(hammer_image, (width/2 - hammer_width/2 + self.horizontal_shift - Obstacle.gap/2 - Obstacle.hammer_shift_x + rotational_offset_x, height - self.vertical_pos - hammer_height/2 + Obstacle.hammer_shift_y - rotational_offset_y))
		

	
		"""
		for collision_box in self.right_hammer_collision_boxes:
			collision_box.draw(win, "red")
		for collision_box in self.left_hammer_collision_boxes:
			collision_box.draw(win, "red")
	
		"""
		


	def swing(self):
		acc = Obstacle.swing_acceleration
		if self.hammer_angle > 0:
			acc = -1 * Obstacle.swing_acceleration
		new_swing_velocity = self.hammer_velocity + acc
		new_swing_velocity = max(new_swing_velocity, -1 * Obstacle.max_swing_velocity)
		new_swing_velocity = min(new_swing_velocity, Obstacle.max_swing_velocity)
		self.hammer_angle += self.hammer_velocity
		self.hammer_velocity = new_swing_velocity
		self.callibrate_hammer_collison_boxes()

	def scroll(self, px):
		self.vertical_pos -= px
		self.left_arm_collision_box.scroll(px)
		self.right_arm_collision_box.scroll(px)
		for collision_box in self.right_hammer_collision_boxes:
			collision_box.scroll(px)
		for collision_box in self.left_hammer_collision_boxes:
			collision_box.scroll(px)


	def check_collision(self, flyer_collision_box):
		if flyer_collision_box.collided(self.left_arm_collision_box):
			return True
		elif flyer_collision_box.collided(self.right_arm_collision_box):
			return True
		for collision_box in self.right_hammer_collision_boxes:
			if flyer_collision_box.collided(collision_box):
				return True
		for collision_box in self.left_hammer_collision_boxes:
			if flyer_collision_box.collided(collision_box):
				return True
		return False

	def callibrate_hammer_collison_boxes(self):
		hammer_width, hammer_height = Obstacle.hammer_image.get_size()

		initial_middle = (380/2 + self.horizontal_shift + Obstacle.gap/2 + Obstacle.hammer_shift_x + 1, 550 - self.vertical_pos + Obstacle.hammer_shift_y)

		self.right_hammer_collision_boxes[0].set_x_pos(initial_middle[0] + 1 * Obstacle.hammer_collision_box_width + (-1 * hammer_width/2 * math.cos(math.radians(self.hammer_angle)) + 2 * hammer_height/2 * math.sin(math.radians(self.hammer_angle))))
		self.right_hammer_collision_boxes[0].set_y_pos(initial_middle[1] -  25 + (hammer_width/2 * math.sin(math.radians(self.hammer_angle)) + hammer_height/2 * math.cos(math.radians(self.hammer_angle))))


		self.right_hammer_collision_boxes[1].set_x_pos(initial_middle[0] - 1 * Obstacle.hammer_collision_box_width + (hammer_width/2 * math.cos(math.radians(self.hammer_angle)) + 2 * hammer_height/2 * math.sin(math.radians(self.hammer_angle))))
		self.right_hammer_collision_boxes[1].set_y_pos(initial_middle[1] - 40 + (-1 * hammer_width/2 * math.sin(math.radians(self.hammer_angle)) + hammer_height/2 * math.cos(math.radians(self.hammer_angle))))


		self.right_hammer_collision_boxes[2].set_x_pos(initial_middle[0] + (hammer_width/2 * math.cos(math.radians(self.hammer_angle)) + 2 * hammer_height/2 * math.sin(math.radians(self.hammer_angle)))/2 - 15)
		self.right_hammer_collision_boxes[2].set_y_pos(initial_middle[1])

		initial_middle = (380/2 + self.horizontal_shift - Obstacle.gap/2 - hammer_width + Obstacle.hammer_shift_x + 1, 550 - self.vertical_pos + Obstacle.hammer_shift_y)

		self.left_hammer_collision_boxes[0].set_x_pos(initial_middle[0] + 1 * Obstacle.hammer_collision_box_width + (-1 * hammer_width/2 * math.cos(math.radians(self.hammer_angle)) + 2 * hammer_height/2 * math.sin(math.radians(self.hammer_angle))))
		self.left_hammer_collision_boxes[0].set_y_pos(initial_middle[1] - 40 + (hammer_width/2 * math.sin(math.radians(self.hammer_angle)) + hammer_height/2 * math.cos(math.radians(self.hammer_angle))))

		self.left_hammer_collision_boxes[1].set_x_pos(initial_middle[0] - 1 * Obstacle.hammer_collision_box_width + (hammer_width/2 * math.cos(math.radians(self.hammer_angle)) + 2 * hammer_height/2 * math.sin(math.radians(self.hammer_angle))))
		self.left_hammer_collision_boxes[1].set_y_pos(initial_middle[1] - 25 + (-1 * hammer_width/2 * math.sin(math.radians(self.hammer_angle)) + hammer_height/2 * math.cos(math.radians(self.hammer_angle))))

		self.left_hammer_collision_boxes[2].set_x_pos(initial_middle[0] + (hammer_width/2 * math.cos(math.radians(self.hammer_angle)) + 2 * hammer_height/2 * math.sin(math.radians(self.hammer_angle)))/2)
		self.left_hammer_collision_boxes[2].set_y_pos(initial_middle[1])