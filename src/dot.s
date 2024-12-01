.globl dot

.text
# =======================================================
# FUNCTION: Strided Dot Product Calculator
#
# Calculates sum(arr0[i * stride0] * arr1[i * stride1])
# where i ranges from 0 to (element_count - 1)
#
# Args:
#   a0 (int *): Pointer to first input array
#   a1 (int *): Pointer to second input array
#   a2 (int):   Number of elements to process
#   a3 (int):   Skip distance in first array
#   a4 (int):   Skip distance in second array
#
# Returns:
#   a0 (int):   Resulting dot product value
#
# Preconditions:
#   - Element count must be positive (>= 1)
#   - Both strides must be positive (>= 1)
#
# Error Handling:
#   - Exits with code 36 if element count < 1
#   - Exits with code 37 if any stride < 1
# =======================================================
dot:
    li t0, 1
    blt a2, t0, error_terminate  
    blt a3, t0, error_terminate   
    blt a4, t0, error_terminate  

    li t0, 0			# current dot product value kept in register t0
    li t1, 0			# loop index kept in register t1
    slli a3, a3, 2
    slli a4, a4, 2

loop_start:
    lw t2, 0(a0)		# load the first input array element in register t2
    lw t3, 0(a1)		# load the second input array element in register t3
    addi t1, t1, 1
multiply:
    beqz t2, loop_start		# this element product can be omitted
    beqz t3, loop_start		# this element product can be omitted
    li t4, 0			# record the accumulation loop in register t4

    # always accumulate value of register t2 into current dot product result in register t0
    # required to make sure the value of register t3 is positive for maintaining the accumulation loops
    bltz t3, handle_negative
    j accumulate
handle_negative:
    neg t3, t3
    neg t2, t2
accumulate:
    add t0, t0, t2
    addi t4, t4, 1
    blt t4, t3, accumulate	# continue the accumulation

    bge t1, a2, loop_end
    # TODO: Add your own implementation
    add a0, a0, a3
    add a1, a1, a4
    j loop_start

loop_end:
    mv a0, t0
    jr ra

error_terminate:
    blt a2, t0, set_error_36
    li a0, 37
    j exit

set_error_36:
    li a0, 36
    j exit
