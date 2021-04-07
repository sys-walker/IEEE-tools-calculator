import unittest
from low_level_bit_operations import *
from bit_operations import *


# LOW LEVEL OPERATIONS
class LowLeverAdderTestCase(unittest.TestCase):

    def test_binary_addition_0(self):
        # trivial case
        self.assertEqual(low_level_bit_adder("0", "0"), "0")

    def test_binary_addition_1(self):
        self.assertEqual(low_level_bit_adder("1", "0"), "1")

    def test_binary_addition_2(self):
        self.assertEqual(low_level_bit_adder("1", "1"), "10")

    def test_binary_addition_3(self):
        #  Operands of different sizes 1
        self.assertEqual(low_level_bit_adder("0000001", "1"), "10")

    def test_binary_addition_4(self):
        # Operands of different sizes 2
        self.assertEqual(low_level_bit_adder("1", "0000001"), "10")

    def test_extra_zeros_remover_0(self):
        # trivial case
        self.assertEqual(low_level_extra_zeros_remover("0"), "0")
        self.assertEqual(low_level_extra_zeros_remover("0000000"), "0")
        self.assertEqual(low_level_extra_zeros_remover("1110"), "1110")

    def test_extra_zeros_remover_1(self):
        self.assertEqual(low_level_extra_zeros_remover("000000001110"), "1110")


class LowLeverShifterTestCase(unittest.TestCase):

    def test_low_lever_shifter_0(self):
        # trivial cases
        self.assertEqual(low_level_bit_left_shifter("1"), "1")
        self.assertEqual(low_level_bit_left_shifter("1", 0), "1")
        self.assertEqual(low_level_bit_left_shifter("1", -5), "1")

    def test_low_lever_shifter_1(self):
        self.assertEqual(low_level_bit_left_shifter("1", 1), "10")

    def test_low_lever_shifter_2(self):
        self.assertEqual(low_level_bit_left_shifter("1", 2), "100")

    def test_low_lever_shifter_3(self):
        self.assertEqual(low_level_bit_left_shifter("1", 3), "1000")

    def test_low_lever_shifter_4(self):
        self.assertEqual(low_level_bit_left_shifter("1", 4), "10000")


class LowLeverBitInverterTestCase(unittest.TestCase):

    def test_low_level_bit_inverter_0(self):
        # trivial cases
        self.assertEqual(low_level_bit_inverter("1"), "0")
        self.assertEqual(low_level_bit_inverter("0"), "1")

    def test_low_level_bit_inverter_1(self):
        # different sizes
        self.assertEqual(low_level_bit_inverter("1000"), "0111")
        self.assertEqual(low_level_bit_inverter("111"), "000")


# NON LOW LEVEL OPERATIONS
class BitAdderTestCase(unittest.TestCase):
    # these test were omitted because it calls same functions in LowLeverAdderTestCase class
    pass


class BitOnesComplementTestCase(unittest.TestCase):
    # these test were omitted because it calls same functions in LowLeverBitInverterTestCase class
    pass


class BitTwosComplementTestCase(unittest.TestCase):
    def test_twos_complement_0(self):
        # trivial cases
        self.assertEqual(bit_twos_complement("1"), "1")
        self.assertEqual(bit_twos_complement("0"), "10")

    def test_twos_complement_1(self):
        # different sizes
        self.assertEqual(bit_twos_complement("10010"), "1110")
        self.assertEqual(bit_twos_complement("0101110"), "1010010")


if __name__ == '__main__':
    unittest.main()
