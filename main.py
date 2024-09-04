import os
import shutil
import threading
from multiprocessing import Pool, cpu_count
import time

# ЧАСТИНА 1: БАГАТОПОТОКОВЕ КОПІЮВАННЯ ФАЙЛІВ

def copy_files(src_dir, dst_dir):
    def copy_file(src_file, dst_file):
        shutil.copy2(src_file, dst_file)

    def process_directory(directory):
        for entry in os.scandir(directory):
            if entry.is_file():
                file_extension = entry.name.split('.')[-1]
                dest_dir = os.path.join(dst_dir, file_extension)
                os.makedirs(dest_dir, exist_ok=True)
                dest_file = os.path.join(dest_dir, entry.name)
                copy_file(entry.path, dest_file)
            elif entry.is_dir():
                # Запуск нового потоку для обробки піддиректорії
                thread = threading.Thread(target=process_directory, args=(entry.path,))
                thread.start()
                thread.join()  # Чекаємо завершення обробки піддиректорії

    os.makedirs(dst_dir, exist_ok=True)
    process_directory(src_dir)

    print("Файли успішно скопійовані та відсортовані.")

# ЧАСТИНА 2: ФАКТОРИЗАЦІЯ ЧИСЕЛ З ВИКОРИСТАННЯМ multiprocessing

def get_factors(n):
    factors = []
    for i in range(1, n + 1):
        if n % i == 0:
            factors.append(i)
    return factors

def factorize_parallel(*numbers):
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(get_factors, numbers)
    return results

# ВИМІРЮВАННЯ ЧАСУ ВИКОНАННЯ

def time_function(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    return result

if __name__ == "__main__":
    # Оновлення директорії і файлів
    source_dir = './picture'
    destination_dir = './dist'
    copy_files(source_dir, destination_dir)
    
    # Факторизація чисел
    numbers = (128, 255, 99999, 10651060)
    print("\nTesting parallel version:")
    factors = time_function(factorize_parallel, *numbers)

    for num, fac in zip(numbers, factors):
        print(f"Factors of {num}: {fac}")