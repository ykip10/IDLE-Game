import pygame, sys, settings
from main import x, y

# Need something that runs the loop, something that executes specific commands for each scene. 

# While True:
#    engine(Scene)
#        
#
#
#

class Transition:
    def __init__(self):
        self.current = None
        self.next_scene = None

    def update(self):
        if self.next_scene:
            self.current = self.next_scene
            self.next_scene = None

class DisplayEngine:
    def __init__(self):
        self.fps = settings.fps
        self.surface = pygame.display.set_mode((settings.width, settings.height))
        self.clock = pygame.time.Clock()
        self.delta = 0 
        self.Transition = Transition()

    def loop(self):
        while True:
            for event in pygame.event.get():
            #Quit Pygame
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    self.Transition.current.on_event(event)
            
            self.Transition.current.draw(self.surface)

class Scene: 
    def __init__(self): pass
    def draw(self, surface): pass
    def on_event(self, event): pass 
        
class main_scene(Scene):
    def __init__(self, background):
        self.background = background
    def draw(self, surface):
        self.surface = surface
    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Clicking for resources 
            if x(600) <= mouse_x <=  x(width) and y(0) <= mouse_y <= y(height):
                for i in range(Resource.id_no):                                      
                    Resource.get_resource(i).add(Resource.get_resource(i).click_rate)
            # Buy Generator Buttons
            elif x(15) <= mouse_x <= x(200) and y(100) <= mouse_y <= y(130):      #Purchase generator 1
                generator1.buy()
            elif x(15) <= mouse_x <= x(200) and y(150) <= mouse_y <= y(180):   #Purchase generator 2
                generator2.buy()
        