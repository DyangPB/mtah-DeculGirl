# PLAYBOOK — DeculGirl

**More than a Hack 2027 · Phase 1: Ball Possession**
Metrica Sports × FC Barcelona (Barça Innovation Hub) × Mobile World Capital Barcelona

Ditulis 24 Oktober 2026 · Deadline submission **17 November 2026**

---

## 0. Cara pakai dokumen ini

**Kalau kamu cuma punya 5 menit, baca [`SUMMARY.md`](SUMMARY.md), bukan dokumen ini.** Dokumen ini
adalah versi lengkapnya — tempat semua angka, alasan, dan keputusan tinggal.

Ini bukan dokumen motivasi. Ini dokumen operasional: setiap bagian di sini punya konsekuensi yang bisa
dicek. Cara pakainya:

- **Seat 1 (Dyang)** memakai §4, §5, §7, §9 dan memelihara `docs/decisions.md`.
- **Seat 2 (Raissa)** memakai §7.2 dan §7.3 sebagai daftar kerja fitur.
- **Seat 3 (Billa)** memakai §7.1, §7.4, §7.5, §7.6.
- **Seat 4 (Yona)** memakai §6 dan §8 — dia penjaga ukurannya.
- **Semua orang** wajib baca §1, §2, §9.

Kalau isi dokumen ini bertentangan dengan repo resmi penyelenggara, **repo resmi yang benar**. Semua
angka di sini diambil dari sana pada 24 Oktober 2026, dari commit `f8f2629`.

---

## 1. Apa yang sebenarnya kita kerjakan

Satu pertandingan LaLiga lengkap: **FC Barcelona vs Athletic Club**, LaLiga EA Sports 2024-25 matchday 2.
Kita diberi rekaman dua kamera, tracking otomatis setiap pemain dan bola, tagging taktis otomatis
(Smart Tagging), dan geometri kamera-ke-lapangan (homography).

Tugasnya satu kalimat:

> **Untuk setiap frame pertandingan, katakan siapa yang menguasai bola.**

Outputnya satu file CSV: `frame,label`, **199.319 baris**, frame `0`–`199318`, label `H` / `A` / `D` / `X`.

| Label | Arti |
|---|---|
| `H` | Barcelona (home) menguasai bola, bola hidup |
| `A` | Athletic (away) menguasai bola, bola hidup |
| `D` | bola mati — bola tidak dalam permainan |
| `X` | tidak menjawab |

**Dan ini bagian yang paling sering disalahpahami orang:** tugas ini **bukan** tantangan computer vision,
**bukan** multi-object tracking, dan **bukan** rekonstruksi game state. Tracking, tagging, dan homography
sudah diberikan supaya tidak ada yang perlu membangun deteksi, re-identifikasi, dan kalibrasi kamera
dari nol. Yang dinilai murni: apa yang geometri 22 pemain dan satu bola katakan tentang siapa yang
menguasai bola.

Dan yang lebih penting lagi — dari `CHALLENGE.md`:

> *"The ground truth is derived from corrected tracking data — not from a human watching video, and not
> from event data. The derivation is mechanical: a frame is `D` where the corrected tracking marks the
> ball dead, and otherwise takes the team the tracking names as owning it. Nothing is smoothed,
> interpolated or hand-adjusted afterwards."*

Artinya: **ground truth-nya bukan penilaian manusia soal sepak bola.** GT adalah output dari sebuah
sistem pelacakan versi terkoreksi. Yang kalian kejar bukan "kebenaran sepak bola", tapi **menebak apa
yang akan dikatakan tracking terkoreksi itu**. Dan satu-satunya jendela untuk melihat logikanya adalah
**5 menit ground truth publik** yang ada di repo.

---

## 2. Peta medan: angka-angka yang menentukan

| | |
|---|---|
| FPS | 25 |
| Total frame video | 199.319 (0–199318) |
| **Frame yang dinilai** | **158.857** |
| Babak 1 dinilai | frame 11.185 – 90.651 (79.467 frame) |
| Babak 2 dinilai | frame 110.808 – 190.197 (79.390 frame) |
| Babak 2 kick-off | frame **113.742** — jadi 2.934 frame pertama babak 2 dinilai dan **semuanya `D`** |
| Bola terdeteksi | 56,9% seluruh frame (113.488 / 199.319) · 59,3% frame dinilai (94.214 / 158.857) |
| **Bola hilang** | **41% frame yang dinilai**, 43% seluruh frame |
| Track slot | 46 (feed taktis) · 51 (broadcast) |
| Tracker broadcast | 164.488 record (timeline sendiri, tidak selaras frame) |
| Smart Tagging | 638 fase |
| Homography valid | taktis 100% · broadcast 65,8% |
| Pitch | 105,3 × 68,0 m (versi `games.py`; metadata menulis 105,0 × 68,0) |
| Frame offset | `{1: 1702057, 2: 1702058}` — beda satu frame antar babak |
| `video_frame` | `= id_frame − 1` (tracking 1-based, submission 0-based) |

**5 menit ground truth publik** (satu-satunya yang kita punya):

| | |
|---|---|
| Cakupan | frame 11.185 – 18.684 |
| Frame dinilai | 7.500 |
| Possession | **17** · 21 segmen · rata-rata 14,2 detik |
| Komposisi | `H` 3.454 · `A` 2.577 · `D` 1.469 |

**Lantai yang harus dilewati** — `baseline_smooth50`, diukur pada pertandingan penuh:

