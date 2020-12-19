#!/bin/python3

class Yac8pe():
    def __init__(self):
        # the memory has 4096 memory locations
        self.memory = [0 for _ in range(0x1000)]
        # The stack could be placed in memory
        self.stack = [0 for _ in range(0xF)]
        # Has 16 registers V0 to VF
        self.registers = [0 for _ in range(0xF)]
        # Index register 
        self.index = 0
        # The program counter
        self.pc = 0
        # Used for timing events in games can be both set and read
        self.delay_timer = 0
        # Used for sound effects, when non zero makes beep sound
        self.sound_timer = 0

    def __str__(self):
        return f"{len(self.memory)}"

    def load_rom(self, rom):
        with open(rom, "rb") as f:
            counter = 0x200
            while True:
                content = f.read(1)
                if not content:
                    break
                print(hex(content[0]))
                self.memory[counter] = content[0]
                counter += 1

if __name__ == '__main__':
    yac8pe = Yac8pe()
    print(len(yac8pe.memory))
    print(yac8pe.stack)
    print(yac8pe.registers)
    yac8pe.load_rom('roms/games/Pong (1 player).ch8')
    print(yac8pe.memory)
