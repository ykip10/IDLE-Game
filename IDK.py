import pygame, sys 
import numpy as np 
import time

pygame.init()

FPS = 30
BLACK = 0, 0, 0

clock = pygame.time.Clock()

#Game Window
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

terrain = pygame.image.load(r'sprites\grassy terrain.jpg')
terrain = pygame. transform.scale(terrain, (1280, 720))
terrainrect = terrain.get_rect()
ball = pygame.image.load(r'sprites\ball.jpg')
ballrect = ball.get_rect()
ballrect = ballrect.move(500, 200)

velocity = [0, -8] # initial speed
acceleration = [0, 0.098] # acceleration

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    ballrect = ballrect.move(velocity) # Update position 
    velocity = np.add(velocity, acceleration) # Update velocity 

    if ballrect.bottom > screen_height: # Bounce off the bottom 
        velocity = [0, -8] 

    screen.blit(terrain, terrainrect)
    screen.blit(ball, ballrect)
    clock.tick(FPS)

    pygame.display.flip() 
pygame.quit()
