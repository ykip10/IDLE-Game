import pygame, math, numpy as np
import settings, utility as u, resources as r


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
    def __init__(self, goal_width, ini_speed, ini_acceleration, jerk):
        """ 
        goal_width: width of goal indicator
        width: width of combat indicator
        ini_speed: initial speed of combat indicator
        ini_acceleration: initial acceleration of combat indicator
        jerk: jerk of combat indicator 
        """
        
        super().__init__(ini_speed, ini_acceleration, jerk)
        
        # Dimensions of bar 
        self.bar_width = settings.combat_bar_width
        self.bar_height = settings.combat_bar_height

        # Coordinates of bar
        self.x_bar = settings.combat_bar_x
        self.y_bar = settings.combat_bar_y

        self.width = settings.COMBAT_INDICATOR_WIDTH
        self.x = self.x_bar # Starting x position of combat indicator
        self.combat_indicator = pygame.Rect(self.x, self.y_bar - 10, self.width, self.bar_height + 20)

        self.bar = pygame.Surface((self.bar_width, self.bar_height))
        self.bar.fill(settings.DARK_BLUE)
        self.dest = (self.x_bar, self.y_bar)
        self.goal_width = goal_width

        # Controls the minimum distance from either edge the goal_bar is allowed to spawn 
        self.min_distance = 50
        self.offset = np.random.normal(-5, 20)

        self.goal_bar = pygame.Rect(self.x_bar + (self.bar_width - self.width) / 2 - self.offset, self.y_bar - 10, self.goal_width, self.bar_height + 20)
        self.goal = False

        self.hit_left = False
        self.hit_right = False 
        
    def draw(self, surface):
        """ Draws the combat bar.
        """
        surface.blit(self.bar, dest = (self.x_bar, self.y_bar)) # Draws the bar 
        
        # Drawing of goal bar and combat indicator 
        pygame.draw.rect(surface, settings.GREEN, self.goal_bar)
        pygame.draw.rect(surface, settings.WHITE, self.combat_indicator)

    def update(self, surface):
        """ Updates the position of the combat bar and checks if the combat indicator is in the bounds of the goal indicator. 
        """
        if self.x_bar <= self.x <= self.x_bar + (self.bar_width - self.width ) / 2: # In first half 
            self.x += self.speed
            self.speed += self.acceleration
            self.acceleration = abs(self.acceleration)
            self.acceleration += self.jerk
            self.hit_left = False
        elif self.x_bar + (self.bar_width - self.width ) / 2 <= self.x  <= self.x_bar + self.bar_width - self.width: # In second half 
            self.x += self.speed
            self.acceleration = -abs(self.acceleration)
            self.speed += self.acceleration
            self.acceleration -= self.jerk
            self.hit_right = False 
        elif self.x >= self.x_bar + self.bar_width - self.width: # Past right border
            self.x += self.speed 
            self.speed = -abs(self.ini_speed)
            self.speed += self.acceleration
            self.acceleration -= self.jerk 
            self.hit_right = True
        elif self.x <= self.x_bar: # Past left border
            self.x += self.speed    
            self.speed = abs(self.ini_speed) 
            self.speed += self.acceleration
            self.acceleration += self.jerk 
            self.hit_left = True

        # Update combat indicator position based on the value of x. 
        self.combat_indicator = pygame.Rect(self.x, self.y_bar - 10, self.width, self.bar_height + 20)

        # Check if combat indicator is in goal bounds 
        self.goal = self.goal_bar.contains(self.combat_indicator) 
        self.draw(surface)

    def reset(self):
        """ Randomises position of goal 
        """

        self.offset = np.random.uniform(-(self.bar_width - self.width) / 2 + self.min_distance, (self.bar_width - self.width) / 2 - self.min_distance) 
        self.goal_bar = pygame.Rect(self.x_bar + (self.bar_width - self.width - self.goal_width) / 2 - self.offset, self.y_bar - 10, self.goal_width, self.bar_height + 20)


