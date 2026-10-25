# AGENDA — Rapat Perdana DeculGirl

**Minggu, 25 Oktober 2026 · online · 90 menit**
Pemimpin rapat: Dyang. Notulis: siapa pun yang paling cepat mengetik.

> Tujuan rapat ini **bukan** membahas ide. Tujuannya adalah supaya pada Senin malam kalian sudah punya
> submission valid yang pertama, dan keempat anggota tahu persis apa yang harus dikerjakan. Ide baru
> dibahas di Gate 1.

---

## ✅ Yang sudah selesai sebelum rapat

**Tim sudah terdaftar, dan bundle data pertandingan sudah tersedia.** Ada lima file di folder Drive:
`tactical.mp4`, `atd.txt`, `atd.xml`, `smart_tagging.xml`, dan `homography.csv`.

Yang perlu dipastikan di rapat hanya satu: file-file itu **bisa diunduh**, bukan sekadar bisa dilihat.
Ikon "shared" di Drive hanya menandakan file itu dibagikan. Itu belum berarti kalian boleh mengunduhnya.

- **Kalau bisa diunduh:** taruh di `data\tactical\` dengan **nama file yang persis sama dengan aslinya**,
  lalu jalankan `python run.py`. Angka `spellF1` pertama kalian akan langsung muncul.
- **Kalau tidak bisa:** kirim email ke **hackathon.talentarena@mobileworldcapital.com** sekarang juga,
  jangan menunggu besok. Ini satu-satunya masalah di proyek ini yang tidak bisa diatasi dengan kerja keras.

Yang **tidak** kalian butuhkan adalah `tactical.mp4`. Video berdurasi 2¼ jam itu sama sekali tidak
dipakai pipeline kita. Alasannya ada di `decisions.md` nomor 005. Kalau ukuran filenya jadi masalah,
lewati saja.

Satu catatan soal administrasi: **form pendaftaran tidak meminta tanda tangan, dan itu tidak
mengurangi kewajiban apa pun.** Aturan di `RULES.md` berlaku karena kalian adalah peserta, bukan karena
kalian menandatangani sesuatu. Larangan pelabelan manual dan larangan mengunggah data ke LLM cloud
tetap berlaku penuh. Jangan sampai "tidak ada tanda tangan" dibaca sebagai "tidak ada aturan".

---

## 1. Fakta tentang kompetisi — 10 menit

Hal-hal yang harus dipahami keempat anggota sebelum lanjut:

- **Ini bukan hackathon akhir pekan.** Ada tiga fase selama sekitar 6 bulan, dan kalian ada di Fase 1.
- **Fase 1 murni dinilai dari angka.** Tidak ada juri dan tidak ada presentasi. Ide sebagus apa pun
  tidak bernilai.
- **Tugasnya:** membuat satu CSV `frame,label` berisi 199.319 baris, dengan label `H`/`A`/`D`/`X`.
- **Peringkat ditentukan oleh `spellF1`**, bukan akurasi dan bukan `macroF1`. `macroF1` hanya dipakai
  sebagai pemutus kalau `spellF1` seri.
- **Batas minimum:** `spellF1` 0,2433.
- **Tiga hal yang harus dikumpulkan:** file CSV, repo publik yang bisa menghasilkan file itu **persis
  sama**, dan dokumen teknis setebal beberapa halaman.
- **Satu tim boleh 3–5 orang.** Kalian berempat, jadi aman.

Kalau ada yang belum paham kenapa `spellF1` bukan akurasi, **berhenti dulu dan jelaskan** sampai
semuanya paham. Keempat baseline di repo resmi memakai algoritma yang sama dan hanya berbeda pada lebar
window. Akibatnya `macroF1` hanya bergeser 0,04, sedangkan `spellF1` berbeda 11 kali lipat di jendela
publik. Inilah satu-satunya konsep yang wajib dipahami semua orang.

## 2. Keputusan yang harus diambil hari ini — 20 menit

| # | Keputusan | Usulan | Catatan |
|---|---|---|---|
| 1 | Hak akses repo | **Owner: Dyang** (`DyangPB`) · **admin kedua: Billa** (`nabilland`) · Raissa dan Yona: **Write** | Adminnya dua orang, bukan satu. Alasannya ada di bawah |
| 2 | Nama repo | **`mtah-DeculGirl`** | Dibuat publik sejak hari pertama |
| 3 | Seat 1–4 (domain · data · model · metrik) | Dyang · Raissa · Billa · Yona | Lihat `PLAYBOOK.md` bagian 4. **Ubah sekarang kalau ada yang tidak setuju** |
| 4 | **Siapa yang jadi PM** | **Sengaja dikosongkan** | Tidak harus Dyang. Tanyakan langsung di rapat siapa yang bersedia |
| 5 | Akses ke bundle data | **Sudah ada** | Pastikan bisa diunduh, bukan hanya dilihat |
| 6 | Jam rapat harian | **Putuskan di rapat ini** | 20 menit, jamnya tetap. Tanpa ini, tim remote akan berjalan sendiri-sendiri dalam 4 hari |
| 7 | Zona waktu | Semua WIB | Cukup dikonfirmasi |

Dua keputusan berikut paling sering terlewat, dan akibatnya mahal.

**#1 — Kenapa adminnya dua orang.** GitHub tidak punya peran "co-owner". Yang ada adalah **Admin**,
di samping Read, Triage, Write, dan Maintain. Jadi "admin kedua" berarti Billa diberi peran **Admin**,
bukan Write.

Alasannya bukan membagi beban kerja, melainkan **mengurangi risiko bergantung pada satu orang**. Hanya
Admin yang bisa mengubah Settings, mengatur siapa yang boleh mengakses repo, menyalakan proteksi
branch, dan mengelola Actions. Kalau hanya satu orang yang memegang akses itu dan dia tidak bisa
dihubungi pada 14 November, tim tidak bisa memperbaiki repo tepat di minggu paling genting. Punya dua
admin itu hal yang wajar, bukan berlebihan.

Billa dipilih karena dia satu-satunya yang pernah bekerja di dua GitHub Organization
(`Solo-Digital-Solution` dan `ppw24-teaching-assistant`), sehingga urusan hak akses, review PR, dan
merge bukan hal baru baginya. Raissa dan Yona cukup diberi **Write**, karena mereka hanya perlu push
dan membuka PR, bukan mengubah pengaturan.

**#4 — PM.** Tidak ada bagian teknis di proyek ini yang bergantung pada adanya PM. Yang bergantung
padanya adalah hal-hal yang baru terasa penting setelah semuanya terlambat: menjaga rapat harian tetap
berjalan, memutuskan apakah sebuah gate sudah hijau atau belum, dan yang paling menentukan, **menjadi
satu nama yang bertanggung jawab atas file submission**. Kalau sampai 2 November belum ada yang
bersedia, tugas ini otomatis jatuh ke Dyang, karena file submission harus punya satu penanggung jawab
dan Dyang adalah pemilik repo.

**#6 — Jam rapat harian.** Pilih jam yang benar-benar bisa dihadiri keempat orang, lalu **anggap
seperti jadwal kuliah**.

## 3. Aturan main — 10 menit

Ada empat aturan, dan aturan nomor 1 tidak bisa ditawar:

1. **Tidak boleh ada pelabelan manual, dalam bentuk apa pun dan untuk tujuan apa pun.** Tidak untuk
   submission, tidak untuk melatih model, dan tidak untuk memvalidasi. Memperbaiki hasil algoritma
   dengan tangan juga termasuk. Pelabelan manual pada pertandingan **lain** boleh, sebanyak apa pun.
2. **Ingatan kalian tentang pertandingan ini tidak boleh masuk ke kode.** Ini jebakan terutama bagi
   Dyang dan Raissa, yang paham sepak bola dan rutin menonton LaLiga. Memahami *arti* sepak bola itu
   boleh. Mengingat *pertandingan ini* (skor, menit gol, kejadian VAR) tidak boleh. Kalau ragu, tanyakan
   di chat sebelum memakainya.
3. **Jangan pernah mengunggah data, video, atau potongannya ke LLM cloud.** Larangan ini ada di syarat
   penggunaan (ToU). Memakai AI untuk menulis kode tetap boleh. Yang dilarang adalah mengirim isi
   datanya.
4. **Folder `data/` tidak boleh masuk git.** Repo kalian bersifat publik.

## 4. Pekerjaan Gate 0 — Sab 24 – Sen 26 Okt — 30 menit

Target Gate 0 harus dipegang erat:

> Pada Senin malam, `run.py` menghasilkan file 199.319 baris yang **lolos `validate_submission.py`**,
> dan kita sudah punya angka `spellF1` yang terukur.

Pembagian kerja **tiga hari ke depan**:

| Orang | Sabtu–Minggu | Senin |
|---|---|---|
| **Dyang** | Repo sudah jadi dan ter-push. Undang tiga anggota lain dengan akses **Write** | Mulai mengisi `docs/possession-rules.md` dengan bantuan `docs/gt-public-transitions.md`, dan buka `docs/experiments.md` untuk mencatat variasi pertama |
| **Raissa** | Jalankan `tools/fetch_official.py` dan `tools/gate0.py`, pastikan evaluator resmi berjalan di laptopnya. Ekstrak data ke `data/` dan pastikan jumlah baris tracking = **199.319** | Kerjakan `src/deculgirl/features/`: pembaca data dan penyeragaman formatnya |
| **Billa** | Baca `CHALLENGE.md` dan `FAQ.md` sampai habis. Pikirkan baik-baik bagian 7.1 di playbook | Rancang pendeteksi bola mati (bagian 7.1) |
| **Yona** | Siapkan `run.py`, `metrics/`, dan CI. Ukur baseline resmi di jendela publik; angka itu jadi titik awal | Buat regression suite dan bootstrap CI |

**Semua orang hari ini:** clone repo, simpan di **drive D:** (drive C: Dyang hanya tersisa 8 GB), lalu
jalankan `tools/gate0.py`. Gate 0 bukan empat pekerjaan yang berurutan. Ini satu jalur yang dilewati
berempat, dan siapa pun yang tersendat langsung memberi tahu di chat.

## 5. Pembagian bahan bacaan — 10 menit

Tidak ada yang perlu membaca ketujuh dokumen resmi. Tetapi setiap seat **wajib** membaca bagiannya,
lalu melaporkan satu hal yang mengejutkan di rapat besok.

| Seat | Baca | Cari tahu |
|---|---|---|
| 1 · Dyang | `CHALLENGE.md` (bagian Possession rules) dan `EVALUATION.md` | Apa persisnya yang membuat sebuah frame berlabel `D` |
| 2 · Raissa | `DATA.md` | Setiap jenis data, formatnya, dan cara menyelaraskan nomor frame |
| 3 · Billa | `CHALLENGE.md` dan `FAQ.md` | Kenapa bola hilang di 41% frame, dan apa kata penyelenggara soal `X` |
| 4 · Yona | `EVALUATION.md` dan `SUBMISSION.md` | Format file yang persis diminta, dan kenapa 5 menit publik bukan leaderboard |
| **Semua** | **`RULES.md`** | **Aturan yang tidak boleh dilanggar. Wajib, tanpa kecuali** |

## 6. Penutup — 10 menit

- Konfirmasi jam rapat harian.
- Tunjuk satu orang yang mencatat `docs/decisions.md` di setiap rapat (usulan: Dyang, karena dia
  pemilik dokumennya).
- Sepakati targetnya: **masuk top 20**, dengan pengaman berupa **submission valid** di minggu pertama.
- Masing-masing menyebut satu kalimat penutup: **apa yang akan kamu selesaikan sebelum rapat besok?**

---

## Tindak lanjut setelah rapat

**Sudah selesai:** pendaftaran, repo publik, commit pertama, situs dokumen.
**Besok:** unduh bundle ke `data\tactical\`, undang tiga anggota lain dengan akses **Write**, lalu
jalankan `tools/gate0.py` berempat.
**Senin malam:** submission valid pertama sudah ada, dan angka `spellF1` pertama tercatat.
**Mulai Selasa:** Gate 1, yaitu empat pekerjaan struktural yang dikerjakan paralel oleh empat seat.

---

> Satu hal yang perlu diingat berempat: waktu kalian **25 hari**, dan sekitar 20 hari di antaranya
> benar-benar bisa dipakai setelah dikurangi masa freeze dan penulisan dokumen. Itu cukup untuk masuk
> top 20, tetapi hanya kalau tidak ada hari yang terbuang karena tidak jelas siapa mengerjakan apa.
> Itulah gunanya rapat ini.
