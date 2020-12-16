#!/bin/python

from sys import exit

class C8cpu():
    def __init__(self, big_endianness):
        # Big or little endianness
        # True or false
        self.big_endianness = big_endianness
        # all the operations which an opcode can map too

        self.operations = {}
    def fetch(pc, memory):
        instruction = None
        try:
            instruction = memory[pc]
            if self.big_endianness:
                instruction <<= 8
                instruction |= memory[pc + 1]
            else:
                instruction = (memory[pc + 1] << 8) | instruction
        except IndexError:
            print(f"pc {pc} out of memory bounds")
            exit(0)
        pc += 2
        return instruction

    def decode(instruction):
        # The idea is to decode instruction and then return
        # corresponding function call
        pass

    def execute(fnptr):
        pass

    def call(self, opcode):
        # opcode 0x0NNN
        pass

    def display_clear(self, screen, opcode):
        # opcode 0x00E0
        # clears the screen
        pass

    def flow_return(self, opcode):
        # opcode 0x00EE
        # return from subrutine
        pass

    def call_subrutine(self, opcode):
        # opcode 0x2NNN
        # call subrutine
        pass

    def jump_equal_val(self, opcode, registers, pc):
        # opcode 0x3XNN
        # skips next instruction if Vx == NN
        x = opcode & 0x0F00
        value = opcode & 0x00FF
        if registers[x] == value:
            pc += 2

    def jump_not_equal_val(self, opcode, registers, pc):
        # opcode 0x4XNN
        # skips next instruction if Vx != NN
        x = opcode & 0x0F00
        value = opcode & 0x00FF
        if registers[x] != value:
            pc += 2

    def jump_equal(self, opcode, registers, pc):
        # opcode 0x5XY0
        # skips next instruction if Vx == Vy
        x = opcode & 0x0F00
        y = opcode & 0x00F0
        if registers[x] == registers[y]:
            pc += 2

    def set_val_const(self, opcode, registers):
        # opcode 0x6XNN
        # sets Vx to NN
        x = opcode & 0x0F00
        value = opcode & 0x00FF
        registers[x] = value

    def add_val_const(self, opcode, registers):
        # opcode 0x7XNN
        # adds NN to Vx not changing carry flag
        x = opcode & 0x0F00
        value = opcode & 0x00FF
        registers[x] += value

    def assign_reg(self, opcode, registers):
        # opcode 8XY0
        # Sets Vx = Vy
        x = opcode & 0x0F00
        y = opcode & 0x00F0
        registers[x] = registers[y]

    def bit_op_or(self, opcode, registers):
        # opcode 8XY1
        # Sets Vx |= Vy
        x = opcode & 0x0F00
        y = opcode & 0x00F0
        registers[x] = registers[x] | registers[y]

    def bit_op_and(self, opcode, registers):
        # opcode 8XY2
        # Sets Vx &= Vy
        x = opcode & 0x0F00
        y = opcode & 0x00F0
        registers[x] = registers[x] & registers[y]

    def bit_op_xor(self, opcode, registers):
        # opcode 8XY3
        # Sets Vx ^= Vy
        x = opcode & 0x0F00
        y = opcode & 0x00F0
        registers[x] = registers[x] ^ registers[y]

    def math_add(self, opcode, registers):
        # opcode 8XY4
        # Vx += Vy and sets carry flag if Vx overflows
        x = opcode & 0x0F00
        y = opcode & 0x00F0
        if registers[x] > 0xF:
            registers[0xF] = 1
        else:
            registers[0xF] = 0
        registers[x] += (registers[y] % 0xF)
