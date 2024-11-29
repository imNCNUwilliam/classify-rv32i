.globl relu

.text
# ==============================================================================
# FUNCTION: Array ReLU Activation
#
# Applies ReLU (Rectified Linear Unit) operation in-place:
# For each element x in array: x = max(0, x)
#
# Arguments:
#   a0: Pointer to integer array to be modified
#   a1: Number of elements in array
#
# Returns:
#   None - Original array is modified directly
#
# Validation:
#   Requires non-empty array (length ≥ 1)
#   Terminates (code 36) if validation fails
#
# Example:
#   Input:  [-2, 0, 3, -1, 5]
#   Result: [ 0, 0, 3,  0, 5]
# ==============================================================================
relu:
    li t0, 1            # used for input validation check
    blt a1, t0, error     
    li t1, 0            # record the current max with register t1
    li t0, 0		# for the valid data input, used for recording the loop ID

loop_start:
    # TODO: Add your own implementation
    # similar to FUNCTION: Absolute Value Converter
    # required to access array elements as well as keep the current max
    lw t2, 0(a0)
    blt x0, t2, update_max
    add t2, x0, x0
    sw t2, 0(a0)
    j next_loop

update_max:
    bge t1, t2, finish_update
    add t1, t2, x0

finish_update:
    add t2, t1, x0
    sw t2, 0(a0)

next_loop:
    addi t0, t0, 1
#    addi a0, a0, 4
    bne t0, a1, loop_start
    j exit

error:
    li a0, 36          
    j exit          
