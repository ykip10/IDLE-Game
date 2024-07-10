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



# Drawing tools 
def draw_text(surface, text, x, y): 
    """ Draws a string onto a surface, with (x, y) representing coordinates of top left
    of string. 
    """                    
    text_surface = settings.font.render(text, True, settings.WHITE)       
    surface.blit(text_surface, (x_scaled(x), y_scaled(y)))


def image_to_surface(image, size, desired_size, background_color):
    """ Takes an image and outputs a surface pygame object representing the image
    Image refers to the location of the image, size the dimensions of the image, 
    and desired_size the upscaled size. Background_color represents the color backdrop.
    """
    surface = pygame.Surface(size).convert_alpha()
    surface.fill(background_color)
    surface.blit(image, (0, 0), (0, 0, size[0], size[1]))
    surface = pygame.transform.scale(surface, desired_size)
    return surface


def get_mob_frame(sheet, size, row, column, colour):
    """ Get frame of sprite sheet for a mob. Size refers to the pixel x pixel size of each sprite, 
    row, column refers to the position of the mob on the slime sheet, colour refers to the background color, essentially. 
      """
    frame = pygame.Surface(size).convert_alpha()
    frame.fill(colour)
    frame.blit(sheet, (0, 0), (row*size[0], column*size[1], size[0], size[1]))
    frame = pygame.transform.scale(frame, (settings.MOB_HEIGHT, settings.MOB_SIZE))
    return frame

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
    colour_rect = pygame.Surface((2, 2))
    pygame.draw.line(colour_rect, bottom_colour, (0, 0), (1, 0))
    pygame.draw.line(colour_rect, top_colour, (0, 1), (1, 1))
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))
    surface.blit(colour_rect, target_rect)