import pygame, settings, scenes, math, random, numpy as np

# credit: https://stackoverflow.com/questions/62336555/how-to-add-color-gradient-to-rectangle-in-pygame
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

def get_random_seed():
    return int(np.random.uniform(0, 1000))


class Bar: # Only supports 1 dimensional motion in x or y direction 
    ''' Super class for all Bar mechanics
    '''
    def __init__(self, ini_speed, ini_acceleration, jerk):
        """ Width refers to the width of the """
        self.ini_speed = ini_speed
        self.speed = ini_speed # Speed of combat indicator (pixels/s)
        self.ini_acceleration = ini_acceleration
        self.acceleration = ini_acceleration # Acceleration of combat indicator (pixels/s^2)
        self.jerk = jerk # d^3x/dt^3

        # Dimensions of bar 
        self.bar_width = 0
        self.bar_height = 0

        # Coordinates of top left of bar
        self.x_bar = 0
        self.y_bar = 0

        self.bar = None # Bar to be drawn 

    def draw(self, surface): pass
        # Drawings need to be specified in the subclass
    def update(self, surface): 
        # speed etc. logic here
        pass 


class Combat_Bar(Bar): 
    """ Contains information about the combat bar and all associated mechanics
    """
    def __init__(self, goal_width, width, ini_speed, ini_acceleration, jerk):
        """ 
        goal_width: width of goal indicator
        width: width of combat indicator
        ini_speed: initial speed of combat indicator
        ini_acceleration: initial acceleration of combat indicator
        jerk: jerk of combat indicator 
        """
        
        super().__init__(ini_speed, ini_acceleration, jerk)
        
        # Dimensions of bar 
        self.bar_width = 250
        self.bar_height = 50

        # Coordinates of bar
        self.x_bar = 150
        self.y_bar = 500

        self.width = width 
        self.x = self.x_bar # Starting x position of combat indicator

        self.bar = pygame.Surface((self.bar_width, self.bar_height))
        self.bar.fill(settings.DARK_BLUE)
        self.dest = (self.x_bar, self.y_bar)
        self.goal_width = goal_width

        # Controls the minimum distance from either edge the goal_bar is allowed to spawn 
        self.min_distance = 50
        self.offset = np.random.normal(-5, 20)

        self.goal_bar = (self.x_bar + (self.bar_width - self.width) / 2 - self.offset, self.y_bar - 10, self.goal_width, self.bar_height + 20)
        self.goal = False

        
        
    def draw(self, surface):
        """ Draws the combat bar.
        """
        surface.blit(self.bar, dest = (self.x_bar, self.y_bar)) # Draws the bar 
        
        # Drawing of goal bar and combat indicator 
        pygame.draw.rect(surface, settings.GREEN, self.goal_bar)
        pygame.draw.rect(surface, settings.WHITE, (self.x, self.y_bar - 10, self.width, self.bar_height + 20))

    def update(self, surface):
        """ Updates the position of the combat bar and checks if the combat indicator is in the bounds of the goal indicator. 
        """
        if self.x_bar <= self.x <= self.x_bar + (self.bar_width - self.width ) / 2: # In first half 
            self.x += self.speed
            self.speed += self.acceleration
            self.acceleration = abs(self.acceleration)
            self.acceleration += self.jerk
        elif self.x_bar + (self.bar_width - self.width ) / 2 <= self.x  <= self.x_bar + self.bar_width - self.width: # In second half 
            self.x += self.speed
            self.acceleration = -abs(self.acceleration)
            self.speed += self.acceleration
            self.acceleration -= self.jerk
        elif self.x >= self.x_bar + self.bar_width - self.width: # Past right border
            self.x += self.speed 
            self.speed = -abs(self.ini_speed)
            self.speed += self.acceleration
            self.acceleration -= self.jerk 
        elif self.x <= self.x_bar: # Past left border
            self.x += self.speed    
            self.speed = abs(self.ini_speed) 
            self.speed += self.acceleration
            self.acceleration += self.jerk 

        # Check if combat indicator is in goal bounds 
        self.goal = (self.goal_bar[0] <= self.x <= self.goal_bar[0] + self.goal_bar[2]) and (self.goal_bar[0] <= self.x + self.width <= self.goal_bar[0] + self.goal_bar[2])  

        self.draw(surface)

    def reset(self):
        """ Resets comabt indicator to starting position"""
        self.x = self.x_bar
        self.speed = self.ini_speed
        self.acceleration = self.ini_acceleration
        #         <-goal_w->
        # ----------  ---  ------------  |     |
        # |          |   |            |  | self.bar_height
        # ----------  ---  ------------  |     |
        # <-------self.bar_width------>
        #
        
        self.offset = np.random.uniform(-(self.bar_width - self.width) / 2 + self.min_distance, (self.bar_width - self.width) / 2 - self.min_distance) 
        self.goal_bar = (self.x_bar + (self.bar_width - self.width - self.goal_width) / 2 - self.offset, self.y_bar - 10, self.goal_width, self.bar_height + 20)


