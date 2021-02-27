#!/bin/python3
import cpu
class System():
    def __init__(self, screen):
        # the memory has 4096 memory locations
        self.memory = [0 for _ in range(0x1000)]
        # The stack could be placed in memory
        self.stack = list()
        # Has 16 registers V0 to VF
        self.registers = [0 for _ in range(0xF + 1)]
        # Index register 
        self.index = 0
        # The program counter
        self.pc = 0x200
        # Used for timing events in games can be both set and read
        self.delay_timer = 0
        # Used for sound effects, when non zero makes beep sound
        self.sound_timer = 0
        # Screen
        self.screen = screen

    def __str__(self):
        return f"{self.pc}\n{self.registers}\n{self.stack}"

    def load_rom(self, rom):
        with open(rom, "rb") as f:
            counter = 0x200
            content = f.read(1)
            while content:
                self.memory[counter] = content[0]
                counter += 1
                content = f.read(1)

if __name__ == '__main__':
    yac8pe = System(None)
    print(len(yac8pe.memory))
    print(yac8pe.stack)
    # print(len(yac8pe.registers))
    yac8pe.load_rom('/home/fredrik/projects/c8_roms/roms/hires/Hires Test [Tom Swan, 1979].ch8')
    cpu = cpu.C8cpu()
    # print(yac8pe.memory)
    try:
        while True:
            instruction = cpu.fetch(yac8pe)
            opcode =  cpu.decode(instruction)
            cpu.execute(instruction, opcode, yac8pe)
            print(yac8pe)
    except KeyboardInterrupt:
        print("got keyboard interupt")
