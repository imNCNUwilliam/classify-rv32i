#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>

#define MAX_LEN 11
char text[MAX_LEN + 1];

/*
 * %type: 0 for delimiter, 1 for carriage return, 2 for ending
 */ 
int append(int val, char *data, int *ppos, int type) {
    memset(text, '\0', MAX_LEN);

    if (type == 0) 
        sprintf(text, "%d ", val);
    else if (type == 1)
        sprintf(text, "%d\n", val);
    else if (type == 2)
        sprintf(text, "%d", val);

    memcpy(data + (*ppos), text, strlen(text));
    *ppos += strlen(text);

    return *ppos;
}

int consume(int fp, unsigned char *symbol) {
    long long sz;

    memset(symbol, '\0', 4);
    sz = read(fp, symbol, 4);

    return *((int32_t *)symbol);
}

int decode(char *src, char *dst) {
    int32_t row, col, val;
    int remaining;
    unsigned char symbol[4];
    long long sz;
    int fp1 = open(src, O_RDWR, 0444);
    int fp2 = open(dst, O_RDWR | O_CREAT, 0644);
    char *data;
    int pos = 0;

    if (fp1 < 0 || fp2 < 0) {
        printf("Failed to open the src / dst files %s / %s\n", src, dst);
        exit(-1);
    }

    row = consume(fp1, &(symbol[0]));
    col = consume(fp1, &(symbol[0]));
    remaining = row * col;
    printf("row / col / remaining bytes: %d / %d / %d\n", row, col, remaining);
    data = (char *)malloc((row * col + 2) * MAX_LEN * sizeof(char));
    memset(data, '\0', sizeof(data));
    append(row, data, &pos, 0);
    append(col, data, &pos, 1);

    while (remaining) {
        val = consume(fp1, &(symbol[0]));
        append(val, data, &pos, remaining == 1 ? 2: 0);
//        printf("%s %d\n", symbol, val);
        remaining--;
    }

    sz = write(fp2, data, pos);
    if (sz != pos) {
        printf("Failed to write the file %s", dst);
        exit(-1);
    }

    free(data);

    close(fp1);
    close(fp2);
    return sz;
}

int main(void) {
    decode("batch1-input.bin", "batch1-input.txt");
    decode("batch1-m0.bin", "batch1-m0.txt");
    decode("batch1-m1.bin", "batch1-m1.txt");
    decode("batch1-reference.bin", "batch1-reference.txt");

    return 0;
}

