#obstacle.py
import pygame
import random
import math
from classes.obstacle import Obstacle
from classes.flyer import Flyer

class Obstacle_Layer:
	obstacle_spread = 250
	completion_line = 165

	def __init__(self, window):
		self.win = window
		self.obstacles = [] 
		self.obstacles.append(Obstacle(400))
		self.obstacles_completed = 0
		self.next_obstacle_index = 0
		for _ in range(2):
			self.add_obstacle()

	def draw(self):
		width, height = self.win.get_size()

		for obstacle in self.obstacles:
			obstacle.draw(self.win)

	def swing(self):
		for i in range(len(self.obstacles)):
			self.obstacles[i].swing()

	def scroll(self, px):
		for i in range(len(self.obstacles)):
			before_scroll = self.obstacles[i].vertical_pos
			self.obstacles[i].scroll(px)
			after_scroll = self.obstacles[i].vertical_pos
			if before_scroll > Obstacle_Layer.completion_line and after_scroll <= Obstacle_Layer.completion_line:
				self.obstacles_completed += 1
				self.next_obstacle_index = 1
		if self.obstacles[0].vertical_pos < -20:
			self.add_obstacle()
			del self.obstacles[0]
			self.next_obstacle_index = 0

	def add_obstacle(self):
		last_obstacle = self.obstacles[len(self.obstacles) - 1]
		self.obstacles.append(Obstacle(last_obstacle.vertical_pos + Obstacle_Layer.obstacle_spread))

	def check_collision(self, flyer):
		for obstacle in self.obstacles:
			if obstacle.check_collision(flyer.copter_collision_box):
				return True
			if obstacle.check_collision(flyer.body_collision_box):
				return True
		return False

	def get_nn_info(self):
		right_hammer = self.obstacles[self.next_obstacle_index].right_hammer_collision_boxes[0].pos[0]
		left_hammer = self.obstacles[self.next_obstacle_index].left_hammer_collision_boxes[1].pos[0]

		return left_hammer, right_hammer, self.obstacles[self.next_obstacle_index].horizontal_shift
