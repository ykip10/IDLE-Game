import pygame, sys, settings, mobs, player, utility as u
import resources as r
import utility as u
from collections import defaultdict

pygame.init()


rect_coords = defaultdict() # Stores rectangle coordinates for each labelled rectangle 

def draw_button(surface, text, x, y, color = settings.GREEN):
    """
    Draws a button (text + rectangle). (x, y) represent coordinates of start of TEXT. Use this if what you want to draw is a button.
    """
    text_surface = settings.font.render(text, True, settings.WHITE) # Turn text into a surface
    text_rect = text_surface.get_rect() # Find rectangle of the surface 
    rect_coords[text] = (u.x_scaled(x-5), u.y_scaled(y), u.x_scaled(text_rect.width + 10), u.y_scaled(text_rect.height)) # Map the text label to the corresponding rectangles coordinates 
    pygame.draw.rect(surface, color, rect_coords[text])  # .draw.rect takes arguments (surface, RGB, (x_left, y_top, width, height))
    
    u.draw_text(surface, text, x, y) # After drawing the rectangle, draw the text. 
       

def in_bounds(text, mouse_x, mouse_y):
    """
    Returns a boolean. Checks if the mouse is inside the bounds of the button 
    """
    return rect_coords[text][0] <= mouse_x <= rect_coords[text][0] + rect_coords[text][2] and rect_coords[text][1] <= mouse_y <= rect_coords[text][1] + rect_coords[text][3]


def show_hp(surface, player):
    ''' Shows hp bar. ''' 
    hp_bar_width, hp_bar_height = 300, 50 
    hp_x, hp_y = 50, 300

    text = f'HP: {player.curr_hp}/{player.hp}'
    text_surface = settings.font.render(text, True, settings.WHITE) # 
    text_rect = text_surface.get_rect()

    hp_bar_rect = pygame.Rect(u.x_scaled(hp_x) , u.y_scaled(hp_y), u.x_scaled(hp_bar_width), u.y_scaled(hp_bar_height))
    pygame.draw.rect(surface, settings.RED, hp_bar_rect)
    u.draw_text(surface, f'HP: {player.curr_hp}/{player.hp}', u.x_scaled(hp_x + hp_bar_width / 2 - text_rect.width / 2), u.y_scaled(hp_y + hp_bar_height / 2 - text_rect.height / 2)) # draws text in the MIDDLE of the hp bar
        


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
        self.player = player.Player(0, 'Skippay')

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

        # Load images 
        self.slime_sheet = pygame.image.load(r'sprites/slimes/slime-Sheet.png').convert_alpha()
        self.atk_icon = pygame.image.load(r'sprites/icons/attack_icon.png').convert_alpha()

        self.curr_frame = u.get_mob_frame(self.slime_sheet, (32, 32), 1, 0, settings.MAIN_BACKGROUND)
        self.curr_mob = mobs.Mob(self.curr_frame, 'Slime', 1, 0)
        
    def draw(self): # Draw MAIN scene here 
        screen = self.engine.surface
        screen.fill(self.background)

        pygame.display.set_caption('Main')

        total_rate = 0
        for i in range(r.Generator.id_no):
            total_rate += r.Generator.get_gen(i).rate

        # Resources info
        u.draw_text(screen, str(r.gold), 10, 10)                                   # Current Resource Amount
        u.draw_text(screen, str(r.gems), 200, 10)                           # Gem count
        u.draw_text(screen, f'Income: {str(total_rate)}g/s', 410, 10)     # Current income 

        # Work button
        draw_button(screen, "Go to work", 1130, 670)

        # Shop button
        draw_button(screen, "Shop", 20, 670)

        # Settings button
        draw_button(screen, "Settings", 100, 670)

        # Draw mob + combat bar
        self.curr_mob.draw(screen, 810, 340)
        
        # HUD
        show_hp(screen, self.engine.player)
        
    def on_event(self, event): # Functionality (clicking) of main scene
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.curr_mob.stats.combat_bar.goal:
                self.curr_mob.damage(2)
                self.curr_mob.stats.combat_bar.reset()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Clicking for resources 
            if in_bounds('Go to work', mouse_x, mouse_y):
                self.engine.Transition.next_scene = working_scene(self.engine)
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

        u.draw_text(screen, str(r.gold), 10, 10)                            # Current Resource Amount
        u.draw_text(screen, str(r.gems), 200, 10)                           # Gem count

        # Drawing "Return" button
        draw_button(screen, "Return",  20, 670)
        
        # Drawing Upgrade buttons/text 
        u.draw_text(screen, "Generators", 20, 50)
        u.draw_text(screen, "Click Upgrades", 650, 50)

        draw_button(screen, "Buy Generator 1", 20, 90)
        u.draw_text(screen, '+' + str(r.generator1.base_rate) + ' g/s', 225, 90)
        u.draw_text(screen, 'Current: ' + str(r.generator1.rate) + 'g/s', 315, 90)
        draw_button(screen, "Buy Generator 2", 20, 140)
        u.draw_text(screen, '+' + str(r.generator2.base_rate) + ' g/s', 225,  140)
        u.draw_text(screen, 'Current: ' + str(r.generator2.rate) + 'g/s', 315, 140)

        draw_button(screen, "Buy Clicker 1", 650, 90)
        u.draw_text(screen, '+' + str(r.clicker1.base_rate) + ' g/click', 815,  90)
        u.draw_text(screen, 'Current: ' + str(r.clicker1.rate) + 'g/click', 940, 90)
        draw_button(screen, "Buy Clicker 2", 650, 140)
        u.draw_text(screen, '+' + str(r.clicker2.base_rate) + ' g/click', 815,  140)
        u.draw_text(screen, 'Current: ' + str(r.clicker2.rate) + 'g/click', 940, 140)

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

        #Scientific Notation Stuff
        pygame.draw.rect(screen, settings.WHITE, (20, 55, 20, 20), 2)   # Draws check box corresponding to scientific notation
        if settings.show_scientific_notation == True:
            draw_button(screen, f"Toggle Scientific Notation: {settings.show_scientific_notation} ", 50, 50) # Draws Scientific Notation Button as green
            pygame.draw.line(screen, settings.WHITE, (20,75), (40,55), 2) #ticks box if S.N is toggled
        elif settings.show_scientific_notation == False:
            draw_button(screen, f"Toggle Scientific Notation: {settings.show_scientific_notation} ", 50, 50, settings.RED) # Draws Scientific Notation Button as red
            
        # Drawing "Return" button
        draw_button(screen, "Return",  20, 670)
    #Events    
    def on_event(self, event): # Functionality (clicking) of settings scene
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if in_bounds('Return', mouse_x, mouse_y): # "Return" button
                self.engine.Transition.next_scene = main_scene(self.engine)
            elif in_bounds(f"Toggle Scientific Notation: {settings.show_scientific_notation} ", mouse_x, mouse_y): # "Scientific Notation Toggle Button"
                settings.show_scientific_notation = not settings.show_scientific_notation
            

class working_scene(scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.background = settings.MAIN_BACKGROUND
        self.work = mobs.Work_Bar(0, 0.01, 0) # Initialise the working bar

    def draw(self): 
        pygame.display.set_caption('Working')
        screen = self.engine.surface
        screen.fill(self.background)

        draw_button(screen, 'Return', 20, 670) # Draw return button

        u.draw_text(screen, str(r.gold), 10, 10) # Show gold 
        self.work.update(screen) # Update the working bar

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if in_bounds('Return', mouse_x, mouse_y):
                self.engine.Transition.next_scene = main_scene(self.engine)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.work.reset()
        
            

