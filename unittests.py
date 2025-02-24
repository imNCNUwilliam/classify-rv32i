#!/usr/bin/env python3

import sys
import unittest
from framework import AssemblyTest, run_raw_venus, test_asm_dir, _venus_default_args
from tools.check_hashes import check_hashes


class TestAbs(unittest.TestCase):
    def test_abs_zero(self):
        # load the test for abs.s
        t = AssemblyTest(self, "abs.s")
        # create an array in the data section
        array0 = t.array([0])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # call the `abs` function
        t.call("abs")
        # check that the array0 was changed appropriately
        t.check_array(array0, [0])
        # generate the `assembly/TestAbs_test_zero.s` file and run it through venus
        t.execute()

    def test_abs_one(self):
        # load the test for abs.s
        t = AssemblyTest(self, "abs.s")
        # create an array in the data section
        array0 = t.array([1])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # call the `abs` function
        t.call("abs")
        # check that the array0 was changed appropriately
        t.check_array(array0, [1])
        # generate the `assembly/TestAbs_test_one.s` file and run it through venus
        t.execute()

    def test_abs_minus_one(self):
        # load the test for abs.s
        t = AssemblyTest(self, "abs.s")
        # create an array in the data section
        array0 = t.array([-1])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # call the `abs` function
        t.call("abs")
        # check that the array0 was changed appropriately
        t.check_array(array0, [1])
        # generate the `assembly/TestAbs_test_minus_one.s` file and run it through venus
        t.execute()


class TestRelu(unittest.TestCase):
    def test_relu_standard(self):
        # load the test for relu.s
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([1, -2, 3, -4, 5, -6, 7, -8, 9])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the `relu` function
        t.call("relu")
        # check that the array0 was changed appropriately
        t.check_array(array0, [1, 0, 3, 0, 5, 0, 7, 0, 9])
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute()

    def test_relu_length_1(self):
        # load the test for relu.s
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([-1])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the `relu` function
        t.call("relu")
        # check that the array0 was changed appropriately
        t.check_array(array0, [0])
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute()

    def test_relu_invalid_n(self):
        t = AssemblyTest(self, "relu.s")
        # set a1 to an invalid length of array
        t.input_scalar("a1", -1)
        # call the `relu` function
        t.call("relu")
        # generate the `assembly/TestRelu_test_invalid_n.s` file and run it through venus
        t.execute(code=36)


class TestArgmax(unittest.TestCase):
    def test_argmax_standard(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array0 = t.array([3, -42, 432, 7, -5, 6, 5, -114, 2])
        # load address of the array into register a0
        t.input_array("a0", array0)
        # set a1 to the length of the array
        t.input_scalar("a1", len(array0))
        # call the `argmax` function
        t.call("argmax")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 2)
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute()

    def test_argmax_length_1(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array0 = t.array([3])
        # load address of the array into register a0
        t.input_array("a0", array0)
        # set a1 to the length of the array
        t.input_scalar("a1", len(array0))
        # call the `argmax` function
        t.call("argmax")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 0)
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute()

    def test_argmax_invalid_n(self):
        t = AssemblyTest(self, "argmax.s")
        # set a1 to an invalid length of the array
        t.input_scalar("a1", 0)
        # call the `argmax` function
        t.call("argmax")
        # generate the `assembly/TestArgmax_test_invalid_n.s` file and run it through venus
        t.execute(code=36)


