#background.py
import pygame
import random

class Background:		  #blue     blue-green  purple
	background_colors = ["#47c4e4", "#13b39b", "#8781bd"]
	cloud_colors = ["#D5F2F8","#BDEAE3","#DFDCED"]

	town_images = [] #blue, blue-green, purple
	town_images.append(pygame.image.load("images/town_day.jpg"))
	town_images.append(pygame.image.load("images/town_dusk.jpg"))
	town_images.append(pygame.image.load("images/town_night.jpg"))

	cloud_size = 60

	concrete_color = "#b2b7b1"
	def __init__(self, window):
		self.win = window
		self.background_color = self.__class__.background_colors[0]
		self.town_image = self.__class__.town_images[0]
		self.town_pos = 120
		self.cloud_color = self.__class__.cloud_colors[0]
		self.cloud_positions = []
		for i in range(10):
			if i % 2 == 0:
				pos_x = 80
			else:
				pos_x = 220
			pos_y = 320 + (i * 150)
			self.cloud_positions.append((pos_x, pos_y))

	def draw(self):
		width, height = self.win.get_size()
		cloud_size = self.__class__.cloud_size

		self.win.fill(self.background_color)
		self.win.blit(self.town_image, (0, height - 81 - self.town_pos))
		pygame.draw.rect(self.win, self.__class__.concrete_color, pygame.Rect(0, height - self.town_pos, width, self.town_pos))  

		for cloud_pos in self.cloud_positions:
			pygame.draw.rect(self.win, self.cloud_color, pygame.Rect(cloud_pos[0], height - cloud_pos[1], cloud_size, cloud_size)) 
			pygame.draw.circle(self.win, self.cloud_color, (cloud_pos[0], height - cloud_pos[1] + cloud_size/2), cloud_size/2) 
			pygame.draw.circle(self.win, self.cloud_color, (cloud_pos[0] + cloud_size, height - cloud_pos[1] + cloud_size/2), cloud_size/2) 


	def scroll(self, px):
		self.town_pos -= px
		for i in range(len(self.cloud_positions)):
			self.cloud_positions[i] = (self.cloud_positions[i][0], self.cloud_positions[i][1] - px)
		first_cloud = self.cloud_positions[0]
		last_cloud = self.cloud_positions[len(self.cloud_positions) - 1]
		if first_cloud[1] < -1 * self.__class__.cloud_size:
			self.cloud_positions.append((first_cloud[0], last_cloud[1] + 150))
			del self.cloud_positions[0]

	def randomize_color(self):
		rand_num = random.randint(0, 2)
		self.background_color = self.__class__.background_colors[rand_num]
		self.town_image = self.__class__.town_images[rand_num]
		self.cloud_color = self.__class__.cloud_colors[rand_num]