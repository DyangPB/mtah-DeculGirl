# RINGKASAN — DeculGirl

**Cukup 5 menit untuk membaca ini.** Penjelasan lengkapnya ada di `docs/PLAYBOOK.md`. Kalau isi file
ini berbeda dengan playbook, yang benar adalah playbook.

More than a Hack 2027 · Phase 1: Ball Possession · batas kumpul **17 November 2026** · hari ini **24 Oktober**

---

## Apa yang kita kerjakan

Penyelenggara memberi kita satu pertandingan LaLiga lengkap, **Barcelona vs Athletic**, beserta data
pelacakan otomatis (posisi pemain dan bola), penandaan taktik otomatis, dan data pemetaan kamera ke
lapangan. Tugas kita bisa dirangkum dalam satu kalimat:

> **Untuk setiap frame, tentukan tim mana yang sedang menguasai bola.**

Hasilnya satu file CSV `frame,label` berisi **199.319 baris**, dengan label `H` / `A` / `D` / `X`.
Penilaiannya otomatis memakai **`spellF1`**. Tidak ada juri dan tidak ada presentasi.

Ada tiga hal yang harus dikumpulkan: **file CSV**, **repo publik yang bisa menghasilkan file itu persis
sama**, dan **dokumen teknis** setebal beberapa halaman.

---

## Delapan angka penting

| Angka | Kenapa penting |
|---|---|
| **0,2433** | Batas minimum `spellF1` yang harus dilewati (`baseline_smooth50`, pertandingan penuh) |
| **158.857** | Jumlah frame yang dinilai, dari 199.319 frame. Sisanya tidak berpengaruh sama sekali |
| **41%** | Bagian dari frame yang dinilai yang **posisi bolanya tidak terdeteksi** — dan justru sering hilang di momen penting |
| **11×** | Selisih `spellF1` antara baseline terbaik dan terburuk di jendela publik 5 menit. Keempat baseline memakai **algoritma yang sama**; hanya lebar windownya yang berbeda (di pertandingan penuh selisihnya 5×) |
| **0,04** | Selisih `spellF1` di bawah angka ini hanya noise, bukan kemajuan |
| **17** | Jumlah possession di jendela publik 5 menit (21 segmen, rata-rata 14,2 detik) |
| **19** | Frame pada possession terpendek di GT (0,76 detik). Possession sependek ini **memang nyata** |
| **14 Nov** | Hari pembekuan kode (freeze). Setelah itu kode tidak boleh diubah |

---

## Kenapa kita punya peluang menang, dan kenapa jawabannya bukan model yang canggih

`spellF1` mengukur **seberapa rapi possession tidak terpecah-pecah**, bukan akurasi tiap frame. Keempat
baseline di repo resmi memakai algoritma yang sama. Perbedaan `macroF1` di antara mereka hanya 0,04,
tetapi `spellF1`-nya berbeda jauh.

Skor kita nanti berasal dari **empat hal yang bersifat struktural**. Tidak satu pun dari keempatnya
berupa "model yang lebih canggih":

1. **Mendeteksi bola mati (dead ball).** Baseline sama sekali tidak punya cara mengenali bola mati.
   Ia hanya menganggap "bola tidak terdeteksi" berarti bola mati. Inilah kelemahan terbesarnya. Kelas `D`
   malah **makin buruk** kalau hasilnya dihaluskan.
2. **Mengisi posisi bola yang hilang (imputasi).** Pada 41% frame yang dinilai, bola tidak terdeteksi,
   dan itu sering terjadi di momen yang paling menentukan.
3. **Menentukan tim yang menguasai bola.** Baseline hanya melihat "pemain terdekat". Padahal masih ada
   jarak ke beberapa pemain, arah gerak pemain, konteks sebelumnya, dan tag tim dari Smart Tagging yang
   belum dipakai siapa pun.
4. **Menyusun possession tanpa memecahnya.** Memecah satu possession menjadi dua berarti **1 hasil positif
   palsu (false positive) sekaligus 1 hasil negatif palsu (false negative)**. Kolom `frag` di papan skor
   hampir bisa langsung dipakai untuk memperkirakan `spellF1`.

Satu alat lagi yang paling sering disalahpahami: **`X` bukan tanda menyerah. `X` berarti "ikuti label
sebelumnya".** Sebelum menyusun possession, scorer mengganti setiap `X` dengan label terakhir yang
bukan `X`. Jadi tidak menjawab di tengah possession itu **tidak merugikan**. Sebaliknya, tidak menjawab
tepat saat bola berpindah ke tim lawan **sangat merugikan**.

---

## Siapa mengerjakan apa

