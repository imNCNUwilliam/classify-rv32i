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
    li t0, 0		# for the valid data input, used for recording the loop ID

loop_start:
    # TODO: Add your own implementation
    # require to access array elements
    # for each array element `n`, only deal with this case
    # 		n < 0			, in-place modify its value as 0
    lw t1, 0(a0)
    bge t1, x0, next_loop
    add t1, x0, x0
    sw t1, 0(a0)

next_loop:
    addi t0, t0, 1
    addi a0, a0, 4
    bne t0, a1, loop_start
    jr ra

error:
    li a0, 36          
    j exit          
