import pygame
import os
import sys

pygame.init()

base_path = os.path.dirname(os.path.abspath(__file__))

COLOUR_BG = (175, 215, 70)
COLOUR_FRUIT = (183, 111, 122)

canva = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

head_right = pygame.image.load(os.path.join(base_path, "Assets", "Graphics", "head_right.png")).convert_alpha()
surface = pygame.Surface((50, 50))
surface.fill(COLOUR_FRUIT)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    canva.fill(COLOUR_BG)
    canva.blit(surface, (100, 100))
    pygame.display.update()
    clock.tick(60)