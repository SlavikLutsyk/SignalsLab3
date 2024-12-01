import numpy as np
import time


# Функція для генерації випадкового вхідного сигналу розміром N=18
def generate_signal(N=18):
    return np.random.rand(N)


# Лічильник операцій
class OperationCounter:
    def __init__(self):
        self.multiplications = 0
        self.additions = 0

    def increment_multiplications(self, count=1):
        self.multiplications += count

    def increment_additions(self, count=1):
        self.additions += count


# Функція для обчислення ШПФ вручну з підрахунком операцій
def fft_manual(x, op_counter):
    N = len(x)
    if N <= 1:
        return x

    even = fft_manual(x[0::2], op_counter)
    odd = fft_manual(x[1::2], op_counter)

    T = [0] * N
    for k in range(N // 2):
        op_counter.increment_multiplications(3)  # одна комплексна експонента (2 множення + 1 додавання)
        T[k] = np.exp(-2j * np.pi * k / N) * odd[k]

    result = [0] * N
    for k in range(N // 2):
        result[k] = even[k] + T[k]
        result[k + N // 2] = even[k] - T[k]
        op_counter.increment_additions(2)  # одна комплексна операція = 2 додавання

    return result


# Основна програма для обчислення ШПФ і вимірювання часу та операцій
def main():
    N = 22  # Розмір сигналу
    signal = generate_signal(N)
    op_counter = OperationCounter()

    # Обчислення ШПФ вручну та вимірювання часу
    start_time = time.time()
    fft_result = fft_manual(signal, op_counter)
    fft_time = time.time() - start_time

    print(f"Час обчислення ШПФ (N={N}): {fft_time:.5f} секунд")
    print(f"Кількість операцій множення: {op_counter.multiplications}")
    print(f"Кількість операцій додавання: {op_counter.additions}")

    # Вивід результатів ШПФ
    print("\nРезультати ШПФ:")
    for i, value in enumerate(fft_result):
        print(f"C[{i}] = {value:.5f}")


if __name__ == "__main__":
    main()
