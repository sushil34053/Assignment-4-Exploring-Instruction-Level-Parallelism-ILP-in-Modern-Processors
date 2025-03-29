#include <stdio.h>
#include <immintrin.h> // For vector intrinsics (e.g., AVX)

#define SIZE 1024

void vector_add(float *a, float *b, float *c, int n) {
    for (int i = 0; i < n; i += 8) {
        // Load 8 elements from arrays a and b
        __m256 vec_a = _mm256_loadu_ps(&a[i]);
        __m256 vec_b = _mm256_loadu_ps(&b[i]);
        // Perform element-wise addition
        __m256 vec_c = _mm256_add_ps(vec_a, vec_b);
        // Store the result in array c
        _mm256_storeu_ps(&c[i], vec_c);
    }
}

int main() {
    float a[SIZE], b[SIZE], c[SIZE];
    // Initialize arrays
    for (int i = 0; i < SIZE; i++) {
        a[i] = i * 1.0f;
        b[i] = (SIZE - i) * 1.0f;
    }

    // Perform vector addition
    vector_add(a, b, c, SIZE);

    // Print some results
    for (int i = 0; i < 10; i++) {
        printf("c[%d] = %f\n", i, c[i]);
    }

    return 0;
}
