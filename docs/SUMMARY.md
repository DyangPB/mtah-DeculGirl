# RINGKASAN — DeculGirl

**Baca ini 5 menit.** Detailnya ada di `docs/PLAYBOOK.md`. Kalau ada yang bertentangan antara file ini
dan playbook, playbook yang benar.

More than a Hack 2027 · Phase 1: Ball Possession · deadline **17 November 2026** · hari ini **24 Oktober**

---

## Apa yang kita kerjakan

Penyelenggara memberi satu pertandingan LaLiga lengkap — **Barcelona vs Athletic**, plus tracking
otomatis, tagging taktis, dan geometri kamera. Tugas kita satu kalimat:

> **Untuk setiap frame, katakan siapa yang menguasai bola.**

Output: satu CSV `frame,label`, **199.319 baris**, label `H` / `A` / `D` / `X`.
Dinilai otomatis pada **`spellF1`**. Tidak ada juri. Tidak ada presentasi.

Tiga yang wajib dikumpul: **file CSV** · **repo publik yang bisa mereproduksi file itu persis** ·
**dokumen teknis** beberapa halaman.

---

## Delapan angka yang menentukan

| Angka | Kenapa penting |
|---|---|
| **0,2433** | Lantai `spellF1` yang harus dilewati (`baseline_smooth50`, pertandingan penuh) |
| **158.857** | Frame yang dinilai, dari 199.319. Sisanya tidak berpengaruh sama sekali |
| **41%** | Frame dinilai yang **bolanya hilang** — dan hilangnya justru di frame penting |
| **11×** | Selisih `spellF1` antar-empat baseline yang **algoritmanya sama**, cuma beda window |
| **0,04** | Selisih di bawah ini bukan kemajuan, cuma noise |
| **17** | Possession di jendela publik 5 menit. 21 segmen, rata-rata 14,2 detik |
| **19** | Possession terpendek di GT — 0,76 detik — dan itu **sungguhan** |
| **14 Nov** | Tanggal freeze. Setelah itu tidak ada perubahan kode |

---

## Kenapa kita bisa menang, dan kenapa bukan soal model

`spellF1` mengukur **fragmentasi**, bukan akurasi. Empat baseline di repo resmi adalah algoritma yang
sama: `macroF1` bergerak 0,04, `spellF1` bergerak 11×.

Skor kita datang dari **empat hal struktural**, dan tidak satu pun berupa "model yang lebih canggih":

1. **Deteksi dead-ball.** Baseline tidak punya logika bola mati sama sekali — dia cuma bilang "bola tidak
   terdeteksi". Ini lubang terbesar, dan kelas `D` justru **memburuk** kalau dihaluskan.
2. **Imputasi bola.** 41% frame dinilai bolanya hilang, dan tepat di frame yang paling penting.
3. **Atribusi tim.** Baseline cuma "pemain terdekat". Ada jarak, arah gerak, konteks, dan tag tim dari
   Smart Tagging yang belum dipakai siapa pun.
4. **Segmentasi anti-fragmentasi.** Memecah satu possession jadi dua = **1 false positive + 1 false
   negative sekaligus**. Kolom `frag` di papan skor hampir merupakan prediktor langsung `spellF1`.

Dan satu tool yang paling sering disalahpahami: **`X` bukan tombol menyerah, tapi tombol "sama seperti
sebelumnya"**. Scorer mengisi `X` dengan label terakhir sebelum menyusun possession. Jadi diam di tengah
possession itu **gratis**; diam di titik hand-over itu **bencana**.

---

## Siapa mengerjakan apa

| Seat | Orang | Tugas | Output yang dicek |
|---|---|---|---|
| 1 | **Dyang** | Domain + aturan + owner repo **+ alat diagnosa** | `docs/possession-rules.md`, laporan diagnosa |
| 2 | **Raissa** | Data, alignment, fitur per frame **+ co-owner domain** | `features.parquet`, laporan diagnosa |
| 3 | **Billa** | Dead-ball, atribusi, segmentasi, dokumen teknis | `src/deculgirl/model/`, draf dokumen |
| 4 | **Yona** | Metrik, validasi, reproducibility (paruh waktu) | `metrics/`, `run.py`, CI |
| — | ⬜ **PM** | **Belum ditetapkan** — tanyakan di rapat | Pemilik file submission, penjaga timeline |

Tiga catatan. **Seat-nya masih sementara** — rapat pertama yang mengunci. **PM itu topi, bukan seat**,
jadi kalian tidak butuh orang kelima; pemegangnya tetap punya seat teknisnya sendiri, dan harus ada yang
memegang paling lambat **2 November**. Dan Yona satu-satunya yang masih intern, sementara Seat 4 adalah
jalur kritis — jadi Gate 0 dikerjakan berpasangan lalu dibekukan, gate-nya diotomasi, dan fungsi "apakah
bedanya nyata?" pindah ke Raissa.

---

## Timeline

Hari ini Sabtu **24 Okt**. Deadline Selasa **17 Nov**.

| Gate | Tanggal | Angka hijau |
|---|---|---|
| 🔴 **0** — pipeline & fail-safe | 24–26 Okt | File 199.319 baris lolos validator, dan `spellF1` terukur |
| 🟠 **1** — empat pilar | 27 Okt – 2 Nov | Lewati baseline sendiri, `macroF1` kelas `D` naik |
| 🟡 **2** — model sekuensial | 3–9 Nov | Menang pada CI yang tidak tumpang tindih |
| 🟢 **3** — reproducibility & dokumen | 10–17 Nov | Orang lain bisa reproduksi file identik |

**Registrasi tutup 10 November** — dan kalian belum enroll.

---

## Lima hal yang harus terjadi sekarang

1. **Malam ini:** satu orang enroll + tanda tangan ToU. Fase kerjanya sudah jalan sejak 20 Oktober;
   kalian sudah kehilangan 4 hari.
2. **Besok:** bikin repo kosong `mtah-DeculGirl`, invite tiga lainnya sebagai **write**.
3. **Besok:** `git push`, lalu `python tools/fetch_official.py && python tools/gate0.py`.
4. **Besok:** **hapus `team-research.md`** — isinya data pribadi, jangan pernah masuk repo publik.
5. **Sepanjang waktu:** tidak ada hand label, dalam bentuk apa pun, untuk tujuan apa pun — termasuk
   **ingatan kalian sendiri soal pertandingan aslinya**, dan jangan pernah upload data ke LLM cloud.

---

## Urutan baca

| # | Dokumen | Untuk siapa |
|---|---|---|
| 1 | `docs/SUMMARY.md` | **ini** — semua orang |
| 2 | `docs/AGENDA.md` | semua orang, sebelum rapat besok |
| 3 | `docs/PLAYBOOK.md` §1–3 | semua orang — kenapa strateginya begini |
| 4 | `docs/PLAYBOOK.md` §4–5 | semua orang — job desk + flow |
| 5 | `docs/PLAYBOOK.md` §9 | **semua orang — garis merah, tanpa kecuali** |
| 6 | §7 sesuai seat | 7.1 & 7.4 & 7.5 & 7.6 → Billa · 7.2 & 7.3 → Raissa · 7.7 → Dyang & Billa |
| 7 | §6 & §8 | Yona |
| 8 | `docs/gt-public-transitions.md` | Dyang — pekerjaan hari pertama |
| 9 | `RULES.md` + `CHALLENGE.md` di repo resmi | semua orang |
