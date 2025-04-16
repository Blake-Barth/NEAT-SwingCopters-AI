import pygame
import sys
from classes.background import Background
from classes.flyer import Flyer
from classes.obstacle_layer import Obstacle_Layer

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

my_background = Background(win)
my_background.randomize_color()
main_flyer = Flyer(win)
my_obstacle_layer = Obstacle_Layer(win)
# Main game loop
running = True
start = False
dead = False
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not main_flyer.is_dead:
            if start:
                flip_sound.play()
                main_flyer.change_direction()
            else:
                start = True
                fan_sound.play()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Check if spacebar is pressed
                my_obstacle_layer = Obstacle_Layer(win)
                start = False
                main_flyer = Flyer(win)
                my_background = Background(win)

    prev_score = my_obstacle_layer.obstacles_completed

    if start:
        if not main_flyer.is_dead:
            my_background.scroll(scroll_speed)
            my_obstacle_layer.scroll(scroll_speed)
            main_flyer.move()
        else:
            main_flyer.death_animation()
    if my_obstacle_layer.check_collision(main_flyer):
        if not main_flyer.is_dead:
            crash_sound.play()
        main_flyer.hit_obstacle()
    if my_obstacle_layer.obstacles_completed > prev_score:
        point_sound.play()
    my_obstacle_layer.swing()
    my_background.draw()
    my_obstacle_layer.draw()
    main_flyer.draw()
    text = font.render(str(my_obstacle_layer.obstacles_completed), True, WHITE)
    text_rect = text.get_rect(center=(screen_width/2, 50)) 
    win.blit(text, text_rect)
    pygame.display.update()
# Quit Pygame
pygame.quit()
