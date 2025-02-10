
TARGET := decoder

all: 
	$(CC) -o $(TARGET) $(TARGET).c

clean:
	$(RM) $(TARGET)
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
	./$(TARGET)