class Work_Bar(Bar):
    """ Contains information about the bar on the employment screen and all associated mechanics
    """
    def __init__(self, ini_speed, ini_acceleration, jerk):
        """ ini_speed: initial speed of the bar
        ini_acceleration: initial acceleration of the bar
        jerk: jerk of the bar 
        """
        super().__init__(ini_speed, ini_acceleration, jerk)

        # Dimensions of the bar
        self.bar_width = 50
        self.bar_height = 250

        # Coordinates of the bar
        self.x_bar = 500
        self.y_bar = 300

        self.y = self.bar_height # Starting y position of black box 
        self.bar = pygame.Rect((self.x_bar, self.y_bar, self.bar_width, self.bar_height))     # initalisation of gradiented meter 
        self.black_box = pygame.Rect((self.x_bar, self.y_bar, self.bar_width, self.y))   # initialisation of black box (wi)

        # For logic in update method
        self.speed = ini_speed
        self.acceleration = ini_acceleration
        self.jerk = jerk

        self.going_up = True 

    def draw(self, surface):
        """ Draws the gradiented meter as well as the black box
        """
        ver_gradientRect(surface, settings.RED, settings.YELLOW, self.bar) # Draw gradiented meter
        pygame.draw.rect(surface, settings.BLACK, self.black_box) 

    def update(self, surface):
        """ Updates position of the black box and redraws the scene
        """
        if self.going_up:
            self.y -= self.speed
            self.speed += self.acceleration
            self.acceleration += self.jerk
            if self.y <= 0: 
                self.going_up = False 
        else:
            self.y += self.speed
            self.speed -= self.acceleration
            self.acceleration -= self.jerk
            if self.y >= self.bar_height:
                self.going_up = True
                self.speed = self.ini_speed
                self.acceleration = self.ini_acceleration

        self.black_box = pygame.Rect((self.x_bar, self.y_bar, self.bar_width, self.y))
        self.draw(surface)

    def reset(self):
        """ Resets bar to the bottom 
        """
        self.y = self.bar_height
        self.speed = self.ini_speed
        self.acceleration = self.ini_acceleration


class Mob_stats: 
    def __init__(self, level, player_id):
        self.level = level
        base_hp = level * 50
        base_atk = level * 5

        rng = np.random.default_rng(player_id)
        self.hp = round(rng.normal(loc = base_hp, scale = base_hp / settings.VAR_FACTOR))
        self.atk = round(rng.normal(loc = base_atk, scale = base_atk / settings.VAR_FACTOR))

        jerk = 0
        if level >= 10:
            jerk = math.sqrt(level)
        self.combat_bar = Combat_Bar(30, 10, 0, settings.BAR_DIFFICULTY * round(math.log(1 + level, settings.BAR_SPEED_GROWTH)), jerk)


class Mob:
    def __init__(self, sprite, name, level, player_id):
        """ Size is a tuple describing the pixel by pixel size of the sprite. 
        """
        self.sprite = sprite
        self.name = name 
        self.stats = Mob_stats(level, player_id)
        self.current_hp = self.stats.hp
        
        self.max_bar_width = 200 
        self.hp_bar_height = 20 
        self.hp_bar_width = self.max_bar_width

    def draw(self, surface, x, y):
        """ Draws the sprite and level of the mob. (x, y) position are coordinates of top left of sprite rectangle.  
        """
        surface.blit(self.sprite, dest = (scenes.x_scaled(x), scenes.y_scaled(y)))
        scenes.draw_text(surface, f'{self.stats.level}', scenes.x_scaled(x-50), scenes.y_scaled(y-2))
        hp_bar_rect = pygame.Rect(scenes.x_scaled(x-30), scenes.y_scaled(y), self.hp_bar_width, self.hp_bar_height)
        pygame.draw.rect(surface, settings.RED, hp_bar_rect)
        
        scenes.draw_text(surface, f'HP: {self.current_hp}/{self.stats.hp}', scenes.x_scaled(x+200), scenes.y_scaled(y))
    def damage(self, amount):
        self.current_hp -= amount
        self.hp_bar_width = self.max_bar_width * self.current_hp / self.stats.hp
    #def kill(self):


class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name

        self.level = 1

        # Tweakable gameplay parameters; keep as integer 
        max_level = 100
        hp_gain_variation = 3    
        atk_gain_variation = 1
        self.hp_growth = 10     # average amount of hp growth on level up
        self.atk_growth = 2     # average amount of atk growth on level up

        # Tweakable ui parameters
        self.hp_bar_width = 300
        self.hp_bar_height = 50

        # Create variation in stats gained from levelling up (just random noise)
        rng = np.random.default_rng(1461296)
        rand = rng.integers(-1, 1, max_level + 1)               # Stores max_level + 1 random values in between -1 and 1 (fixed) 
        self.hp_var = hp_gain_variation * rand         # Variation in hp gain with a level up  (same for all players)
        self.atk_var = atk_gain_variation * rand        # Variation in atk gain with a level up (same for all players)

        self.hp = 30
        self.atk = 4 
        self.curr_hp = self.hp
    
    def level_up(self):
        self.hp += self.hp_growth + self.hp_var[self.level]
        self.atk += self.atk_growth + self.atk_var[self.level]
        self.level += 1

    def show_hud(self, surface): 
        hp_x, hp_y = 100, 100
        scenes.draw_text(surface, f'HP: {self.curr_hp}/{self.hp}', scenes.x_scaled(hp_x), scenes.y_scaled(hp_y))
        draw_hp_bar(surface, scenes.x_scaled(hp_x + 30), scenes.y_scaled(hp_y), self.hp_bar_width, self.hp_bar_height)

