import pygame, sys, settings
import objects as o
from collections import defaultdict

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)

rect_coords = defaultdict() # Stores rectangle coordinates for each labelled rectangle 

def x_scaled(x):
    """
    Returns x-coordinate scaled to custom resolutions
    """
    return settings.width * x / settings.NATIVE_WIDTH


def y_scaled(y):
    """
    Returns y-coordinate scaled to custom resolutions
    """
    return settings.height * y / settings.NATIVE_HEIGHT


#Text draw function (replace with images)
def draw_text(surface, text, x, y):                     # surface = screen it draws on
    text_surface = settings.font.render(text, True, WHITE)       
    surface.blit(text_surface, (x_scaled(x), y_scaled(y)))


def draw_button(surface, text, x, y, color = GREEN):
    """
    Draws a button (text + rectangle). (x, y) represent coordinates of start of TEXT. Use this if what you want to draw is a button.
    """
    text_surface = settings.font.render(text, True, WHITE) # Turn text into a surface
    text_rect = text_surface.get_rect() # Find rectangle of the surface 
    rect_coords[text] = (x_scaled(x-5), y_scaled(y), x_scaled(text_rect.width + 10), y_scaled(text_rect.height)) # Map the text label to the corresponding rectangles coordinates 
    pygame.draw.rect(surface, color, rect_coords[text])  # .draw.rect takes arguments (surface, RGB, (x_left, y_top, width, height))
    
    draw_text(surface, text, x, y) # After drawing the rectangle, draw the text. 
       

def in_bounds(text, mouse_x, mouse_y):
    """
    Returns a boolean. Checks if the mouse is inside the bounds of the button 
    """
    return rect_coords[text][0] <= mouse_x <= rect_coords[text][0] + rect_coords[text][2] and rect_coords[text][1] <= mouse_y <= rect_coords[text][1] + rect_coords[text][3]


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
        self.background = BLACK # Background of scene 
    def draw(self): # Draw MAIN scene here 
        screen = self.engine.surface
        screen.fill(self.background)

        pygame.display.set_caption('Main')

        total_rate = 0
        for i in range(o.Generator.id_no):
            total_rate += o.Generator.get_gen(i).rate

        # Resources info
        draw_text(screen, str(o.gold), 10, 10)                           # Current Resource Amount
        draw_text(screen, str(o.gems), 200, 10)                           # Gem count
        draw_text(screen, f'Income: {str(total_rate)}g/s', 390, 10)     # Current income 

        # Clicking area 
        pygame.draw.rect(screen, GREEN, (600, 0, 720, 720))     
        draw_text(screen, f'Click for {o.gold.click_rate} gold!', 850, 360)

        # Shop button
        draw_button(screen, "Shop", 20, 670)

        # Settings button
        draw_button(screen, "Settings", 110, 670)
        
    def on_event(self, event): # Functionality (clicking) of main scene
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Clicking for resources 
            if x_scaled(600) <= mouse_x <=  x_scaled(settings.width) and y_scaled(0) <= mouse_y <= y_scaled(settings.height):
                for i in range(o.Resource.id_no):                                      
                    o.Resource.get_resource(i).add(o.Resource.get_resource(i).click_rate)
            # Buy Generator Buttons
            elif in_bounds('Shop', mouse_x, mouse_y):    # "Shop" button
                self.engine.Transition.next_scene = shop_scene(self.engine)
            elif in_bounds('Settings', mouse_x, mouse_y):
                self.engine.Transition.next_scene = settings_scene(self.engine)
            

class shop_scene(scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.background = BLACK  
    def draw(self): # Draw SHOP scene here 
        screen = self.engine.surface
        screen.fill(self.background)

        pygame.display.set_caption('Shop')

        draw_text(screen, str(o.gold), 10, 10)                            # Current Resource Amount
        draw_text(screen, str(o.gems), 200, 10)                           # Gem count

        # Drawing "Return" button
        draw_button(screen, "Return",  20, 670)
        
        # Drawing Upgrade buttons/text 
        draw_text(screen, "Generators", 20, 50)
        draw_text(screen, "Click Upgrades", 650, 50)

        draw_button(screen, "Buy Generator 1", 20, 90)
        draw_text(screen, '+' + str(o.generator1.base_rate) + ' g/s', 225, 90)
        draw_text(screen, 'Current: ' + str(o.generator1.rate) + 'g/s', 315, 90)
        draw_button(screen, "Buy Generator 2", 20, 140)
        draw_text(screen, '+' + str(o.generator2.base_rate) + ' g/s', 225,  140)
        draw_text(screen, 'Current: ' + str(o.generator2.rate) + 'g/s', 315, 140)

        draw_button(screen, "Buy Clicker 1", 650, 90)
        draw_text(screen, '+' + str(o.clicker1.base_rate) + ' g/click', 815,  90)
        draw_text(screen, 'Current: ' + str(o.clicker1.rate) + 'g/click', 940, 90)
        draw_button(screen, "Buy Clicker 2", 650, 140)
        draw_text(screen, '+' + str(o.clicker2.base_rate) + ' g/click', 815,  140)
        draw_text(screen, 'Current: ' + str(o.clicker2.rate) + 'g/click', 940, 140)

    def on_event(self, event): # Functionality (clicking) of shop scene
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if in_bounds('Return', mouse_x, mouse_y): # "Return" button
                self.engine.Transition.next_scene = main_scene(self.engine) 
            elif in_bounds("Buy Clicker 1", mouse_x, mouse_y):
                o.clicker1.buy()
            elif in_bounds("Buy Clicker 2", mouse_x, mouse_y):
                o.clicker2.buy()
            elif in_bounds('Buy Generator 1', mouse_x, mouse_y):   # Purchase generator 1
                o.generator1.buy()
            elif in_bounds('Buy Generator 2', mouse_x, mouse_y):   # Purchase generator 2
                o.generator2.buy()


class settings_scene(scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.background = BLACK  # Background of scene 
    def draw(self): # Drawing of shop scene
        pygame.display.set_caption('Settings')
        screen = self.engine.surface
        screen.fill(self.background)
        # Drawing "Return" button
        draw_button(screen, "Return",  20, 670)
    def on_event(self, event): # Functionality (clicking) of shop scene
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if in_bounds('Return', mouse_x, mouse_y): # "Return" button
                self.engine.Transition.next_scene = main_scene(self.engine) 