import pygame, settings, scenes, math, numpy as np

# Combat stuff 
class Combat_Bar: 
    def __init__(self, width, speed, acceleration, jerk):
        """ Speed refers to the initial speed of the combat indicator, acceleration refers to the acceleration of the combat indicator, 
        colour refers to the colour of the bar. 
        """
        self.width = width
        self.speed = speed # Speed of combat indicator (pixels/s)
        self.acceleration = acceleration # Acceleration of combat indicator (pixels/s^2)
        self.jerk = jerk # d^3x/dt^3
        self.x = settings.x_bar # Starting x position of combat indicator 

        self.bar = pygame.Surface((settings.bar_width, settings.bar_height))
        self.bar.fill(settings.DARK_BLUE)
        
        
    def draw(self, surface):
        """ x is the x-coordinate of the combat indicator. width, height refer to the width  
        sliding combat INDICATOR. Draws the bar + combat indicator. 
        """
        surface.blit(self.bar, dest = (settings.x_bar, settings.y_bar))
        pygame.draw.rect(surface, settings.WHITE, (self.x, settings.y_bar - 10, self.width, settings.bar_height + 20))

    def update(self, surface):
        if settings.x_bar <= self.x <= settings.x_bar + (settings.bar_width / 2): # In first half 
            self.x += self.speed
            self.speed += self.acceleration
            self.acceleration += self.jerk
        elif settings.x_bar + (settings.bar_width / 2) <= self.x  <= settings.x_bar + settings.bar_width - self.width: # In second half 
            self.x += self.speed
            self.speed += self.acceleration
            self.acceleration -= self.jerk
        elif self.x >= settings.x_bar + settings.bar_width - self.width: # Past right border
            self.x = settings.x_bar + settings.bar_width - self.width 
            self.speed = -abs(self.speed)
            self.speed += self.acceleration
            self.acceleration -= self.jerk 
        elif self.x <= settings.x_bar: # Past left border 
            self.x = settings.x_bar
            self.speed = abs(self.speed) 
            self.speed += self.acceleration
            self.acceleration += self.jerk 
        print(self.speed)
        self.draw(surface)
        

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
        self.combat_bar = Combat_Bar(10, 0, 0.2 * round(math.log(1 + level, settings.HP_growth)), jerk)

class Mob:
    def __init__(self, sprite, name, level):
        """ Size is a tuple describing the pixel by pixel size of the sprite. 
        """
        self.sprite = sprite
        self.name = name 
        self.stats = Stats(level)
        self.current_hp = self.stats.hp
    def draw(self, surface, x, y):
        """ Draws the sprite and level of the mob. (x, y) position are coordinates of top left of sprite rectangle.  
        """
        surface.blit(self.sprite, dest = (scenes.x_scaled(x), scenes.y_scaled(y)))
        scenes.draw_text(surface, f' Level {self.stats.level}', scenes.x_scaled(x + 12), scenes.y_scaled(y))


