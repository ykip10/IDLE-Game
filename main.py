import pygame, settings
from objects import Resource
import scene_change as sc

pygame.init()

# Main Game Loop
def main():
    engine = sc.DisplayEngine()
    engine.run(sc.main_scene(engine))   

main()