| Seat | Orang | Tugas | Hasil yang diperiksa |
|---|---|---|---|
| 1 | **Dyang** | Domain sepak bola, aturan, alat diagnosa, menjalankan eksperimen | `possession-rules.md`, `experiments.md` |
| 2 | **Raissa** | Data, penyelarasan frame, fitur per frame, **dan ikut memegang domain** | `features.parquet`, laporan diagnosa |
| 3 | **Billa** | Deteksi bola mati, penentuan tim, penyusunan possession, dokumen teknis | `src/deculgirl/model/`, draf dokumen |
| 4 | **Yona** | Pengukuran, validasi, reproduksi hasil (paruh waktu) | `metrics/`, `run.py`, CI |
| — | ⬜ **PM** | **Belum ditetapkan** — tanyakan di rapat | Pemilik file submission, penjaga jadwal |

Ada tiga catatan:

- **Pembagian seat masih sementara.** Rapat pertama yang menetapkannya.
- **PM adalah peran tambahan, bukan seat tersendiri.** Jadi kita tidak butuh orang kelima. Siapa pun
  yang memegangnya tetap mengerjakan seat teknisnya, dan harus sudah ada yang bersedia paling lambat
  **2 November**.
- **Yona satu-satunya yang masih berstatus intern, padahal Seat 4 adalah jalur yang tidak boleh
  terputus.** Karena itu Gate 0 dikerjakan berpasangan lalu dibekukan, pemeriksaannya diotomatiskan,
  dan tugas menilai "apakah selisih ini nyata?" dipindahkan ke Raissa.

---

## Jadwal

Hari ini Sabtu **24 Okt**. Batas kumpul Selasa **17 Nov**. Pekerjaan dibagi menjadi empat **gate**
(tahap). Setiap gate punya satu angka yang harus "hijau" (tercapai) sebelum lanjut ke gate berikutnya.

| Gate | Tanggal | Angka yang harus hijau |
|---|---|---|
| 🔴 **0** — Pipeline dan pengaman | 24–26 Okt | File 199.319 baris lolos validator, dan `spellF1` sudah terukur |
| 🟠 **1** — Empat hal struktural | 27 Okt – 2 Nov | Melewati baseline buatan kita sendiri, dan `macroF1` kelas `D` naik |
| 🟡 **2** — Model sekuensial | 3–9 Nov | Menang dengan confidence interval yang tidak saling tumpang tindih |
| 🟢 **3** — Reproduksi hasil dan dokumen | 10–17 Nov | Orang lain bisa menghasilkan file yang identik |

**Pendaftaran ditutup 10 November.** Kalian sudah terdaftar, jadi tanggal itu tidak perlu dikhawatirkan.

---

## Lima hal yang harus terjadi sekarang

1. **Sudah selesai:** tim sudah terdaftar, bundle data sudah terlihat di Drive, repo sudah publik, dan situs
   dokumen sudah aktif.
2. **Sekarang:** unduh bundle ke `data\tactical\` dengan nama file yang persis sama. Hanya empat file
   yang dibutuhkan; `tactical.mp4` tidak dipakai. Kalau Drive tidak mengizinkan unduhan, kirim email
   ke penyelenggara hari ini juga.
3. **Besok:** undang tiga anggota lain dengan akses **Write**, lalu masing-masing menjalankan
   `python tools/fetch_official.py` dan `python tools/gate0.py` di laptopnya.
4. **Besok:** **hapus `team-research.md`**. Isinya data pribadi dan tidak boleh sampai masuk repo publik.
5. **Setiap saat:** tidak ada pelabelan manual, dalam bentuk apa pun dan untuk tujuan apa pun. Ini
   termasuk **ingatan kalian sendiri tentang pertandingan aslinya**. Jangan pernah mengunggah data ke
   LLM cloud.

---

## Urutan membaca

| # | Dokumen | Untuk siapa |
|---|---|---|
| 1 | `docs/SUMMARY.md` | **dokumen ini** — semua orang |
| 2 | `docs/AGENDA.md` | semua orang, sebelum rapat besok |
| 3 | `docs/PLAYBOOK.md` bagian 1–3 | semua orang — alasan di balik strategi ini |
| 4 | `docs/PLAYBOOK.md` bagian 4–5 | semua orang — pembagian tugas dan jadwal |
| 5 | `docs/PLAYBOOK.md` bagian 9 | **semua orang — larangan yang tidak boleh dilanggar** |
| 6 | bagian 7 sesuai seat | 7.1, 7.4, 7.5, 7.6 → Billa · 7.2 dan 7.3 → Raissa · 7.7 → Dyang dan Billa |
| 7 | bagian 6 dan 8 | Yona |
| 8 | `docs/gt-public-transitions.md` | Dyang — pekerjaan hari pertama |
| 9 | `RULES.md` dan `CHALLENGE.md` di repo resmi | semua orang |
