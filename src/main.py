import re
import sys
import os
import json
import importlib.util

# ==========================================
# 1. IMPORT CLASS DARI MODUL KAWAN-KAWANMU
# ==========================================

# --- JALUR SELUNDUPAN KHUSUS PARSER (Anti Bentrok Nama) ---
lokasi_parser = os.path.join(os.path.dirname(__file__), 'parser.py')
spec_p = importlib.util.spec_from_file_location("modul_parser_kita", lokasi_parser)
modul_parser = importlib.util.module_from_spec(spec_p)
spec_p.loader.exec_module(modul_parser)
Parser = modul_parser.Parser
# ----------------------------------------------------------

from semantik import SemanticAnalyzer
from icg import IntermediateCodeGenerator
from optimasi import CodeOptimizer
from code_generator import TargetCodeGenerator
from error_handler import CompilerErrorHandler

# ==========================================
# 2. MESIN SCANNER (Karya Yeheskiel - ASLI)
# ==========================================
TOKEN_RULES = [
    ('KEYWORD', r'\b(int|if|else|while|return|print)\b'),
    ('NUMBER',  r'\b\d+\b'),
    ('ID',      r'\b[a-zA-Z_]\w*\b'),
    ('OP_REL',  r'<=|>=|==|!=|<|>'),
    ('OP_ARITH',r'\+|-|\*|/'),
    ('ASSIGN',  r'='),
    ('SEMI',    r';'),
    ('LPAREN',  r'\('),
    ('RPAREN',  r'\)'),
    ('LBRACE',  r'\{'),
    ('RBRACE',  r'\}'),
    ('SKIP',    r'[ \t\n]+'),
    ('MISMATCH',r'.'),
]

def tokenize(code):
    tokens = []
    rules_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_RULES)
    
    for match in re.finditer(rules_regex, code):
        jenis_token = match.lastgroup
        nilai_token = match.group()
        
        if jenis_token == 'SKIP':
            continue
        elif jenis_token == 'MISMATCH':
            print(f"❌ ERROR LEKSIKAL: Karakter '{nilai_token}' tidak dikenali!")
            return None
        
        tokens.append((jenis_token, nilai_token))
    return tokens

# ==========================================
# 3. STASIUN PUSAT (Orkestrasi CLI)
# ==========================================
def main():
    if len(sys.argv) < 2:
        print("❌ CARA PAKAI SALAH!")
        print("Gunakan perintah terminal: python src/main.py tests/test1.src")
        return

    filepath = sys.argv[1]
    
    try:
        with open(filepath, 'r') as file:
            kode_sumber = file.read()

        print(f"\n==============================================")
        print(f" 🚀 MULAI KOMPILASI TINYC: {filepath}")
        print(f"==============================================\n")

        # --- TAHAP 1: SCANNER ---
        print("--- 1. PROSES SCANNER (TOKENISASI) ---")
        tokens = tokenize(kode_sumber)
        if not tokens: 
            print("🚨 Kompilasi dihentikan karena Error Leksikal.")
            return
        for t in tokens: print(t)

        # --- TAHAP 2: PARSER ---
        print("\n--- 2. PROSES PARSER (AST) ---")
        mesin_parser = Parser(tokens)
        ast = mesin_parser.parse_program()
        print(json.dumps(ast, indent=4))

        # --- TAHAP 6: ERROR HANDLING (Audit Keselamatan) ---
        print("\n--- 3. AUDIT ERROR HANDLING ---")
        auditor = CompilerErrorHandler()
        auditor.jalankan_audit_error(kode_sumber, ast)
        if auditor.errors:
            return # Stop jika konstitusi dilanggar

        # --- TAHAP 3: SEMANTIK ---
        print("\n--- 4. PROSES SEMANTIC ANALYZER ---")
        mesin_semantik = SemanticAnalyzer()
        mesin_semantik.analisis_pohon(ast)

        # --- TAHAP 4: ICG (TAC) ---
        print("\n--- 5. PROSES ICG (TAC) ---")
        generator = IntermediateCodeGenerator()
        tac = generator.generate(ast)
        for baris in tac: print(baris)

        # --- TAHAP 5: OPTIMASI ---
        print("\n--- 6. PROSES OPTIMASI ---")
        optimizer = CodeOptimizer(tac)
        tac_bersih = optimizer.jalankan_optimasi()

        # --- TAHAP 7: CODE GENERATOR (BONUS) ---
        print("\n--- 7. CODE GENERATOR & EKSEKUSI ---")
        builder = TargetCodeGenerator()
        output_file = 'dist/hasil_kompilasi.py'
        
        # Method dari kodingan code_generator.py kamu
        builder.jalankan_build(filepath, output_file)
        
        print("\n>>> HASIL EKSEKUSI PROGRAM <<<")
        try:
            # Gunakan os.system agar dieksekusi sebagai script independen
            os.system(f"python {output_file}")
        except Exception as e:
             print(f"Gagal menjalankan output: {e}")

        print("\n==============================================")
        print(" 🎉 [INFO] SELURUH PROSES KOMPILASI SELESAI!")
        print("==============================================\n")

    except FileNotFoundError:
        print(f"❌ ERROR: File '{filepath}' tidak ditemukan! Cek lagi letak foldernya.")
    except Exception as e:
        print(f"❌ ERROR SISTEM FATAL: {str(e)}")

if __name__ == '__main__':
    main()