class TestDot(unittest.TestCase):
    def test_dot_standard(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        arr0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        arr1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", arr0)
        t.input_array("a1", arr1)
        # load array attributes into argument registers
        t.input_scalar("a2", len(arr0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", 285)
        t.execute()

    def test_dot_standard2(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        arr0 = t.array([8, -6, 7, 1, -9, -6, 10, 2, 10, 6, -2, 2, -4, -3, 3])
        arr1 = t.array([-5, -5, 15, 5, 0, 9, -3, 9, 10, 13, 15, -4, 15, 5, 0])
        # load array addresses into argument registers
        t.input_array("a0", arr0)
        t.input_array("a1", arr1)
        # load array attributes into argument registers
        t.input_scalar("a2", len(arr0))
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", 99)
        t.execute()

    def test_dot_stride(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        arr0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        arr1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", arr0)
        t.input_array("a1", arr1)
        # load array attributes into argument registers
        t.input_scalar("a2", 3)
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 2)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", 22)
        t.execute()

    def test_dot_length_1(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        arr0 = t.array([9])
        arr1 = t.array([1])
        # load array addresses into argument registers
        t.input_array("a0", arr0)
        t.input_array("a1", arr1)
        # load array attributes into argument registers
        t.input_scalar("a2", 1)
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", 9)
        t.execute()

    def test_dot_stride_error1(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        arr0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        arr1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", arr0)
        t.input_array("a1", arr1)
        # load array attributes into argument registers
        t.input_scalar("a2", 3)
        t.input_scalar("a3", 0)
        t.input_scalar("a4", 2)
        # call the `dot` function
        t.call("dot")
        t.execute(code=37)

    def test_dot_stride_error2(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        arr0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        arr1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", arr0)
        t.input_array("a1", arr1)
        # load array attributes into argument registers
        t.input_scalar("a2", 3)
        t.input_scalar("a3", 2)
        t.input_scalar("a4", 0)
        # call the `dot` function
        t.call("dot")
        t.execute(code=37)

    def test_dot_length_error(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        arr0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        arr1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", arr0)
        t.input_array("a1", arr1)
        # load array attributes into argument registers
        t.input_scalar("a2", 0)
        t.input_scalar("a3", 2)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        t.execute(code=36)

    def test_dot_length_error2(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        arr0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        arr1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", arr0)
        t.input_array("a1", arr1)
        # load array attributes into argument registers
        t.input_scalar("a2", -1)
        t.input_scalar("a3", 2)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        t.execute(code=36)


class TestMatmul(unittest.TestCase):
    def doMatmul(self, m0, m0_rows, m0_cols, m1, m1_rows, m1_cols, result, code=0):
        t = AssemblyTest(self, "matmul.s")
        # we need to include (aka import) the dot.s file since it is used by matmul.s
        t.include("dot.s")

        # load address of input matrices and set their dimensions
        t.input_array("a0", t.array(m0))
        t.input_scalar("a1", m0_rows)
        t.input_scalar("a2", m0_cols)
        t.input_array("a3", t.array(m1))
        t.input_scalar("a4", m1_rows)
        t.input_scalar("a5", m1_cols)
        # load address of output array
        output_array = t.array([-1] * len(result))
        t.input_array("a6", output_array)

        # call the matmul function
        t.call("matmul")
        t.check_array(output_array, result)
        t.execute(code=code)

    def test_matmul_square(self):
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            3,
            3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            3,
            3,
            [30, 36, 42, 66, 81, 96, 102, 126, 150],
        )

    def test_matmul_nonsquare_1(self):
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            2,
            5,
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            5,
            2,
            [95, 110, 220, 260],
        )

    def test_matmul_nonsquare_2(self):
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            5,
            2,
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            2,
            5,
            # fmt: off
            [13, 16, 19, 22, 25, 27, 34, 41, 48, 55, 41, 52, 63, 74, 85, 55, 70, 85, 100, 115, 69, 88, 107, 126, 145],
            # fmt: on
        )
#
#    def test_matmul_nonsquare_3(self):
#        self.doMatmul(
#            [8, -6, 7, 1, -9, -6, 10, 2, 10, 6, -2, 2, -4, -3, 3, 8, 5, 8, -7, -1, -3, -10, 2, 2, -6, -7, 9, 5, -4, -3, 0, 10, -8, -10, -5, 9, 10, 1, 2, -1, -6, -9, 7, -4, 10, -7, -1, 1, 2, 3, -6, 2, -8, 6, -3, 8, 4, 3, -6, -9, -6, 8, 1, -3, 1, 3, -9, -6, 3, -5, -7, 8, 10, 2, 6, 8, -7, 7, 2, 5, 2, -7, 6, -3, 4, 4, 6, 0, 8, 10, -6, -3, -5, -2, 7, 4, 4, 7, 10, 10, 9, -4, -9, -1, 1, 7, 1, 6, 2, 4, -6, -9, -9, 3, -2, -7, -5, -10, 3, 6, 10, 10, 4, -8, 10, 9, -3, -2, 9, 6, -3, -1, -8, 1, 3, 2, 2, -10, 1, 9, -7, 7, -9, 0, -6, 2, 1, 2, -2, 0, 9, 1, -4, -2, 5, -7, 1, -10, -5, -6, -2, 0, -3, 4, -9, -1, -9, -7, -9, 10, -2, 10, 3, -2, 5, -3, 6, -2, 7, -4, 10, 2, 4, -7, 1, -6, 4, -8, 9, -7, -6, 0, 5, -6, 0, 7, 7, 10, -10, -4, -10, -8, -8, 10, -10, -5, -4, -3, -3, 1, -8, -3, -6, -5, -2, -10, -5, 0, 9, -7, -10, -10, -9, 1, -4, 10, -10, 3, 7, -7, 1, 7, 0, 2, -8, -10, 5, 8, -1, 0, 1, 3, 10, -8, 8, -4, 0, -3, -8, 6, -4, -4, -7, -9, 2, -4, -9, -3, -7, 9, -2, -6, 0, 0, -4, 10, -10, 0, -3, 2, -4, -9, 1, -9, -2, -6, 0, 6, 6, 5, 4, 1, -1, -3, 7, -4, 6, -10, 2, 8, 2, 5, 10, 10, -4, 3, 1, -3, -6, -1, 10, -8, -8, 4, -2, 9, 4, -3, -3, 10, 3, 5, -2, 8, 1, 1, 9, 2, 10, -8, -3, -3, -1, -4, -7, -5, 3, 9, -1, -1, -7, 3, 0, 0, 9, -1, 9, -1, 2, -5, -10, -3, -10, 9, -4, -7, 7, 2, 10, -3, -4, 0, 1, -3, 0, -4, 4, 3, 9, 3, -2, -3, 6, 0, -3, 5, 8, -5, 3, -1, 8, 10, 6, -1, -9, -3, 9, -10, -3, 10, -9, 8, -10, -5, -3, -3, -8, -10, -7, -8, 5, -8, 5, 10, -1, 5, -4, 1, -7, 2, 6, -10, -7, 8, 7, -6, 1, 10, -4, 3, 9, 3, 10, -4, -7, 3, 9, -10, 7, 6, -3, 0, -9, -10, -1, -9, -5, -6, 4, -10, -7, 7, -7, 8, -6, -6, -10, -10, 6, 9, -6, -3, -1, 2, -9, -10, -4, 9, 9, 6],
#            30,
#            15,
#            [-5, 2, 1, 8, 12, 12, -1, 13, 2, 15, 15, 0, -5, 5, 10, -5, 15, 1, 15, -3, 1, 3, 9, 8, 14, 0, 15, -2, 8, 12, 15, 10, 5, 5, 11, 14, 2, -4, 0, -1, 10, 5, 10, 15, 1, 5, 6, -5, 6, 12, 13, 6, 13, 8, 8, -3, 8, -4, -1, 12, 0, 13, 15, 7, -2, 5, -5, 3, -3, 12, 1, -5, -2, 10, -4, 9, -3, 9, 3, -4, 10, 3, 9, 2, -1, 6, 11, 15, 7, 7, -3, 7, 11, 6, 2, 11, -4, 0, -1, 3, 14, 15, 10, 13, -1, 9, -5, 7, 10, -1, -5, 12, 8, 7, 12, 3, -5, 4, 2, -3, 10, 12, 15, -2, 2, 1, -5, 7, 0, 2, 11, 2, 8, 14, 15, 13, -2, 7, 13, 7, 8, 13, 0, 5, 8, 6, 7, 0, -3, 2, 15, 12, -1, 12, 10, 15, -3, 12, -1, -4, 0, 6, 3, 7, 2, -4, 7, -2, 9, 12, 5, -1, 12, -4, 10, -3, -4, -4, 10, 2, 15, 3, 10, 0, 7, -1, -4, 7, 9, 8, -3, -5, 6, 9, 11, 5, 13, 14, 7, 0, 9, 9, -1, 0, 5, 5, 15, -5, -5, 12, 0, 2, -5, 0, 9, -1, 14, 3, 3, -1, 0, 7, 5, 14, 13],
#            15,
#            15,
            # fmt: off
#            [99, 16, 60, 45, 328, 208, 68, 24, -8, 35, 425, 110, 146, 247, 126, -103, 17, -64, -32, 85, -177, -133, 80, -2, 208, -8, -351, -83, 160, 41, -122, -137, 154, -86, -277, -256, 58, -17, 160, -3, 144, 271, 335, 237, 219, 73, 219, -12, -80, 43, 46, -408, -1, -124, -153, -133, -150, -10, 88, -137, -22, 157, 22, -108, -26, -223, -23, 52, 56, 65, -237, -57, 16, 206, 294, 301, 143, 113, 281, 404, 332, 339, 241, 36, 240, 134, 20, -16, 206, 219, 288, 95, 320, 200, -93, 117, 118, 73, -41, -21, 178, 145, 187, 108, -68, -264, 95, -168, -161, 24, -11, 46, -190, -95, -55, 55, -8, -231, -78, 111, 4, 302, 365, 283, -33, 220, 71, 162, -13, 306, 397, 242, 108, 360, 262, -362, 195, -19, -63, -43, -37, -323, 41, -101, 64, -90, -58, -183, 59, -27, -459, 77, -91, -89, -107, 8, -321, -123, -172, 42, -14, -110, -353, -250, -159, -140, -21, 357, 58, -142, -19, -61, -158, -195, 113, 120, -103, -65, -64, -310, -219, 134, 74, -202, 56, -80, -365, -42, -79, 48, 220, -159, 44, 317, 110, -257, 127, -164, -302, -67, -257, -262, -235, -119, -165, 91, -182, -80, 118, 78, -376, -272, -131, -555, -529, -638, -150, -521, -167, -386, -178, -309, -187, -469, -297, -71, -137, 1, -207, 255, 91, -112, 118, 34, 88, 186, -115, 90, 145, 175, -169, -88, -115, 16, -73, -50, 1, -326, -98, -48, 50, -106, -14, 45, -374, 108, -111, -12, -246, -190, -192, -169, -194, -145, -336, -165, -322, 23, -107, -297, 186, -136, 27, -99, 59, -182, 86, -147, -87, -189, 38, -212, 122, 93, -153, -43, 159, 213, 143, -172, -113, -88, 290, 44, 212, 16, -13, 96, 227, 25, 67, -51, 115, 224, 232, 411, 184, 249, -1, 156, 215, 255, -45, -94, 198, -85, 45, -246, -3, 133, -56, 3, 166, 204, 159, -193, 26, -111, -13, 253, -313, 191, 271, -60, -361, -50, -57, -287, -140, 4, 97, 207, -45, -61, -143, 37, 215, -22, 153, 108, 53, 241, 57, 154, 167, -148, 256, -113, -21, 252, 273, 229, 179, 121, 218, 364, -278, 172, -78, -37, 128, 99, 221, 289, 20, -677, -9, -177, -152, -466, -267, -369, -342, -178, -109, -152, -46, -288, -298, -450, 227, -50, -105, 77, 186, 369, 340, 20, 52, -124, 97, 260, -3, -166, 120, 80, 200, 132, 242, 6, 202, 223, 66, -106, 1, 103, 234, 219, 319, -66, -578, -43, -136, -356, -372, -473, -269, -312, -290, -190, -224, -283, -371, -370, -214, -145, -57, 116, -409, -169, -361, -35, -167, -7, -36, -282, -274, -175, -194, 79],
            # fmt: on
#        )

    def test_matmul_nonsquare_outer_dims(self):
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            5,
            2,
            [1, 2, 3, 4, 5, 6],
            2,
            3,
            [9, 12, 15, 19, 26, 33, 29, 40, 51, 39, 54, 69, 49, 68, 87],
        )

    def test_matmul_length_1(self):
        self.doMatmul([4], 1, 1, [5], 1, 1, [20])

    def test_matmul_zero_dim_m0(self):
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            0,
            3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            3,
            3,
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],  # result does not matter
            code=38,
        )

    def test_matmul_negative_dim_m0_y(self):
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            3,
            -1,
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            3,
            3,
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],  # result does not matter
            code=38,
        )

    def test_matmul_negative_dim_m0_x(self):
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            -1,
            3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            3,
            3,
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],  # result does not matter
            code=38,
        )

    def test_matmul_incorrect_check(self):
        # fmt: off
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            5,
            3,
            [ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            4,
            5,
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # result does not matter
            code=38,
        )
        # fmt: on

    def test_matmul_zero_dim_m1(self):
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            3,
            3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            0,
            3,
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],  # result does not matter
            code=38,
        )

    def test_matmul_negative_dim_m1_y(self):
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            3,
            3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            3,
            -1,
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],  # result does not matter
            code=38,
        )

    def test_matmul_negative_dim_m1_x(self):
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            3,
            3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            -1,
            3,
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],  # result does not matter
            code=38,
        )

    def test_matmul_unmatched_dims(self):
        self.doMatmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            3,
            2,
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            3,
            3,
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],  # result does not matter
            code=38,
        )


