# ASSIGNMENT 2: CLASSIFY

## INTRODUCTION
In Assignment 2, we obtained a framework to execute RV32I with UCB CS61C Venus (RISV-V Simulator). Within the framework, we have to modified to several draft RV32I assemblies used for Artificial Neural Network (ANN) on Handwritten Digit Classification.


## ABOUT THE FRAMEWORK
This framework is built with Python, composed of the following five Python files. In addition to launch the framework with Python commands, this framework can also be launched with shell script `test.sh`.

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
                          |    which calls the predefined or customized 
                          |    run_venus()

`run_venus()` will spawn a child process to execute Venus with JAVA.


## MODIFICATION OF RISC-V ASSEMBLY ROUTINES

### Function: Absolute Value Converter (src/abs.s)
It is related to two's compliment number representation. Just deal with negative numbers, my implementation is to perform bitwise NOT operation upon the given negative number and then plus 1.

### FUNCTION: Array ReLU Activation (src/relu.s)
It is required to access array elements as well as keep the current max. However, I am a little confused that why it can use the same array offset to access every element.

