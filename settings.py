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
RED = (204, 0, 0)
YELLOW = (255, 255, 0)

MAIN_BACKGROUND = GREY 

NATIVE_WIDTH = 1280
NATIVE_HEIGHT = 720

VAR_FACTOR = 10  # The lower this number, the more variation in the stats of objects of the same level 
MOB_HEIGHT = 128
MOB_SIZE = 128

# Settings pertaining to the dimensions, positions and other tweakable parameters of the Bar class. 
BAR_DIFFICULTY = 0.05
BAR_SPEED_GROWTH = math.e # Base of the logarithm C
COMBAT_INDICATOR_WIDTH = 5 # Width of the combat indicator
combat_bar_width = 250 
combat_bar_height = 50
combat_bar_x = 750 # x coordinate of combat bar ( top left )
combat_bar_y = 500 # y coordinate of combat bar 
work_bar_width = 20
work_bar_height = 250
work_bar_x = 1100
work_bar_y = 400
MAX_WORK_ACCELERATION = 0.2

width = 1280
height = 720
fps = 60 

font = pygame.font.Font(None, 36) # font 

#User Preferences
show_scientific_notation = True
