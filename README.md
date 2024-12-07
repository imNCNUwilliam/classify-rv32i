# ASSIGNMENT 2: CLASSIFY

## INTRODUCTION
In Assignment 2, we obtained a framework to execute RV32I with UCB CS61C Venus (RISV-V Simulator). Within the framework, we have to modify several draft RV32I assemblies used for Artificial Neural Network (ANN) on Handwritten Digit Classification.


## ABOUT THE FRAMEWORK
This framework is built with Python, composed of the following five Python files. In addition to launch the framework with Python commands, this framework can also be launched with the prepared shell script `test.sh`.

        coverage tests ___                                           ___ function tests
                          \          unittests.py     ______________/
                           \_____    framework.py     _____________/
                            \____    studenttest.py               /
                             \___    tools/check_hashes.py    ___/
                                     convert.py

`test.sh` checks the installed Python version `3` so that the framework can be launched successfully. Then, it will launch the framework with `studenttest.py` for coverage tests, or `unittests.py` for function tests. Regardless of coverage tests or function tests, the common procedure defined in `framework.py` will be followed, i.e., Test Case Init, Workload Specify, and Workload Execute.

          Procedure           |    class / methods defined in `framework.py`
        ----------------------------------------------------------------------
          Test Case Init      |    class AssemblyTest
        ----------------------------------------------------------------------
          Workload Specify    |    several methods in class AssemblyTest
        ----------------------------------------------------------------------
          Workload Execute    |    execute() in class AssemblyTest 
                              |    which eventually calls the predefined 
                              |    or customized run_venus()

Actually, RV32I assemblies in `src/` are not executables. During the Workload Execute procedure triggered by execute() of certain Test Case in `unittests.py`, it will generate the corresponding executable based on the Test Case Init configurations, such as linking the libraries, embedding the sub-routine call to the specified RV32I assembly in `src/`, and adding test result verification. Then, the generated executable will be run by predefined or customized run_venus().

I think the Workload Execute procedure is similar to the preprocessing, and linking. The generated executable will be saved at `test-src/` with save_assembly() before run_venus(). It also means that we can specify different workloads in `unittest.py` for function test.

run_venus() will spawn a child process to execute Venus with JAVA. Therefore, when encountering this error `FileNotFoundError: [Errno 2] No such file or directory: 'java'`, it is likely that the JAVA related toolkit, e.g., JDK or JRE, has not been installed yet. Issue `sudo apt install openjdk-11-jdk` can solve the problem.


## MODIFICATION OF RISC-V ASSEMBLY ROUTINES
As mentioned in INTRODUCTION, these RV32I assemblies aim to provide the function of Artificial Neural Network (ANN) on Handwritten Digit Classification. In the implementation, several fundamental functions are integrated to complete the ANN. Following are the fundamental functions integrated as the ANN for classification.

### Function: Absolute Value Converter (src/abs.s)
It is related to two's compliment number representation. Just deal with negative numbers, my implementation is to perform bitwise NOT operation upon the given negative number and then plus 1.

### Function: Array ReLU Activation (src/relu.s)
It is required to access array elements as well as keep the current max. However, I am a little confused that why it can use the same array offset to access every element.

        Example: array0 = [1, -2, 3, -4, -5, 6, 7, -8, 9]
                 result = [1, 0, 3, 0, 0, 6, 7, 0, 9]
                         modified workload in TestRelu specified in `unittest.py`

### Function: Maximum Element First Index Finder (src/argmax.s)
It is required to access array elements as well as determin whether to update the index of current max. Hence, my implementation should not only keep the current max, but its index.

        Example: array0 = [3, 432, 432, 7, -5, 6, 5, -114, 2]
                 result = [1]
                         modified workload in TestArgmax specified in `unittest.py`

### Function: Strided Dot Product Calculator (src/dot.s)
Given two arrays, for the standard dot product, it is required to access elements of two arrays at the same index, and do the multiplication on these two elements. After each index-access, accumulate the product result.

        Example: array0 = [-1, 2, -3, 4, 5, 6, 7, 8, -9]
                 array1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                 result = [103]
                         modified workload in TestDot specified in `unittest.py`

