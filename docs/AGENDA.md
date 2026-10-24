# AGENDA — Rapat Perdana DeculGirl

**Minggu, 25 Oktober 2026 · online · 90 menit**
Dipimpin: Dyang. Notulen: siapa pun yang paling cepat mengetik.

> Tujuan rapat ini **bukan** membahas ide. Tujuannya: supaya pada Senin malam, kalian sudah punya
> submission valid pertama dan empat orang tahu persis apa yang dikerjakannya. Ide dibahas di Gate 1.

---

## ⚡ Sebelum rapat — 10 menit, malam ini, jangan tunggu besok

**Dyang: enroll di https://landing.mobileworldcapital.com/more-than-a-hack-2027**

Alasannya bukan karena registrasi tutup 10 November. Registrasi memang tutup 10 November, tapi **fase
kerjanya sudah jalan sejak 20 Oktober** — kalian sudah kehilangan empat hari. Kalau ada jeda antara
mendaftar dan kirim link download, jeda itu mulai berjalan malam ini, bukan besok.

Yang perlu disiapkan: tanda tangan ToU (baca dulu, terutama bagian larangan hand annotation dan
larangan upload data), dan satu akun Google untuk form submission nanti.

**Aksi ini lebih penting dari seluruh isi rapat di bawah.**

---

## 1. Fakta kompetisi — 10 menit

Yang harus dipahami berempat sebelum lanjut:

- **Ini bukan hackathon akhir pekan.** Tiga fase, ~6 bulan. Kalian di Fase 1.
- **Fase 1 murni angka.** Tidak ada juri, tidak ada presentasi. Ide sebagus apa pun bernilai nol.
- **Tugasnya:** satu CSV `frame,label`, 199.319 baris, label `H`/`A`/`D`/`X`.
- **Ranking:** `spellF1` (bukan akurasi, bukan `macroF1`). `macroF1` cuma tie-break.
- **Lantai:** `spellF1` 0,2433.
- **Tiga deliverable:** file CSV · repo publik yang bisa mereproduksi file itu **persis** · dokumen
  teknis beberapa halaman.
- **Tim 3–5 orang.** Kalian 4. Aman.

Kalau ada yang belum paham kenapa `spellF1` bukan akurasi, **berhenti di sini dan jelaskan** sampai
semua paham. Empat baseline di repo resmi adalah algoritma yang sama dengan window berbeda: `macroF1`
bergerak 0,04, `spellF1` bergerak 11×. Itu satu-satunya konsep yang wajib dipahami semua orang.

## 2. Keputusan yang harus diambil hari ini — 20 menit

| # | Keputusan | Usulan | Catatan |
|---|---|---|---|
| 1 | Owner repo | **Dyang** (`DyangPB`) | Kamu sudah punya badge Pull Shark — ini bukan kerjaan baru bagimu |
| 2 | Nama repo | **`mtah-DeculGirl`** | Publik dari hari pertama |
| 3 | Seat 1–4 | Dyang · Raissa · Billa · Yona | Lihat `PLAYBOOK.md` §4. **Ubah sekarang kalau ada yang tidak setuju** — setelah Gate 1 mulai, mengubahnya mahal |
| 4 | Siapa enroll | **Dyang** | Malam ini |
| 5 | Jam sync harian | **Putuskan di sini** | 20 menit, jam tetap. Tanpa ini, tim remote akan drift dalam 4 hari |
| 6 | Zona waktu | Semua WIB | Konfirmasi cepat |

Keputusan #5 yang paling sering diremehkan dan paling mahal akibatnya. Pilih jam yang kalian
berempat benar-benar bisa, lalu **perlakukan seperti jadwal kuliah**.

## 3. Aturan main — 10 menit

Empat hal, dan nomor 1 tidak bisa ditawar:

1. **Tidak ada hand label, dalam bentuk apa pun, untuk tujuan apa pun.** Bukan untuk submission, bukan
   untuk melatih model, bukan untuk memvalidasi. Termasuk memperbaiki output algoritma secara manual.
   Hand label pada pertandingan **lain** boleh, sebanyak apa pun.
2. **Ingatan kalian soal pertandingan ini tidak boleh masuk ke kode.** Ini jebakan khusus untuk Dyang —
   satu-satunya yang menonton LaLiga konsisten. Memahami *arti* sepak bola: boleh. Mengingat
   *pertandingan ini* (skor, menit gol, kejadian VAR): tidak boleh. Kalau ada yang ragu, tanya di chat
   sebelum memakainya.
