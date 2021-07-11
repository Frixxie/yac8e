#!/bin/python3
import cpu
import pygame
from screen import Screen
from fontset import FONTSET
from time import sleep


class Emulator():
    def __init__(self, screen=None, fontset=FONTSET):
        # the memory has 4096 memory locations
        self.memory = [0 for _ in range(0x1000)]
        # The stackpointer
        self.stackpointer = 0
        # Has 16 registers, which are 0 to 0xF (V0 to VF)
        self.registers = [0 for _ in range(0xF + 1)]
        # Index register
        self.index = 0
        # The program counter
        self.pc = 0
        # Used for timing events in games can be both set and read
        self.delay_timer = 0
        # Used for sound effects, when non zero makes beep sound
        self.sound_timer = 0
        # Screen which the cpu will use
        self.screen = screen
        # fontset which will be loaded into memory
        self.fontset = fontset

    def __str__(self):
        return f"{self.pc},{self.index}\n{self.registers}\n{self.stack}"

    def load_font(self):
        """loads a font into reserved space"""
        self.index = 0
        for i in range(len(self.fontset)):
            for j in range(5):
                self.memory[self.index] = self.fontset[i][j]
                self.index += 1
        self.pc = self.index
        self.index = 0

    def load_rom(self, rom):
        """
        Loads a rom into the emulators memory
        """
        with open(rom, "rb") as f:
            # 0 -> 0x200 is reserved for interpreter or in this case fonts
            counter = 0x200
            content = f.read(1)
            while content:
                self.memory[counter] = content[0]
                counter += 1
                content = f.read(1)


if __name__ == '__main__':
    # The key map the screen wil use
    keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
            pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r,
            pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f,
            pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v]
    #screen = Screen(64, 32, 20, keys, show = False)
    screen = Screen(64, 32, 20, keys)
    yac8pe = Emulator(screen)
    print(len(yac8pe.memory))
    # print(yac8pe.stack)
    print(len(yac8pe.registers))
    yac8pe.load_font()
    yac8pe.load_rom(
        '/home/fredrik/projects/c8_roms/roms/games/Space Invaders [David Winter].ch8')
    cpu = cpu.C8cpu(verbose=True)
    # print(yac8pe.memory)
    try:
        while True:
            instruction = cpu.fetch(yac8pe)
            opcode = cpu.decode(instruction)
            cpu.execute(instruction, opcode, yac8pe)
            yac8pe.delay_timer -= 1
            yac8pe.sound_timer -= 1
            sleep(0.1)
            print(yac8pe, hex(instruction))
    except KeyboardInterrupt:
        print("got keyboard interupt")
