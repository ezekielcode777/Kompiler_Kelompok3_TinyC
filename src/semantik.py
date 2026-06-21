# file: src/semantik.py

from main import tokenize

# --- JALUR SELUNDUPAN: Memaksa Python membaca parser.py lokal ---
import importlib.util
import os

lokasi_file_parser = os.path.join(os.path.dirname(__file__), 'parser.py')
spec = importlib.util.spec_from_file_location("modul_parser_kita", lokasi_file_parser)
modul_parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(modul_parser)
Parser = modul_parser.Parser
# ----------------------------------------------------------------

class SemanticAnalyzer:
    def __init__(self):
        # Kamus perintah yang sah di bahasa TinyC kita
        self.keyword_valid = ['if', 'else', 'return', 'int', 'print']

    def analisis_pohon(self, pohon_ast):
        print("\n=== MEMULAI TAHAP 3: SEMANTIC ANALYZER ===")
        
        daftar_fungsi = pohon_ast.get("Daftar_Fungsi", [])
        
        for fungsi in daftar_fungsi:
            nama_fungsi = fungsi["Nama_Fungsi"]
            print(f"Memeriksa fungsi: {nama_fungsi}...")
            
            isi_blok = fungsi["Isi_Blok_Kode"]
            
            for item in isi_blok:
                perintah = item["Perintah"]
                
                if perintah in self.keyword_valid:
                    print(f"  ✓ [VALID] Perintah '{perintah}' dikenali oleh sistem.")
                else:
                    print(f"  ❌ [ERROR] Perintah '{perintah}' tidak valid atau belum dideklarasi!")

if __name__ == '__main__':
    try:
        with open('tests/test1.src', 'r') as file:
            kode_sumber = file.read()
            
        daftar_token = tokenize(kode_sumber)
        if daftar_token:
            mesin_parser = Parser(daftar_token)
            pohon_ast = mesin_parser.parse_program()
            
            mesin_semantik = SemanticAnalyzer()
            mesin_semantik.analisis_pohon(pohon_ast)
            
            print("\n[SUKSES] Tahap 3 selesai! Logika bahasa TinyC tervalidasi aman.")
    except Exception as e:
        print("Waduh, ada error:", e)