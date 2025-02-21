#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>

void matmul(int *m1, int row1, int col1, int *m2, int row2, int col2, int *m3) {
    int i, j, k, sum;

    for (i = 0; i < row1; i++) {
        for (j = 0; j < col2; j++) {
            sum = 0;
            for (k = 0; k < col1; k++) {
                sum += (*(m1 + i * col1 + k)) * (*(m2 + k * col2 + j));
            }
            *(m3 + i * col2 + j) = sum;
            printf("%d ", sum);
        }
        printf("\n");
    }
}

void toMat(FILE *fd, int row, int col, int *mat) {
    int status;
    int i, j;

    for (i = 0; i < row; i++) {
        for (j = 0; j < col; j++) {
            status = fscanf(fd, "%d", mat + i * col + j);
            printf("%d ", *(mat + i * col + j));
//            printf("%d ", status);
        }
        printf("\n");
    }
}

int dimension_check(FILE *fd, int *row, int *col) {
    char header[21];
    int status = 0;

    if (fgets(header, sizeof(header), fd) == NULL) {
        fprintf(stderr, "Empty file!\n");
        return -2;
    }
    printf("fgets() got: %s", header);

    status = sscanf(header, "%d %d", row, col);
    printf("sscanf() returned: %d\n", status);
    if (status < 2) {
        printf("Valid Matrix Dimension?\n");
        return -3;
    }

    printf("%d rows; %d cols\n", *row, *col);
    if (*row <= 0 || *col <= 0) {
        printf("Matrix Dimension should be positive!\n");
        return -4;
    }

    return 0;
}

int main(int argc, char *argv[]) {
    char *file1 = argv[1];
    char *file2 = argv[2];
    FILE *fd1, *fd2;
    int row1 = -1, col1 = -1, row2 = -1, col2 = -1;
    int *m1, *m2, *m3;
    int ret;
    int i, j, k, sum;

    // Parse command line arguments
    if (argc != 3) {
        fprintf(stderr, "usage: ./matmul <file1> <file2>\n");
        exit(-1);
    }

    fd1 = fopen(file1, "r");
    fd2 = fopen(file2, "r");
    if (!fd1 || !fd2) {
        fprintf(stderr, "Cannot open file %s or %s.\n", file1, file2);
        return -1;
    }
//    printf("filename / fd are %s / %p and %s / %p\n", file1, fd1, file2, fd2);

    ret = dimension_check(fd1, &row1, &col1);
//    printf("row / col / ret: %d / %d / %d\n", row1, col1, ret);
    m1 = (int *)malloc(row1 * col1 * sizeof(int));
    toMat(fd1, row1, col1, m1);
    printf("%s close with returned code: %d.\n", file1, fclose(fd1));

    ret = dimension_check(fd2, &row2, &col2);
//    printf("row / col / ret: %d / %d / %d\n", row2, col2, ret);
    m2 = (int *)malloc(row2 * col2 * sizeof(int));
    toMat(fd2, row2, col2, m2);
    printf("%s close with returned code: %d.\n", file2, fclose(fd2));

    // dimension check
    if (col1 != row2)
        return -2;
    m3 = (int *)malloc(row1 * col2 * sizeof(int));
    matmul(m1, row1, col1, m2, row2, col2, m3);

    free(m1);
    free(m2);
    free(m3);

    return 0;
}

