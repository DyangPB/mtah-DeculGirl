# AGENDA — Rapat Perdana DeculGirl

**Minggu, 25 Oktober 2026 · online · 90 menit**
Dipimpin: Dyang. Notulen: siapa pun yang paling cepat mengetik.

> Tujuan rapat ini **bukan** membahas ide. Tujuannya: supaya pada Senin malam, kalian sudah punya
> submission valid pertama dan empat orang tahu persis apa yang dikerjakannya. Ide dibahas di Gate 1.

---

## ✅ Sudah selesai sebelum rapat

**Kalian sudah terdaftar, dan bundle pertandingannya sudah ada** — lima file di folder Drive:
`tactical.mp4`, `atd.txt`, `atd.xml`, `smart_tagging.xml`, `homography.csv`.

Yang perlu dipastikan di rapat cuma satu: **bisa diunduh**, bukan cuma dilihat. Ikon "shared" di Drive
itu tanda file-nya dibagikan, bukan tanda kalian boleh mengunduhnya.

- **Kalau bisa diunduh** → taruh di `data\tactical\` dengan **nama file persis seperti aslinya**, lalu
  jalankan `python run.py`. Angka `spellF1` pertama kalian akan muncul.
- **Kalau tidak bisa** → kirim email ke **hackathon.talentarena@mobileworldcapital.com** sekarang,
  jangan tunggu besok. Ini satu-satunya hal di proyek ini yang tidak bisa dikejar dengan kerja keras.

Dan yang **tidak** kalian butuhkan: `tactical.mp4`. Itu 2¼ jam video yang tidak dipakai pipeline kita
sama sekali — alasannya di `decisions.md` #005. Kalau ukuran file-nya yang jadi masalah, lewati saja.

Satu catatan soal administrasi: **tidak ada tanda tangan yang diminta di form itu, dan itu tidak
mengurangi apa pun.** Aturan di `RULES.md` berlaku karena kalian peserta, bukan karena kalian
menandatangani sesuatu — larangan hand label dan larangan mengunggah data ke LLM cloud tetap berlaku
penuh. Jangan sampai "tidak ada tanda tangan" terbaca sebagai "tidak ada aturan".

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
| 1 | Akses repo | **Owner: Dyang** (`DyangPB`) · **co-admin: Billa** (`nabilland`) · Raissa & Yona: **Write** | Dua admin, bukan satu — lihat alasannya di bawah |
| 2 | Nama repo | **`mtah-DeculGirl`** | Publik dari hari pertama |
| 3 | Seat 1–4 (domain · data · model · metrik) | Dyang · Raissa · Billa · Yona | Lihat `PLAYBOOK.md` §4. **Ubah sekarang kalau ada yang tidak setuju** |
| 4 | **Siapa jadi PM** | **Sengaja dikosongkan** | Tidak harus Dyang. Tanyakan langsung di rapat — siapa yang bersedia |
| 5 | Akses bundle data | **Sudah ada** | Pastikan bisa diunduh, bukan cuma dilihat |
| 6 | Jam sync harian | **Putuskan di sini** | 20 menit, jam tetap. Tanpa ini, tim remote akan drift dalam 4 hari |
| 7 | Zona waktu | Semua WIB | Konfirmasi cepat |

Dua keputusan di atas yang paling sering dilewatkan, dan keduanya mahal:

**#1 — Kenapa dua admin.** Di GitHub tidak ada peran "co-owner"; yang ada **Admin** di samping Read,
Triage, Write, dan Maintain. Jadi "co-admin" maksudnya Billa diberi role **Admin**, bukan Write.

Alasannya bukan berbagi beban, tapi **bus factor**. Admin adalah satu-satunya role yang bisa mengubah
Settings, mengatur siapa punya akses, menyalakan branch protection, dan menyentuh Actions. Kalau cuma
satu orang yang bisa membuka pintu itu, dan orang itu tidak bisa dihubungi di 14 November, tim kalian
kehilangan kemampuan memperbaiki repo tepat di minggu paling berbahaya. Dua admin adalah kelaziman,
bukan kelebihan.

Dan Billa memang orang yang tepat: dia satu-satunya yang sudah pernah bekerja di dalam dua GitHub
Organization (`Solo-Digital-Solution` dan `ppw24-teaching-assistant`), jadi urusan akses, review PR,
dan merge bukan hal baru baginya. Raissa dan Yona cukup **Write** — mereka perlu push dan buka PR, tidak
perlu mengubah setting.

**#4 — PM.** Tidak ada satu pun bagian teknis di proyek ini yang bergantung pada adanya PM. Yang
bergantung padanya adalah hal-hal yang tidak dihitung sampai semuanya telat: menjaga sync tetap jalan,
memutuskan "gate ini hijau atau belum", dan — yang paling menentukan — **punya satu nama yang bertanggung
jawab atas file submission**. Kalau sampai 2 November tidak ada yang bersedia, jatuh ke Dyang secara
default, karena file submission harus punya satu nama dan kamu pemilik repo-nya.

**#6 — Jam sync.** Pilih jam yang berempat benar-benar bisa, lalu **perlakukan seperti jadwal kuliah**.

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
| **Dyang** | Repo sudah jadi dan ter-push. Invite tiga lainnya sebagai **write** | Mulai `docs/possession-rules.md` pakai `docs/gt-public-transitions.md`, dan buka `docs/experiments.md` — catat variasi pertama kalian di situ |
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

**Sudah selesai:** enrollment, repo publik, commit pertama, situs dokumen.
**Besok:** unduh bundle ke `data\tactical\`, invite tiga lainnya sebagai **write**, jalankan `tools/gate0.py` berempat.
**Senin malam:** submission valid pertama ada. Angka `spellF1` pertama tercatat.
**Mulai Selasa:** Gate 1 — empat pilar, empat seat, paralel.

---

> Satu hal yang perlu diingat berempat: kalian punya **25 hari**, dan kira-kira 20 hari di antaranya
> efektif setelah dipotong freeze dan dokumen. Itu cukup untuk menembus top 20 — tapi hanya kalau
> tidak ada hari yang hilang karena tidak jelas siapa mengerjakan apa. Rapat ini gunanya untuk itu.