class TestReadMatrix(unittest.TestCase):
    def doReadMatrix(
        self,
        input_file,
        result_row=3,
        result_col=3,
        result_array=[1, 2, 3, 4, 5, 6, 7, 8, 9],
        fail="",
        code=0,
    ):
        t = AssemblyTest(self, "read_matrix.s")
        # load address to the name of the input file into register a0
        t.input_read_filename("a0", input_file)

        # allocate space to hold the rows and cols output parameters
        rows = t.array([-1])
        cols = t.array([-1])

        # load the addresses to the output parameters into the argument registers
        t.input_array("a1", rows)
        t.input_array("a2", cols)

        # call the main function within test_read_matrix_no_cc, which randomizes registers and calls read_matrix
        t.call("read_matrix")

        if not fail:
            # check the output from the function
            t.check_array(rows, [result_row])
            t.check_array(cols, [result_col])
            t.check_array_pointer("a0", result_array)

        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)

    def test_read_1(self):
        self.doReadMatrix(
            input_file="../tests/read-matrix-1/input.bin",
            result_row=3,
            result_col=3,
            result_array=[1, 2, 3, 4, 5, 6, 7, 8, 9],
        )

    def test_read_2(self):
        self.doReadMatrix(
            input_file="../tests/read-matrix-2/input.bin",
            result_row=3,
            result_col=1,
            result_array=[2, 1, 6],
        )

    def test_read_3(self):
        self.doReadMatrix(
            input_file="../tests/read-matrix-3/input.bin",
            result_row=15,
            result_col=15,
            # fmt: off
            result_array= [-5, 2, 1, 8, 12, 12, -1, 13, 2, 15, 15, 0, -5, 5, 10, 
                           -5, 15, 1, 15, -3, 1, 3, 9, 8, 14, 0, 15, -2, 8, 12, 
                           15, 10, 5, 5, 11, 14, 2, -4, 0, -1, 10, 5, 10, 15, 1, 
                           5, 6, -5, 6, 12, 13, 6, 13, 8, 8, -3, 8, -4, -1, 12, 
                           0, 13, 15, 7, -2, 5, -5, 3, -3, 12, 1, -5, -2, 10, -4, 
                           9, -3, 9, 3, -4, 10, 3, 9, 2, -1, 6, 11, 15, 7, 7, 
                           -3, 7, 11, 6, 2, 11, -4, 0, -1, 3, 14, 15, 10, 13, -1, 
                           9, -5, 7, 10, -1, -5, 12, 8, 7, 12, 3, -5, 4, 2, -3, 
                           10, 12, 15, -2, 2, 1, -5, 7, 0, 2, 11, 2, 8, 14, 15, 
                           13, -2, 7, 13, 7, 8, 13, 0, 5, 8, 6, 7, 0, -3, 2, 
                           15, 12, -1, 12, 10, 15, -3, 12, -1, -4, 0, 6, 3, 7, 2, 
                           -4, 7, -2, 9, 12, 5, -1, 12, -4, 10, -3, -4, -4, 10, 2, 
                           15, 3, 10, 0, 7, -1, -4, 7, 9, 8, -3, -5, 6, 9, 11, 
                           5, 13, 14, 7, 0, 9, 9, -1, 0, 5, 5, 15, -5, -5, 12, 
                           0, 2, -5, 0, 9, -1, 14, 3, 3, -1, 0, 7, 5, 14, 13]
            # fmt: on
        )

    def test_read_fail_fopen(self):
        self.doReadMatrix(
            input_file="../tests/read-matrix-1/input.bin",
            result_row=3,
            result_col=3,
            result_array=[1, 2, 3, 4, 5, 6, 7, 8, 9],
            fail="fopen",
            code=27,
        )

    def test_read_fail_fread(self):
        self.doReadMatrix(
            input_file="../tests/read-matrix-1/input.bin",
            result_row=3,
            result_col=3,
            result_array=[1, 2, 3, 4, 5, 6, 7, 8, 9],
            fail="fread",
            code=29,
        )

    def test_read_fail_fclose(self):
        self.doReadMatrix(
            input_file="../tests/read-matrix-1/input.bin",
            result_row=3,
            result_col=3,
            result_array=[1, 2, 3, 4, 5, 6, 7, 8, 9],
            fail="fclose",
            code=28,
        )

    def test_read_fail_malloc(self):
        self.doReadMatrix(
            input_file="../tests/read-matrix-1/input.bin",
            result_row=3,
            result_col=3,
            result_array=[1, 2, 3, 4, 5, 6, 7, 8, 9],
            fail="malloc",
            code=26,
        )


