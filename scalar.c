#include <iostream>
#include <vector>
#include <chrono>

void add_scalar(const float* a, const float* b, float* result, size_t size) {
    for (size_t i = 0; i < size; ++i) {
        result[i] = a[i] + b[i];
    }
}

int main() {
    size_t size = 1000000;
    std::vector<float> a(size, 1.0f), b(size, 2.0f), result(size);
    auto start = std::chrono::high_resolution_clock::now();
    add_scalar(a.data(), b.data(), result.data(), size);
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "Scalar Execution Time: "
              << std::chrono::duration_cast<std::chrono::microseconds>(end - start).count()
              << " microseconds\n";
    return 0;
}