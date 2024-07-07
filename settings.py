import pygame, math 

pygame.init()

# Colours
BLACK = (0, 0, 0)
GREY = (64, 64, 64)
WHITE = (255, 255, 255)
LIGHT_BLUE = (51, 255, 255)
DARK_BLUE = (0, 102, 204)
GREEN = (0, 128, 0)
DARK_GREEN = (0, 51, 0)

MAIN_BACKGROUND = GREY 

NATIVE_WIDTH = 1280
NATIVE_HEIGHT = 720

VAR_FACTOR = 10  # The lower this number, the more variation in the stats of objects of the same level 
HP_growth = math.e
MOB_HEIGHT = 128
MOB_SIZE = 128

width = 1280
height = 720
fps = 30 

# Combat bar
bar_width = 250
bar_height = 50
x_bar = 150
y_bar = 500

font = pygame.font.Font(None, 36) # font 

