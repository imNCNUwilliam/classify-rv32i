
TARGET1 := decoder
TARGET2 := matmul

all: 
	$(CC) -o $(TARGET1) $(TARGET1).c
	$(CC) -o $(TARGET2) $(TARGET2).c

clean:
	$(RM) $(TARGET1)
	$(RM) $(TARGET2)
	$(RM) batch1-input.txt
	$(RM) batch1-m0.txt
	$(RM) batch1-m1.txt
	$(RM) batch1-reference.txt

PRINTF = env printf
PASS_COLOR = \e[32;01m
NO_COLOR = \e[0m
pass = $(PRINTF) "$(PASS_COLOR)$1 Passed [-]$(NO_COLOR)\n"

check:	
	make clean || true > /dev/null
	make
	./$(TARGET1)
	./$(TARGET2) batch1-m0.txt batch1-input.txt

