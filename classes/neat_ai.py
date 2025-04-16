#neat_ai.py
import neat
import os

class NEAT_AI:
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, "NEAT_config.txt")
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
		neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

	def __init__(self, win):
		p = neat.Population(config)
