import pygame, sys, settings
from objects import Resource, Generator
import numpy as np 

pygame.init()

NATIVE_WIDTH = 1280
NATIVE_HEIGHT = 720
# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
clock = pygame.time.Clock()

# Settings
fps = settings.fps
screen = pygame.display.set_mode((settings.width, settings.height))

def x(x):
    """
    Returns x-coordinate scaled to custom resolutions
    """
    return settings.width * x / NATIVE_WIDTH


def y(y):
    """
    Returns y-coordinate scaled to custom resolutions
    """
    return settings.height * y / NATIVE_HEIGHT


#Resource Types
money = Resource("Money", 1)                            #Standard resource to buy upgrades
gems = Resource("Gems", 0)                              #Rare & Premium currency

#Resource Generator                                           
generator1 = Generator("generator1", money, 1,10)          #tier 1 generator
generator2 = Generator("generator2", money, 5,100)          #tier 2 generator
generator3 = Generator("generator3", money, 20,1000)         #tier 3 generator
      
# Font
font = pygame.font.Font(None, 36)

#Text draw function (replace with images)
def draw_text(surface, text, x, y):                     #surface = screen it draws on
    text_surface = font.render(text, True, WHITE)       
    surface.blit(text_surface, (x, y))

#   def buy(object_name, resource):
#       if object_name.

# Changes scenes to main screen 
def show_mainscreen():
    """
    Draws Visuals & Buttons for the main screen 
    """

    # Resources info
    draw_text(screen, str(money), x(10), y(10))                           # Current Resource Amount
    draw_text(screen, str(gems), x(200), y(10))                           # Gem count
    draw_text(screen, f'Income: {str(total_rate)}g/s', x(390), y(10))     # Current income 

    # Clicking area 
    pygame.draw.rect(screen, (0, 128, 0), (x(600), y(0), x(720), y(720)))     

    # Generators information
    pygame.draw.rect(screen, (0, 128, 0), (x(15), y(100), x(200), y(30)))      # screen, RGB, position(x1,y1,x2,y2)
    draw_text(screen, "Buy Generator 1", x(20), y(100))
    draw_text(screen, '+' + str(generator1.base_rate) + ' g/s', x(225), y(100))
    draw_text(screen, 'Current: ' + str(generator1.rate) + 'g/s', x(315), y(100))
    pygame.draw.rect(screen, (0, 128, 0), (x(15), y(150), x(200), y(30)))
    draw_text(screen, "Buy Generator 2", x(20), y(150))
    draw_text(screen, '+' + str(generator2.base_rate) + ' g/s', x(225),  y(150))
    draw_text(screen, 'Current: ' + str(generator2.rate) + 'g/s', x(315), y(150))

    # Shop button
    pygame.draw.rect(screen, (0, 128, 0), (x(15), y(670), x(80), y(30)))
    draw_text(screen, "Shop", x(20), y(670))


# Changes scenes to shop screen 
def show_shopscreen():
    screen.fill(BLACK)

    # Return button
    pygame.draw.rect(screen, (0, 128, 0), (x(15), y(670), x(90), y(30)))
    draw_text(screen, "Return", x(20), y(670))


# Screens 
main_screen = True
shop_screen = False

#Main Game Loop
run = True  
while run:
    for event in pygame.event.get():
        #Quit Pygame
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Clicking for resources 
            if x(600) <= mouse_x <= x(settings.width) and y(0) <= mouse_y <= y(settings.height):
                for i in range(Resource.id_no):                                      
                    Resource.get_resource(i).add(Resource.get_resource(i).click_rate)
            # Buy Generator Buttons
            elif x(15) <= mouse_x <= x(200) and y(100) <= mouse_y <= y(130):      #Purchase generator 1
                generator1.buy()
            elif x(15) <= mouse_x <= x(200) and y(150) <= mouse_y <= y(180):   #Purchase generator 2
                generator2.buy()
            # Shop button 
            elif x(15) <= mouse_x <= x(90) and y(670) <= mouse_y <= y(700):
                main_screen = False
                shop_screen = True
    #Update Resource Generators and get total rate
    total_rate = 0

    for i in range(Generator.id_no):                                      
        Generator.get_gen(i).update()
        total_rate += Generator.get_gen(i).rate

    #Fill screen with black
    screen.fill(BLACK)

    if main_screen:
        show_mainscreen()
    elif shop_screen:
        show_shopscreen()

    #Update Display
    pygame.display.flip()


