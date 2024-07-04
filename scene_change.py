import pygame, sys, settings
import objects as o

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def x(x):
    """
    Returns x-coordinate scaled to custom resolutions
    """
    return settings.width * x / settings.NATIVE_WIDTH


def y(y):
    """
    Returns y-coordinate scaled to custom resolutions
    """
    return settings.height * y / settings.NATIVE_HEIGHT


#Text draw function (replace with images)
def draw_text(surface, text, x, y):                     #surface = screen it draws on
    text_surface = settings.font.render(text, True, WHITE)       
    surface.blit(text_surface, (x, y))


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
            self.Transition.update()
            for event in pygame.event.get():
            #Quit Pygame
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  
                else:
                    self.Transition.current.on_event(event) # Execute event based on scene 

            for i in range(o.Generator.id_no):
                o.Generator.get_gen(i).update() # Update money 

            self.Transition.current.draw() # Draw the current scene 
            pygame.display.flip() # Update Display 

    def run(self, state):
        self.Transition.current = state
        self.loop()


class scene: 
    def __init__(self, engine): 
        self.engine = engine
    def draw(self): pass
    def on_event(self, event): pass 


class main_scene(scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.background = BLACK
    def draw(self): # Drawing of main scene 
        screen = self.engine.surface
        screen.fill(self.background)

        total_rate = 0
        for i in range(o.Generator.id_no):
            total_rate += o.Generator.get_gen(i).rate

        # Resources info
        draw_text(screen, str(o.money), x(10), y(10))                           # Current Resource Amount
        draw_text(screen, str(o.gems), x(200), y(10))                           # Gem count
        draw_text(screen, f'Income: {str(total_rate)}g/s', x(390), y(10))     # Current income 

        # Clicking area 
        pygame.draw.rect(screen, (0, 128, 0), (x(600), y(0), x(720), y(720)))     

        # Generators information
        pygame.draw.rect(screen, (0, 128, 0), (x(15), y(100), x(200), y(30)))      # screen, RGB, position(x1,y1,x2,y2)
        draw_text(screen, "Buy Generator 1", x(20), y(100))
        draw_text(screen, '+' + str(o.generator1.base_rate) + ' g/s', x(225), y(100))
        draw_text(screen, 'Current: ' + str(o.generator1.rate) + 'g/s', x(315), y(100))
        pygame.draw.rect(screen, (0, 128, 0), (x(15), y(150), x(200), y(30)))
        draw_text(screen, "Buy Generator 2", x(20), y(150))
        draw_text(screen, '+' + str(o.generator2.base_rate) + ' g/s', x(225),  y(150))
        draw_text(screen, 'Current: ' + str(o.generator2.rate) + 'g/s', x(315), y(150))

        # Shop button
        pygame.draw.rect(screen, (0, 128, 0), (x(15), y(670), x(80), y(30)))
        draw_text(screen, "Shop", x(20), y(670))
    def on_event(self, event): # Functionality (clicking) of main scene
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Clicking for resources 
            if x(600) <= mouse_x <=  x(settings.width) and y(0) <= mouse_y <= y(settings.height):
                for i in range(o.Resource.id_no):                                      
                    o.Resource.get_resource(i).add(o.Resource.get_resource(i).click_rate)
            # Buy Generator Buttons
            elif x(15) <= mouse_x <= x(200) and y(100) <= mouse_y <= y(130):   #Purchase generator 1
                o.generator1.buy()
            elif x(15) <= mouse_x <= x(200) and y(150) <= mouse_y <= y(180):   #Purchase generator 2
                o.generator2.buy()
            elif x(15) <= mouse_x <= x(95) and y(670) <= mouse_y <= y(700):    # "Shop" button
                self.engine.Transition.next_scene = shop_scene(self.engine)


class shop_scene(scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.background = BLACK
    def draw(self): # Drawing of shop scene
        screen = self.engine.surface
        screen.fill(self.background)
        pygame.draw.rect(screen, (0, 128, 0), (x(15), y(670), x(90), y(30)))
        draw_text(screen, "Return", x(20), y(670))
    def on_event(self, event): # Functionality (clicking) of shop scene
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if x(15) <= mouse_x <= x(105) and y(670) <= mouse_y <= y(700): # "Return" button
                self.engine.Transition.next_scene = main_scene(self.engine) 
        