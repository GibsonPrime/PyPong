import sys
import pygame
import World
import Renderer

from pygame.locals import *

# ============
# Attributes
# ============
world = World.World()
renderer = Renderer.Renderer(world)

# ============
# Main
# ============
# Init
pygame.init()

# Game loop
while True:
    # Check quit
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update
    world.update()
    renderer.draw()