class Mob_stats: 
    def __init__(self, level, player_id):
        self.level = level
        base_hp = level * 20
        base_atk = level * 3

        rng = np.random.default_rng(player_id)
        self.hp = round(rng.normal(loc = base_hp, scale = base_hp / settings.VAR_FACTOR))
        self.atk = round(rng.normal(loc = base_atk, scale = base_atk / settings.VAR_FACTOR))

        jerk = 0
        if level >= 10:
            jerk = math.sqrt(level)
        self.combat_bar = Combat_Bar(30, 0, settings.BAR_DIFFICULTY * round(math.log(1 + level, settings.BAR_SPEED_GROWTH)), jerk)


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

        self.can_attack = True
        
    def draw(self, surface, x, y):
        """ Draws the sprite and level of the mob. (x, y) position are coordinates of top left of sprite rectangle.  
        """
        self.hp_bar_width = self.max_bar_width * self.current_hp / self.stats.hp
        surface.blit(self.sprite, dest = (u.x_scaled(x), u.y_scaled(y)))
        u.draw_text(surface, f'{self.stats.level}', u.x_scaled(x-50), u.y_scaled(y-2))
        hp_bar_rect = pygame.Rect(u.x_scaled(x-30), u.y_scaled(y), self.hp_bar_width, self.hp_bar_height)
        pygame.draw.rect(surface, settings.RED, hp_bar_rect)
        
        u.draw_text(surface, f'HP: {self.current_hp}/{self.stats.hp}', u.x_scaled(x+200), u.y_scaled(y))
        self.stats.combat_bar.update(surface)
    def damage(self, amount):
        self.current_hp -= amount

    #def kill(self):


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
        self.bar_width = settings.work_bar_width
        self.bar_height = settings.work_bar_height

        # Coordinates of the bar
        self.x_bar = settings.work_bar_x
        self.y_bar = settings.work_bar_y

        self.y = self.bar_height # Starting y position of black box 
        self.bar = pygame.Rect((self.x_bar, self.y_bar, self.bar_width, self.bar_height))     # initalisation of gradiented meter 
        self.black_box = pygame.Rect((self.x_bar, self.y_bar, self.bar_width, self.y))   # initialisation of black box (wi)

        # For logic in update method
        self.speed = ini_speed
        self.combod_accel = ini_acceleration
        self.acceleration = self.combod_accel
        self.jerk = jerk
        self.going_up = True 

        # goal indicator
        self.proportion_goal1 = 0.99 # Need fill up this much of the bar to get a goal
        self.proportion_goal2 = 0.96
        self.proportion_goal3 = 0.9

        goal_x = self.x_bar - 5 
        goal1_y, goal2_y, goal3_y = self.y_bar + self.bar_height * (1 - self.proportion_goal1),  self.y_bar + self.bar_height * (1 - self.proportion_goal2),  self.y_bar + self.bar_height * (1 - self.proportion_goal3)
        goal_width, goal_height = self.bar_width + 10, 1
        self.goal1_indicator = pygame.Rect(goal_x, goal1_y, goal_width, goal_height)
        self.goal2_indicator = pygame.Rect(goal_x, goal2_y, goal_width, goal_height)
        self.goal3_indicator = pygame.Rect(goal_x, goal3_y, goal_width, goal_height)

        # combo
        self.goal1 = False
        self.goal2 = False
        self.goal3 = False
        self.combo = 1

    def draw(self, surface):
        """ Draws the gradiented meter as well as the black box
        """
        u.ver_gradientRect(surface, settings.RED, settings.YELLOW, self.bar) # Draw gradiented meter
        pygame.draw.rect(surface, settings.BLACK, self.black_box)
        pygame.draw.rect(surface, settings.WHITE, self.goal1_indicator) 
        pygame.draw.rect(surface, settings.WHITE, self.goal2_indicator) 
        pygame.draw.rect(surface, settings.WHITE, self.goal3_indicator) 

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
                self.combo = 1 


        self.black_box = pygame.Rect((self.x_bar, self.y_bar, self.bar_width, self.y))

        self.goal1 = self.goal1_indicator.topleft[1] >= self.black_box.bottomleft[1]  
        self.goal2 = self.goal1_indicator.bottomleft[1] <= self.black_box.bottomleft[1] <= self.goal2_indicator.topleft[1]
        self.goal3 = self.goal2_indicator.bottomleft[1] <= self.black_box.bottomleft[1] <= self.goal3_indicator.topleft[1]

        self.draw(surface)


    def hard_reset(self):
        """ Resets bar to initial state
        """
        self.y = self.bar_height
        self.going_up = True
        self.speed = self.ini_speed
        self.acceleration = self.ini_acceleration*math.sqrt(self.combo)

