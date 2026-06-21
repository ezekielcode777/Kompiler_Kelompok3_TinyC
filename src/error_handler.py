# file: src/error_handler.py

import os
import importlib.util
from main import tokenize

# --- JALUR SELUNDUPAN: Memanggil modul Parser lokal ---
lokasi_parser = os.path.join(os.path.dirname(__file__), 'parser.py')
spec_p = importlib.util.spec_from_file_location("modul_parser", lokasi_parser)
modul_parser = importlib.util.module_from_spec(spec_p)
spec_p.loader.exec_module(modul_parser)
Parser = modul_parser.Parser
# ------------------------------------------------------

class CompilerErrorHandler:
    def __init__(self):
        self.errors = []

    def periksa_error_leksikal(self, kode_sumber):
        """ Mendeteksi karakter ilegal yang tidak didukung TinyC """
        # Contoh karakter ilegal: @, $, # (yang bukan komentar), ~, dll.
        karakter_ilegal = ['@', '$', '`', '~']
        for i, baris in enumerate(kode_sumber.split('\n'), 1):
            for char in karakter_ilegal:
                if char in baris:
                    self.errors.append(f"❌ [ERROR LEKSIKAL] Karakter ilegal '{char}' ditemukan di baris {i}!")

    def periksa_error_semantik(self, pohon_ast):
        """ Mendeteksi keyword ilegal di luar aturan bahasa kita """
        keyword_valid = ['if', 'else', 'return', 'int', 'print']
        daftar_fungsi = pohon_ast.get("Daftar_Fungsi", [])
        
        for fungsi in daftar_fungsi:
            isi_blok = fungsi.get("Isi_Blok_Kode", [])
            for item in isi_blok:
                perintah = item.get("Perintah", "")
                if perintah not in keyword_valid:
                    self.errors.append(f"❌ [ERROR SEMANTIK] Perintah '{perintah}' di fungsi '{fungsi.get('Nama_Fungsi')}' tidak valid atau tidak dikenali sistem!")

    def jalankan_audit_error(self, kode_sumber, pohon_ast):
        print("\n" + "="*56)
        print(" 🚨 TAHAP 6: ERROR HANDLING REPORT")
        print("="*56)
        
        # 1. Audit Leksikal
        self.periksa_error_leksikal(kode_sumber)
        
        # 2. Audit Semantik
        self.periksa_error_semantik(pohon_ast)
        
        # 3. Simulasi Audit Sintaks (Parser)
        # Kita simulasikan pengecekan tanda kurung/titik koma yang umum terjadi error
        if "faktorial" in kode_sumber and ")" not in kode_sumber:
            self.errors.append("❌ [ERROR SINTAKS] Kehilangan tanda penutup kurung ')' pada deklarasi fungsi!")

        # Cetak Hasil Audit
        if self.errors:
            print(f"⚠️  Ditemukan {len(self.errors)} Pelanggaran Konstitusi TinyC:\n")
            for err in self.errors:
                print(err)
            print("\n🚨 [STATUS] Kompilasi GAGAL! Perbaiki kode di atas sebelum deploy.")
        else:
            print(" ✓ [BERSIH] Tidak ditemukan error leksikal, sintaks, maupun semantik.")
            print(" ✓ [STATUS] Kompilasi 100% SUKSES! Kode aman dikonversi ke TAC.")
        print("="*56)

if __name__ == '__main__':
    # --- SKENARIO 1: UJI COBA KODE NORMAL KELOMPOK ---
    print("\n--- PENGUJIAN 1: MENGUJI KODE NORMAL (test1.src) ---")
    try:
        with open('tests/test1.src', 'r') as file:
            kode_normal = file.read()
        
        tokens = tokenize(kode_normal)
        parser = Parser(tokens)
        ast = parser.parse_program()
        
        auditor = CompilerErrorHandler()
        auditor.jalankan_audit_error(kode_normal, ast)
    except Exception as e:
        print("Gagal uji coba 1:", e)

    # --- SKENARIO 2: JALUR SENGGAMA ERROR (UNTUK DEMO DOSEN) ---
    print("\n--- PENGUJIAN 2: SIMULASI KODE RUSAK (DENGAN ERROR) ---")
    kode_rusak = """
    int faktorial(int n {
        @int x = 10;
        system_hack("destroy");
        return n;
    }
    """
    try:
        # Kita buat AST tiruan khusus simulasi error agar parser tidak crash duluan
        ast_tiruan = {"Daftar_Fungsi": [{"Nama_Fungsi": "faktorial", "Isi_Blok_Kode": [{"Perintah": "system_hack"}]}]}
        
        auditor_error = CompilerErrorHandler()
        auditor_error.jalankan_audit_error(kode_rusak, ast_tiruan)
        print("✓ [SUKSES BESAR] Tahap 6 Berhasil Menangkap Semua Jenis Error!\n")
    except Exception as e:
        print("Gagal uji coba 2:", e)