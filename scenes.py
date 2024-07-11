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


def show_hud(surface, player, atk_icon, background):
    ''' Shows hud (atk_icon and HP bar). ''' 

    # Hp bar
    hp_bar_width, hp_bar_height = 300, 50 
    hp_x, hp_y = 10, 70

    text = f'HP: {player.curr_hp}/{player.hp}'
    text_surface = settings.font.render(text, True, settings.WHITE) # 
    text_rect = text_surface.get_rect()

    hp_bar_rect = pygame.Rect(u.x_scaled(hp_x) , u.y_scaled(hp_y), u.x_scaled(hp_bar_width)* player.curr_hp / player.hp , u.y_scaled(hp_bar_height))
    pygame.draw.rect(surface, settings.RED, hp_bar_rect)
    u.draw_text(surface, f'HP: {player.curr_hp}/{player.hp}', u.x_scaled(hp_x + hp_bar_width / 2 - text_rect.width / 2), u.y_scaled(hp_y + hp_bar_height / 2 - text_rect.height / 2)) # draws text in the MIDDLE of the hp bar
    
    # Drawing attack icon and corresponding string 
    text = f'{player.atk}'
    font = pygame.font.Font(None, 48) # font
    if player.can_attack: 
        text_surface = font.render(text, True, settings.WHITE)
    else: 
        text_surface = font.render(text, True, settings.BLACK)

    atk_icon_surface = u.image_to_surface(atk_icon, (32, 32), (64, 64), background)
    atk_icon_x = settings.combat_bar_x + (settings.combat_bar_width - atk_icon_surface.get_width() + text_surface.get_width()) / 2 
    atk_icon_y = settings.combat_bar_y + settings.combat_bar_height + 15 # +10 to account for the goal bar
    text_x = atk_icon_x - text_surface.get_width() + 10 
    text_y = atk_icon_y + (atk_icon_surface.get_height() - text_surface.get_height()) / 2 
    surface.blit(atk_icon_surface, dest = (atk_icon_x, atk_icon_y))
    surface.blit(text_surface, dest = (text_x, text_y))


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
        
        # Mobs
        self.slime_sheet = pygame.image.load(r'sprites/slimes/slime-Sheet.png').convert_alpha()
        self.curr_frame = u.get_mob_frame(self.slime_sheet, (32, 32), 1, 0, settings.MAIN_BACKGROUND)
        self.mob_rotation = mobs.mob_rotation([self.curr_frame]*10, self.player)
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

            # On mob death, change mobs 
            if self.mob_rotation.curr_mob.current_hp <= 0:
                self.player.can_attack = True 
                self.player.curr_hp = self.player.hp
                self.mob_rotation.rotate()

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
        self.mob_rotation = mobs.mob_rotation([self.curr_frame]*10, self.engine.player)

        
    def draw(self): # Draw MAIN scene here 
        screen = self.engine.surface
        screen.fill(self.background)

        mob = self.engine.mob_rotation.curr_mob
        player = self.engine.player

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

        # Draw mob + combat bar. Also need to check if the player should take damage. 
        mob.draw(screen, 810, 340)

        if mob.stats.combat_bar.hit_right or mob.stats.combat_bar.hit_left: # If the bar is in etiher boundary, check if it has already attacked before dishing out damage 
            if mob.can_attack:
                player.damage(mob.stats.atk)
                mob.can_attack = False 
                player.can_attack = True
        else:
            mob.can_attack = True 
    
        # Show hud 
        show_hud(screen, player, self.atk_icon, self.background)

        # On player death, reset mobs and players hp
        if player.curr_hp <= 0:
            player.can_attack = True
            mob.current_hp = mob.stats.hp
            player.curr_hp = player.hp

        
    def on_event(self, event): # Functionality (clicking) of main scene
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            mob = self.engine.mob_rotation.curr_mob
            player = self.engine.player
            if player.can_attack:
                if mob.stats.combat_bar.goal:
                    # Fading text would be useful here as well (Perfect!)
                    mob.damage(self.engine.player.atk)
                    player.can_attack = False
                    mob.stats.combat_bar.reset() # resets goal bar 
                else: 
                    # Want to display some fading text as well like Missed! need write a function for that, many use cases 
                    player.damage(mob.stats.atk) # Enemy attacks 
                    player.can_attack = False
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
                self.engine.mob_rotation.curr_mob.current_hp = self.engine.mob_rotation.curr_mob.stats.hp
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
        self.work = mobs.Work_Bar(0, 0.02, 0) # Initialise the working bar

    def draw(self): 
        pygame.display.set_caption('Working')
        screen = self.engine.surface
        screen.fill(self.background)

        draw_button(screen, 'Return', 20, 670) # Draw return button

        u.draw_text(screen, str(r.gold), 10, 10) # Show gold 
        self.work.update(screen) # Update the working bar

        u.draw_text(screen, f'x{self.work.combo - 1}!', 1000, 600)
    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if in_bounds('Return', mouse_x, mouse_y):
                self.engine.Transition.next_scene = main_scene(self.engine)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Need fade away text everywhere here :D
                if self.work.goal1:
                    r.gold.amount += 3*self.work.combo 
                    self.work.combo += 2
                elif self.work.goal2:
                    r.gold.amount += 2*self.work.combo
                    self.work.combo += 1
                elif self.work.goal3:
                    r.gold.amount += self.work.combo
                else:
                    self.work.combo = 1
                self.work.hard_reset()
        