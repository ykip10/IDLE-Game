import pygame, sys, settings

pygame.init()

screen = pygame.display.set_mode((settings.width, settings.height))
slime_sheet = pygame.image.load(r'sprites\slimes\slime-Sheet.png').convert_alpha()

def get_slime_frame(sheet, width, height, row, column, scale, colour):
    """ Sheet is the sprite sheet. (width, height) is the size of each sprite. (row, column) is the row and column the sprite is in
    Scale is the factor by which the image should be scaled
    """
    frame = pygame.Surface((width, height)).convert_alpha()
    frame.blit(sheet, (0, 0), (0, 0, width, height))

screen.blit(slime_sheet, (0, 0), (32, 0, 32, 32))
pygame.display.flip() # updates display 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

class Enemy:
    def __init__(self, on_death, on_hit, standby):
        self.standby = standby
        self.on_hit = on_hit
        self.on_death = on_death
    
class Slime(Enemy):
    def __init__(self, hp, atk):
        super().init()
        self.hp = hp
        self.atk = atk
    