class TestWriteMatrix(unittest.TestCase):
    def doWriteMatrix(self, output_file, reference_file, fail="", code=0):
        t = AssemblyTest(self, "write_matrix.s")
        # load output file name into a0 register
        t.input_write_filename("a0", output_file)
        # load input array and other arguments
        t.input_array("a1", t.array([1, 2, 3, 4, 5, 6, 7, 8, 9]))
        t.input_scalar("a2", 3)  # rows
        t.input_scalar("a3", 3)  # columns
        # call `write_matrix` function
        t.call("write_matrix")
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
        # compare the output file against the reference
        if code == 0:
            t.check_file_output(output_file, reference_file)

    def test_write_1(self):
        self.doWriteMatrix(
            output_file="../tests/write-matrix-1/output.bin",
            reference_file="../tests/write-matrix-1/reference.bin",
        )

    def test_write_fail_fopen(self):
        self.doWriteMatrix(
            output_file="../tests/write-matrix-1/output.bin",
            reference_file="../tests/write-matrix-1/reference.bin",
            fail="fopen",
            code=27,
        )

    def test_write_fail_fwrite(self):
        self.doWriteMatrix(
            output_file="../tests/write-matrix-1/output.bin",
            reference_file="../tests/write-matrix-1/reference.bin",
            fail="fwrite",
            code=30,
        )

    def test_write_fail_fclose(self):
        self.doWriteMatrix(
            output_file="../tests/write-matrix-1/output.bin",
            reference_file="../tests/write-matrix-1/reference.bin",
            fail="fclose",
            code=28,
        )


