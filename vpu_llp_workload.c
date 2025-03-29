#include <stdio.h>
#include <pthread.h> // For multithreading

#define SIZE 1024
#define NUM_THREADS 4 // Number of threads to use

// Shared matrices
float A[SIZE][SIZE];
float B[SIZE][SIZE];
float C[SIZE][SIZE];

typedef struct {
    int thread_id;
    int start_row;
    int end_row;
} ThreadData;

// Function to perform matrix addition for assigned rows
void* matrix_add(void* arg) {
    ThreadData* data = (ThreadData*) arg;

    for (int i = data->start_row; i < data->end_row; i++) {
        for (int j = 0; j < SIZE; j++) {
            C[i][j] = A[i][j] + B[i][j];
        }
    }

    pthread_exit(NULL);
}

int main() {
    // Initialize matrices A and B
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            A[i][j] = i * 1.0f;
            B[i][j] = j * 1.0f;
            
            // printf("A[%d][%d] = %f\n", i, j, A[i][j]);
            // printf("B[%d][%d] = %f\n", i, j, B[i][j]);
        }
    }

    pthread_t threads[NUM_THREADS];
    ThreadData thread_data[NUM_THREADS];
    int rows_per_thread = SIZE / NUM_THREADS;

    // Create threads for parallel matrix addition
    for (int t = 0; t < NUM_THREADS; t++) {
        thread_data[t].thread_id = t;
        thread_data[t].start_row = t * rows_per_thread;
        thread_data[t].end_row = (t + 1) * rows_per_thread;

        pthread_create(&threads[t], NULL, matrix_add, (void*) &thread_data[t]);
    }

    // Join all threads
    for (int t = 0; t < NUM_THREADS; t++) {
        pthread_join(threads[t], NULL);
    }

    // Print a portion of the result matrix for verification
    for (int i = 0; i < 10; i++) {
        printf("C[%d][%d] = %f\n", i, i, C[i][i]);
    }

    return 0;
}
