# Catatan Keputusan — DeculGirl

Satu keputusan = satu baris. Tambahkan **saat** keputusannya diambil, bukan saat merekap di akhir.

Di tim remote, keputusan yang cuma diucapkan di chat akan hilang dalam dua hari dan diulang lagi
minggu depan. Dokumen ini mencegah itu — dan di bulan Desember, dokumen ini jadi bahan mentah untuk
Innovation Challenge, karena bahan cerita tidak bisa dirakit ulang dari ingatan.

**Aturan:** kalau sebuah keputusan tidak ada di sini, keputusan itu belum ada.

---

## Format

| # | Tanggal | Keputusan | Alasan | Alternatif yang ditolak | Diputuskan oleh |
|---|---|---|---|---|---|

Ambang untuk masuk ke sini: keputusan yang **mahal untuk dibalik**, **mengejutkan tanpa konteks**, dan
**hasil dari trade-off nyata**. Kalau tidak memenuhi ketiganya, jangan dicatat — dia akan berubah sendiri.

---

## Keputusan yang sudah diambil

### Hari 0 — sebelum rapat pertama, 24 Oktober 2026

| # | Tanggal | Keputusan | Alasan | Alternatif yang ditolak | Oleh |
|---|---|---|---|---|---|
| 001 | 24 Okt 2026 | Ikut **Phase 1: Ball Possession** dengan target **top 20**, dieksekusi seolah targetnya cuma "submit valid" | Top 20 adalah pintu masuk Innovation Challenge (10 pertandingan + mentoring). Asuransi dulu karena 25 hari itu pendek | Langsung kejar ranking tanpa fail-safe; berhenti di submit saja | Berempat |
| 002 | 24 Okt 2026 | **Satu repo, satu owner (Dyang), tiga lainnya collaborator `write`.** Nama `mtah-DeculGirl`, publik sejak hari pertama | Git history dari repo berbeda tidak bisa digabung bersih. Dan form submission cuma menerima satu URL, yang harus bisa mereproduksi file itu persis | Empat repo terpisah lalu digabung; GitHub Organization | Berempat |
| 003 | 24 Okt 2026 | Seat: **1 Dyang (domain) · 2 Raissa (data & sinyal) · 3 Billa (model & dead-ball) · 4 Yona (metrik & reproducibility)** — *(direvisi #013 dan #014)* | Dipetakan ke bukti rekam jejak, bukan ke selera. Billa satu-satunya dengan jejak *sequence labelling*; Yona satu-satunya dengan kode berbentuk produksi | Menukar Seat 3 dan 4 | Berempat |
| 004 | 24 Okt 2026 | **Aturan & fitur dulu, model sekuensial belakangan** (Gate 1 sebelum Gate 2) | Setiap pilar bisa diverifikasi sendiri. Kalau model end-to-end naik skor tanpa kita tahu kenapa, tidak ada yang bisa ditulis di dokumen teknis | Langsung model; murni aturan tanpa model | Berempat |

### Keputusan teknis

| # | Tanggal | Keputusan | Alasan | Alternatif yang ditolak | Oleh |
|---|---|---|---|---|---|
| 005 | 24 Okt 2026 | **Tidak memakai video sama sekali.** Tidak ada detektor bola sendiri, tidak ada decode video | `RULES.md` melarang hand annotation "in any amount and for any purpose" — termasuk untuk melatih model. Jadi kita harus bergantung pada model pra-latih yang kebetulan menemukan bola, lalu memvalidasinya tanpa ground truth. Tidak ada satu pun bagiannya yang bisa dibuktikan benar sebelum deadline | Detektor bola sendiri dengan GTX 1650 Ti 4 GB; template matching lokal di sekitar posisi yang diharapkan | Berempat |
| 006 | 24 Okt 2026 | **`X` diperlakukan sebagai operator penggabung**, bukan abstain: `X` di tengah possession, wajib menebak di titik hand-over | Scorer mengisi `X` dengan label terakhir di babak yang sama sebelum menyusun possession. Diam di tengah = gratis; diam di hand-over = menarik label lama ke wilayah tim lawan | Tidak memakai `X` sama sekali; memakai `X` sebagai abstain biasa | Seat 1 + 3 |
| 007 | 24 Okt 2026 | **Minimum spell harus konservatif** — di bawah 19 frame | Possession terpendek di GT publik adalah **19 frame (0,76 detik)** dan itu possession sungguhan. Scorer tidak menggabungkan possession pendek, jadi filter yang agresif akan menghapus possession nyata. Satu possession hilang ≈ 6 poin `spellF1` | Minimum spell 1 detik / 30 frame; median filter agresif | Seat 1 + 3 + 4 |
| 008 | 24 Okt 2026 | **Freeze kode pada 14 November 2026.** Setelah itu hanya perbaikan kerusakan | Mayoritas poin hilang di 72 jam terakhir, dan hilangnya bukan karena skor — tapi karena file yang tadinya valid jadi tidak valid | Kerja sampai menit terakhir | Berempat |
| 009 | 24 Okt 2026 | **Jendela publik 5 menit hanya untuk memverifikasi kebenaran pipeline**, bukan untuk memilih versi | `EVALUATION.md` membuktikan tuning di situ memilih baseline yang salah: `smooth125` menang di publik (0,4242) tapi kalah di pertandingan penuh (0,2243). Dan itu aturan resmi, bukan saran | Tuning hyperparameter di jendela publik | Seat 4 |
| 010 | 24 Okt 2026 | **Seat 4 harus jalan tanpa kehadiran Yona.** Mekanika pipeline dibangun berpasangan di Gate 0 lalu dibekukan; gate validasi diotomasi lewat CI; fungsi "apakah bedanya nyata?" pindah ke Raissa | Yona satu-satunya yang masih intern, dan Seat 4 adalah jalur kritis. Kalau dia hilang tiga hari di minggu terakhir, tidak ada yang bisa mereproduksi submission — dan itu syarat gugur | Menggeser Yona ke seat yang lebih ringan; tidak melakukan apa-apa dan berharap dia tidak sibuk | Berempat |
| 011 | 24 Okt 2026 | **Semua entry point memakai Python, bukan shell script.** `python run.py`, `python tools/fetch_official.py`, `python tools/gate0.py` | Timnya di Windows; `run.sh` tidak jalan di cmd/PowerShell, dan itu perbedaan yang bikin orang kehilangan 20 menit pertama setiap kali | `.sh` + `.bat` terpisah; Makefile | Seat 4 |
| 012 | 24 Okt 2026 | **Repo resmi di-vendor sebagai clone yang di-pin** (`third_party/`, di-gitignore, diambil `tools/fetch_official.py`) dan **baseline-nya diimpor, bukan disalin** ke `submit.py` | `possession_metrics.py` **adalah** spesifikasi metriknya. Pin menjaga angka lokal kita tidak berubah diam-diam kalau upstream bergerak. Mengimpor, bukan menyalin, membuat jelas bahwa yang berjalan adalah kode mereka (MIT) dan bukan rekaan kita | Menyalin baseline ke dalam kode kita; tidak memakai repo resmi sama sekali | Seat 4 |
| 013 | 24 Okt 2026 | **Seat 1 dapat topi kedua: alat & diagnosa.** Seat 2 (Raissa) ditambah jadi **co-owner domain**. Klaim "Dyang satu-satunya yang paham bola" dihapus | Klaim itu **keliru** dan menopang seluruh analisis risiko di §4 playbook: Raissa juga paham sepak bola, dan Dyang juga menulis kode. Risiko domain turun dari satu orang jadi dua, dan kapasitas menulis kode bertambah satu orang. Konsekuensinya: lembar 21 transisi dibagi dua, dan tekanan "tuliskan semuanya segera" jadi jauh lebih ringan | Tetap seperti semula dan membiarkan asumsi yang salah tinggal di dokumen | Berempat |
| 014 | 24 Okt 2026 | **PM sengaja dikosongkan**, diputuskan di rapat. Kalau sampai 2 Nov tidak ada yang bersedia, jatuh ke Dyang secara default | PM tidak bisa dipetakan ke rekam jejak — itu soal kesediaan, dan itu hanya bisa dijawab orangnya sendiri. Dikunci lebih awal berisiko menempatkan orang yang sebenarnya tidak mau. Tapi tidak boleh kosong selamanya: pemilik file submission harus punya satu nama, karena submission tanpa pemilik adalah cara paling umum kehilangan poin | Menetapkan Dyang sekarang karena dia yang menggerakkan tim | Berempat |
| 015 | 24 Okt 2026 | **Semua seat ditandai sementara** sampai rapat pertama | Dipetakan dari jejak publik, bukan dari pilihan orangnya. Menandainya sebagai usulan membuat rapat pertama bisa mengubahnya tanpa terasa seperti membatalkan keputusan | Mengunci sekarang dan mengubahnya nanti | Berempat |
| 016 | 24 Okt 2026 | **Seat 1 jadi "Domain, Aturan & Eksperimen"** dan punya artefak ketiga: `docs/experiments.md`. Setiap perubahan yang masuk `main` wajib punya entri dengan angka dan putusan ✅/❌/⚠️ | Pekerjaan domain yang tidak meninggalkan jejak angka akan terbaca sebagai koordinasi, bukan kerja teknis — padahal menjalankan eksperimen itu satu-satunya cara tim tahu apakah sebuah perubahan benar-benar perbaikan atau cuma selisih di dalam noise band. Dan `SUBMISSION.md` mewajibkan dokumen teknis menyebut aset yang **dicoba lalu dibuang** — bagian itu mustahil dikarang di bulan November, jadi harus dicatat sementara dikerjakan | Membiarkan catatan eksperimen tersebar di chat dan ingatan; mengarang bagian "tried and dropped" saat menyusun dokumen | Berempat |

---

## Templat untuk keputusan baru

```markdown
| 0XX | DD Mmm 2026 | **<keputusan dalam satu kalimat>** | <kenapa, dan angka yang mendukungnya> | <alternatif yang ditolak, dan kenapa> | <seat/orang> |
```

Kalau keputusannya besar dan tidak bisa dimuat di satu baris, buat file di `docs/adr/` dengan nama
`00XX-<slug>.md` — satu halaman, isinya konteks, keputusan, dan konsekuensinya. Tapi jangan berlebihan:
sebagian besar keputusan cukup satu baris di tabel di atas.
