#!/bin/python

from sys import exit
from random import randint
import unittest


class C8cpu():
    def __init__(self, big_endianness: bool = True):
        # Big or little endianness
        # True or false
        self.big_endianness = big_endianness
        # all the operations which an opcode can map too
        self.operations = {}

    def fetch(self, pc, memory):
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
        return pc, instruction

    def decode(self, instruction):
        # The idea is to decode instruction and then return
        # corresponding function call
        pass

    def execute(self, fnptr, opcode):
        # The idea is to take in fnptr with
        # corresponding args and call function
        pass

    def get_x(self, opcode):
        # opcode 0x8ABD = 0xA
        return (opcode >> 8) & 0xF

    def get_y(self, opcode):
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
        return num & 1

    def find_most_significant_bit(self, num):
        return num & (1 << self.find_bit_size(num) - 1) > 0 if 1 else 0

    def call(self, opcode, pc):
        # opcode 0x0NNN
        # execute MLR (machine language routine)
        address = self.get_address(opcode)
        pc = address
        print(f"Calling {opcode & 0xFFF}, opcode: {opcode}")
        return pc

    def display_clear(self, screen, opcode):
        # opcode 0x00E0
        # clears the screen
        screen.clear()
        print(f"Clearing display!, opcode: {opcode}")

    def flow_return(self, opcode, stack, pc):
        # opcode 0x00EE
        # return from subrutine
        address = stack.pop(0)
        pc = address
        print(f"Returning from subrutine!, opcode: {opcode}")
        return pc

    def call_subrutine(self, pc, opcode):
        # opcode 0x2NNN
        # call subrutine
        pc = self.get_address(opcode)
        print(f"Calling subrutine @ {opcode & 0x0FFF}, opcode: {opcode}")
        return pc

    def skip_if_eqv(self, opcode, registers, pc):
        # opcode 0x3XNN
        # skips next instruction if Vx == NN
        x = self.get_x(opcode)
        value = self.get_large_const(opcode)
        print(
            f"Skipping next instruction if: {registers[x]} == {value}, opcode: {opcode}")
        if registers[x] == value:
            print("Skipping")
            pc += 2
        return pc

    def skip_if_neqv(self, opcode, registers, pc):
        # opcode 0x4XNN
        # skips next instruction if Vx != NN
        x = self.get_x(opcode)
        value = self.get_large_const(opcode)
        print(
            f"Skipping next instruction if: {registers[x]} != {value}, opcode: {opcode}")
        if registers[x] != value:
            print("Skipping")
            pc += 2
        return pc

    def skip_if_eq(self, opcode, registers, pc):
        # opcode 0x5XY0
        # skips next instruction if Vx == Vy
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        print(
            f"Skipping next instruction if: {registers[x]} != {registers[y]}, opcode: {opcode}")
        if registers[x] == registers[y]:
            print("Skipping")
            pc += 2
        return pc

    def set_val_const(self, opcode, registers):
        # opcode 0x6XNN
        # sets Vx to NN
        x = self.get_x(opcode)
        value = self.get_large_const(opcode)
        print(f"Setting register Vx {x} to {value}, opcode: {opcode}")
        registers[x] = value

    def add_val_const(self, opcode, registers):
        # opcode 0x7XNN
        # adds NN to Vx not changing carry flag
        x = self.get_x(opcode)
        value = self.get_large_const(opcode)
        print(f"Adding {value} to x, {x} {registers[x]}, opcode: {opcode}")
        registers[x] += value

    def assign_reg(self, opcode, registers):
        # opcode 8XY0
        # Sets Vx = Vy
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        print(
            f"Assigning {registers[y]}, {y} to {registers[x]}, {x}, opcode: {opcode}")
        registers[x] = registers[y]

    def bit_op_or(self, opcode, registers):
        # opcode 8XY1
        # Sets Vx |= Vy
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        print(
            f"Oring {registers[y]}, {y} to {registers[x]} {x}, opcode: {opcode}")
        registers[x] = registers[x] | registers[y]

    def bit_op_and(self, opcode, registers):
        # opcode 8XY2
        # Sets Vx &= Vy
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        print(
            f"Anding {registers[y]}, {y} to {registers[x]} {x}, opcode: {opcode}")
        registers[x] = registers[x] & registers[y]

    def bit_op_xor(self, opcode, registers):
        # opcode 8XY3
        # Sets Vx ^= Vy
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        print(
            f"Xoring {registers[y]}, {y} to {registers[x]} {x}, opcode: {opcode}")
        registers[x] = registers[x] ^ registers[y]

    def math_add(self, opcode, registers):
        # opcode 8XY4
        # Vx += Vy and sets carry flag if Vx overflows
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        if registers[x] + registers[y] > 256:
            registers[0xF - 1] = 1
        else:
            registers[0xF - 1] = 0
        registers[x] = (registers[x] + registers[y]) % 256

    def math_sub(self, opcode, registers):
        # opcode 8XY5
        # Vx -= Vy and sets carry flag to 0 if there is a borrow and 1 when not
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        if registers[x] - registers[y] < 0:
            registers[0xF - 1] = 0
        else:
            registers[0xF - 1] = 1
        registers[x] = (registers[x] - registers[y]) % 256

    def bit_op_right_shift(self, opcode, registers):
        # opcode 8XY6
        # Stores least significant bit in Vf and rightshifts Vx by 1
        x = self.get_x(opcode)
        registers[0xF - 1] = self.find_least_significant_bit(registers[x])
        registers[x] >>= 1

    def math_sub_regs(self, opcode, registers):
        # opcode 8XY7
        # Sets Vx to Vy - Vx, Vf is set to 0 when there is a borrow. and 1 when there is not.
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        if registers[x] - registers[y] < 0:
            registers[0xF - 1] = 0
        else:
            registers[0xF - 1] = 1
        registers[x] = (registers[x] - registers[y]) % 256

    def bit_op_left_shift(self, opcode, registers):
        # opcode 8XYE
        x = self.get_x(opcode)
        registers[0xF - 1] = self.find_most_significant_bit(registers[x])
        registers[x] <<= 1

    def skip_if_neqr(self, opcode, registers, pc):
        # opcode 9XY0
        # skips next instruction if Vx != Vy
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        print(
            f"Skipping next instruction if: {registers[x]} != {registers[y]}, opcode: {opcode}")
        if registers[x] != registers[y]:
            print("skipping")
            pc += 2
        return pc

    def mem_set(self, opcode, index):
        # opcode ANNN
        # sets I = NNN
        index = self.get_address(opcode)
        return index

    def flow_jmp(self, pc, opcode, registers):
        # opcode BNNN
        # sets PC to NNN + V0
        pc = self.get_address(opcode) + registers[0]
        return pc

    def random_valr(self, opcode, registers):
        # opcode CXNN
        # sets Vx to a random number between 0 and 255 mod NN
        x = self.get_x(opcode)
        value = self.get_large_const(opcode)
        registers[x] = randint(0, 255) % value

    def display(self, screen, opcode, registers):
        # opcode DXYN
        # draws on screen
        x = self.get_x(opcode)
        y = self.get_y(opcode)
        value = self.get_small_const(opcode)
        screen.display(registers[x], registers[y], value)

    def key_op_skip_eq(self, pc, opcode, registers):
        # opcode EX9E
        # skips the next index if key stored in Vx is set
        x = self.get_x(opcode)
        if registers[x] > 0:
            pc += 2

    def key_op_skip_neq(self, pc, opcode, registers):
        # opcode EXA1
        # skips the next index if key stored in Vx is set
        x = self.get_x(opcode)
        if registers[x] < 0:
            pc += 2

    def timer_get_delay(self, delay, opcode, registers):
        # opcode FX07
        # Gets the delay timer and stores it in Vx
        x = self.get_x(opcode)
        registers[x] = delay

    def key_op_get_key(self, opcode, registers, screen):
        # opcode FX0A
        # supposed to wait until a key is pressed and store keypress in Vx
        x = self.get_x(opcode)
        registers[x] = screen.get_key()

    def set_delay_timer(self, opcode, registers, delay_timer):
        # opcode FX15
        # Sets the delay_timer to Vx
        x = self.get_x(opcode)
        delay_timer = registers[x]

    def set_sound_timer(self, opcode, registers, sound_timer):
        # opcode FX18
        # Sets the sound_timer to Vx
        x = self.get_x(opcode)
        sound_timer = registers[x]

    def mem_add(self, opcode, registers, index):
        # opcode FX1E
        # adds Vx to I, Vf is not affected
        x = self.get_x(opcode)
        index += registers[x]

    def mem_set_spritaddr(self, opcode, registers, index, sprites):
        # opcode FX29
        # Sets I to the location of the sprite[VX]
        pass

    def binary_coded_decimal_store(self, opcode, registers, index):
        # opcode FX33
        # stores the BCD representation of Vx in I
        pass

    def mem_reg_dump(self, opcode, registers, index):
        # opcode FX55
        # stores V0 to VX in memory starting at I, leaves i unchanged
        pass

    def mem_reg_load(self, opcode, registers, index):
        # opcode FX65
        # stores V0 to VX in memory starting at I, leaves i unchanged
        pass


