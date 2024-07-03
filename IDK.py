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
    id_no = 0
    id_list = []
    id_to_resource = dict()
    def __init__(self, name, click_rate):
        self.name = name                                #Name of Resource
        self.amount = 0                                 #Resource Amount
        self.click_rate = click_rate
        self.id = Resource.id_no
        Resource.id_no += 1
        Resource.id_list.append(self.id)
        Resource.id_to_resource.update({self.id:self})

    def add(self, amount):
        self.amount += amount                           # Increase resource value by "amount"

    def __str__(self):
        return f"{self.name}: {self.amount}"            #Returns resource name and amount
    
    def purchasable(self,price):
        return self.amount >= price

    def get_resource(id_number):
        return Resource.id_to_resource.get(id_number)
        

# Generator class                                    py
class Generator:                                     
    id_no = 0
    id_list = []
    id_to_generator = dict()
    def __init__(self, name, resource, base_rate,cost):       
        self.name = name                                #Name of Generator
        self.resource = resource                        #Resource Generator makes      
        self.base_rate = base_rate
        self.rate = 0                                #Resource generation rate
        self.last_update = pygame.time.get_ticks()      #Stores time since last update (ms)
        self.cost = cost
        self.id = Generator.id_no
        Generator.id_no += 1
        Generator.id_list.append(self.id)
        Generator.id_to_generator.update({self.id:self})

    def update(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.last_update
        if elapsed > 1000:                              # Update every second
            self.resource.add(self.rate)
            self.last_update = now

    def buy(self):
        if self.resource.purchasable(self.cost):                            #checks if player can purchase generator
            money.amount -= self.cost                            #deducts cost if player can purchase generator
            self.rate += self.base_rate                  #increases production of generator by the rate increase ##

    def get_gen(id_number):
        return Generator.id_to_generator.get(id_number)

#Resource Types
money = Resource("Money", 1)                            #Standard resource to buy upgrades
gems = Resource("Gems", 0)                              #Rare & Premium currency


#Resource Generator                                           
generator1 = Generator("generator1", money, 1,10)          #tier 1 generator
generator2 = Generator("generator2", money, 5,100)          #tier 2 generator
generator3 = Generator("generator3", money, 20,1000)         #tier 3 generator

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
            if 600 <= mouse_x <= 1280 and 0 <= mouse_y <= 720:
                for i in range(Resource.id_no):                                      
                    Resource.get_resource(i).add(Resource.get_resource(i).click_rate)
            elif 15 <= mouse_x <= 200 and 100 <= mouse_y <= 130:      #Purchase generator 1
                generator1.buy()
            elif 15 <= mouse_x <= 200 and 150 <= mouse_y <= 180:   #Purchase generator 2
                generator2.buy()

    
    #Update Resource Generators
    for i in range(Generator.id_no):                                      
        Generator.get_gen(i).update()

    #Fill screen with black
    screen.fill(BLACK)

    #Draw Visuals & Buttons
    draw_text(screen, str(money), 10, 10)                           #Current Resource Amount
    draw_text(screen, str(gems), 150, 10)
    

    pygame.draw.rect(screen, (0, 128, 0), (600, 0, 720, 720))      #Clicking area
    pygame.draw.rect(screen, (0, 128, 0), (15, 100, 200, 30))    #screen, RGB, position(x1,y1,x2,y2)
    draw_text(screen, "Buy Generator 1", 20, 100)
    draw_text(screen, '+' + str(generator1.base_rate) + ' g/s', 225, 100)
    draw_text(screen, 'Current: ' + str(generator1.rate) + 'g/s', 315, 100)
    pygame.draw.rect(screen, (0, 128, 0), (15, 150, 200, 30))
    draw_text(screen, "Buy Generator 2", 20, 150)
    draw_text(screen, '+' + str(generator2.base_rate) + ' g/s', 225, 150)
    draw_text(screen, 'Current: ' + str(generator2.rate) + 'g/s', 315, 150)
    

    #Update Display
    pygame.display.flip()
#Quit Pygame
pygame.quit()
sys.exit()
