#collision_box.py
import pygame

class Collision_Box:
	def __init__(self, x_cord, y_cord, width, height):
		self.pos = (x_cord, y_cord)
		self.width = width
		self.height = height
	def draw(self, win, color):
		pygame.draw.rect(win, color, pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)) 
	def set_x_pos(self, x_pos):
		self.pos = (x_pos, self.pos[1])
	def set_y_pos(self, y_pos):
		self.pos = (self.pos[0], y_pos)
	def scroll(self, px):
		self.pos = (self.pos[0], self.pos[1] + px)
	def collided(self, other_box):
		x_overlap = False
		y_overlap = False
		if self.pos[0] > other_box.pos[0] and self.pos[0] < other_box.pos[0] + other_box.width:
			x_overlap = True
		elif other_box.pos[0] > self.pos[0] and other_box.pos[0] < self.pos[0] + self.width:
			x_overlap = True
		if self.pos[1] > other_box.pos[1] and self.pos[1] < other_box.pos[1] + other_box.height:
			y_overlap = True
		elif other_box.pos[1] > self.pos[1] and other_box.pos[1] < self.pos[1] + self.height:
			y_overlap = True
		return x_overlap and y_overlap