import json

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0 # Penunjuk posisi token saat ini

    def ambil_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def maju(self):
        self.pos += 1

    def parse_program(self):
        ast = {
            "Tipe_Node": "Program_TinyC",
            "Daftar_Fungsi": []
        }
        
        while self.pos < len(self.tokens):
            token = self.ambil_token()
            if token and token[0] == 'KEYWORD' and token[1] == 'int':
                ast["Daftar_Fungsi"].append(self.parse_fungsi())
            else:
                self.maju()
                
        return ast

    def parse_fungsi(self):
        node_fungsi = {
            "Tipe_Node": "Deklarasi_Fungsi",
            "Tipe_Kembalian": "int",
            "Nama_Fungsi": "",
            "Isi_Blok_Kode": []
        }
        self.maju() 

        token = self.ambil_token()
        if token and token[0] == 'ID':
            node_fungsi["Nama_Fungsi"] = token[1]
            self.maju()

        while self.ambil_token() and self.ambil_token()[1] != '{':
            self.maju()
        self.maju() 

        while self.ambil_token() and self.ambil_token()[1] != '}':
            token_isi = self.ambil_token()
            if token_isi[0] == 'KEYWORD':
                node_fungsi["Isi_Blok_Kode"].append({"Perintah": token_isi[1]})
            elif token_isi[0] == 'ID' and token_isi[1] == 'print':
                node_fungsi["Isi_Blok_Kode"].append({"Perintah": "print"})
            self.maju()

        self.maju() 
        return node_fungsi

if __name__ == '__main__':
    from main import tokenize # Dipindah ke sini agar tidak bentrok
    print("=== MEMBANGUN POHON AST TAHAP AKHIR ===")
    try:
        with open('tests/test1.src', 'r') as file:
            kode = file.read()
            
        daftar_token = tokenize(kode)
        
        if daftar_token:
            parser = Parser(daftar_token)
            pohon_ast = parser.parse_program()
            
            print(json.dumps(pohon_ast, indent=4))
            print("\n[SUKSES] Pohon AST berhasil dibuat!")
            
    except Exception as e:
        print("Ada error:", e)