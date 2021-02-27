#!/bin/python

from sys import exit
from random import randint

class C8cpu():
    def __init__(self, big_endianness: bool = True, verbose: bool = False):
        # Big or little endianness
        # True or false
        self.big_endianness = big_endianness
        self.verbose = verbose
        # all the operations which an opcode can map too
        self.operations = {}

    def fetch(self, system):
        instruction = None
        try:
            instruction = system.memory[system.pc]
            if self.big_endianness:
                instruction <<= 8
                instruction |= system.memory[system.pc + 1]
            else:
                instruction = (system.memory[system.pc + 1] << 8) | instruction
        except IndexError:
            print(f"pc {system.pc} out of memory bounds")
            exit(0)
        system.pc += 2
        return instruction

    def decode(self, instruction):
        # The idea is to decode instruction and then return
        # corresponding function call entry to dict
        first_word = (instruction & 0xF000) >> 12
        if first_word == 0:
            if instruction == 0x00E0:
                # opcode 0x00E0
                return (first_word, 0)
            elif instruction == 0x00EE:
                # opcode 0x00EE
                return (first_word, 1)
            else:
                # opcode 0x0NNN
                return (first_word, 2)
        elif first_word == 8:
            # opcdoe 0x8XY0 to 0x8XY7 and 0x8XYE
            last_word = instruction & 0xF
            return (first_word, last_word)
        elif first_word == 0xE:
            # opcode 0xEX9E or 0xEXA1
            last_word = instruction & 0xFF
            return (first_word, last_word)
        elif first_word == 0xF:
            # opcode 0xFX07, 0xFX0A, 0xFX15, 0xFX18
            # 0xFX1E, 0xFX29, 0xFX33, 0xFX55 and 0xFX55
            last_word = instruction & 0xFF
            return (first_word, last_word)
        return (first_word, 0)

    def execute(self, instruction, opcode, system):
        # The idea is to take in fnptr with
        # corresponding args and call function
        pass

    def get_x(self, opcode):
        # opcode 0x8ABD = 0xA
        return (opcode >> 8) & 0xF

    def get_y(self, opcode):
        # opcode 0x8ABD = 0xB
        return (opcode >> 4) & 0xF

    def get_address(self, opcode):
        return (opcode & 0x0FFF)

    def get_small_const(self, opcode):
        return (opcode & 0x000F)

    def get_large_const(self, opcode):
        return (opcode & 0x00FF)

    def find_bit_size(self, num):
        # TODO: fix for negative numbers
        size = 0
        while num > 0:
            num >>= 1
            size += 1
        return size

    def find_least_significant_bit(self, num):
        return num & 0b1

    def find_most_significant_bit(self, num):
        return num & (0b1 << (self.find_bit_size(num) - 1)) > 0 if 1 else 0

    def call(self, opcode, system):
        # opcode 0x0NNN
        # execute MLR (machine language routine)
        address = self.get_address(opcode)
        system.pc = address
        if self.verbose:
            print(f"Calling {opcode & 0xFFF}, opcode: {opcode}")

    def display_clear(self, opcode, system):
        # opcode 0x00E0
        # clears the screen
        system.screen.clear()
        if self.verbose:
            print(f"Clearing display!, opcode: {opcode}")

    def flow_return(self, opcode, system):
        # opcode 0x00EE
        # return from subrutine
        address = system.stack.pop(0)
        system.pc = address
        if self.verbose:
            print(f"Returning from subrutine!, opcode: {opcode}")

    def call_subrutine(self, opcode, system):
        # opcode 0x2NNN
        # call subrutine
        system.pc = self.get_address(opcode)
        if self.verbose:
            print(f"Calling subrutine @ {opcode & 0x0FFF}, opcode: {opcode}")

    def skip_if_eqv(self, opcode, system):
        # opcode 0x3XNN
        # skips next instruction if Vx == NN
        x = self.get_x(opcode)
        value = self.get_large_const(opcode)
        if self.verbose:
            print(
                f"Skipping next instruction if: {system.registers[x]} == {value}, opcode: {opcode}")
        if system.registers[x] == value:
            if self.verbose:
                print("Skipping")
            system.pc += 2

    def skip_if_neqv(self, opcode, system):
        # opcode 0x4XNN
        # skips next instruction if Vx != NN
        x = self.get_x(opcode)
        value = self.get_large_const(opcode)
        if self.verbose:
            print(
                f"Skipping next instruction if: {system.registers[x]} != {value}, opcode: {opcode}")
        if system.registers[x] != value:
            if self.verbose:
                print("Skipping")
            system.pc += 2

    def skip_if_eq(self, opcode, system):
        # opcode 0x5XY0
        # skips next instruction if Vx == Vy
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        if self.verbose:
            print(
                f"Skipping next instruction if: {system.registers[x]} != {system.registers[y]}, opcode: {opcode}")
        if system.registers[x] == system.registers[y]:
            if self.verbose:
                print("Skipping")
            system.pc += 2

    def set_val_const(self, opcode, system):
        # opcode 0x6XNN
        # sets Vx to NN
        x = self.get_x(opcode)
        value = self.get_large_const(opcode)
        if self.verbose:
            print(f"Setting register Vx {x} to {value}, opcode: {opcode}")
        system.registers[x] = value

    def add_val_const(self, opcode, system):
        # opcode 0x7XNN
        # adds NN to Vx not changing carry flag
        x = self.get_x(opcode)
        value = self.get_large_const(opcode)
        if self.verbose:
            print(
                f"Adding {value} to x, {x} {system.registers[x]}, opcode: {opcode}")
        system.registers[x] += value

    def assign_reg(self, opcode, system):
        # opcode 8XY0
        # Sets Vx = Vy
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        if self.verbose:
            print(
                f"Assigning {system.registers[y]}, {y} to {system.registers[x]}, {x}, opcode: {opcode}")
        system.registers[x] = system.registers[y]

    def bit_op_or(self, opcode, system):
        # opcode 8XY1
        # Sets Vx |= Vy
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        if self.verbose:
            print(
                f"Oring {system.registers[y]}, {y} to {system.registers[x]} {x}, opcode: {opcode}")
        system.registers[x] = system.registers[x] | system.registers[y]

    def bit_op_and(self, opcode, system):
        # opcode 8XY2
        # Sets Vx &= Vy
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        if self.verbose:
            print(
                f"Anding {system.registers[y]}, {y} to {system.registers[x]} {x}, opcode: {opcode}")
        system.registers[x] = system.registers[x] & system.registers[y]

    def bit_op_xor(self, opcode, system):
        # opcode 8XY3
        # Sets Vx ^= Vy
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        if self.verbose:
            print(
                f"Xoring {system.registers[y]}, {y} to {system.registers[x]} {x}, opcode: {opcode}")
        system.registers[x] = system.registers[x] ^ system.registers[y]

    def math_add(self, opcode, system):
        # opcode 8XY4
        # Vx += Vy and sets carry flag if Vx overflows
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        if system.registers[x] + system.registers[y] > 256:
            system.registers[0xF] = 1
        else:
            system.registers[0xF] = 0
        system.registers[x] = (system.registers[x] + system.registers[y]) % 256

    def math_sub(self, opcode, system):
        # opcode 8XY5
        # Vx -= Vy and sets carry flag to 0 if there is a borrow and 1 when not
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        if system.registers[x] - system.registers[y] < 0:
            system.registers[0xF] = 0
        else:
            system.registers[0xF] = 1
        system.registers[x] = (system.registers[x] - system.registers[y]) % 256

    def bit_op_right_shift(self, opcode, system):
        # opcode 8XY6
        # Stores least significant bit in Vf and rightshifts Vx by 1
        x = self.get_x(opcode)
        system.registers[0xF] = self.find_least_significant_bit(
            system.registers[x])
        system.registers[x] >>= 1

    def math_sub_regs(self, opcode, system):
        # opcode 8XY7
        # Sets Vx to Vy - Vx, Vf is set to 0 when there is a borrow. and 1 when there is not.
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        if system.registers[x] - system.registers[y] < 0:
            system.registers[0xF] = 0
        else:
            system.registers[0xF] = 1
        system.registers[x] = (system.registers[x] - system.registers[y]) % 256

    def bit_op_left_shift(self, opcode, system):
        # opcode 8XYE
        x = self.get_x(opcode)
        system.registers[0xF] = self.find_most_significant_bit(
            system.registers[x])
        system.registers[x] <<= 1

    def skip_if_neqr(self, opcode, system):
        # opcode 9XY0
        # skips next instruction if Vx != Vy
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        if self.verbose:
            print(
                f"Skipping next instruction if: {system.registers[x]} != {system.registers[y]}, opcode: {opcode}")
        if system.registers[x] != system.registers[y]:
            if self.verbose:
                print("skipping")
            system.pc += 2

    def mem_set(self, opcode, system):
        # opcode ANNN
        # sets I = NNN
        system.index = self.get_address(opcode)

    def flow_jmp(self, opcode, system):
        # opcode BNNN
        # sets PC to NNN + V0
        system.pc = self.get_address(opcode) + system.registers[0]

    def random_valr(self, opcode, system):
        # opcode CXNN
        # sets Vx to a random number between 0 and 255 mod NN
        x = self.get_x(opcode)
        value = self.get_large_const(opcode)
        system.registers[x] = randint(0, 255) % value

    def display(self, opcode, system):
        # opcode DXYN
        # draws on screen
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        value = self.get_small_const(opcode)
        system.screen.display(system.registers[x], system.registers[y], value)

    def key_op_skip_eq(self, opcode, system):
        # opcode EX9E
        # skips the next index if key stored in Vx is set
        x = self.get_x(opcode)
        if system.registers[x] > 0:
            system.pc += 2

    def key_op_skip_neq(self, opcode, system):
        # opcode EXA1
        # skips the next index if key stored in Vx is set
        x = self.get_x(opcode)
        if system.registers[x] < 0:
            system.pc += 2

    def timer_get_delay(self, opcode, system):
        # opcode FX07
        # Gets the delay timer and stores it in Vx
        x = self.get_x(opcode)
        system.registers[x] = system.delay

    def key_op_get_key(self, opcode, system):
        # opcode FX0A
        # supposed to wait until a key is pressed and store keypress in Vx
        x = self.get_x(opcode)
        system.registers[x] = system.screen.get_key()

    def set_delay_timer(self, opcode, system):
        # opcode FX15
        # Sets the delay_timer to Vx
        x = self.get_x(opcode)
        system.delay_timer = system.registers[x]

    def set_sound_timer(self, opcode, system):
        # opcode FX18
        # Sets the sound_timer to Vx
        x = self.get_x(opcode)
        system.sound_timer = system.registers[x]

    def mem_add(self, opcode, system):
        # opcode FX1E
        # adds Vx to I, Vf is not affected
        x = self.get_x(opcode)
        system.index += system.registers[x]

    def mem_set_spritaddr(self, opcode, system):
        # opcode FX29
        # Sets I to the location of the sprite[VX]
        pass

    def binary_coded_decimal_store(self, opcode, system):
        # opcode FX33
        # stores the BCD representation of Vx in I
        pass

    def mem_reg_dump(self, opcode, system):
        # opcode FX55
        # stores V0 to VX in memory starting at I, leaves i unchanged
        pass

    def mem_reg_load(self, opcode, system):
        # opcode FX65
        # stores V0 to VX in memory starting at I, leaves i unchanged
        pass
