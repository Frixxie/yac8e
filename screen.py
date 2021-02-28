import pygame
from sys import exit


class Screen():
    def __init__(self, width, height, magnitude, keys):
        pygame.init()
        self.width = width
        self.height = height
        self.magnitude = magnitude
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (width * magnitude, height * magnitude), 0, 32)
        self.keys = keys

    def clear(self, color = (0, 0, 0)):
        self.screen.fill(color)

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

    def display(self, system, x, y, n):
        system.registers[0xf] = 0
        for i in range(n):
            byte = system.memory[system.index + i]
            ypos = ((y + i)) % self.height
            for j in range(8):
                pixel = (byte >> (7 - j)) & 1
                # pixel = (byte & 0x80) >> 7
                xpos = ((x + j)) % self.width
                cur_pixel = self.screen.get_at((xpos, ypos))
                print(cur_pixel, pixel)
                color = (0, 0, 0)
                if pixel:
                    color = (255, 255, 255)
                    if cur_pixel == (255, 255, 255, 255):
                        system.registers[0xf] = 1;
                        color = (0, 0, 0)
                pygame.draw.rect(self.screen, color, ((xpos) * self.magnitude, (ypos) * self.magnitude, self.magnitude, self.magnitude))
        pygame.display.update()

    def keyevents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                print('Quit request recieved! Exiting')
                exit(0)


if __name__ == '__main__':
    keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
            pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r,
            pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f,
            pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v]

    system = System()
    screen = Screen(64, 32, 1, keys)

    while True:
        screen.clear()
        for i in range(8):
            for j in range(32):
                system.memory[j] = randint(0, 2048)
            screen.display(system, i * 8, 0, 32)

