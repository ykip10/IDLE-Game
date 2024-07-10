import numpy as np

class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.level = 1

        self.can_attack = True 
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

    def damage(self, amount):
        self.curr_hp -= amount
