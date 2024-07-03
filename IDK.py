import pygame


#Game Window
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.quit()