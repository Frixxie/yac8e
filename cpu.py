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

    def decode(self, instruction):
        # The idea is to decode instruction and then return
        # corresponding function call
        pass

    def execute(self, fnptr, opcode):
        # The idea is to take in fnptr with
        # corresponding args and call function
        pass

    def find_bit_size(self, num):
        size = 0
        while num > 0:
            num >>= 1
            size += 1
        return size

    def find_least_significant_bit(self, num):
        return num & 1

    def find_most_signigicant_bit(self, num):
        bit_size = self.find_bit_size(num)
        msb = 1 << (bit_size - 1)
        return 1 if num & msb else 0


    def call(self, opcode):
        # opcode 0x0NNN
        print(f"Calling {opcode & 0xFFF}, opcode: {opcode}")

    def display_clear(self, screen, opcode):
        # opcode 0x00E0
        # clears the screen
        print(f"Clearing display!, opcode: {opcode}")


    def flow_return(self, opcode):
        # opcode 0x00EE
        # return from subrutine
        print(f"Returning from subrutine!, opcode: {opcode}")

    def call_subrutine(self, opcode):
        # opcode 0x2NNN
        # call subrutine
        print(f"Calling subrutine @ {opcode & 0x0FFF}, opcode: {opcode}")


    def skip_if_eqv(self, opcode, registers, pc):
        # opcode 0x3XNN
        # skips next instruction if Vx == NN
        x = opcode & 0x0F00
        value = opcode & 0x00FF
        print(f"Skipping next instruction if: {registers[x]} == {value}, opcode: {opcode}")
        if registers[x] == value:
            print("Skipping")
            pc += 2

    def skip_if_neqv(self, opcode, registers, pc):
        # opcode 0x4XNN
        # skips next instruction if Vx != NN
        x = opcode & 0x0F00
        value = opcode & 0x00FF
        print(f"Skipping next instruction if: {registers[x]} != {value}, opcode: {opcode}")
        if registers[x] != value:
            print("skipping")
            pc += 2

    def skip_if_eq(self, opcode, registers, pc):
        # opcode 0x5XY0
        # skips next instruction if Vx == Vy
        x = opcode & 0x0F00
        y = opcode & 0x00F0
        print(f"Skipping next instruction if: {registers[x]} != {registers[y]}, opcode: {opcode}")
        if registers[x] == registers[y]:
            print("skipping")
            pc += 2

    def set_val_const(self, opcode, registers):
        # opcode 0x6XNN
        # sets Vx to NN
        x = opcode & 0x0F00
        value = opcode & 0x00FF
        print(f"Setting register Vx {x} to {value}, opcode: {opcode}")
        registers[x] = value

    def add_val_const(self, opcode, registers):
        # opcode 0x7XNN
        # adds NN to Vx not changing carry flag
        x = opcode & 0x0F00
        value = opcode & 0x00FF
        print(f"Adding {value} to x, {x} {registers[x]}, opcode: {opcode}")
        registers[x] += value

    def assign_reg(self, opcode, registers):
        # opcode 8XY0
        # Sets Vx = Vy
        x = opcode & 0x0F00
        y = opcode & 0x00F0
        print(f"Assigning {registers[y]}, {y} to {registers[x]}, {x}, opcode: {opcode}")
        registers[x] = registers[y]

    def bit_op_or(self, opcode, registers):
        # opcode 8XY1
        # Sets Vx |= Vy
        x = opcode & 0x0F00
        y = opcode & 0x00F0
        print(f"Oring {registers[y]}, {y} to {registers[x]} {x}, opcode: {opcode}")
        registers[x] = registers[x] | registers[y]

    def bit_op_and(self, opcode, registers):
        # opcode 8XY2
        # Sets Vx &= Vy
        x = opcode & 0x0F00
        y = opcode & 0x00F0
        print(f"Anding {registers[y]}, {y} to {registers[x]} {x}, opcode: {opcode}")
        registers[x] = registers[x] & registers[y]

    def bit_op_xor(self, opcode, registers):
        # opcode 8XY3
        # Sets Vx ^= Vy
        x = opcode & 0x0F00
        y = opcode & 0x00F0
        print(f"Xoring {registers[y]}, {y} to {registers[x]} {x}, opcode: {opcode}")
        registers[x] = registers[x] ^ registers[y]

    def math_add(self, opcode, registers):
        # opcode 8XY4
        # Vx += Vy and sets carry flag if Vx overflows
        x = opcode & 0x0F00
        y = opcode & 0x00F0
        if registers[x] + registers[y] > 0xF:
            registers[0xF] = 1
        else:
            registers[0xF] = 0
        registers[x] += (registers[y] % 0xF)

    def math_sub(self, opcode, registers):
        # opcode 8XY5
        # Vx -= Vy and sets carry flag to 0 if there is a borrow and 1 when not
        x = opcode & 0x0F00
        y = opcode & 0x00F0
        if registers[x] - registers[y] < 0:
            registers[0xF] = 0
        else:
            registers[0xF] = 1
        registers[x] -= (registers[y] % 0xF)

    def bit_op_right_shift(self, opcode, registers):
        # opcode 8XY6
        # Stores least significant bit in Vf and rightshifts Vx by 1
        x = opcode & 0x0F0
        registers[0xF] = self.find_least_significant_bit(registers[x])
        registers[x] >>= 1

    def math_sub_regs(self, opcode, registers):
        # opcode 8XY7
        # Sets Vx to Vy - Vx, Vf is set to 0 when there is a borrow. and 1 when there is not.
        x = opcode & 0x0F00
        y = opcode & 0x00F0
        if registers[x] - registers[y] < 0:
            registers[0xF] = 0
        else:
            registers[0xF] = 1
        registers[x] = (registers[x] - registers[y]) % 0xF

    def bit_op_left_shift(self, opcode, registers):
        # opcode 8XYE
        x = opcode & 0x0F0
        registers[0xF] = self.find_least_significant_bit(registers[x])
        registers[x] <<= 1
