import pygame
import sys
from classes.background import Background
from classes.flyer import Flyer
from classes.obstacle_layer import Obstacle_Layer
import neat
import os

pygame.init()
pygame.mixer.init()

crash_sound = pygame.mixer.Sound('audio/crash.wav')
flip_sound = pygame.mixer.Sound('audio/flip.wav')
fan_sound = pygame.mixer.Sound('audio/fan.wav')
point_sound = pygame.mixer.Sound('audio/point.wav')
crash_sound.set_volume(1.0)
flip_sound.set_volume(0.5)
point_sound.set_volume(0.5)

screen_width, screen_height = 380 , 550 
win = pygame.display.set_mode((screen_width, screen_height))

score = 0

font = pygame.font.Font(None, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create a text surface


# Set window title
pygame.display.set_caption("Swing Copters")

clock = pygame.time.Clock()

scroll_speed = 2.5

alternate = 0
# Main game loop

def main(genomes, config):
	global alternate
	running = True

	flyers = []
	nets = []
	ge = []

	for _,g in genomes:
		net = neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		flyers.append(Flyer(win))
		g.fitness = 0
		ge.append(g)
	
	my_background = Background(win)
	my_background.randomize_color()
	my_obstacle_layer = Obstacle_Layer(win)

	frame = 0
	while running:
		clock.tick(60)

		prev_score = my_obstacle_layer.obstacles_completed

		left_hammer, right_hammer, shift = my_obstacle_layer.get_nn_info()


		for x, flyer in enumerate(flyers):
			right_value = abs((flyer.horizantal_position - right_hammer)/screen_width)
			left_value = abs((flyer.horizantal_position - left_hammer)/screen_width)

			if flyer.orientation == 1:
				left_value = 0
				second_value = abs(flyer.horizantal_position - (shift + screen_width/2))/screen_width
			else:
				right_value = 0
				second_value = abs(flyer.horizantal_position - (screen_width/2 - shift))/screen_width

			if flyer.AI_cooldown == 0:
				output = nets[x].activate((max(left_value, right_value),))
				if output[0] > 0.5:
					flyer.AI_cooldown = 8
					flyer.change_direction()

		if len(flyers) <= 0:
			running = False
			break

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
				running = False
				
		my_background.scroll(scroll_speed)
		my_obstacle_layer.scroll(scroll_speed)
		for x, flyer in enumerate(flyers):
			if my_obstacle_layer.check_collision(flyer):
				flyers.pop(x)
				nets.pop(x)
				ge.pop(x)
		if my_obstacle_layer.obstacles_completed > prev_score:
			point_sound.play()
			for g in ge:
				g.fitness += 1
		my_obstacle_layer.swing()
		my_background.draw()
		my_obstacle_layer.draw()
		for flyer in flyers:
			flyer.move()
			flyer.draw()
		text = font.render(str(my_obstacle_layer.obstacles_completed), True, WHITE)
		text_rect = text.get_rect(center=(screen_width/2, 50)) 
		win.blit(text, text_rect)
		pygame.display.update()

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, "config/NEAT_config.txt")
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
	neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
config.species_set_config.fitness_sharing = True  # Reward diverse strategies
config.genome_config.crossover_prob = 0.5
p = neat.Population(config)
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)
winner = p.run(main, 10000000000)