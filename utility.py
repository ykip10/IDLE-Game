import pygame, settings


# Scaling functions 
def x_scaled(x):
    """ Returns x-  coordinate scaled to custom resolutions
    """
    return settings.width * x / settings.NATIVE_WIDTH


def y_scaled(y):
    """ Returns y-coordinate scaled to custom resolutions
    """
    return settings.height * y / settings.NATIVE_HEIGHT



# Conversion Functions
def convert_scientific(number):
    """ Converts input to scientific notation
    """
    return "{:.2e}".format(number)


def convert_decimal(number):
    """ Converts input to a float
    """
    return float(number)



#Drawing tools 

#Text draw function (replace with images)
def draw_text(surface, text, x, y): 
    """ Draws a string onto a surface, with (x, y) representing coordinates of top left
    of string. 
    """                    
    text_surface = settings.font.render(text, True, settings.WHITE)       
    surface.blit(text_surface, (x_scaled(x), y_scaled(y)))

def image_to_rect(image, size, desired_size):
    """ Takes an image and outputs a Rect pygame object representing the image
    Image refers to the location of the image, size the dimensions of the image, 
    and desired_size the upscaled size. 
    """

    rect = pygame.Surface((size[0], size[1])).convert_alpha


def get_mob_frame(sheet, size, row, column, colour):
    """ Get frame of sprite sheet for a mob. Size refers to the pixel x pixel size of each sprite, 
    row, column refers to the position of the mob on the slime sheet, colour refers to the background color, essentially. 
      """
    frame = pygame.Surface((size[0], size[1])).convert_alpha()
    frame.fill(colour)
    frame.blit(sheet, (0, 0), (row*size[0], column*size[1], size[0], size[1]))
    frame = pygame.transform.scale(frame, (settings.MOB_HEIGHT, settings.MOB_SIZE))
    return frame

