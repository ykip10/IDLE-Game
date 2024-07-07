import pygame, mobs, scenes, settings



slime_sheet = scenes.load_slime_sheet()
frame = scenes.get_mob_frame(slime_sheet, (32, 32), 1, 0, settings.MAIN_BACKGROUND)
slime1 = mobs.Mob(frame, 'Slime', 1)