| Baseline | macroF1 | spellF1 |
|---|---|---|
| `baseline_raw` | 0,6532 | 0,0486 |
| `baseline_smooth25` | **0,6752** | 0,1996 |
| `baseline_smooth50` | 0,6724 | **0,2433** ← lantai |
| `baseline_smooth125` | 0,6356 | 0,2242 |

Baca tabel itu sekali lagi. Empat baris itu **algoritma yang sama, empat kali** — pemain tracked terdekat
ke bola, lalu voting mayoritas atas sebuah window. Yang berubah cuma lebar window-nya. `macroF1` bergerak
**0,04**. `spellF1` bergerak **lima kali lipat**.

Itu bukan kebetulan — itu inti dari seluruh kompetisi ini.

---

## 3. Kenapa kita bisa menang, dan kenapa model bukan jawabannya

`spellF1` mengukur **fragmentasi**, bukan ketepatan per frame. Setiap possession (run maksimal `H` atau
`A`) diperlakukan sebagai satu objek, dipasangkan satu-ke-satu dengan possession asli lewat **temporal
IoU**, lalu F1-nya dirata-rata pada threshold 0,3 / 0,4 / 0,5 / 0,6 / 0,7.

Konsekuensinya yang menentukan strategi:

1. **Serpihan kecil bukan setengah benar — dia salah penuh.** Scorer **tidak punya minimum panjang
   possession**. Satu frame pun dihitung possession utuh. Dan `fp` bukan cuma possession hantu:
   possession kita yang overlap dengan yang asli tapi IoU-nya di bawah ambang **juga** dihitung FP.
   Jadi memecah satu possession asli jadi dua menghasilkan **1 FP + 1 FN sekaligus**. "Jangan
   fragmentasi" itu aritmetika, bukan saran gaya.
2. **Satu kesalahan bisa bergerak 6 poin.** Di jendela publik, satu possession yang meleset ≈ 6 poin
   `spellF1`. Efeknya besar per unit kerja.
3. **Terlambat 1 frame itu gratis.** Terlambat 1 detik jatuhnya ke 0,6539. Artinya: **tepat di tepi
   tidak penting, memotong di tengah itu fatal.**
4. **Label konstan bernilai tepat 0.** Tidak ada jalan aman.

**Buktinya, dari menjalankan scorer resmi pada 5 menit publik.** Kolom `frag` adalah rasio jumlah
segmen prediksi terhadap 21 segmen kebenaran:

| Versi baseline | `frag` | `spellF1` | possession dilaporkan (GT: 17) |
|---|---|---|---|
| `baseline_smooth125` | 0,81 | **0,4242** | 16 (−1) |
| `baseline_smooth50` | 1,43 | 0,3256 | 26 (+9) |
| `baseline_smooth25` | 1,90 | 0,2868 | 36 (+19) |
| `baseline_raw` | 6,52 | 0,0378 | 131 (+114) |

Kolom `frag` hampir menjadi prediktor langsung `spellF1`, dan hubungannya monoton. Angka itu dicetak
oleh evaluator resmi setiap kali kalian menjalankan `tools/gate0.py` — **jadikan itu angka yang
dipantau setiap hari, bukan `macroF1`.**

Kesimpulan yang harus dipegang seluruh tim sampai 17 November:

> Skor kita datang dari **empat hal struktural** — deteksi dead-ball, imputasi bola, atribusi tim, dan
> segmentasi yang tidak memecah possession. Tidak satu pun dari empat itu adalah "model yang lebih
> canggih". Keempatnya bisa dikerjakan dengan fitur + aturan + threshold, dan masing-masing bisa
> diverifikasi sendiri-sendiri.

---

## 4. Job desk

Empat orang, empat seat, satu pemilik per output. Kolom terakhir itu yang dipakai di rapat harian —
kalau output-nya tidak ada, seat itu merah.

### Seat 1 — Domain, Aturan & PM · **Dyang** (`DyangPB`)

**Kenapa dia:** satu-satunya yang menonton LaLiga konsisten (terutama Barça) dan menulis soal bola
bertahun-tahun. Dan ini satu-satunya seat yang 80%-nya penilaian, bukan koding.

**Tugas:**
- Membedah 5 menit GT publik frame demi frame — pakai lembar kerja `docs/gt-public-transitions.md`.
- Menuliskan aturan `D` vs `H`/`A` dalam bentuk yang **bisa dikodekan** Billa.
- Pemilik kebijakan `X`: kapan sistem menyerah, kapan wajib menebak.
- Pemilik timeline, pemilik form submission, pemilik file final.
- Pemelihara `docs/decisions.md` — sumber kebenaran tunggal tim.

**Output yang bisa dicek:** `docs/possession-rules.md` · `docs/decisions.md` · file submission akhir

**Definisi selesai:** Billa bisa mengimplementasikan deteksi dead-ball **tanpa bertanya lagi** ke Dyang.

**Bahaya utama:** kamu satu-satunya orang yang paham bola di tim ini. Kamu **single point of failure**
untuk bagian yang tidak bisa digantikan keahlian teknis. Jawabannya bukan bekerja lebih banyak, tapi
**menuliskan pengetahuannya lebih cepat supaya ia berhenti tinggal di kepalamu.**

---

### Seat 2 — Data & Sinyal Bola · **Raissa** (`raisinmee`)

**Kenapa dia:** rekam jejak EDA, clustering, segmentation, dan dashboard — pekerjaan yang 80%-nya
sanitasi data dan pemeriksaan distribusi.

**Tugas:**
- Memuat ATD (EPTS XML + raw txt), Smart Tagging, dan homography. **Mengkanonikalisasi** semuanya ke satu
  tabel per frame.
