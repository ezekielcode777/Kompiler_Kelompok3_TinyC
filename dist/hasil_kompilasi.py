def faktorial(n):
    if n <= 1:
        return 1
    return n * faktorial(n-1)
def main():
    print(faktorial(5))
    return 0

# === TRIGGER EKSEKUSI HASIL BUILD ===
if __name__ == '__main__':
    print('[OUTPUT TinyC] Hasil Perhitungan: ', end='')
    main()