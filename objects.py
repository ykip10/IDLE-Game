import pygame, scenes, settings

# Resources Class
class Resource:
    id_no = 0
    id_list = []
    id_to_resource = dict()
    def __init__(self, name, click_rate):
        self.name = name                                # Name of Resource
        self.amount = 0                                 # Resource Amount
        self.click_rate = click_rate        
        self.id = Resource.id_no
        Resource.id_no += 1
        Resource.id_list.append(self.id)
        Resource.id_to_resource.update({self.id:self})

    def add(self, amount):
        self.amount += amount                           # Increase resource value by "amount"

    def __str__(self):
        return f"{self.name}: {self.amount}"            # Returns resource name and amount
    
    def purchasable(self,price):
        return self.amount >= price

    def get_resource(id_number):
        return Resource.id_to_resource.get(id_number)

class Upgrade:
    def __init__(self, name, resource, cost):
        self.name = name
        self.resource = resource
        self.cost = cost
        self.effect = None # Generally will be a function for more complex upgrades. Simple upgrades like generator and clicking upgrades won't use this
    def apply_effect(self):
        pass
    def buy(self):
        if self.resource.purchasable(self.cost) and not self.effect:              # checks if player can purchase upgrade
            self.resource.amount -= self.cost            # deducts cost if player can purchase upgrade
            self.apply_effect()                                 # performs the effect of the upgrade  


# Generator class
class Generator(Upgrade):                                     
    id_no = 0
    id_list = []
    id_to_generator = dict()
    def __init__(self, name, resource, base_rate, cost):       
        super().__init__(name,  resource, cost)
        self.base_rate = base_rate
        self.rate = 0                                                # Resource generation rate
        self.last_update = pygame.time.get_ticks()      #Stores time since last update (ms)
        self.id = Generator.id_no
        Generator.id_no += 1
        Generator.id_list.append(self.id)
        Generator.id_to_generator.update({self.id:self})
    
    def apply_effect(self):
        self.rate += self.base_rate

    def buy(self):
        super().buy() 

    def update(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.last_update
        if elapsed > 1000:                              # Update every second
            self.resource.add(self.rate)
            self.last_update = now

    def get_gen(id_number):
        return Generator.id_to_generator.get(id_number)

# Clicking upgrades class
class Clicking(Upgrade):
    id_no = 0
    id_list = []
    id_to_clicker = {}
    def __init__(self, name, resource, base_rate, cost):
        super().__init__(name, resource, cost)
        self.base_rate = base_rate
        self.rate = 0
        self.id = Clicking.id_no
        Clicking.id_no += 1
        Clicking.id_list.append(self.id)
        Clicking.id_to_clicker.update({self.id:self})
    def apply_effect(self):
        self.rate += self.base_rate
        self.resource.click_rate += self.base_rate

    def buy(self):
        super().buy()

    def get_clicker(id_no):
        return Upgrade.id_to_clicker.get(id_no)

# Resources
gold = Resource("Gold", 1)   
gems = Resource("Gems", 0)  

# Generator upgrades                                           
generator1 = Generator("generator1", gold, 1, 10)            # tier 1 generator
generator2 = Generator("generator2", gold, 5, 100)           # tier 2 generator
generator3 = Generator("generator3", gold, 20, 1000)         # tier 3 generator     

# Clicking upgrades 
clicker1 = Clicking("clicker1", gold, 1, 10)
clicker2 = Clicking("clicker2", gold, 5, 100)


# Combat stuff 
class Combat_Bar: 
    def __init__(self, surface, width, speed, acceleration, jerk, colour):
        """ Speed refers to the initial speed of the combat indicator, acceleration refers to the acceleration of the combat indicator, 
        colour refers to the colour of the bar. 
        """
        self.surface = surface
        self.width = width
        self.speed = speed # Speed of combat indicator (pixels/s)
        self.acceleration = acceleration # Acceleration of combat indicator (pixels/s^2)
        self.jerk = jerk # d^3x/dt^3
        self.x = settings.x_bar # Starting x position of combat indicator 

        self.bar = pygame.Surface((settings.bar_width, settings.bar_height))
        self.bar.fill(colour)
        
        
    def draw(self, x):
        """ x is the x-coordinate of the combat indicator. width, height refer to the width  
        sliding combat INDICATOR. Draws the bar + combat indicator. 
        """
        self.surface.blit(self.bar, dest = (settings.x_bar, settings.y_bar))
        pygame.draw.rect(self.surface, scenes.WHITE, (x, settings.y_bar - 10, self.width, settings.bar_height + 20))

    def update(self):
        if self.x <= settings.x_bar + (settings.bar_width / 2):
            self.x += self.speed
            self.speed += self.acceleration
            self.acceleration += self.jerk
        elif self.x >= settings.x_bar + (settings.bar_width / 2):
            self.x += self.speed 
            self.speed -= self.acceleration
            self.acceleration -= self.jerk
        elif self.x >= settings.x_bar + settings.bar_width:
            self.speed = -self.speed
            self.acceleration = -self.acceleration
            self.jerk = -self.jerk

            self.x += self.speed
            self.speed += self.acceleration
            self.acceleration += self.jerk 
        elif self.x <= settings.x_bar: 
            self.speed = -self.speed
            self.acceleration = -self.acceleration
            self.jerk = -self.jerk

            self.x += self.speed
            self.speed += self.acceleration
            self.acceleration += self.jerk 
        self.draw(self.x)
        


#class Mob:
#    def __init__(self, sprite, name, hp, atk, level, combat_bar):
 #       self.sprite = sprite
  #      self.name = name 
#        self.hp = hp
   #     self.atk = atk
  #      self.combat_bar = Combat_bar()
    
    