- Menjaga alignment: `video_frame = id_frame − 1`, Smart Tagging `round(seconds × 25)`, homography
  `frame` = baris submission.
- Membangun fitur per frame (§7.2, §7.3).
- Pemilik diagnosa: distribusi label, panjang gap bola, peta serpihan.

**Output yang bisa dicek:** `src/deculgirl/features/` · tabel fitur per frame · laporan diagnosa

**Definisi selesai:** satu perintah menghasilkan `features.parquet` dengan tepat 199.319 baris, tanpa
`NaN` yang tak dijelaskan, dan Billa bisa memakainya tanpa menyentuh file mentah.

---

### Seat 3 — Model Sekuensial & Dead-Ball · **Billa** (`nabilland`)

**Kenapa dia:** satu-satunya di tim dengan rekam jejak *sequence labelling* (LSTM / Bi-LSTM / Bi-GRU) —
dan ini persis masalah sequence labelling: 199.319 frame berurutan yang saling bergantung.

**Tugas:**
- Model dead-ball terpisah (§7.1) — **ini lubang terbesar di baseline**, dan nilainya paling tinggi.
- Atribusi `H`/`A` untuk frame bola hidup (§7.3).
- Segmentasi anti-fragmentasi (§7.4) — dari probabilitas per frame jadi interval.
- Model sekuensial di Gate 2 (§7.6).
- **Penulis utama dokumen teknis** (deliverable #3) — satu-satunya yang sudah punya publikasi ilmiah.

**Output yang bisa dicek:** `src/deculgirl/model/` · file label mentah · draf dokumen teknis

**Definisi selesai:** perubahan konfigurasi apa pun bisa dijalankan ulang dan menghasilkan skor yang
berbeda dengan jelas — bukan hasil yang tidak bisa dijelaskan.

---

### Seat 4 — Metrik, Validasi & Reproducibility · **Yona** (`yonakatitin`)

**Kenapa dia:** satu-satunya dengan kode berbentuk produksi (FastAPI, RAG pipeline, AWS re/Start).

**Tugas:**
- Scorer resmi jalan lokal (§8) — **Gate 0, hari pertama**.
- Regression suite + bootstrap CI, supaya perbedaan 0,01 tidak dipercaya sebagai kemenangan.
- `run.py`: satu perintah yang mereproduksi file submission **identik**.
- Dependensi di-pin. Gate validasi jalan otomatis di setiap PR.
- Penjaga gerbang terakhir sebelum submit.

**Output yang bisa dicek:** `metrics/` · `run.py` · `.github/workflows/validate.yml` · `REPRODUCE.md`

**Definisi selesai:** Dyang bisa menghapus semua output, menjalankan satu perintah di laptopnya sendiri,
dan file yang dihasilkan identik byte-per-byte dengan yang tadi.

> **Catatan penting — Yona satu-satunya yang masih intern.** Seat 4 itu jalur kritis: kalau dia hilang
> tiga hari di minggu terakhir, tidak ada yang bisa menghasilkan ulang submission. Karena itu:
> mekanika pipeline dibangun berpasangan di Gate 0 lalu **dibekukan**, gate-nya **diotomasi** (robot,
> bukan orang), dan fungsi "apakah bedanya nyata?" pindah ke Raissa. Yona tetap pemilik metriknya;
> Raissa pemilik keraguannya.

---

## 5. Flow 25 hari — empat gate

Format gate, bukan kalender. **Setiap gate punya satu angka yang harus hijau sebelum lanjut.** Kalau
gate-nya merah, jangan naik — perbaiki dulu.

Hari ini **Sabtu, 24 Oktober 2026**. Deadline **Selasa, 17 November 2026**. Registrasi tutup
**Selasa, 10 November 2026**.

### 🔴 GATE 0 — Pipeline & fail-safe · Sab 24 – Sen 26 Okt (3 hari)

**Angka hijau:** `run.py` menghasilkan file 199.319 baris yang **lolos `validate_submission.py`**, dan
kita punya skor `spellF1` terukur di jendela publik.

**Angka kedua:** kita sudah **enrolled dan sudah pegang bundle data**.

Daftar kerja:
1. **Dyang: enroll + tanda tangan ToU.** Malam ini, bukan nanti. Kalau ada jeda antara mendaftar dan
   link download, jeda itu mulai berjalan sekarang.
2. Bikin repo `mtah-2027-deculgirl`, publik dari awal. Invite `raisinmee`, `nabilland`, `yonakatitin`
   sebagai collaborator **write**.
3. **Sudah disiapkan:** `tools/fetch_official.py` — ambil repo resmi di commit `f8f2629` ke
   `third_party/`. Kalian cuma perlu menjalankannya.
4. **Sudah disiapkan dan sudah diuji:** `tools/gate0.py` — **tidak butuh data pertandingan sama
   sekali.** Dia membuktikan scorer, validator, dan GT publik bekerja di mesin kalian.
5. **Sudah disambungkan:** versi pertama `submit.py` memakai **baseline resmi** — bukan rekaan kita,
   tapi kode MIT dari penyelenggara yang mereka sendiri sebut *"a starting point, not a constraint"*.
   Begitu data kalian turun, `python run.py` langsung menghasilkan submission berskor. **Itu
   fail-safe kalian, dan itu sebabnya langkah ini tidak boleh dilewati.** Setiap perbaikan
   ditambahkan sebagai varian; `main` selalu bisa menghasilkan submission yang valid.
6. Unpack data ke `data/` (**di drive D:, gitignored**). Konfirmasi jumlah baris tracking = 199.319.
   Kalau tidak sama, **jangan di-pad atau di-trim** — cari tahu kenapa bedanya.

> ### ⚠️ Kalau Gate 0 selesai, kalian sudah punya submission. Itu asuransi.
> Setelah ini, **tidak ada yang boleh menghapus file yang sudah valid.** Setiap perbaikan ditambahkan
> sebagai varian, dan `main` selalu bisa menghasilkan submission yang valid.

---

### 🟠 GATE 1 — Empat pilar struktural · Sel 27 Okt – Sen 2 Nov (7 hari)

**Angka hijau:** `spellF1` publik melewati baseline kita sendiri, dan `macroF1` kelas `D` naik jelas.

Semua seat bekerja paralel, tanpa saling menunggu. Detail teknis di §7.

| Seat | Deliverable gate ini |
|---|---|
| 1 (Dyang) | `docs/possession-rules.md` jadi, ditinjau Billa |
| 2 (Raissa) | `features.parquet` + laporan diagnosa gap bola |
| 3 (Billa) | Dead-ball classifier + segmentasi anti-fragmentasi jalan |
| 4 (Yona) | Regression suite + bootstrap CI; Gate 0 dibekukan |

**Aturan gate ini:** setiap pilar harus bisa **diverifikasi sendiri**. Kalau dead-ball detector
memperbaiki `macroF1` kelas `D` **tanpa** merusak `spellF1`, itu terbukti bekerja. Kalau skor naik tapi
kalian tidak tahu bagian mana yang menyebabkan — itu bukan hasil, itu kebetulan, dan tidak bisa ditulis
di dokumen teknis.

---

### 🟡 GATE 2 — Model sekuensial & tuning jujur · Sel 3 – Sen 9 Nov (7 hari)

**Angka hijau:** model sekuensial mengalahkan versi aturan **pada confidence interval yang tidak
tumpang tindih** (`--bootstrap 1000`). Kalau tumpang tindih, **pertahankan yang lebih sederhana** dan
berhenti di situ. Tidak ada rasa malu di situ — ada riset yang jujur.

**Peringatan yang paling mahal di seluruh proyek ini:** `EVALUATION.md` menunjukkan bahwa tuning di 5
menit publik **memilih baseline yang salah** — `smooth125` menang di publik (0,4242) tapi kalah di
pertandingan penuh (0,2242). Itu cuma satu hyperparameter pada baseline sepele. Jangan pernah memilih
versi berdasarkan jendela publik. Pakai dia untuk memverifikasi pipeline itu **benar**, tidak lebih.

Di gate ini juga: **10 November registrasi tutup.** Kalau ada proses enrollment yang belum beres,
selesaikan jauh sebelum tanggal ini.

---

### 🟢 GATE 3 — Reproducibility & dokumen · Sel 10 – Sel 17 Nov (8 hari)

**Angka hijau:** seseorang yang bukan pemilik Seat 4 bisa menjalankan `run.py` di laptop bersih dan
mendapatkan file **identik**, sambil membaca `REPRODUCE.md` saja.

| Tanggal | Kerjaan |
|---|---|
| 10 – 13 Nov | Dokumen teknis (§7.7) + `REPRODUCE.md` + bersihkan repo |
| **14 Nov** | **FREEZE.** Tidak ada perubahan kode setelah tanggal ini. |
| 15 Nov | Dry run submission: isi form lengkap dengan file & URL final. Cek file bisa dibuka. |
| 16 Nov | Buffer. Hanya untuk memperbaiki yang rusak. |
| **17 Nov** | **Submit.** |

> **Freeze itu bukan saran.** Mayoritas poin yang hilang di kompetisi seperti ini hilang di 72 jam
> terakhir, dan hilangnya bukan karena skor — tapi karena file yang tadinya valid jadi tidak valid,
> atau repo yang tadinya jalan jadi tidak jalan. `SUBMISSION.md`: file yang gagal validasi
> **"is skipped with a one-line reason and scores nothing."**

---

## 6. Cara mengelola proyek ini

### Ritual

| Kapan | Apa | Lama |
|---|---|---|
| Setiap hari, jam tetap | Sync harian: **apa yang hijau, apa yang merah, apa yang menghalangi** | 20 menit |
| Setiap Minggu | Review gate: apakah angka hijaunya tercapai? Lanjut atau perbaiki? | 45 menit |
| Kapan saja | Kalau macet > 2 jam → **post di channel**, jangan diam | — |

Aturan sync harian: **tidak ada laporan status panjang.** Tiga kalimat: hijau, merah, penghalang. Kalau
butuh lebih dari 20 menit, berarti masalahnya belum dirumuskan dan itu sendiri masalahnya.

### Repo

- **Tidak ada yang push langsung ke `main`.** Semua lewat branch + PR, walau dua baris.
  Nama branch: `dyang/rules`, `raissa/features`, `billa/model`, `yona/metrics`.
- **Semua PR lewat gate otomatis** (`.github/workflows/validate.yml`). Kalau gate merah, jangan merge.
- **`docs/decisions.md` adalah sumber kebenaran tunggal.** Di tim remote, keputusan yang cuma diucapkan
  di chat akan hilang dalam dua hari dan diulang lagi minggu depan. Satu keputusan = satu baris.
- **Commit kecil dan sering.** Riwayat commit kalian adalah bukti pekerjaan yang dilihat siapa pun yang
  membuka repo — termasuk juri Innovation Challenge nanti.

### Kenapa remote bukan masalah

Seluruh tugas ini berbentuk **artifact**: CSV, repo, dokumen. Tidak ada satu pun bagian yang butuh
kalian di ruangan yang sama. Yang biasanya rusak di tim remote bukan hasil kerjanya, tapi tiga hal ini —
dan ketiganya sudah dicegah di atas: tidak ada jejak pekerjaan (→ PR), keputusan hilang (→
`decisions.md`), dan orang macet diam-diam (→ aturan 2 jam).

---

## 7. Strategi teknis

Urutan pengerjaan yang direkomendasikan: **aturan & fitur dulu, model belakangan.** Alasannya bukan
konservatif — alasannya karena **setiap pilar bisa diverifikasi sendiri-sendiri**, dan itu satu-satunya
cara kalian punya sesuatu yang benar-benar bisa ditulis di dokumen teknis.

### 7.1 Deteksi dead ball — pilar bernilai tertinggi

Baseline tidak punya logika dead ball sama sekali. Docstring `starter/baseline.py` mengakuinya sendiri:

> *"It has no notion of a dead ball beyond 'the tracking lost the ball', which is why its D class is weak."*

Satu-satunya sinyal `D` di baseline: bola tidak ada di frame itu. Itu berarti satu-satunya `D` yang
benar adalah ketika bola kebetulan sedang tidak terdeteksi **dan** bola memang mati.

**Dan smoothing memperburuk kelas `D`, bukan memperbaikinya.** F1 kelas `D` per varian, dari
menjalankan scorer resmi pada jendela publik:

| Versi | F1 `D` | presisi `D` | recall `D` |
|---|---|---|---|
| `baseline_raw` | **0,4197** | 0,5582 | 0,3363 |
| `baseline_smooth25` | 0,3857 | 0,6106 | 0,2818 |
| `baseline_smooth50` | 0,3225 | 0,6569 | 0,2138 |
| `baseline_smooth125` | 0,1464 | **1,0000** | **0,0790** |

Bacanya begini: `smooth125` **tidak pernah salah** ketika bilang `D` — presisinya sempurna — tapi ia
cuma menangkap **7,9%** frame bola mati yang sesungguhnya. Dan keempat varian lebih buruk dari `raw`
di kelas ini. Artinya detektor dead-ball yang lebih baik **bukan penyempurnaan kecil di atas
baseline** — itu wilayah yang sama sekali belum digarap, dan setiap perbaikan di situ tidak diambil
dari siapa pun.

Fitur yang tersedia, dan belum dipakai siapa pun:

| Fitur | Kenapa relevan |
|---|---|
| Panjang gap bola beruntun | Bola mati sering muncul sebagai gap panjang, bukan pendek |
| Kecepatan bola | Ada di file mentah sebagai angka **ketiga** setiap grup (`x,y,speed`) — baseline cuma membaca dua yang pertama |
| Pergerakan pemain | Pemain berjalan (bukan berlari), atau berhenti, saat bola mati |
| Sebaran & kepadatan pemain | Posisi pemain saat restart (kick-off, throw-in) punya bentuk yang khas |
| Smart Tagging | **Setiap set piece adalah restart** — dan restart mengakhiri bentang bola mati. Setiap fase punya tag tim juga |
| Jeda antar babak, sebelum kick-off | Babak 2 dinilai dari frame 110.808, kick-off 113.742 — 2.934 frame yang semuanya `D` |

> **Catatan kepatuhan untuk poin terakhir.** Fakta 2.934 frame itu **diterbitkan di `FAQ.md` resmi**, jadi
> memakainya bukan pelanggaran. Tapi `RULES.md` melarang *"rules and constants tied to specific frames of
> the game"* yang kalian **turunkan sendiri dari pengamatan**. Jadi bentuk yang aman: bangun detektor
> dead-ball yang **umum**, lalu pakai fakta FAQ itu sebagai **pemeriksa** — apakah detektormu memang
> menandai `D` di sana? Kalau kalian memutuskan untuk meng-hardcode, **cantumkan dan sumbernya** di
> dokumen teknis. Kalau ada keraguan, tanya penyelenggara lewat issue — `FAQ.md` secara eksplisit
> mengundang itu: *"If a rule is unclear or your approach sits near a line, ask before you build on it."*

### 7.2 Imputasi bola

Bola hilang di **41% frame yang dinilai** — dan `DATA.md` bilang hilangnya justru *"disproportionately on
the frames that matter"*: kotak penuh, duel udara, tackle. Tidak ada indikator kepercayaan atau
visibilitas sama sekali di data. `DATA.md`-nya sendiri memberi instruksi: *"design for it on day one."*

Pendekatan bertingkat, dari murah ke mahal:

1. **Gap pendek** (< ~0,5 detik / 12 frame): interpolasi linear atau Kalman. Bola bergerak kontinu;
   mengisi gap pendek hampir selalu benar.
2. **Gap panjang**: **jangan diimputasi.** Kembalikan sebagai ketidakpastian, dan biarkan sistem
   memakainya sebagai sinyal — gap panjang itu sendiri informatif (lihat §7.1).
3. **Validasi geometris:** proyeksikan posisi bola hasil imputasi ke piksel lewat homography dan periksa
   apakah hasilnya masuk akal. Ini pemakaian homography yang paling langsung berguna, dan homography
   feed taktis **100% valid**.
4. **Satu interrupt + satu tebakan buruk lebih mahal dari satu gap.** Ingat: `X` di tengah possession
   itu **gratis** (§7.5). Jadi tidak ada alasan memaksakan posisi bola yang tidak kalian percaya.

**Jangan pakai video.** GTX 1650 Ti-mu punya 4 GB VRAM dan itu cukup untuk inferensi model kecil, tapi
`RULES.md` melarang hand annotation *"in any amount and for any purpose"* — termasuk untuk melatih model.
Artinya kalian harus bergantung pada model pra-latih yang kebetulan bisa menemukan bola, lalu
memvalidasinya tanpa ground truth. Itu eksperimen, bukan rencana — tidak ada satu pun bagiannya yang
bisa kalian buktikan benar sebelum 17 November.

### 7.3 Atribusi tim

Baseline: pemain tracked terdekat ke bola, jarak Euclidean kuadrat dalam satuan meter. Itu saja.

Fitur pengganti, panjang tapi murah semuanya:

- Jarak bola ke **2–3 pemain terdekat per tim**, lalu bandingkan — bukan hanya yang paling dekat global.
- **Arah gerak:** apakah pemain bergerak **menuju** bola (dot product kecepatan pemain dengan vektor
  pemain→bola). Pemain yang mendekati bola jauh lebih mungkin menguasainya daripada yang kebetulan dekat.
- **Konteks sebelum gap:** siapa yang terakhir mengontrol sebelum bola menghilang.
- **Prior dari Smart Tagging:** setiap fase punya tag tim. Dua peringatan dari dokumentasinya:
  `Team = N/A` pada **setiap throw-in**, dan *"the intervals are phases, not possessions"*.
- **Persistensi adalah fitur, bukan bug:** possession adalah *state* yang bertahan, bukan keputusan per
  frame. Frame ini `H` sebagian besar karena frame sebelumnya `H`.

### 7.4 Segmentasi anti-fragmentasi

Dari probabilitas per frame ke interval. Ini pilar yang langsung menyentuh metriknya.

- **Minimum spell.** Scorer tidak punya minimum panjang possession — jadi **kalian** yang harus punya.
  Gabungkan serpihan pendek ke tetangga yang dominan, atau buang. Setiap serpihan yang dibuang adalah FP
  yang hilang.
- **HMM / Viterbi** dengan matriks transisi yang membuat perpindahan `H → A` mahal. Ini bentuk alami dari
  "possession itu state, bukan keputusan independen".
- **Median filter** adalah versi termurah dari ide yang sama — dan baseline sudah membuktikan idenya
  bekerja: cuma dengan memperlebar window, `spellF1` bergerak 5×.
- **Perhatikan jumlah possession kalian.** `validate_submission.py` mencetaknya. Baseline `raw`
  melaporkan **131 possession** pada 5 menit, sementara kebenarannya **17**. Itu rasio fragmentasi 7,7×,
  dan itu alasan `spellF1`-nya 0,0378.

### 7.5 Kebijakan `X` — tool paling kuat yang kita punya

Scorer mengganti setiap `X` dengan label non-`X` terakhir **di babak yang sama** (back-fill di awal
babak), **sebelum** possession disusun. Jadi:

```
H H H X X X H H H   →   H H H H H H H H H   →   SATU possession
```

**`X` bukan tombol menyerah. `X` adalah tombol "sama seperti sebelumnya".**

Terjemahan operasionalnya:

| Situasi | Tindakan | Alasan |
|---|---|---|
| Bola hilang **di tengah** possession | Tulis `X` | Gratis. Possession tetap utuh. Lebih aman dari tebakan yang bisa memecahnya |
| Di titik **hand-over** | **Wajib menebak** | `X` akan menarik label lama ke wilayah tim lawan. Ini mahal sekali |
| Di luar jam pertandingan | `X` | Tidak dinilai sama sekali |

Dan soal biayanya: `macroF1` menghitung `X` sebagai salah, tapi `macroF1` hanya **tie-break**.
`spellF1` — yang menentukan ranking — tidak pernah melihatnya. Jadi secara praktis **`X` itu murah**,
dan tidak ada alasan untuk malu memakainya.

### 7.6 Model sekuensial (Gate 2, bukan Gate 1)

Baru setelah empat pilar berdiri dan terbukti. Bentuk yang paling masuk akal: **CRF atau GRU/Bi-GRU
atas fitur per frame**, dengan pilar 1–4 sebagai fitur input, bukan sebagai pengganti. Billa sudah
mengerjakan bentuk ini sebelumnya.

Aturan gate: kalau tidak mengalahkan versi aturan pada CI yang tidak tumpang tindih, **pertahankan versi
aturan.** Model sekuensial itu bonus, bukan jalan keluar.

### 7.7 Dokumen teknis (deliverable #3)

`SUBMISSION.md` meminta *"a few pages"*. Struktur yang diminta, dan sebaiknya diikuti persis:

1. **Pendekatan dan alasannya** — kenapa begitu, bukan cuma apa.
2. **Aset mana yang dipakai dan bagaimana** — termasuk **yang sudah dicoba lalu dibuang**. Bagian ini
   yang paling sering dilewatkan orang, dan justru yang paling menunjukkan kalian serius.
3. **Data latih** — setiap dataset berlabel, sumbernya, siapa yang melabeli, berapa banyak. Kalau tidak
   ada, tulis "tidak ada" — itu jawaban yang sah.
4. **Aturan possession yang diimplementasikan** — dari `docs/possession-rules.md`.
5. **Keterbatasan** — jujur. Ini menaikkan kredibilitas, bukan menurunkannya.
6. **Cara reproduksi** — satu perintah.

Lampirkan juga: fakta mana dari dokumentasi resmi yang kalian pakai (§7.1), dan keputusan apa saja yang
kalibrasi/manual — kalau ada.

---

## 8. Cara mengukur tanpa menipu diri sendiri

**Scorer yang kalian jalankan lokal adalah scorer yang menentukan kompetisi.** `EVALUATION.md`:
*"Organisers run this exact script against the private full-match ground truth; the published board is
its output. There is no stricter version held back."* Ini hadiah besar — manfaatkan sampai habis.

```bash
python tools/gate0.py              # ambil repo resmi, jalankan evaluator resmi
python evaluation/validate_submission.py <file>   # SEBELUM setiap submission
```

Aturan pengukuran:

- **Noise band `spellF1` di pertandingan penuh ≈ 0,04.** Di bawah itu bukan perbaikan.
  Noise band `macroF1` ≈ 0,01.
- **Selalu jalankan `--bootstrap 1000`** sebelum percaya bahwa satu versi lebih baik dari versi lain.
  Intervalnya biasanya tumpang tindih.
- **Jendela publik 5 menit bukan leaderboard.** 17 possession, dan satu possession yang meleset ≈ 6 poin.
  `EVALUATION.md` membuktikan tuning di situ memilih baseline yang salah. Pakai untuk memverifikasi
  **kebenaran pipeline**, bukan untuk memilih versi.
- **Reproducibility itu deterministik.** Kalau skor berubah antar run, ada bug — bukan keberuntungan.
- **`reports/<nama>_transitions.csv`** dari evaluator resmi mendaftar setiap transisi
  `matched` / `missed` / `spurious` per video frame. Itu alat debug terbaik yang kalian punya, dan tidak
  banyak yang tahu dia ada.

### Kolom papan skor yang wajib kalian baca

`tools/gate0.py` mencetak papan resminya. Selain `spellF1` / `macroF1`, ada empat kolom yang jauh
lebih berguna untuk kerja harian:

| Kolom | Artinya | Yang kalian cari |
|---|---|---|
| **`frag`** | segmen prediksi ÷ segmen kebenaran | **Mendekati 1,0 atau sedikit di bawah.** Ini kolom terpenting di seluruh papan |
| **`poss`** | jumlah possession yang kalian laporkan | Kebenarannya **17** di jendela ini. 26 sudah mulai melenceng; 131 itu alarm |
| **`dur`** | rata-rata durasi possession | Kebenarannya **14,2 s**. Terlalu pendek = kalian memecah possession |
| **`shareE`** | selisih porsi penguasaan home dibanding kebenaran | Kebenarannya 0,5727 — Barcelona menguasai 57% frame hidup di jendela ini |
| **`lat_f`** | latency rata-rata, dalam frame | Di bawah 25 frame masih murah (§3 poin 3); di atas itu mahal |

Dan di laporan per-submission (yang ditulis evaluator sebagai file `.txt`) ada yang lebih tajam lagi:
matriks konfusi 4×4, presisi/recall/F1 per kelas, `alive/dead F1`, akurasi tim, dan — ini yang paling
berhubungan dengan §7.5 — **berapa frame `X` kalian jatuh pada ground truth yang dinilai.** Itu ukuran
langsung dari kebijakan abstain kalian. Evaluator juga menulis `scoreboard.csv`.

---

## 9. Garis merah

Ini daftar hal yang bisa membuat kerja tiga minggu bernilai nol. Bukan soal etika — soal **apa yang
dihitung**.

| ❌ Dilarang | Detail yang mudah terlewat |
|---|---|
| **Hand label pada pertandingan ini** | *"in any amount and for any purpose"* — untuk submission, **untuk melatih model, maupun untuk memvalidasi**. Termasuk memperbaiki output algoritma secara manual: *frame by frame, segment by segment, atau hanya di transisi* |
| **Data buatan manusia tentang pertandingan ini** | Event data (Opta, StatsBomb, Wyscout, LaLiga, siapa pun), corrected tracking, data possession, atau anotasi apa pun — dari sumber mana pun |
| ⚠️ **Ingatan kalian sendiri tentang pertandingan ini** | Ini turunannya, dan ini jebakan spesifik untuk **Dyang**. Kalau ada yang ingat skor akhir, menit gol, atau kejadian VAR, itu **pengetahuan manusia tentang pertandingan ini**. Memakainya sebagai fitur, label, atau konstanta adalah pelanggaran. Yang boleh: memahami **arti** sepak bola. Yang tidak boleh: mengingat **pertandingan ini** |
| **Upload data ke LLM cloud** | ToU melarang mengunggah video, dataset, atau **ekstraknya** ke LLM pihak ketiga berbasis cloud. Pakai AI untuk menulis kode tetap boleh — yang dilarang mengirim isi datanya |
| **Menyebarkan data** | Jangan commit `data/` ke repo publik. Jangan publikasikan turunan yang bisa merekonstruksi data |
| **Repo yang tidak bisa mereproduksi file** | *"A private in-house model or an unavailable internal dataset is the one thing this rules out"* |
| **Menuning di 5 menit publik** | Bukan saran — aturan. Dan terbukti merugikan (§8) |

**Yang justru diizinkan**, dan mungkin belum kalian sadari:

- Memperbaiki atau **mengganti** tracking yang diberikan — asal **oleh algoritma**, bukan tangan.
- Memakai model pra-latih apa pun, LLM apa pun, framework apa pun.
- Memakai data eksternal — **asal tentang pertandingan lain**.
- Hand label pada pertandingan **lain** — sebanyak apa pun.
- Memakai `Smart Tagging`. FAQ-nya menjawab curiga ini langsung: *"Use it — that is why it is there."*
- Model milik sendiri: detektor, pelacak, pengenal event. *"If it produces a better answer, it is a better answer."*

---

## 10. Sepuluh hal yang menentukan — urut dari yang paling sering diabaikan

1. **Pemenangnya bukan yang modelnya paling canggih.** Empat baseline di repo itu algoritma **yang sama**
   dengan window berbeda: `macroF1` bergerak 0,04, `spellF1` bergerak 11×.
2. **`X` adalah tombol "ulangi jawaban sebelumnya".** Diam di tengah possession itu gratis; diam di titik
   hand-over itu bencana. Satu kebijakan, dua arah berlawanan.
3. **Scorer tidak punya minimum panjang possession.** Serpihan kecil bukan setengah benar — dia FP murni,
   dan memecah satu possession jadi dua menghasilkan FP + FN sekaligus.
4. **Kelas `D` adalah lubang terbesar.** Baseline mengakuinya sendiri. Smart Tagging memberi tag tim dan
   set-piece gratis, dan **tidak ada yang memakainya**.
5. **Bola hilang di 41% frame yang dinilai, dan hilangnya tepat di frame yang penting.** Ini bukan
   gangguan yang harus ditoleransi — ini soalnya.
6. **5 menit publik tidak bisa meranking siapa pun.** `smooth125` menang di publik, kalah di pertandingan
   penuh. Dan itu cuma satu hyperparameter pada baseline sepele.
7. **Kebanyakan poin hilang di meja administrasi.** File yang gagal validasi dinilai **nol**, dan repo
   yang tidak bisa mereproduksi file adalah syarat gugur. `validate_submission.py` berjalan dua detik.
8. **Di luar dua babak, label kalian tidak berpengaruh apa pun.** `macroF1` hanya menghitung frame yang
   dinilai, `spellF1` hanya menyusun possession di dalam bentang yang dinilai. Jangan buang waktu di jeda.
9. **2.934 frame pertama babak 2 semuanya `D`**, dan itu diterbitkan resmi di `FAQ.md`. Pakai sebagai
   pemeriksa detektor dead-ball kalian, dan cantumkan sumbernya.
10. **Semua yang kalian hasilkan akan dibaca.** Dua dari tiga deliverable bukan angka — repo dan dokumen.
    Dan keduanya ikut menentukan nasib kalian di Innovation Challenge, di mana penilaiannya berubah
    total: ada juri, ada presentasi, ada desain.

---

## 11. Checklist submission

Dijalankan **15 November**, tidak boleh lebih lambat.

**File CSV**
- [ ] `DeculGirl.csv` — tepat **199.319** baris data, header `frame,label`
- [ ] Kolom `frame` = 0…199318, berurutan, tidak ada duplikat
- [ ] Tidak ada satu pun sel kosong — tulis `X` untuk abstain
- [ ] `python evaluation/validate_submission.py DeculGirl.csv` → **`Valid.`**
- [ ] Jumlah possession yang dilaporkan masuk akal (bandingkan dengan 17 pada 5 menit; 131 itu alarm)
- [ ] Kolom `frag` mendekati 1,0 atau sedikit di bawah — bukan 2 ke atas
- [ ] Baris `abstained ... frames of X on graded ground truth` di laporan sesuai dengan kebijakan `X`
      kalian, bukan 0% dan bukan 100%

**Repo publik**
- [ ] `mtah-2027-deculgirl` **public**, URL bisa dibuka di jendela incognito
- [ ] `data/` **tidak ada** di repo
- [ ] `run.py` mereproduksi file yang identik, diuji di laptop orang lain
- [ ] Dependensi di-pin (`requirements.txt` dengan versi)
- [ ] `README.md` menjelaskan cara menjalankan, dalam bahasa yang bisa diikuti orang luar

**Dokumen teknis**
- [ ] `DeculGirl.pdf` atau `.md`, beberapa halaman, struktur §7.7
- [ ] Menyebut aset yang dicoba **lalu dibuang**, bukan hanya yang dipakai
- [ ] Menyebut tidak ada / ada data latih, dengan sumbernya
- [ ] Mencantumkan fakta resmi yang dipakai sebagai kalibrasi

**Form**
- [ ] Satu response per tim. **Response terakhir sebelum deadline yang dinilai.**
- [ ] Nama tim: `DeculGirl` · file: `DeculGirl.csv`, `DeculGirl.pdf`
- [ ] Butuh akun Google · tidak ada leaderboard langsung dan tidak ada feedback
- [ ] Screenshot konfirmasi submission, simpan di tempat yang bisa diakses berempat

---

## 12. Setelah 17 November

Hasil diumumkan **sebelum 26 November**. Kalau lolos **top 20**, kalian masuk Innovation Challenge
(**26 Nov – 14 Jan**, online): dataset **10 pertandingan profesional**, tantangan desain terbuka, dan
mentoring teknis. Kalau lolos **top 5** di situ, Final Pitch **2 Maret 2027** di Talent Arena Barcelona —
travel dan akomodasi ditanggung, plus jersey resmi Barça dan pengalaman eksklusif. Tidak ada hadiah uang.

Dan kalau tidak lolos: kalian tetap punya repo publik berisi analisis satu pertandingan LaLiga sungguhan
dengan pipeline yang reproducible, dokumen teknis yang bisa dibaca orang, dan empat orang yang sudah
terbukti bisa mengirim hasil kerja bareng secara remote dalam tiga minggu. Itu bukan hasil yang kecil.

**Penilaiannya berubah total di fase berikutnya.** Phase 1 murni angka tanpa juri — tidak ada nilai untuk
ide bagus. Innovation Challenge justru menilai desain, interpretasi, dan cara bercerita. Jadi selama 25
hari ini: **skornya dulu, ceritanya nanti.** Tapi mulai sekarang, catat setiap keputusan di
`docs/decisions.md` — bahan cerita itu tidak bisa dirakit ulang di bulan Desember.
