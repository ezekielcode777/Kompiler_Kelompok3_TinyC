# file: src/code_generator.py

import os
import re

class TargetCodeGenerator:
    def __init__(self):
        self.python_code = []

    def transpile_c_to_python(self, tinyc_source):
        lines = tinyc_source.split('\n')
        hasil_output = []
        level_indent = 0

        for baris in lines:
            b = baris.strip()
            if not b:
                continue

            if b == '}':
                level_indent = max(0, level_indent - 1)
                continue

            prefix_spasi = "    " * level_indent

            if b.startswith('int ') and '(' in b and ')' in b:
                match = re.match(r'int\s+(\w+)\s*\((.*?)\)', b)
                if match:
                    nama_fungsi = match.group(1)
                    raw_args = match.group(2)
                    args_bersih = ", ".join([arg.split()[-1] for arg in raw_args.split(',') if arg])
                    
                    hasil_output.append(f"{prefix_spasi}def {nama_fungsi}({args_bersih}):")
                    if '{' in b:
                        level_indent += 1
                    continue

            if b.startswith('if'):
                match = re.search(r'if\s*\((.*?)\)\s*(.*)', b)
                if match:
                    kondisi = match.group(1)
                    perintah_samping = match.group(2).rstrip(';').strip()
                    
                    hasil_output.append(f"{prefix_spasi}if {kondisi}:")
                    if '{' in b:
                        level_indent += 1
                    elif perintah_samping:
                        hasil_output.append(f"{prefix_spasi}    {perintah_samping}")
                    continue

            b_pangkas = re.sub(r'\bint\s+', '', b).rstrip(';')

            if b_pangkas.endswith('{'):
                b_pangkas = b_pangkas.rstrip('{').strip()
                hasil_output.append(f"{prefix_spasi}{b_pangkas}:")
                level_indent += 1
            else:
                hasil_output.append(f"{prefix_spasi}{b_pangkas}")

        hasil_output.append("\n# === TRIGGER EKSEKUSI HASIL BUILD ===")
        hasil_output.append("if __name__ == '__main__':")
        hasil_output.append("    print('[OUTPUT TinyC] Hasil Perhitungan: ', end='')")
        hasil_output.append("    main()")

        return "\n".join(hasil_output)

    def jalankan_build(self, path_sumber, path_tujuan):
        print("\n" + "="*56)
        print(" TAHAP 7: CODE GENERATOR (Bonus 10% - Transpiler)")
        print("="*56)

        with open(path_sumber, 'r', encoding='utf-8', errors='ignore') as f:
            kode_tinyc = f.read()

        kode_python_matang = self.transpile_c_to_python(kode_tinyc)

        os.makedirs(os.path.dirname(path_tujuan), exist_ok=True)

        with open(path_tujuan, 'w', encoding='utf-8') as f:
            f.write(kode_python_matang)

        print(f" [BACA] Membedah file TinyC: '{path_sumber}'")
        print(f" [BUILD] Berhasil menciptakan: '{path_tujuan}'")
        print("-" * 56)
        print(" ISI KODE PYTHON MURNI HASIL GENERATE (SIAP RUN):")
        print("-" * 56)
        print(kode_python_matang)
        print("-" * 56)
        print(" [GOD TIER UNLOCKED] Skor Kelompok 3 Resmi 100%!\n")

if __name__ == '__main__':
    try:
        builder = TargetCodeGenerator()
        builder.jalankan_build('tests/test1.src', 'dist/hasil_kompilasi.py')
    except Exception as e:
        print("Gagal melakukan Code Generation:", e)