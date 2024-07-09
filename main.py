import pygame, scenes
pygame.init()

# Main Game Loop
def main():
    engine = scenes.DisplayEngine()
    engine.run(scenes.main_scene(engine))
main()
