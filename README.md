# ASSIGNMENT 2: CLASSIFY

## INTRODUCTION
In Assignment 2, we obtained a framework to execute RV32I with [UCB CS61C Venus (RISV-V Simulator)](https://venus.cs61c.org/). Within the framework, we have to modify several draft RV32I assemblies used for Artificial Neural Network (ANN) on Handwritten Digit Classification.


## ABOUT THE FRAMEWORK
This framework is built with Python, composed of the following five Python files. In addition to launch the framework with Python commands, this framework can also be launched with the prepared shell script `test.sh`.

        coverage tests ___                                           ___ function tests
                          \          unittests.py     ______________/
                           \_____    framework.py     _____________/
                            \____    studenttest.py               /
                             \___    tools/check_hashes.py    ___/
                                     convert.py

`test.sh` firstly checks the installed Python version `3` so that the framework can be launched successfully. Then, it will launch the framework with `studenttest.py` for coverage tests, or `unittests.py` for function tests. Regardless of coverage tests or function tests, the common procedure defined in `framework.py` will be followed, i.e., Test Case Init, Workload Specify, and Workload Execute.

          Procedure           |    class / methods defined in `framework.py`
        ----------------------------------------------------------------------
          Test Case Init      |    the constructor of class AssemblyTest
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
It is required to access array elements as well as keep the current max.

        Example: array0 = [1, -2, 3, -4, -5, 6, 7, -8, 9]
                 result = [1, 0, 3, 0, 0, 6, 7, 0, 9]
                         modified workload in TestRelu specified in `unittest.py`

### Function: Maximum Element First Index Finder (src/argmax.s)
It is required to access array elements as well as determine whether to update the index of current max. Hence, my implementation should not only keep the current max, but its index.

        Example: array0 = [3, 432, 432, 7, -5, 6, 5, -114, 2]
                 result = [1]
                         modified workload in TestArgmax specified in `unittest.py`

### Function: Strided Dot Product Calculator (src/dot.s)
Given two arrays, for the standard dot product, it is required to access elements of two arrays at the same index, and do the multiplication on these two elements. After each index-access, accumulate the product result.

        Example: array0 = [-1, 2, -3, 4, 5, 6, 7, 8, -9]
                 array1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                 result = [103]
                         modified workload in TestDot specified in `unittest.py`

For the stride dot product, it may access elements of two arrays with different indices. Hence, two other parameters are needed to specify the strides of arrays. In my implementation, I did not handle the folding cases, so the array access happens on the element out of boundary will cause the error! Besides, we add one another parameter to specify the access count.

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

During each access, if any element of given two arrays has value `0`, this access can be skipped. The below workload is extracted from batch-1 test case of chain-1 workload. I had the wrong skipping flow and struggled to find the bug. The most important lesson I learned from this experience is that each flow design needs to go through the verification test, and we should use the customized workload when the given workload not covering the flow design.

        Example: array0 = [8, -6, 7, 1, -9, -6, 10, 2, 10, 6, -2, 2, -4, -3, 3]
                 array1 = [-5, -5, 15, 5, 0, 9, -3, 9, 10, 13, 15, -4, 15, 5, 0]
                 result = [99]
                         modified workload in TestDot specified in `unittest.py`

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

Function call procedures with stack are involved from the following implementations. I describe what I know about the function call procedure later.

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

The draft RV32I assembly almost complete the implementation with these fundamental function calls, so what should be revised is the substitutions of several `mul` instructions to RV32I instructions. Similarly, I assume that caller is responsible for checking the validation of both the two counts. Besides, the other test case for `Two classifications` is finished in the same time.

#### debug route 1: anatomy of the input and output matrices
I would like to observe input and output matrices, and then try aforementioned stages to obtain the result as well as compare the workload result. However, input and output matrices for this Neural Network Classifier are all binary files. Nevertheless, `hexdump` tool can be used to view their contents. Following are the matrices for workloads classify-1 and classify-2. Assumed that the binary file is stored with 32-bit little-endian format, the binary file can be decoded as the corresponding integer arrays.

          :classify-rv32i$ hexdump tests/classify-1/input.bin
          0000000 0003 0000 0001 0000 0001 0000 0001 0000
          0000010 0001 0000                              
          0000014
                  input[3][1] = {1, 
                                 1, 
                                 1}
          :classify-rv32i$ hexdump tests/classify-1/m0.bin
          0000000 0003 0000 0003 0000 0001 0000 0002 0000
          0000010 0003 0000 0004 0000 0005 0000 0006 0000
          0000020 0007 0000 0008 0000 0009 0000          
          000002c
                  m0[3][3] = {1, 2, 3
                              4, 5, 6,
                              7, 8, 9}
          :classify-rv32i$ hexdump tests/classify-1/m1.bin
          0000000 0003 0000 0003 0000 0001 0000 0003 0000
          0000010 0005 0000 0007 0000 0009 0000 000b 0000
          0000020 000d 0000 000f 0000 0011 0000          
          000002c
                  m1[3][3] = {1, 3, 5
                              7, 9, 11,
                              13, 15, 17}
          :classify-rv32i$ hexdump tests/classify-1/reference.bin
          0000000 0003 0000 0001 0000 00ab 0000 01b9 0000
          0000010 02c7 0000                              
          0000014
                  reference[3][1] = {171, 
                                     441, 
                                     711}
        --------------------------------------------------------------
          Stage 1. h = matmul(m0, input)
                   h[3][1] = {6, 
                              15, 
                              24}
          Stage 2. h = relu(h)
                   h'[3][1] = {6, 
                               15, 
                               24}
          Stage 3. o = matmul(m1, h')
                   o[3][1] = {171, 
                              441, 
                              711}  ... identical to reference[3][1]
          Stage 4. o' = argmax(o) = 2  ... classification as type 2

I tried substituting input and output matrices into the corresponding fundamental function workloads within `unittests.py`, such as matmul(), relu(), argmax(), read_matrix(), write_matrix(). All can pass the function tests correctly. Therefore, I thought that input and output are not the problem cause.

          :classify-rv32i$ hexdump tests/classify-3/input.bin
          0000000 0004 0000 0001 0000 0001 0000 0002 0000
          0000010 0003 0000 0004 0000                    
          0000018
                  input[4][1] = {1, 
                                 2, 
                                 3,
                                 4}
          :classify-rv32i$ hexdump tests/classify-3/m0.bin
          0000000 0003 0000 0004 0000 ffff ffff fffe ffff
          0000010 0003 0000 0004 0000 fffb ffff 0006 0000
          0000020 fff9 ffff 0008 0000 0009 0000 fff6 ffff
          0000030 000b 0000 fff4 ffff                    
          0000038
                  m0[3][4] = {-1, -2, 3, 4, 
                              -5, 6, -7, 8, 
                              9, -10, 11, -12}
          :classify-rv32i$ hexdump tests/classify-3/m1.bin
          0000000 0005 0000 0003 0000 0001 0000 fffd ffff
          0000010 0004 0000 002e 0000 fffe ffff fffb ffff
          0000020 0002 0000 ffc2 ffff 0000 0000 0001 0000
          0000030 0003 0000 000d 0000 001a 0000 fff9 ffff
          0000040 0022 0000                              
          0000044
                  m1[5][3] = {1, -3, 4, 
                              46, -2, -5, 
                              2, -62, 0, 
                              1, 3, 13, 
                              26, -7, 34}
          :classify-rv32i$ hexdump tests/classify-3/reference.bin
          0000000 0005 0000 0001 0000 ffde ffff 0374 0000
          0000010 fbcc ffff 004a 0000 018a 0000          
          000001c
                  reference[5][1] = {-34, 
                                     884, 
                                     -1076, 
                                     74, 
                                     394}
        --------------------------------------------------------------
          Stage 1. h = matmul(m0, input)
                   h[3][1] = {20, 
                              18, 
                              -26}
          Stage 2. h = relu(h)
                   h'[3][1] = {20, 
                               18, 
                               0}
          Stage 3. o = matmul(m1, h')
                   o[5][1] = {-34, 
                              884, 
                              -1076, 
                              74, 
                              394}  ... identical to reference[5][1]
          Stage 4. o' = argmax(o) = 1  ... classification as type 1

I also observe input and output matrices with `hexdump` tool. The above are the matrices for workloads classify-3. I found bugs in `src/dot.s` for not handling the zero sub-dot cases, and `src/relu.s` for misunderstanding its definition.

#### debug route 2: function call procedures
Why function calls? Real world applications are often divided into several fundamental functions for code reuses and collaboration among engineers. On the other hand, the amount of registers in the microprocessor is limited. Hence, when all the object codes are linked into one executable, programmer should avoid the register contents being modified during function call procedures. However, it is impractical to require programmers to use or not to use certain registers. Therefore, the most common solution is using the stack frame. Following are the function call procedures what I know.
 
        Step 1. At the function entry region. 
                The callee function will create new stack frame in memory, 
                and save certain register contents into this stack frame.
        Step 2. During the callee function main body. 
                These saved registers can be used arbitrarily.
        Step 3. At the function exit region. 
                The callee function will restore these register contents 
                from the saved stack frame. Then, free the stack frame.

In the function call procedure, which registers should be saved and restored is depends on the body of the callee function implementation. Besides, the caller function should use `jal` instruction to enter the callee function, and the callee function should use `jr ra` instruction to return to the caller function. I am delighted to learn the difference between `jr ra` and `j exit`, where `j exit` will never return to the caller function, and thus stop the function call procedures.

#### debug route 3: Venus Debugger
According to the introduction of [UCB CS61C Lab3](https://cs61c.org/fa24/labs/lab03/), Venus Debugger provides an online / offline debug GUI for tracing the elements of computer architectures during one RISC-V assembly execution. I use the offline Venus debug GUI to find the problem cause with the following settings.

        Setting 1. Launch the Venus as a local server with default port 6161. 
                   To access local RISC-V assemblies, LOCAL_DIR should be 
                   specified for the local directory with RISC-V assemblies. 
                   #java -jar <PATH_OF_VENUS> -dm <LOCAL_DIR>
        Setting 2. Launch the browser to link to the Venus offline Debug GUI. 
                   Navigate to http://localhost:6161/venus with your brower.
        Setting 3. Access the local RISC-V assemblies with the GUI. 
                   The local RISC-V assemblies are allowable to be access 
                   after LOCAL_DIR be mounted with issuing the command in GUI. 
                   #mount local <REMOTE_DIR> 
                   This command will create <REMOTE_DIR> for mounting the 
                   <LOCAL_DIR>. The password of Venus should be provided.
        Setting 4. Now, the <REMOTE_DIR> will be created in Venus GUI. 
                   For this function test framework, the assemblies often use 
                   relative file path, I suggest change the working directory 
                   into `test-src/` for executing the executable, or you may 
                   encounter some file read failure.

        Example Usage: Interactive between terminal and the browser. 
                   (terminal) // change directory to classify-rv32i
                   (terminal) # java -jar tools/venus.jar -dm .
                   (terminal) // notice the shown venus password
       (Venus GUI in browser) // Enter the GUI `Terminal` tab
       (browser website line) http://localhost:6161/venus
       (Venus GUI in browser) # mount local labs
       (Venus GUI in browser) // input venus password in prompt
       (Venus GUI in browser) # cd labs/test-src
       (Venus GUI in browser) // switch the GUI to `Editor` tab
       (Venus GUI in browser) # edit test_dot_standard.s
       (Venus GUI in browser) // switch the GUI to `Simulator` tab
       (Venus GUI in browser) // Observe the RV32I program execution now!

To debug the function test for `classify`, I found out that the binary file paths for input and output matrix are missing in the generated executables in `test-src/`. During its Workload Specify procedure in `unittests.py`, it is missing one statement to set up the `args`. Because methods for Workload Specify are defined in `framework.py`, I found that method `_input_args()` can be used in this case.

