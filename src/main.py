import re

# 1. Buku Kamus Scanner (Aturan Regex)
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

# 2. Mesin Pemotong Kata
def tokenize(code):
    tokens = []
    rules_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_RULES)
    
    for match in re.finditer(rules_regex, code):
        jenis_token = match.lastgroup
        nilai_token = match.group()
        
        if jenis_token == 'SKIP':
            continue
        elif jenis_token == 'MISMATCH':
            print(f"ERROR LEKSIKAL: Karakter '{nilai_token}' tidak dikenali!")
            return None
        
        tokens.append((jenis_token, nilai_token))
    return tokens

# 3. Uji Coba Mesin
if __name__ == '__main__':
    # Membaca file test1.src
    try:
        with open('tests/test1.src', 'r') as file:
            kode_contoh = file.read()
            
        print("Membaca file tests/test1.src:")
        print("-" * 30)
        
        hasil_potongan = tokenize(kode_contoh)
        
        if hasil_potongan:
            for token in hasil_potongan:
                print(token)
    except FileNotFoundError:
        print("Error: File tests/test1.src tidak ditemukan. Pastikan posisinya benar.")