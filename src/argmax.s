.globl argmax

.text
# =================================================================
# FUNCTION: Maximum Element First Index Finder
#
# Scans an integer array to find its maximum value and returns the
# position of its first occurrence. In cases where multiple elements
# share the maximum value, returns the smallest index.
#
# Arguments:
#   a0 (int *): Pointer to the first element of the array
#   a1 (int):  Number of elements in the array
#
# Returns:
#   a0 (int):  Position of the first maximum element (0-based index)
#
# Preconditions:
#   - Array must contain at least one element
#
# Error Cases:
#   - Terminates program with exit code 36 if array length < 1
# =================================================================
argmax:
    li t6, 1
    blt a1, t6, handle_error
    # for the valid data input, use register t6 for recording the loop element index

    lw t0, 0(a0)
    li t1, 0 			# by default the returned index is 0
    add t2, t0, x0 		# by default the current max as 0th array element
    blt t6, a1, next_loop	# examine the single element input array
    add a0, t1, x0
    jr ra

loop_start:
    # TODO: Add your own implementation
    # required to access array elements as well as determine whether to update the index of current max
    # Hence, there should be two registers for recording the current max, and the index respectively
    # keep the index with register t1, and keep the current max with register t2 in my implementation
    # for each array element `n`, we only need to notice this case
    # 		n > current_max, update its value as current max and keep its index
    lw t0, 0(a0)
    bge t2, t0, next_loop
    add t2, t0, x0
    addi t1, t6, -1 

next_loop:
    addi t6, t6, 1
    addi a0, a0, 4
    bge a1, t6, loop_start
    add a0, t1, x0
    jr ra

handle_error:
    li a0, 36
    j exit