3. **Jangan pernah upload data, video, atau potongannya ke LLM cloud.** Ini ada di ToU. Pakai AI untuk
   menulis kode tetap boleh — yang dilarang mengirim isi datanya.
4. **`data/` tidak pernah masuk git.** Repo kalian publik.

## 4. Kerja Gate 0 — Sel 24 – Sen 26 Okt — 30 menit

Target Gate 0, dan ini yang harus dipegang:

> Pada Senin malam, `run.py` menghasilkan file 199.319 baris yang **lolos `validate_submission.py`**,
> dan kita punya angka `spellF1` terukur.

Pembagian **tiga hari ke depan**:

| Orang | Sabtu–Minggu | Senin |
|---|---|---|
| **Dyang** | Enroll + tanda tangan ToU. Bikin repo kosong (**tanpa** README/`.gitignore`/license — biar push pertama tidak konflik), invite tiga lainnya sebagai **write** | Mulai `docs/possession-rules.md` pakai `docs/gt-public-transitions.md` |
| **Raissa** | `tools/fetch_official.py`, `tools/gate0.py`, pastikan evaluator resmi jalan di laptopmu. Unpack data ke `data/`, konfirmasi tracking = **199.319 baris** | `src/deculgirl/features/` — loader + kanonikalisasi |
| **Billa** | Baca `CHALLENGE.md` + `FAQ.md` sampai habis. Renungkan §7.1 playbook | Rancang dead-ball classifier (§7.1) |
| **Yona** | `run.py`, `metrics/`, CI. Ukur baseline resmi di jendela publik — angka itu jadi titik nol | Regression suite + bootstrap CI |

**Semua orang hari ini:** clone repo, taruh di **drive D:** (drive C: Dyang tinggal 8 GB), dan
jalankan `tools/gate0.py`. Gate 0 bukan pekerjaan berempat yang berurutan — ini satu jalan yang
dilewati berempat, dan siapa pun yang macet mengangkat tangan di chat.

## 5. Pembagian bacaan — 10 menit

Tidak ada yang perlu membaca ketujuh dokumen resmi. Tapi setiap seat **wajib** membaca miliknya, dan
melaporkan satu hal yang mengejutkan di sync besok.

| Seat | Baca | Cari |
|---|---|---|
| 1 · Dyang | `CHALLENGE.md` (§Possession rules) + `EVALUATION.md` | Apa persisnya yang bikin sebuah frame jadi `D` |
| 2 · Raissa | `DATA.md` | Setiap aset, formatnya, dan bagaimana frame diselaraskan |
| 3 · Billa | `CHALLENGE.md` + `FAQ.md` | Kenapa bola hilang 41%, dan apa kata mereka soal `X` |
| 4 · Yona | `EVALUATION.md` + `SUBMISSION.md` | Kontrak file persis, dan kenapa 5 menit publik bukan leaderboard |
| **Semua** | **`RULES.md`** | **Garis merah. Ini wajib, tanpa kecuali** |

## 6. Penutup — 10 menit

- Konfirmasi jam sync harian.
- Tunjuk satu orang yang menulis `docs/decisions.md` di setiap rapat (usulan: Dyang, karena dia pemilik
  dokumennya).
- Setuju target: **top 20**, dengan asuransi **submit valid** di minggu pertama.
- Satu kalimat penutup dari masing-masing: **apa yang akan kamu selesaikan sebelum sync besok?**

---

## Aksi setelah rapat

**Malam ini:** Dyang enroll.
**Besok pagi:** repo dibuat, tiga orang di-invite, `tools/gate0.py` dijalankan berempat.
**Senin malam:** submission valid pertama ada. Angka `spellF1` pertama tercatat.
**Mulai Selasa:** Gate 1 — empat pilar, empat seat, paralel.

---

> Satu hal yang perlu diingat berempat: kalian punya **25 hari**, dan kira-kira 20 hari di antaranya
> efektif setelah dipotong freeze dan dokumen. Itu cukup untuk menembus top 20 — tapi hanya kalau
> tidak ada hari yang hilang karena tidak jelas siapa mengerjakan apa. Rapat ini gunanya untuk itu.
