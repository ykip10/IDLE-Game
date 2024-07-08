import pygame, settings, scenes, math, numpy as np

# https://stackoverflow.com/questions/62336555/how-to-add-color-gradient-to-rectangle-in-pygame
def hor_gradientRect(surface, left_colour, right_colour, target_rect):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface((2, 2))                                   # tiny! 2x2 bitmap
    pygame.draw.line(colour_rect, left_colour, (0, 0), (0, 1))            # left colour line
    pygame.draw.line(colour_rect, right_colour, (1, 0), (1, 1))            # right colour line
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))  # stretch!
    surface.blit(colour_rect, target_rect)                  


def ver_gradientRect(surface, bottom_colour, top_colour, target_rect):
    """ Draw a Vertical-gradient filled rectangle covering <target_rect> """
    colour_rect = colour_rect = pygame.Surface((2, 2))
    pygame.draw.line(colour_rect, bottom_colour, (0, 0), (1, 0))
    pygame.draw.line(colour_rect, top_colour, (0, 1), (1, 1))
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))
    surface.blit(colour_rect, target_rect)

# Combat stuff 
class Bar: # Only supports 1 dimensional motion in x or y direction 
    def __init__(self, ini_speed, ini_acceleration, jerk):
        """ Width refers to the width of the """
        self.ini_speed = ini_speed
        self.speed = ini_speed # Speed of combat indicator (pixels/s)
        self.ini_acceleration = ini_acceleration
        self.acceleration = ini_acceleration # Acceleration of combat indicator (pixels/s^2)
        self.jerk = jerk # d^3x/dt^3

        self.dest = () # Destination of top left of bar
        self.bar = None # Bar to be drawn 
    def draw(self, surface): 
        surface.blit(self.bar, dest = self.dest) # Draws the bar 

        # Other drawings need to be specified in the subclass
    def update(self, surface): 
        # speed etc. logic here
        pass 


class Combat_Bar(Bar): 
    def __init__(self, goal_width, width, ini_speed, ini_acceleration, jerk):
        """ Speed refers to the initial speed of the combat indicator, acceleration refers to the acceleration of the combat indicator, 
        colour refers to the colour of the bar. 
        """
        super().__init__(ini_speed, ini_acceleration, jerk)

        self.width = width 
        self.x = settings.x_bar # Starting x position of combat indicator
        
        self.bar = pygame.Surface((settings.bar_width, settings.bar_height))
        self.bar.fill(settings.DARK_BLUE)
        self.dest = (settings.x_bar, settings.y_bar)

        offset = 30 
        self.goal_width = goal_width
        self.goal_bar = (settings.x_bar + (settings.bar_width - self.width) / 2 - offset, settings.y_bar - 10, self.goal_width, settings.bar_height + 20)
        self.goal = False
    def draw(self, surface):
        """ x is the x-coordinate of the combat indicator. width, height refer to the width  
        sliding combat INDICATOR. Draws the bar + combat indicator. 
        """
        super().draw(surface)

        # Drawing of goal bar and combat indicator 
        pygame.draw.rect(surface, settings.GREEN, self.goal_bar)
        pygame.draw.rect(surface, settings.WHITE, (self.x, settings.y_bar - 10, self.width, settings.bar_height + 20))

    def update(self, surface):
        if settings.x_bar <= self.x <= settings.x_bar + (settings.bar_width - self.width ) / 2: # In first half 
            self.x += self.speed
            self.speed += self.acceleration
            self.acceleration = abs(self.acceleration)
            self.acceleration += self.jerk
        elif settings.x_bar + (settings.bar_width - self.width ) / 2 <= self.x  <= settings.x_bar + settings.bar_width - self.width: # In second half 
            self.x += self.speed
            self.acceleration = -abs(self.acceleration)
            self.speed += self.acceleration
            self.acceleration -= self.jerk
        elif self.x >= settings.x_bar + settings.bar_width - self.width: # Past right border
            self.x += self.speed 
            self.speed = -abs(self.ini_speed)
            self.speed += self.acceleration
            self.acceleration -= self.jerk 
        elif self.x <= settings.x_bar: # Past left border
            self.x += self.speed    
            self.speed = abs(self.ini_speed) 
            self.speed += self.acceleration
            self.acceleration += self.jerk 

        # Check if combat indicator is in goal bounds 
        self.goal = (self.goal_bar[0] <= self.x <= self.goal_bar[0] + self.goal_bar[2]) and (self.goal_bar[0] <= self.x + self.width <= self.goal_bar[0] + self.goal_bar[2])  
        self.draw(surface)

    def reset(self):
        """ Resets comabt indicator to starting position"""
        self.x = settings.x_bar
        self.speed = self.ini_speed
        self.acceleration = self.ini_acceleration

class Work_Bar(Bar):
    def __init__(self, ini_speed, ini_acceleration, jerk):
        super().__init__(ini_speed, ini_acceleration, jerk)
        self.x = settings.x_bar # Starting x position of combat indicator
        self.dest = (500, 300)
        self.bar = pygame.Surface((settings.bar_height, settings.bar_width))
        self.bar.fill(settings.DARK_BLUE)
    def draw(self, surface):
        super().draw(surface)
    #def update(self, surface):



class Stats: 
    def __init__(self, level):
        self.level = level
        base_hp = level * 50
        base_atk = level * 10

        self.hp = round(np.random.normal(loc = base_hp, scale = base_hp / settings.VAR_FACTOR))
        self.atk = round(np.random.normal(loc = base_atk, scale = base_atk / settings.VAR_FACTOR))

        jerk = 0
        if level >= 10:
            jerk = math.sqrt(level)
        self.combat_bar = Combat_Bar(30, 10, 0, settings.BAR_DIFFICULTY * round(math.log(1 + level, settings.BAR_SPEED_GROWTH)), jerk)

class Mob:
    def __init__(self, sprite, name, level):
        """ Size is a tuple describing the pixel by pixel size of the sprite. 
        """
        self.sprite = sprite
        self.name = name 
        self.stats = Stats(level)
        self.current_hp = self.stats.hp
        self.hp_bar_width = settings.hp_bar_width

    def draw(self, surface, x, y):
        """ Draws the sprite and level of the mob. (x, y) position are coordinates of top left of sprite rectangle.  
        """
        surface.blit(self.sprite, dest = (scenes.x_scaled(x), scenes.y_scaled(y)))
        scenes.draw_text(surface, f'{self.stats.level}', scenes.x_scaled(x-50), scenes.y_scaled(y-2))
        hp_bar_rect = pygame.Rect(scenes.x_scaled(x-30), scenes.y_scaled(y), self.hp_bar_width, settings.hp_bar_height)
        pygame.draw.rect(surface, settings.RED, hp_bar_rect)
        
        scenes.draw_text(surface, f'HP: {self.current_hp}/{self.stats.hp}', scenes.x_scaled(x+200), scenes.y_scaled(y))
    def damage(self, amount):
        self.current_hp -= amount
        self.hp_bar_width = settings.hp_bar_width * self.current_hp / self.stats.hp
    #def kill(self):

