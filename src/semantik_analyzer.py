# file: semantik_analyzer.py

# 1. Kita ambil 'mesin' Parser dan Tokenize dari file temanmu
from main import tokenize
from parser import Parser

class SemanticAnalyzer:
    def __init__(self):
        # Ini adalah daftar kata kunci (keyword) yang valid di tinyC temanmu
        self.keyword_valid = ['if', 'else', 'return', 'int', 'print']

    def analisis_pohon(self, pohon_ast):
        """
        Fungsi untuk memeriksa isi pohon AST dari temanmu.
        Apakah ada perintah (semantic) yang aneh atau salah?
        """
        print("\n=== MEMULAI ANALISIS SEMANTIK ===")
        
        # Ambil daftar fungsi dari batang utama pohon
        daftar_fungsi = pohon_ast.get("Daftar_Fungsi", [])
        
        # Kita periksa setiap fungsi satu per satu
        for fungsi in daftar_fungsi:
            nama_fungsi = fungsi["Nama_Fungsi"]
            print(f"Memeriksa fungsi: {nama_fungsi}...")
            
            # Ambil semua perintah yang ada di dalam fungsi tersebut
            isi_blok = fungsi["Isi_Blok_Kode"]
            
            for item in isi_blok:
                perintah = item["Perintah"]
                
                # CEK SEMANTIK: Apakah perintah ini dikenali oleh bahasa tinyC kita?
                if perintah in self.keyword_valid:
                    print(f"  ✓ Perintah '{perintah}' VALID (Artinya jelas dan dimengerti komputer).")
                else:
                    # Jika ada kata asing yang lolos dari parser tapi tidak logis
                    print(f"  ❌ ERROR SEMANTIK: Perintah '{perintah}' tidak logis atau tidak didukung!")

# --- Tempat Menjalankan Gabungan Kode Kamu dan Temanmu ---
if __name__ == '__main__':
    try:
        # 1. Menggunakan alamat lengkap yang pasti ketemu!
        with open('C:/Users/Asus/Downloads/Kompiler_Kelompok3_TinyC-main/Kompiler_Kelompok3_TinyC-main/tests/test1.src', 'r') as file:
            kode_sumber = file.read()
            
        # 2. Jalankan Tokenizer temanmu
        daftar_token = tokenize(kode_sumber)
        
        if daftar_token:
            # 3. Jalankan Parser temanmu untuk bikin pohon AST
            mesin_parser = Parser(daftar_token)
            pohon_ast = mesin_parser.parse_program()
            
            # 4. SEKARANG TUGAS KAMU: Masukkan pohon itu ke Semantic Analyzer milikmu
            mesin_semantik = SemanticAnalyzer()
            mesin_semantik.analisis_pohon(pohon_ast)
            
            print("\n[SUKSES BESAR] Tugas nomor 3 selesai! Analisis semantik berhasil dijalankan.")
            
    except Exception as e:
        print("Aduh, ada error saat menyambungkan kode:", e)