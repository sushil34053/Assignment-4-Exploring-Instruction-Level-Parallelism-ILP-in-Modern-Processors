// #include <omp.h>

// // void daxpy(int n, double a, double *x, double *y) {
// void main(int n, double a, double *x, double *y) {
//     #pragma omp parallel for
//     for (int i = 0; i < n; i++) {
//         y[i] = a * x[i] + y[i];
//     }
// }

#include <stdio.h>
#include <stdlib.h>

// Function to perform DAXPY: Y = a * X + Y
void daxpy(int n, double a, double *x, double *y) {
    for (int i = 0; i < n; i++) {
        y[i] = a * x[i] + y[i];
    }
}

int main() {
    int n = 100; // Length of the vectors
    double a = 2.0; // Scalar multiplier

    // Allocate memory for the vectors
    double *x = (double *)malloc(n * sizeof(double));
    double *y = (double *)malloc(n * sizeof(double));

    // Initialize vectors
    for (int i = 0; i < n; i++) {
        x[i] = i + 1.0; // Example: x = [1.0, 2.0, ..., n]
        y[i] = (i + 1.0) * 2.0; // Example: y = [2.0, 4.0, ..., 2n]
    }

    // Perform DAXPY operation
    daxpy(n, a, x, y);

    // Print the result
    printf("Result of DAXPY:\n");
    for (int i = 0; i < n; i++) {
        printf("y[%d] = %f\n", i, y[i]);
    }

    // Free allocated memory
    free(x);
    free(y);

    return 0;
}