class TestClassify(unittest.TestCase):
    def make_test(self):
        t = AssemblyTest(self, "classify.s")
        t.include("argmax.s")
        t.include("dot.s")
        t.include("matmul.s")
        t.include("read_matrix.s")
        t.include("relu.s")
        t.include("write_matrix.s")
        return t

    def run_classify(self, test_dir, classification, msg: str = "", fail="", code=0):
        t = self.make_test()
        outfile = f"{test_dir}/output.bin"
        args = [
            f"{test_dir}/m0.bin",
            f"{test_dir}/m1.bin",
            f"{test_dir}/input.bin",
            outfile,
        ]
        silent = len(msg) == 0
        t._input_args(args)
        t.input_scalar("a0", 5)
        t.input_scalar("a2", 1 if silent else 0)
        t.call("classify")
        t.check_scalar("a0", classification)
        t.execute(fail=fail, code=code, args=args)
        if code == 0:
            t.check_file_output(outfile, f"{test_dir}/reference.bin")
            if msg != "":
                msg += "\n\n"
            msg += f"Exited with error code {code}"
            t.check_stdout(msg)

    def test_classify_1_silent(self):
        self.run_classify(test_dir="../tests/classify-1", classification=2)

    def test_classify_fail_malloc(self):
        # unfortunately this test actually does not fail inside classify, but inside read_matrix
        self.run_classify(
            test_dir="../tests/classify-1", classification=2, fail="malloc", code=26
        )

    def test_classify_2_print(self):
        self.run_classify(test_dir="../tests/classify-2", classification=2, msg="2")

    def test_classify_3_print(self):
        self.run_classify(test_dir="../tests/classify-3", classification=1, msg="1")

    def test_classify_4_print(self):
        self.run_classify(test_dir="../tests/classify-4", classification=48)

    def test_classify_not_enough_args(self):
        t = self.make_test()
        t.input_scalar("a2", 1)
        t.call("classify")
        t.execute(code=31, args=[""])


