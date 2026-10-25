# metrics/ — Seat 4 (Yona)

Alat ukur, regression suite (uji untuk menangkap kemunduran hasil), dan alat diagnosa.

## Kenapa folder ini ada

> Kunci peringkat kompetisi ini ada di tangan kalian: **scorer yang kalian jalankan di komputer sendiri
> adalah scorer yang menentukan peringkat.** Kata `EVALUATION.md`:
> *"Organisers run this exact script against the private full-match ground truth; the published board
> is its output. There is no stricter version held back."* (Penyelenggara menjalankan skrip yang persis
> sama terhadap ground truth pertandingan penuh yang dirahasiakan; papan skor yang diterbitkan adalah
> keluarannya. Tidak ada versi yang lebih ketat yang disembunyikan.)

Ini keuntungan besar, tetapi hanya berguna kalau dipakai dengan disiplin. Folder ini yang menjaga
disiplin itu.

## Isi yang direncanakan

| File | Gunanya |
|---|---|
| `regression.py` | Menjalankan sekumpulan submission dan membandingkannya dengan hasil terakhir yang diketahui. Menangkap kemunduran yang tidak disadari |
| `compare.py` | Membandingkan dua versi dengan `--bootstrap 1000`, lalu melaporkan apakah intervalnya tumpang tindih. **Alat ini mencegah kalian menipu diri sendiri** |
| `diagnose.py` | Meringkas `reports/<nama>_transitions.csv` dari evaluator resmi: mana yang `matched` (cocok), `missed` (terlewat), dan `spurious` (palsu) |
| `ci.py` | Menjalankan pemeriksaan yang sama dengan `.github/workflows/validate.yml`, tetapi di komputer lokal |

## Tiga aturan pengukuran

1. **Batas noise pertandingan penuh: `spellF1` ≈ 0,04 · `macroF1` ≈ 0,01.**
   Selisih di bawah itu bukan kemajuan. Jangan dirayakan dan jangan dikejar.
2. **Selalu jalankan `--bootstrap 1000` sebelum percaya bahwa satu versi lebih baik.**
   Biasanya intervalnya tumpang tindih. Kalau tumpang tindih, pilih versi yang lebih sederhana dan
   berhenti di situ.
3. **Jendela publik 5 menit bukan leaderboard.** Isinya hanya 17 possession, dan satu possession yang
   meleset ≈ 6 poin. `EVALUATION.md` membuktikan bahwa menyetel parameter di situ memilih baseline yang
   salah. Pakai hanya untuk memastikan pipeline **benar**: nomor frame selaras, file sesuai format yang
   diminta, dan label berarti apa yang kalian kira.

## Satu hal yang jarang diketahui orang

Evaluator resmi menulis `reports/<nama>_transitions.csv`, yaitu daftar setiap transisi beserta statusnya
(`matched` / `missed` / `spurious`) untuk setiap video frame. Itu alat debug terbaik yang tersedia, dan
gratis. Gunakan `diagnose.py` untuk membacanya.

## Kepemilikan

Seat 4 adalah **jalur yang tidak boleh terputus**. Kalau tidak ada yang bisa menjalankan folder ini,
tidak ada yang bisa mereproduksi file submission, dan itu membuat tim gugur, bukan sekadar kurang
nilai.

Karena itu: bangun berpasangan di Gate 0, **bekukan** setelah hijau, dan **otomatiskan** pemeriksaannya
lewat CI. Setelah dibekukan, beban rutinnya kecil, dan ketidakhadiran satu orang tidak lagi menjadi
risiko bagi tim.
