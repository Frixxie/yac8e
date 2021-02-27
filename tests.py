import unittest
from cpu import C8cpu
from system import System


class CpuTester(unittest.TestCase):
    def test_big_fetch(self):
        system = System()
        system.memory = [0xDA, 0xBF]
        cpu = C8cpu()
        opcode = cpu.fetch(system)
        self.assertEqual(opcode, 0xDABF)
        self.assertEqual(system.pc, 2)

    def test_small_fetch(self):
        system = System()
        system.memory = [0xDA, 0xBF]
        cpu = C8cpu(False)
        opcode = cpu.fetch(system)
        self.assertEqual(opcode, 0xBFDA)
        self.assertEqual(system.pc, 2)

    def test_get_x(self):
        cpu = C8cpu()
        opcode = 0x8ABD
        x = cpu.get_x(opcode)
        self.assertEqual(x, 0xA)

    def test_get_y(self):
        cpu = C8cpu()
        opcode = 0x8ABD
        y = cpu.get_y(opcode)
        self.assertEqual(y, 0xB)

    def test_get_address(self):
        cpu = C8cpu()
        opcode = 0x8ABD
        address = cpu.get_address(opcode)
        self.assertEqual(address, 0xABD)

    def test_get_small_const(self):
        cpu = C8cpu()
        opcode = 0x8ABD
        const = cpu.get_small_const(opcode)
        self.assertEqual(const, 0xD)

    def test_get_large_const(self):
        cpu = C8cpu()
        opcode = 0x8ABD
        const = cpu.get_large_const(opcode)
        self.assertEqual(const, 0xBD)

    def test_find_bit_size(self):
        cpu = C8cpu()
        bit_size = cpu.find_bit_size(17)
        self.assertEqual(bit_size, 5)

    def test_find_least_significant_bit(self):
        cpu = C8cpu()
        bit_set = cpu.find_least_significant_bit(3)
        bit_nset = cpu.find_least_significant_bit(4)
        self.assertEqual(bit_set, 1)
        self.assertEqual(bit_nset, 0)

    def test_find_most_significant_bit(self):
        cpu = C8cpu()
        bit_set = cpu.find_most_significant_bit(3)
        self.assertEqual(bit_set, 1)

    def test_call(self):
        system = System()
        cpu = C8cpu()
        opcode = 0x0ABD
        cpu.call(opcode, system)
        self.assertEqual(system.pc, 0xABD)

    def test_flow_return(self):
        system = System()
        cpu = C8cpu()
        opcode = 0x8ABD
        system.stack.append(cpu.get_address(opcode))
        cpu.flow_return(0x00EE, system)
        self.assertEqual(system.pc, 0xABD)

    def test_flow_goto(self):
        system = System()
        cpu = C8cpu()
        opcode = 0x1123
        cpu.flow_goto(opcode, system)
        self.assertEqual(system.pc, 0x123)

    def test_call_subrutine(self):
        system = System()
        cpu = C8cpu()
        opcode = 0x2ABD
        cpu.call_subrutine(opcode, system)
        self.assertEqual(system.pc, 0xABD)

    def test_skip_if_eqv(self):
        system = System()
        cpu = C8cpu()
        opcode = 0x3277
        system.registers[2] = 0x77
        # test if it works
        cpu.skip_if_eqv(opcode, system)
        self.assertEqual(system.pc, 2)
        system.registers[2] = 0x76
        # test if it works not increasing
        cpu.skip_if_eqv(opcode, system)
        self.assertEqual(system.pc, 2)

    def test_skip_if_neqv(self):
        system = System()
        cpu = C8cpu()
        opcode = 0x4277
        system.registers[2] = 0x77
        # test if it works
        cpu.skip_if_neqv(opcode, system)
        self.assertEqual(system.pc, 0)
        system.registers[2] = 0x76
        # test if it works working
        cpu.skip_if_neqv(opcode, system)
        self.assertEqual(system.pc, 2)

    def test_skip_if_eq(self):
        system = System()
        cpu = C8cpu()
        opcode = 0x5260
        system.registers[2] = 0x77
        system.registers[6] = 0x77
        # test if it works
        cpu.skip_if_eq(opcode, system)
        self.assertEqual(system.pc, 2)
        system.registers[2] = 0x76
        # test if it works working
        cpu.skip_if_eq(opcode, system)
        self.assertEqual(system.pc, 2)

    def test_set_val_const(self):
        system = System()
        cpu = C8cpu()
        opcode = 0x6277
        cpu.set_val_const(opcode, system)
        self.assertEqual(system.registers[2], 0x77)

    def test_add_val_const(self):
        system = System()
        cpu = C8cpu()
        opcode = 0x7437
        system.registers[4] = 0x11
        cpu.add_val_const(opcode, system)
        self.assertEqual(system.registers[4], 0x48)

    def test_assign_reg(self):
        system = System()
        cpu = C8cpu()
        opcode = 0x8430
        system.registers[3] = 0x77
        cpu.assign_reg(opcode, system)
        self.assertEqual(system.registers[3], system.registers[4])

    def test_bit_op_or(self):
        system = System()
        cpu = C8cpu()
        opcode = 0x8431
        system.registers[3] = 0x44
        cpu.bit_op_or(opcode, system)
        self.assertEqual(system.registers[4], 0x44)

    def test_bit_op_and(self):
        system = System()
        cpu = C8cpu()
        opcode = 0x8432
        system.registers[3] = 0x44
        cpu.bit_op_and(opcode, system)
        self.assertEqual(system.registers[4], 0)

    def test_bit_op_xor(self):
        system = System()
        cpu = C8cpu()
        opcode = 0x8433
        system.registers[3] = 0x44
        cpu.bit_op_xor(opcode, system)
        self.assertEqual(system.registers[4], 0x44)

    def test_math_add(self):
        system = System()
        cpu = C8cpu()
        opcode = 0x8434
        system.registers[4] = 15
        system.registers[3] = 20
        cpu.math_add(opcode, system)
        self.assertEqual(system.registers[4], 35)
        self.assertEqual(system.registers[0xF], 0)
        system.registers[4] = 255
        system.registers[3] = 2
        cpu.math_add(opcode, system)
        self.assertEqual(system.registers[4], 1)
        self.assertEqual(system.registers[0xF], 1)

    def test_math_sub(self):
        system = System()
        cpu = C8cpu()
        opcode = 0x8435
        system.registers[4] = 20
        system.registers[3] = 15
        cpu.math_sub(opcode, system)
        self.assertEqual(system.registers[4], 5)
        self.assertEqual(system.registers[0xF], 1)
        system.registers[4] = 1
        system.registers[3] = 2
        cpu.math_sub(opcode, system)
        self.assertEqual(system.registers[4], 255)
        self.assertEqual(system.registers[0xF], 0)

    def test_bit_op_right_shift(self):
        system = System()
        cpu = C8cpu()
        opcode = 0x8435
        system.registers[4] = 4
        cpu.bit_op_right_shift(opcode, system)
        self.assertEqual(system.registers[4], 2)
        self.assertEqual(system.registers[0xF], 0)
        system.registers[4] = 3
        cpu.bit_op_right_shift(opcode, system)
        self.assertEqual(system.registers[4], 1)
        self.assertEqual(system.registers[0xF], 1)

    def test_math_sub_regs(self):
        system = System()
        cpu = C8cpu()
        opcode = 0x8436
        system.registers[4] = 20
        system.registers[3] = 15

        cpu.math_sub(opcode, system)
        self.assertEqual(system.registers[4], 5)
        self.assertEqual(system.registers[0xF], 1)

        system.registers[4] = 1
        system.registers[3] = 2

        cpu.math_sub(opcode, system)
        self.assertEqual(system.registers[4], 255)
        self.assertEqual(system.registers[0xF], 0)

    def test_bit_op_left_shift(self):
        system = System()
        cpu = C8cpu()
        opcode = 0x8437
        system.registers[4] = 4

        cpu.bit_op_left_shift(opcode, system)
        self.assertEqual(system.registers[4], 8)
        self.assertEqual(system.registers[0xF], 1)

        system.registers[4] = 3

        cpu.bit_op_left_shift(opcode, system)
        self.assertEqual(system.registers[4], 6)
        self.assertEqual(system.registers[0xF], 1)

    def test_skip_if_neqr(self):
        system = System()
        cpu = C8cpu()
        opcode = 0x9340
        system.registers[3] = 15
        system.registers[4] = 15
        # test if it not works
        cpu.skip_if_neqr(opcode, system)
        self.assertEqual(system.pc, 0)
        system.registers[3] = 15
        system.registers[4] = 16
        # test if it works
        cpu.skip_if_neqr(opcode, system)
        self.assertEqual(system.pc, 2)

    def test_mem_set(self):
        system = System()
        cpu = C8cpu()
        opcode = 0xA123
        cpu.mem_set(opcode, system)
        self.assertEqual(system.index, 0x123)

    def test_flow_jump(self):
        system = System()
        cpu = C8cpu()
        opcode = 0xB123

        cpu.flow_jmp(opcode, system)
        self.assertEqual(system.pc, 0x123)

        system.registers[0] = 2
        cpu.flow_jmp(opcode, system)
        self.assertEqual(system.pc, 0x125)

    def test_decode(self):
        cpu = C8cpu()

        # Call
        instruction = 0x0123
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (0, 2))

        # display_clear
        instruction = 0x00E0
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (0, 0))

        # flow_return
        instruction = 0x00EE
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (0, 1))

        # flow_goto
        instruction = 0x1123
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (1, 0))

        # call subrutine
        instruction = 0x2123
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (2, 0))

        # skip if eqv
        instruction = 0x3123
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (3, 0))

        # skip if neqv
        instruction = 0x4123
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (4, 0))

        # skip if eq
        instruction = 0x5120
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (5, 0))

        # set val const
        instruction = 0x6120
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (6, 0))

        # add val const
        instruction = 0x7120
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (7, 0))

        # addign reg
        instruction = 0x8120
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (8, 0))

        # bit op or
        instruction = 0x8121
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (8, 1))

        # bit op and
        instruction = 0x8122
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (8, 2))

        # bit op xor
        instruction = 0x8123
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (8, 3))

        # math add
        instruction = 0x8124
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (8, 4))

        # math sub
        instruction = 0x8125
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (8, 5))

        # bit op right shift
        instruction = 0x8126
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (8, 6))

        # math sub regs
        instruction = 0x8127
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (8, 7))

        # bit op left shift
        instruction = 0x812E
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (8, 0xE))

        # skip if neqr
        instruction = 0x9120
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (9, 0))

        # mem set
        instruction = 0xA12E
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (0xA, 0))

        # flow jmp
        instruction = 0xB12E
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (0xB, 0))

        # flow random_valr
        instruction = 0xC12E
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (0xC, 0))

        # display
        instruction = 0xD12E
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (0xD, 0))

        # key op skip eq
        instruction = 0xE19E
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (0xE, 0x9E))

        # key op skip neq
        instruction = 0xE1A1
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (0xE, 0xA1))

        # timer get delay
        instruction = 0xF107
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (0xF, 0x7))

        # key op get key
        instruction = 0xF10A
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (0xF, 0xA))

        # set delay timer
        instruction = 0xF115
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (0xF, 0x15))

        # set sound timer
        instruction = 0xF118
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (0xF, 0x18))

        # mem add
        instruction = 0xF11E
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (0xF, 0x1E))

        # mem set spritaddr
        instruction = 0xF129
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (0xF, 0x29))

        # binary voded decimal store
        instruction = 0xF133
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (0xF, 0x33))

        # mem reg dump
        instruction = 0xF155
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (0xF, 0x55))

        # mem reg load
        instruction = 0xF165
        opcode = cpu.decode(instruction)
        self.assertEqual(opcode, (0xF, 0x65))

    def test_execute(self):
        cpu = C8cpu(testing=True)
        system = System()

        # Call
        instruction = 0x0123
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # display_clear
        instruction = 0x00E0
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # flow_return
        instruction = 0x00EE
        system.stack.append(0x999)
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # flow_goto
        instruction = 0x1123
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # call subrutine
        instruction = 0x2123
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # skip if eqv
        instruction = 0x3123
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # skip if neqv
        instruction = 0x4123
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # skip if eq
        instruction = 0x5120
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # set val const
        instruction = 0x6120
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # add val const
        instruction = 0x7120
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # addign reg
        instruction = 0x8120
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # bit op or
        instruction = 0x8121
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # bit op and
        instruction = 0x8122
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # bit op xor
        instruction = 0x8123
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # math add
        instruction = 0x8124
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # math sub
        instruction = 0x8125
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # bit op right shift
        instruction = 0x8126
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # math sub regs
        instruction = 0x8127
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # bit op left shift
        instruction = 0x812E
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # skip if neqr
        instruction = 0x9120
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # mem set
        instruction = 0xA12E
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # flow jmp
        instruction = 0xB12E
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # flow random_valr
        instruction = 0xC12E
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # display
        instruction = 0xD12E
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # key op skip eq
        instruction = 0xE19E
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # key op skip neq
        instruction = 0xE1A1
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # timer get delay
        instruction = 0xF107
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # key op get key
        instruction = 0xF10A
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # set delay timer
        instruction = 0xF115
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # set sound timer
        instruction = 0xF118
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # mem add
        instruction = 0xF11E
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # mem set spritaddr
        instruction = 0xF129
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # binary voded decimal store
        instruction = 0xF133
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # mem reg dump
        instruction = 0xF155
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)

        # mem reg load
        instruction = 0xF165
        opcode = cpu.decode(instruction)
        cpu.execute(instruction, opcode, system)


if __name__ == '__main__':
    unittest.main()