For the stride dot product, it may access elements of two arrays with different indices. Hence, two other parameters are needed to specify the strides of arrays. In my implementation, I did not handle the folding cases, so the array access happens on the element out of boundary will cause the error! Besides, we add one another parameter to specify the access times.

        Example: array0 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                 array1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                 access = [3]
                stride0 = [1]
                stride1 = [3]
                 result = [30]    which equals to (1 * 1 + 2 * 4 + 3 * 7)
                         modified workload in TestDot specified in `unittest.py`

For the multiplication in RV32I, I simply use `add` instruction in the implementation. However, negative values in array elements should be dealt with. In my implementation, I would like to always accumulate value of array0 element `a0` into current dot product result during each access, so it is required to make sure the value of array1 element `a1` is positive for maintaining the accumulation loops. Therefore, the following check needs to be performed.

        a0 > 0, a1 > 0: do nothing
        a0 > 0, a1 < 0: negate both a0 and a1
        a0 < 0, a1 > 0: do nothing
        a0 < 0, a1 < 0: negate both a0 and a1

### Function: Matrix Multiplication Implementation (src/matmul.s)
This function leverages the above strided dot product function in `src/dot.s`. It can be observed that `unittests.py` includes `src/dot.s` after TestMatmul test case init. Besides, given two matrix M0 (rows0 x cols0) and M1 (rows1 x cols1), the implementation of the draft RV32I assembly is capable of finishing the multiplication of M0's the 0-th row with M1. Hence, I simply complete the implementation with accessing the next row of M0, as well as restoring the offset of M1.

        Example: M0 = [1, 2, 3, 
                       4, 5, 6, 
                       7, 8, 10]
                 M1 = [1, 2, 3, 
                       4, 5, 6, 
                       7, 8, 10]
             result = [30, 36, 45, 
                       66, 81, 102, 
                       109, 134, 169]
                     modified workload in TestMatmul specified in `unittest.py`

Although I finish the implementation, I am not familiar with the function call procedure with stack. I got to understand its operations.

### Function: Binary Matrix File Reader (src/read_matrix.s)
The draft RV32I assembly is almost complete. What needs to be revised is the number of elements, which is derived from row count and column count, prepared for dynamic memory allocation. I assume that caller is responsible for validation checks that both of the row count and column count are positive integers.

### Function: Write a matrix of integers to a binary file (src/write_matrix.s)
It is similar to `src/read_matrix.s` that the draft RV32I assembly is almost complete. Hence, I adopt the same revision to complete the implementation. Additionally, both of these two functions use the prepared binary file as the input or output matrix. Hence, I do not modify the workload for further verifications.

### Integration: Neural Network Classifier (src/classify.s)
I think this RV32I assembly is an ANN with pretrained weights, M0, and M1, used for predictions. It could be viewed as a single hidden layer Neural Network. M0 is the weights from input layer to the hidden layer for feature extractions, and ReLU is used for the activation. M1 is the weights from the hidden layer to the output layer for classifications, and Argmax is applied to the output matrix for detemining the most likely outcome.

Therefore, in the draft RV32I assembly of this Neural Network Classifier, it mostly calls the above fundamental functions corresponding to the following stages to finish the classification.

        Stage 0. Preparation.
                 read_matrix for preparing m0, m1, input
        Stage 1. Feature Extraction on Input Matrix with Weights0.
                 h = matmul(m0, input)
        Stage 2. Activation of Features.
                 h = relu(h)
        Stage 3. Classification with Weights1.
                 o = matmul(m1, h)
        Stage 4. Conclusion.
                 argmax(o)

The draft RV32I assembly almost complete the implementation with these fundamental function calls, so what should be revised is the substitutions of several `mul` instructions to RV32I instructions? Similarly, I assume that caller is responsible for checking the validation of both the two counts. Besides, the other test case for `Two classifications` is finished in the same time?