# The following are some simple sanity checks:
import subprocess, pathlib, os

script_dir = pathlib.Path(os.path.dirname(__file__)).resolve()


def compare_files(test, actual, expected):
    full_actual = (test_asm_dir / actual).resolve()
    full_expected = (test_asm_dir / expected).resolve()
    assert (
        full_expected.is_file()
    ), f"Reference file {str(full_expected)} does not exist!"
    test.assertTrue(
        full_actual.is_file(),
        f"It seems like the program never created the output file {str(full_actual)}",
    )
    # open and compare the files
    with full_actual.open("rb") as a:
        actual_bin = a.read()
    with full_expected.open("rb") as e:
        expected_bin = e.read()
    test.assertEqual(
        actual_bin,
        expected_bin,
        f"Bytes of {str(full_actual)} and {str(full_expected)} did not match!",
    )


class TestChain(unittest.TestCase):
    def run_venus(self, args):
        # run venus from the project root directory
        r = run_raw_venus(args=args, check_calling_convention=True)
        return r.returncode, r.stdout.decode("utf-8").strip()

    def test_chain_1(self):
        code, stdout = self.run_venus(["../tests/chain-1/chain.s"])

        self.assertEqual(
            stdout,
            "Two classifications:\n2\n2\nTwo classifications:\n2\n48\nTwo classifications:\n48\n48\n\nExited with error code 0",
        )

        batch0_outfile = f"../tests/chain-1/batch0-output.bin"
        batch0_reffile = f"../tests/chain-1/batch0-reference.bin"
        batch1_outfile = f"../tests/chain-1/batch1-output.bin"
        batch1_reffile = f"../tests/chain-1/batch1-reference.bin"

        compare_files(
            self,
            actual=batch0_outfile,
            expected=batch0_reffile,
        )
        compare_files(
            self,
            actual=batch1_outfile,
            expected=batch1_reffile,
        )


if __name__ == "__main__":
    split_idx = sys.argv.index("--")
    for arg in sys.argv[split_idx + 1 :]:
        _venus_default_args.append(arg)

    check_hashes()

    unittest.main(argv=sys.argv[:split_idx])
