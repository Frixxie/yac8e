import pygame
from sys import exit


class Screen():
    def __init__(self, width, height, magnitude, keys):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width * magnitude, height * magnitude), 0, 32)
        self.keys = keys

    def get_key(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    for i, key in enumerate(self.keys):
                        if event.key == key:
                            return i

    def key(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                print('Quit request recieved! Exiting')
                exit(0)
            elif event.type == pygame.KEYDOWN:
                for i, key in enumerate(self.keys):
                    if event.key == key:
                        return i
        return None

    def keyevents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                print('Quit request recieved! Exiting')
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    print("1 pressed!")


if __name__ == '__main__':
    keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
            pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r,
            pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f,
            pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v]

    screen = Screen(64, 32, 10, keys)

    while True:
        key = screen.get_key()
        print(key)
