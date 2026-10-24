# metrics/ — Seat 4 (Yona)

Harness pengukuran, regression suite, dan alat diagnostik.

## Kenapa folder ini ada

> Kunci ranking kompetisi ini ada di tangan kalian: **scorer yang kalian
> jalankan lokal adalah scorer yang menentukan kompetisi.** `EVALUATION.md`:
> *"Organisers run this exact script against the private full-match ground
> truth; the published board is its output. There is no stricter version held
> back."*

Itu hadiah besar, dan hadiahnya cuma berguna kalau dipakai dengan disiplin.
Folder ini yang menjaga disiplin itu.

## Isi yang direncanakan

| File | Gunanya |
|---|---|
| `regression.py` | Jalankan satu set submission, bandingkan dengan hasil terakhir yang diketahui. Menangkap kemunduran yang tidak disadari |
| `compare.py` | Dua versi, `--bootstrap 1000`, laporkan apakah intervalnya tumpang tindih. **Ini alat yang mencegah kalian menipu diri sendiri** |
| `diagnose.py` | Ringkas `reports/<nama>_transitions.csv` dari evaluator resmi: mana yang `matched`, `missed`, `spurious` |
| `ci.py` | Jalankan gate yang sama seperti `.github/workflows/validate.yml`, tapi lokal |

## Tiga aturan pengukuran

1. **Noise band pertandingan penuh: `spellF1` ≈ 0,04 · `macroF1` ≈ 0,01.**
   Selisih di bawah itu bukan kemajuan. Jangan rayakan, jangan kejar.
2. **Selalu `--bootstrap 1000` sebelum percaya bahwa satu versi lebih baik.**
   Intervalnya biasanya tumpang tindih. Kalau tumpang tindih, pilih yang lebih
   sederhana dan berhenti di situ.
3. **Jendela publik 5 menit bukan leaderboard.** 17 possession; satu possession
   meleset ≈ 6 poin. `EVALUATION.md` membuktikan tuning di situ memilih baseline
   yang salah. Pakai untuk memverifikasi pipeline **benar** — frame selaras, file
   sesuai kontrak, labelnya berarti apa yang kalian kira.

## Satu hal yang jarang diketahui orang

Evaluator resmi menulis `reports/<nama>_transitions.csv`: daftar setiap transisi
beserta statusnya — `matched` / `missed` / `spurious` — per video frame. Itu alat
debug terbaik yang tersedia, dan gratis. Pakai `diagnose.py` untuk membacanya.

## Kepemilikan

Seat 4 adalah **jalur kritis**: kalau tidak ada yang bisa menjalankan folder ini,
tidak ada yang bisa mereproduksi file submission — dan itu syarat gugur, bukan
sekadar kurang nilai.

Karena itu: bangun berpasangan di Gate 0, **bekukan** setelah hijau, dan
**otomasi** gate-nya lewat CI. Setelah beku, beban rutinnya kecil, dan kehadiran
satu orang berhenti menjadi risiko tim.
