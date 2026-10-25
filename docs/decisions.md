# Catatan Keputusan — DeculGirl

Satu keputusan = satu baris. Tambahkan **saat** keputusannya diambil, bukan saat merekap di akhir.

Di tim remote, keputusan yang hanya diucapkan di chat akan hilang dalam dua hari dan dibahas lagi
minggu depan. Dokumen ini mencegah hal itu. Di bulan Desember, dokumen ini juga menjadi bahan mentah
untuk Innovation Challenge, karena bahan cerita tidak bisa disusun ulang dari ingatan.

**Aturan:** kalau sebuah keputusan tidak ada di sini, keputusan itu dianggap belum ada.

---

## Format

| # | Tanggal | Keputusan | Alasan | Alternatif yang ditolak | Diputuskan oleh |
|---|---|---|---|---|---|

Syarat untuk dicatat di sini: keputusan itu **mahal kalau dibatalkan**, **mengejutkan bagi orang yang
tidak tahu konteksnya**, dan **hasil dari pertimbangan untung-rugi yang nyata**. Kalau tidak memenuhi
ketiganya, jangan dicatat, karena nanti akan berubah dengan sendirinya.

---

## Keputusan yang sudah diambil

### Hari 0 — sebelum rapat pertama, 24 Oktober 2026

