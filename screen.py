import pygame
from sys import exit

class Screen():
    def __init__(self, x, y):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((x, y), 0, 32)

    def keyevents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                print('Quit request recieved! Exiting')
                exit(0)