class Test:
    def __init__(self, pc: int):
        self.pc = pc


class CpuTester(unittest.TestCase):
    def test_big_fetch(self):
        memory = [0xDA, 0xBF]
        pc = 0
        cpu = C8cpu(True)
        pc, opcode = cpu.fetch(pc, memory)
        self.assertEqual(opcode, 0xDABF)
        self.assertEqual(pc, 2)

    def test_small_fetch(self):
        memory = [0xDA, 0xBF]
        pc = 0
        cpu = C8cpu(False)
        pc, opcode = cpu.fetch(pc, memory)
        self.assertEqual(opcode, 0xBFDA)
        self.assertEqual(pc, 2)

    def test_get_x(self):
        cpu = C8cpu(True)
        opcode = 0x8ABD
        x = cpu.get_x(opcode)
        self.assertEqual(x, 0xA)

    def test_get_y(self):
        cpu = C8cpu(True)
        opcode = 0x8ABD
        y = cpu.get_y(opcode)
        self.assertEqual(y, 0xB)

    def test_get_address(self):
        cpu = C8cpu(True)
        opcode = 0x8ABD
        address = cpu.get_address(opcode)
        self.assertEqual(address, 0xABD)

    def test_get_small_const(self):
        cpu = C8cpu(True)
        opcode = 0x8ABD
        const = cpu.get_small_const(opcode)
        self.assertEqual(const, 0xD)

    def test_get_large_const(self):
        cpu = C8cpu(True)
        opcode = 0x8ABD
        const = cpu.get_large_const(opcode)
        self.assertEqual(const, 0xBD)

    def test_find_bit_size(self):
        cpu = C8cpu(True)
        bit_size = cpu.find_bit_size(17)
        self.assertEqual(bit_size, 5)

    def test_find_least_significant_bit(self):
        cpu = C8cpu(True)
        bit_set = cpu.find_least_significant_bit(3)
        bit_nset = cpu.find_least_significant_bit(4)
        self.assertEqual(bit_set, 1)
        self.assertEqual(bit_nset, 0)

    def test_find_most_significant_bit(self):
        cpu = C8cpu(True)
        bit_set = cpu.find_most_significant_bit(3)
        self.assertEqual(bit_set, 1)

    def test_call(self):
        cpu = C8cpu(True)
        opcode = 0x0ABD
        pc = 0
        pc = cpu.call(opcode, pc)
        self.assertEqual(pc, 0xABD)

    def test_flow_return(self):
        cpu = C8cpu(True)
        opcode = 0x8ABD
        stack = list()
        stack.append(cpu.get_address(opcode))
        pc = 0
        pc = cpu.flow_return(0x00EE, stack, pc)
        self.assertEqual(pc, 0xABD)

    def test_call_subrutine(self):
        cpu = C8cpu(True)
        opcode = 0x2ABD
        pc = 0
        pc = cpu.call_subrutine(pc, opcode)
        self.assertEqual(pc, 0xABD)

    def test_skip_if_eqv(self):
        cpu = C8cpu(True)
        opcode = 0x3277
        registers = [0 for _ in range(0xF)]
        registers[2] = 0x77
        pc = 0
        # test if it works
        pc = cpu.skip_if_eqv(opcode, registers, pc)
        self.assertEqual(pc, 2)
        registers[2] = 0x76
        # test if it works not increasing
        pc = cpu.skip_if_eqv(opcode, registers, pc)
        self.assertEqual(pc, 2)

    def test_skip_if_neqv(self):
        cpu = C8cpu(True)
        opcode = 0x4277
        registers = [0 for _ in range(0xF)]
        registers[2] = 0x77
        pc = 0
        # test if it works
        pc = cpu.skip_if_neqv(opcode, registers, pc)
        self.assertEqual(pc, 0)
        registers[2] = 0x76
        # test if it works working
        pc = cpu.skip_if_neqv(opcode, registers, pc)
        self.assertEqual(pc, 2)

    def test_skip_if_eq(self):
        cpu = C8cpu(True)
        opcode = 0x5260
        registers = [0 for _ in range(0xF)]
        registers[2] = 0x77
        registers[6] = 0x77
        pc = 0
        # test if it works
        pc = cpu.skip_if_eq(opcode, registers, pc)
        self.assertEqual(pc, 2)
        registers[2] = 0x76
        # test if it works working
        pc = cpu.skip_if_eq(opcode, registers, pc)
        self.assertEqual(pc, 2)

    def test_set_val_const(self):
        cpu = C8cpu(True)
        opcode = 0x6277
        registers = [0 for _ in range(0xF)]
        cpu.set_val_const(opcode, registers)
        self.assertEqual(registers[2], 0x77)

    def test_add_val_const(self):
        cpu = C8cpu(True)
        opcode = 0x7437
        registers = [0 for _ in range(0xF)]
        registers[4] = 0x11
        cpu.add_val_const(opcode, registers)
        self.assertEqual(registers[4], 0x48)

    def test_assign_reg(self):
        cpu = C8cpu(True)
        opcode = 0x8430
        registers = [0 for _ in range(0xF)]
        registers[3] = 0x77
        cpu.assign_reg(opcode, registers)
        self.assertEqual(registers[3], registers[4])

    def test_bit_op_or(self):
        cpu = C8cpu(True)
        opcode = 0x8431
        registers = [0 for _ in range(0xF)]
        registers[3] = 0x44
        cpu.bit_op_or(opcode, registers)
        self.assertEqual(registers[4], 0x44)

    def test_bit_op_and(self):
        cpu = C8cpu(True)
        opcode = 0x8432
        registers = [0 for _ in range(0xF)]
        registers[3] = 0x44
        cpu.bit_op_and(opcode, registers)
        self.assertEqual(registers[4], 0)

    def test_bit_op_xor(self):
        cpu = C8cpu(True)
        opcode = 0x8433
        registers = [0 for _ in range(0xF)]
        registers[3] = 0x44
        cpu.bit_op_xor(opcode, registers)
        self.assertEqual(registers[4], 0x44)

    def test_math_add(self):
        cpu = C8cpu(True)
        opcode = 0x8434
        registers = [0 for _ in range(0xF)]
        registers[4] = 15
        registers[3] = 20
        cpu.math_add(opcode, registers)
        self.assertEqual(registers[4], 35)
        registers[4] = 255
        registers[3] = 2
        cpu.math_add(opcode, registers)
        self.assertEqual(registers[4], 1)
        self.assertEqual(registers[0xF - 1], 1)

    def test_math_sub(self):
        cpu = C8cpu(True)
        opcode = 0x8435
        registers = [0 for _ in range(0xF)]
        registers[4] = 20
        registers[3] = 15
        cpu.math_sub(opcode, registers)
        self.assertEqual(registers[4], 5)
        self.assertEqual(registers[0xF - 1], 1)
        registers[4] = 1
        registers[3] = 2
        cpu.math_sub(opcode, registers)
        self.assertEqual(registers[4], 255)
        self.assertEqual(registers[0xF - 1], 0)

    def test_bit_op_right_shift(self):
        cpu = C8cpu(True)
        opcode = 0x8435
        registers = [0 for _ in range(0xF)]
        registers[4] = 4
        cpu.bit_op_right_shift(opcode, registers)
        self.assertEqual(registers[4], 2)
        self.assertEqual(registers[0xF - 1], 0)
        registers[4] = 3
        cpu.bit_op_right_shift(opcode, registers)
        self.assertEqual(registers[4], 1)
        self.assertEqual(registers[0xF - 1], 1)

    def test_math_sub_regs(self):
        cpu = C8cpu(True)
        opcode = 0x8436
        registers = [0 for _ in range(0xF)]
        registers[4] = 20
        registers[3] = 15
        cpu.math_sub(opcode, registers)
        self.assertEqual(registers[4], 5)
        self.assertEqual(registers[0xF - 1], 1)
        registers[4] = 1
        registers[3] = 2
        cpu.math_sub(opcode, registers)
        self.assertEqual(registers[4], 255)
        self.assertEqual(registers[0xF - 1], 0)

    def test_bit_op_left_shift(self):
        cpu = C8cpu(True)
        opcode = 0x8437
        registers = [0 for _ in range(0xF)]
        registers[4] = 4
        cpu.bit_op_left_shift(opcode, registers)
        self.assertEqual(registers[4], 8)
        self.assertEqual(registers[0xF - 1], 1)
        registers[4] = 3
        cpu.bit_op_left_shift(opcode, registers)
        self.assertEqual(registers[4], 6)
        self.assertEqual(registers[0xF - 1], 1)


    def test_skip_if_neqr(self):
        cpu = C8cpu(True)
        opcode = 0x9340
        registers = [0 for _ in range(0xF)]
        registers[3] = 15
        registers[4] = 15
        pc = 0
        # test if it not works
        pc = cpu.skip_if_neqr(opcode, registers, pc)
        self.assertEqual(pc, 0)
        registers[3] = 15
        registers[4] = 16
        # test if it works
        pc = cpu.skip_if_neqr(opcode, registers, pc)
        self.assertEqual(pc, 2)

    def test_mem_set(self):
        cpu = C8cpu(True)
        opcode = 0xA123
        index = 0
        index = cpu.mem_set(opcode, index)
        self.assertEqual(index, 0x123)


    def test_flow_jump(self):
        cpu = C8cpu()
        registers = [0 for _ in range(0xF)]
        print(len(registers))
        opcode = 0xB123
        pc = 0
        pc = cpu.flow_jmp(pc, opcode, registers)
        self.assertEqual(pc, 0x123)
        pc = 0
        registers[0] = 2
        pc = cpu.flow_jmp(pc, opcode, registers)
        self.assertEqual(pc, 0x125)

if __name__ == '__main__':
    unittest.main()