| # | Tanggal | Keputusan | Alasan | Alternatif yang ditolak | Oleh |
|---|---|---|---|---|---|
| 001 | 24 Okt 2026 | Ikut **Phase 1: Ball Possession** dengan target **masuk top 20**, tetapi dikerjakan seolah targetnya hanya "mengumpulkan submission yang valid" | Top 20 adalah pintu masuk Innovation Challenge (10 pertandingan dan bimbingan teknis). Pengaman didahulukan karena 25 hari itu singkat | Langsung mengejar peringkat tanpa pengaman; berhenti di mengumpulkan saja | Berempat |
| 002 | 24 Okt 2026 | **Satu repo, satu owner (Dyang), tiga anggota lain sebagai collaborator `write`.** Nama `mtah-DeculGirl`, publik sejak hari pertama | Riwayat git dari repo yang berbeda tidak bisa digabung dengan bersih. Selain itu form pengumpulan hanya menerima satu URL, dan URL itu harus bisa menghasilkan file yang persis sama | Empat repo terpisah yang digabung belakangan; GitHub Organization | Berempat |
| 003 | 24 Okt 2026 | Seat: **1 Dyang (domain) · 2 Raissa (data dan sinyal) · 3 Billa (model dan bola mati) · 4 Yona (metrik dan reproduksi hasil)** — *(direvisi oleh #013 dan #014)* | Dicocokkan dengan bukti pengalaman, bukan selera. Billa satu-satunya yang punya pengalaman *sequence labelling*; Yona satu-satunya yang pernah menulis kode berstandar produksi | Menukar Seat 3 dan 4 | Berempat |
| 004 | 24 Okt 2026 | **Aturan dan fitur dulu, model sekuensial belakangan** (Gate 1 sebelum Gate 2) | Setiap hal struktural bisa dibuktikan sendiri-sendiri. Kalau model end-to-end menaikkan skor tanpa kita tahu sebabnya, tidak ada yang bisa ditulis di dokumen teknis | Langsung memakai model; murni aturan tanpa model | Berempat |

### Keputusan teknis

| # | Tanggal | Keputusan | Alasan | Alternatif yang ditolak | Oleh |
|---|---|---|---|---|---|
| 005 | 24 Okt 2026 | **Tidak memakai video sama sekali.** Tidak membuat pendeteksi bola sendiri, tidak mendekode video | `RULES.md` melarang anotasi manual "in any amount and for any purpose", termasuk untuk melatih model. Jadi kita harus mengandalkan model yang sudah dilatih pihak lain dan kebetulan bisa menemukan bola, lalu memvalidasinya tanpa ground truth. Tidak ada bagiannya yang bisa dibuktikan benar sebelum batas waktu | Pendeteksi bola buatan sendiri dengan GTX 1650 Ti 4 GB; template matching lokal di sekitar posisi bola yang diperkirakan | Berempat |
| 006 | 24 Okt 2026 | **`X` diperlakukan sebagai alat penggabung**, bukan tanda tidak menjawab: pakai `X` di tengah possession, dan wajib menebak saat possession berpindah ke tim lawan | Scorer mengganti `X` dengan label terakhir di babak yang sama sebelum menyusun possession. Tidak menjawab di tengah possession tidak merugikan; tidak menjawab saat possession berpindah akan menarik label lama ke wilayah tim lawan | Tidak memakai `X` sama sekali; memakai `X` sebagai tanda tidak menjawab biasa | Seat 1 + 3 |
| 007 | 24 Okt 2026 | **Batas minimum panjang possession harus konservatif**, yaitu di bawah 19 frame | Possession terpendek di GT publik adalah **19 frame (0,76 detik)** dan itu possession yang sungguhan. Scorer tidak menggabungkan possession pendek, jadi filter yang agresif akan menghapus possession yang nyata. Satu possession yang hilang ≈ 6 poin `spellF1` | Batas minimum 1 detik / 30 frame; median filter yang agresif | Seat 1 + 3 + 4 |
| 008 | 24 Okt 2026 | **Kode dibekukan (freeze) pada 14 November 2026.** Setelah itu hanya boleh memperbaiki yang rusak | Kebanyakan poin hilang di 72 jam terakhir, dan penyebabnya bukan skor, melainkan file yang tadinya valid menjadi tidak valid | Bekerja sampai menit terakhir | Berempat |
| 009 | 24 Okt 2026 | **Jendela publik 5 menit hanya untuk memastikan pipeline benar**, bukan untuk memilih versi | `EVALUATION.md` membuktikan bahwa menyetel parameter di situ memilih baseline yang salah: `smooth125` menang di jendela publik (0,4242) tetapi kalah di pertandingan penuh (0,2242). Ini juga aturan resmi, bukan sekadar saran | Menyetel hyperparameter di jendela publik | Seat 4 |
| 010 | 24 Okt 2026 | **Seat 4 harus tetap berjalan walaupun Yona tidak ada.** Cara kerja pipeline dibangun berpasangan di Gate 0 lalu dibekukan; pemeriksaan validasi diotomatiskan lewat CI; tugas "apakah selisih ini nyata?" dipindahkan ke Raissa | Yona satu-satunya yang masih intern, dan Seat 4 adalah jalur yang tidak boleh terputus. Kalau dia tidak bisa dihubungi tiga hari di minggu terakhir, tidak ada yang bisa mereproduksi submission, dan itu membuat tim gugur | Memindahkan Yona ke seat yang lebih ringan; tidak berbuat apa-apa dan berharap dia tidak sibuk | Berempat |
| 011 | 24 Okt 2026 | **Semua perintah dijalankan dengan Python, bukan shell script.** `python run.py`, `python tools/fetch_official.py`, `python tools/gate0.py` | Tim memakai Windows. `run.sh` tidak jalan di cmd/PowerShell, dan perbedaan itu membuat orang kehilangan 20 menit pertamanya setiap kali | `.sh` dan `.bat` terpisah; Makefile | Seat 4 |
| 012 | 24 Okt 2026 | **Repo resmi disalin sebagai clone yang dikunci versinya** (`third_party/`, masuk .gitignore, diunduh oleh `tools/fetch_official.py`), dan **baseline-nya diimpor, bukan disalin** ke `submit.py` | `possession_metrics.py` **adalah** spesifikasi metriknya. Mengunci versi menjaga angka lokal kita tidak berubah diam-diam kalau repo asalnya berubah. Mengimpor, bukan menyalin, membuat jelas bahwa yang berjalan adalah kode mereka (MIT), bukan buatan kita | Menyalin baseline ke dalam kode kita; tidak memakai repo resmi sama sekali | Seat 4 |
| 013 | 24 Okt 2026 | **Seat 1 mendapat tugas kedua: alat dan diagnosa.** Seat 2 (Raissa) ditambah menjadi **ikut memegang domain**. Pernyataan "Dyang satu-satunya yang paham bola" dihapus | Pernyataan itu **keliru** dan menjadi dasar seluruh analisis risiko di bagian 4 playbook: Raissa juga paham sepak bola, dan Dyang juga menulis kode. Risiko domain turun dari satu orang menjadi dua, dan kapasitas menulis kode bertambah satu orang. Akibatnya, lembar 21 transisi dibagi dua, dan tekanan "tuliskan semuanya segera" jauh berkurang | Membiarkan seperti semula dan membiarkan anggapan yang salah tetap ada di dokumen | Berempat |
| 014 | 24 Okt 2026 | **Peran PM sengaja dikosongkan**, dan diputuskan di rapat. Kalau sampai 2 Nov tidak ada yang bersedia, tugasnya jatuh ke Dyang secara otomatis | PM tidak bisa dicocokkan dengan pengalaman siapa pun. Ini soal kesediaan, dan hanya orangnya sendiri yang bisa menjawab. Kalau dikunci terlalu awal, ada risiko menempatkan orang yang sebenarnya tidak mau. Tetapi tidak boleh kosong selamanya: pemilik file submission harus punya satu nama, karena submission tanpa pemilik adalah cara paling umum kehilangan poin | Menetapkan Dyang sekarang karena dia yang menggerakkan tim | Berempat |
| 015 | 24 Okt 2026 | **Semua seat ditandai sementara** sampai rapat pertama | Pembagiannya dicocokkan dari jejak publik, bukan dari pilihan orangnya. Menandainya sebagai usulan membuat rapat pertama bisa mengubahnya tanpa terasa seperti membatalkan keputusan | Mengunci sekarang dan mengubahnya nanti | Berempat |
| 016 | 24 Okt 2026 | **Seat 1 menjadi "Domain, Aturan, dan Eksperimen"** dan punya hasil kerja ketiga: `docs/experiments.md`. Setiap perubahan yang masuk `main` wajib punya catatan dengan angka dan putusan ✅/❌/⚠️ | Pekerjaan domain yang tidak meninggalkan jejak angka akan terbaca sebagai koordinasi, bukan kerja teknis. Padahal menjalankan eksperimen adalah satu-satunya cara tim tahu apakah sebuah perubahan benar-benar perbaikan atau hanya selisih di dalam batas noise. Selain itu `SUBMISSION.md` mewajibkan dokumen teknis menyebut aset yang **dicoba lalu dibuang**. Bagian itu mustahil dikarang di bulan November, jadi harus dicatat selama pekerjaan berlangsung | Membiarkan catatan eksperimen tersebar di chat dan ingatan; mengarang bagian "tried and dropped" saat menyusun dokumen | Berempat |
| 017 | 24 Okt 2026 | **Seat 1 dan Seat 2 dinyatakan bisa ditukar.** Pembagiannya diputuskan berdasarkan preferensi, bukan kemampuan | Koreksi fakta: Dyang juga punya pengalaman EDA, clustering, segmentation, dan dashboard. Dia dan Raissa mengikuti program yang sama (Startup Campus DS Batch 5), dan keduanya paham sepak bola. Profilnya hampir sepenuhnya sama, jadi berpura-pura ada satu pembagian yang "benar" itu keliru. Yang tetap tidak bisa ditukar: Seat 3 dan Seat 4 | Mempertahankan pembagian sekarang seolah-olah didasarkan pada kemampuan yang berbeda | Berempat |
| 018 | 24 Okt 2026 | **Admin repo dua orang, bukan satu:** Dyang = owner, **Billa = Admin**, Raissa dan Yona = Write | Menghindari ketergantungan pada satu orang. GitHub tidak punya peran "co-owner"; yang ada adalah Admin, dan Admin adalah satu-satunya peran yang bisa mengubah Settings, mengatur akses, menyalakan proteksi branch, dan mengelola Actions. Kalau hanya satu orang yang memegangnya dan dia tidak bisa dihubungi di minggu terakhir, tim tidak bisa memperbaiki repo di saat paling berbahaya. Billa dipilih karena dia satu-satunya yang sudah pernah bekerja di dalam GitHub Organization | Menjadikan semua orang Admin; membiarkan hanya satu admin | Berempat |

---

## Templat untuk keputusan baru

```markdown
| 0XX | DD Mmm 2026 | **<keputusan dalam satu kalimat>** | <kenapa, beserta angka yang mendukung> | <alternatif yang ditolak, dan alasannya> | <seat/orang> |
```

Kalau keputusannya besar dan tidak muat dalam satu baris, buat file di `docs/adr/` dengan nama
`00XX-<slug>.md`, satu halaman saja, berisi konteks, keputusan, dan akibatnya. Tetapi jangan
berlebihan: sebagian besar keputusan cukup ditulis satu baris di tabel di atas.
