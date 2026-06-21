# TinyC Compiler - Kelompok 3 (Teknik Kompilasi)

Kompiler sederhana berbasis CLI untuk bahasa **TinyC** yang dilengkapi dengan fitur *Code Generator* (Transpiler ke Python murni).

## Anggota Kelompok 3:
1. Yeheskiel Boyke Lumban Gaol (Ketua / Koordinasi, menyelesaikan parser dan menampilkan pohon ast utuh)
2. Tri Putra (semantic analyzer)
3. Dida Aldeaneva (intermedia code generation)
4. Lucky Sitinjak (code optimization)
5. Muhammad Reza Erlangga (code generator)
6. Fathiah Vianata (leksikal, sintaks, semantik & Error Handling)

## Struktur Folder
- `src/` : Kode sumber kompiler (Scanner, Parser, Semantic, ICG, Optimasi, Error Handler, Code Gen)
- `tests/`: Kumpulan file `.src` berisi kode bahasa TinyC untuk pengujian
- `docs/` : File Laporan Proyek Akhir (PDF)

## Persyaratan & Cara Instalasi

1. Pastikan Python 3.10 atau versi lebih baru sudah terinstal di komputer Anda.
2. Clone repositori ini:
```bash
   git clone [https://github.com/ezekielcode777/Kompliler_Kelompok3_TinyC.git](https://github.com/ezekielcode777/Kompliler_Kelompok3_TinyC.git)
   cd Kompliler_Kelompok3_TinyC