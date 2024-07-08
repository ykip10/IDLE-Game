import pygame, sys, settings, mobs as mobs
import resources as r
from collections import defaultdict

pygame.init()



rect_coords = defaultdict() # Stores rectangle coordinates for each labelled rectangle 

def x_scaled(x):
    """
    Returns x-  coordinate scaled to custom resolutions
    """
    return settings.width * x / settings.NATIVE_WIDTH


def y_scaled(y):
    """
    Returns y-coordinate scaled to custom resolutions
    """
    return settings.height * y / settings.NATIVE_HEIGHT


#Text draw function (replace with images)
def draw_text(surface, text, x, y):                     # surface = screen it draws on
    text_surface = settings.font.render(text, True, settings.WHITE)       
    surface.blit(text_surface, (x_scaled(x), y_scaled(y)))


def draw_button(surface, text, x, y, color = settings.GREEN):
    """
    Draws a button (text + rectangle). (x, y) represent coordinates of start of TEXT. Use this if what you want to draw is a button.
    """
    text_surface = settings.font.render(text, True, settings.WHITE) # Turn text into a surface
    text_rect = text_surface.get_rect() # Find rectangle of the surface 
    rect_coords[text] = (x_scaled(x-5), y_scaled(y), x_scaled(text_rect.width + 10), y_scaled(text_rect.height)) # Map the text label to the corresponding rectangles coordinates 
    pygame.draw.rect(surface, color, rect_coords[text])  # .draw.rect takes arguments (surface, RGB, (x_left, y_top, width, height))
    
    draw_text(surface, text, x, y) # After drawing the rectangle, draw the text. 
       

def in_bounds(text, mouse_x, mouse_y):
    """
    Returns a boolean. Checks if the mouse is inside the bounds of the button 
    """
    return rect_coords[text][0] <= mouse_x <= rect_coords[text][0] + rect_coords[text][2] and rect_coords[text][1] <= mouse_y <= rect_coords[text][1] + rect_coords[text][3]


def load_slime_sheet():
    sheet = pygame.image.load(r'sprites/slimes/slime-Sheet.png').convert_alpha()
    return sheet 


def get_mob_frame(sheet, size, row, column, colour):
    frame = pygame.Surface((size[0], size[1])).convert_alpha()
    frame.fill(colour)
    frame.blit(sheet, (0, 0), (row*size[0], column*size[1], size[0], size[1]))
    frame = pygame.transform.scale(frame, (settings.MOB_HEIGHT, settings.MOB_SIZE))
    return frame


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

            for i in range(r.Generator.id_no):
                r.Generator.get_gen(i).update() # Update money 

            self.Transition.current.draw() # Draw the current scene 
            self.clock.tick(settings.fps)
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
        self.background = settings.MAIN_BACKGROUND # Background of scene 

        # Load mob sheets
        self.slime_sheet = load_slime_sheet()
        self.curr_frame = get_mob_frame(self.slime_sheet, (32, 32), 1, 0, settings.MAIN_BACKGROUND)
        self.curr_mob = mobs.Mob(self.curr_frame, 'Slime', 1)

        
    def draw(self): # Draw MAIN scene here 
        screen = self.engine.surface
        screen.fill(self.background)

        pygame.display.set_caption('Main')

        total_rate = 0
        for i in range(r.Generator.id_no):
            total_rate += r.Generator.get_gen(i).rate

        # Resources info
        draw_text(screen, str(r.gold), 10, 10)                           # Current Resource Amount
        draw_text(screen, str(r.gems), 200, 10)                           # Gem count
        draw_text(screen, f'Income: {str(total_rate)}g/s', 390, 10)     # Current income 

        # Clicking area 
        pygame.draw.rect(screen, settings.DARK_GREEN, (x_scaled(600), y_scaled(0), x_scaled(720), y_scaled(720)))     
        draw_text(screen, f'Click for {r.gold.click_rate} gold!', 850, 360)

        # Shop button
        draw_button(screen, "Shop", 20, 670)

        # Settings button
        draw_button(screen, "Settings", 100, 670)

        self.curr_mob.draw(screen, 210, 340)
        self.curr_mob.stats.combat_bar.update(screen)
        #self.combat_bar = r.Combat_Bar(10, 0, 5, 0)
        
    def on_event(self, event): # Functionality (clicking) of main scene
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.curr_mob.stats.combat_bar.goal:
                self.curr_mob.damage(2)
                self.curr_mob.stats.combat_bar.reset()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Clicking for resources 
            if x_scaled(600) <= mouse_x <=  x_scaled(settings.width) and y_scaled(0) <= mouse_y <= y_scaled(settings.height):
                for i in range(r.Resource.id_no):                                      
                    r.Resource.get_resource(i).add(r.Resource.get_resource(i).click_rate)
            # Buy Generator Buttons
            elif in_bounds('Shop', mouse_x, mouse_y):    # "Shop" button
                self.engine.Transition.next_scene = shop_scene(self.engine)
            elif in_bounds('Settings', mouse_x, mouse_y):
                self.engine.Transition.next_scene = settings_scene(self.engine)
        
        
            

class shop_scene(scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.background = settings.MAIN_BACKGROUND   
    def draw(self): # Draw SHOP scene here 
        screen = self.engine.surface
        screen.fill(self.background)

        pygame.display.set_caption('Shop')

        draw_text(screen, str(r.gold), 10, 10)                            # Current Resource Amount
        draw_text(screen, str(r.gems), 200, 10)                           # Gem count

        # Drawing "Return" button
        draw_button(screen, "Return",  20, 670)
        
        # Drawing Upgrade buttons/text 
        draw_text(screen, "Generators", 20, 50)
        draw_text(screen, "Click Upgrades", 650, 50)

        draw_button(screen, "Buy Generator 1", 20, 90)
        draw_text(screen, '+' + str(r.generator1.base_rate) + ' g/s', 225, 90)
        draw_text(screen, 'Current: ' + str(r.generator1.rate) + 'g/s', 315, 90)
        draw_button(screen, "Buy Generator 2", 20, 140)
        draw_text(screen, '+' + str(r.generator2.base_rate) + ' g/s', 225,  140)
        draw_text(screen, 'Current: ' + str(r.generator2.rate) + 'g/s', 315, 140)

        draw_button(screen, "Buy Clicker 1", 650, 90)
        draw_text(screen, '+' + str(r.clicker1.base_rate) + ' g/click', 815,  90)
        draw_text(screen, 'Current: ' + str(r.clicker1.rate) + 'g/click', 940, 90)
        draw_button(screen, "Buy Clicker 2", 650, 140)
        draw_text(screen, '+' + str(r.clicker2.base_rate) + ' g/click', 815,  140)
        draw_text(screen, 'Current: ' + str(r.clicker2.rate) + 'g/click', 940, 140)

    def on_event(self, event): # Functionality (clicking) of shop scene
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if in_bounds('Return', mouse_x, mouse_y): # "Return" button
                self.engine.Transition.next_scene = main_scene(self.engine) 
            elif in_bounds("Buy Clicker 1", mouse_x, mouse_y):
                r.clicker1.buy()
            elif in_bounds("Buy Clicker 2", mouse_x, mouse_y):
                r.clicker2.buy()
            elif in_bounds('Buy Generator 1', mouse_x, mouse_y):   # Purchase generator 1
                r.generator1.buy()
            elif in_bounds('Buy Generator 2', mouse_x, mouse_y):   # Purchase generator 2
                r.generator2.buy()


class settings_scene(scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.background = settings.MAIN_BACKGROUND   # Background of scene 
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