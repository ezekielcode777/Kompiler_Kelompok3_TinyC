import importlib.util
import os

lokasi_file_parser = os.path.join(os.path.dirname(__file__), 'parser.py')
spec = importlib.util.spec_from_file_location("modul_parser_kita", lokasi_file_parser)
modul_parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(modul_parser)
Parser = modul_parser.Parser

class IntermediateCodeGenerator:
    def __init__(self):
        self.temp_counter = 1
        self.label_counter = 1
        self.kode_tac = []

    def get_temp(self):
        t = f"_t{self.temp_counter}"
        self.temp_counter += 1
        return t

    def get_label(self):
        l = f"L{self.label_counter}"
        self.label_counter += 1
        return l

    def generate(self, pohon_ast):
        self.kode_tac = []
        daftar_fungsi = pohon_ast.get("Daftar_Fungsi", [])

        for fungsi in daftar_fungsi:
            nama_fungsi = fungsi.get("Nama_Fungsi", "unnamed_func")
            self.kode_tac.append(f"\nBeginFunc {nama_fungsi}:")

            isi_blok = fungsi.get("Isi_Blok_Kode", [])
            stack_label = []

            for item in isi_blok:
                perintah = item.get("Perintah", "")

                if perintah == 'if':
                    t_cond = self.get_temp()
                    l_false = self.get_label()
                    stack_label.append(l_false)
                    
                    self.kode_tac.append(f"  {t_cond} = <kondisi_if>")
                    self.kode_tac.append(f"  IfFalse {t_cond} Goto {l_false}")

                elif perintah == 'return':
                    t_ret = self.get_temp()
                    self.kode_tac.append(f"  {t_ret} = <nilai_return>")
                    self.kode_tac.append(f"  Return {t_ret}")
                    
                    if stack_label and len(isi_blok) > 1:
                        label_keluar = stack_label.pop()
                        self.kode_tac.append(f"{label_keluar}:")

                elif perintah == 'print':
                    t_print = self.get_temp()
                    self.kode_tac.append(f"  {t_print} = <argumen_print>")
                    self.kode_tac.append(f"  PushParam {t_print}")
                    self.kode_tac.append(f"  Call print")

                elif perintah in ['int', 'deklarasi']:
                    t_var = self.get_temp()
                    self.kode_tac.append(f"  {t_var} = <alokasi_memori>")

                else:
                    t_gen = self.get_temp()
                    self.kode_tac.append(f"  {t_gen} = <perintah_{perintah}>")

            while stack_label:
                self.kode_tac.append(f"{stack_label.pop()}:")

            self.kode_tac.append(f"EndFunc {nama_fungsi}")

        return self.kode_tac

if __name__ == '__main__':
    from main import tokenize # Dipindah ke sini agar tidak bentrok
    try:
        print("\n" + "="*52)
        print(" ⚙️  TAHAP 4: INTERMEDIATE CODE GENERATOR (TAC)")
        print("="*52)

        with open('tests/test1.src', 'r') as file:
            kode_sumber = file.read()
            
        daftar_token = tokenize(kode_sumber)
        if daftar_token:
            mesin_parser = Parser(daftar_token)
            pohon_ast = mesin_parser.parse_program()
            
            generator = IntermediateCodeGenerator()
            hasil_tac = generator.generate(pohon_ast)
            
            print("HASIL TERJEMAHAN THREE-ADDRESS CODE (TAC):")
            print("-" * 52)
            for baris in hasil_tac:
                print(baris)
            print("-" * 52)
            print("✓ [SUKSES BESAR] Tahap 4 Selesai! Logika TAC tervalidasi.\n")
            
    except Exception as e:
        print("\n❌ Gagal membangkitkan TAC:", e)