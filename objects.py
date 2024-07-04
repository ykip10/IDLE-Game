import pygame

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
    
# Generator class
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
            self.resource.amount -= self.cost                            #deducts cost if player can purchase generator
            self.rate += self.base_rate                  #increases production of generator by the rate increase ##

    def get_gen(id_number):
        return Generator.id_to_generator.get(id_number)

# Resources
gold = Resource("Gold", 1)   
gems = Resource("Gems", 0)  

# Resource Generators                                           
generator1 = Generator("generator1", gold, 1, 10)            # tier 1 generator
generator2 = Generator("generator2", gold, 5, 100)           # tier 2 generator
generator3 = Generator("generator3", gold, 20, 1000)         # tier 3 generator     