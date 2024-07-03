import pygame, sys 
import numpy as np 

pygame.init()

FPS = 30
#Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()

#Screen Settings
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

#Resources Class
class Resource:
    def __init__(self, name, amount=0):
        self.name = name                                #Name of Resource
        self.amount = amount                            #Resource Amount

    def add(self, amount):
        self.amount += amount                           #Increase resource value by "amount"

    def __str__(self):
        return f"{self.name}: {self.amount}"            #Returns resource name and amount

# Generator class                                    
class Generator:                                     
    def __init__(self, name, resource, rate):       
        self.name = name                                #Name of Generator
        self.resource = resource                        #Resource Generator makes      
        self.rate = rate                                #Resource generation rate
        self.last_update = pygame.time.get_ticks()      #Stores time since last update (ms)

    def update(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.last_update
        if elapsed > 1000:                              # Update every second
            self.resource.add(self.rate)
            self.last_update = now

#Resource Types
money = Resource("Money", 0)                            #Standard resource to buy upgrades
Gems = Resource("Gems", 0)                               #Rare & Premium currency

#Resource Generator                                           
generator1 = Generator("generator1", money, 1)          #tier 1 generator
generator2 = Generator("generator2", money, 0)          #tier 2 generator
generator3 = Generator("generator3", money, 0)         #tier 3 generator

#Buying Producers
def buy_producer(producer, cost, rate_increase):
    if money.amount >= cost:                            #checks if player can purchase generator
        money.amount -= cost                            #deducts cost if player can purchase generator
        producer.rate += rate_increase                  #increases production of generator by the rate increase

# Font
font = pygame.font.Font(None, 36)

#Text draw function (replace with images)
def draw_text(surface, text, x, y):                     #surface = screen it draws on
    text_surface = font.render(text, True, WHITE)       
    surface.blit(text_surface, (x, y))


#Main Game Loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if 15 <= mouse_x <= 200 and 100 <= mouse_y <= 130:      #Purchase generator 1
                buy_producer(generator1, 10, 1)
            elif 15 <= mouse_x <= 200 and 150 <= mouse_y <= 180:   #Purchase generator 2
                buy_producer(generator2, 100, 5)

    
    #Update Resource Generators
    generator1.update()
    generator2.update()
    generator3.update()

    #Fill screen with black
    screen.fill(BLACK)

    #Draw Visuals & Buttons
    draw_text(screen, str(money), 10, 10)                           #Current Resource Amount
    draw_text(screen, str(Gems), 200, 10)
    pygame.draw.rect(screen, (0, 128, 0), (15, 100, 200, 30))    #screen, RGB, position(x1,y1,x2,y2)
    draw_text(screen, "Buy Generator 1", 20, 100)
    pygame.draw.rect(screen, (0, 128, 0), (15, 150, 200, 30))
    draw_text(screen, "Buy Generator 2", 20, 150)

    #Update Display
    pygame.display.flip()
#Quit Pygame
pygame.quit()
sys.exit()
