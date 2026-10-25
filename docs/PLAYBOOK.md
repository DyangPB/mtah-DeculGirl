# PLAYBOOK — DeculGirl

**More than a Hack 2027 · Phase 1: Ball Possession**
Metrica Sports × FC Barcelona (Barça Innovation Hub) × Mobile World Capital Barcelona

Ditulis 24 Oktober 2026 · Batas pengumpulan **17 November 2026**

---

## 0. Cara memakai dokumen ini

**Kalau hanya punya 5 menit, baca [`SUMMARY.md`](SUMMARY.md), bukan dokumen ini.** Dokumen ini adalah
versi lengkapnya, tempat semua angka, alasan, dan keputusan dicatat.

Dokumen ini bukan dokumen penyemangat. Ini dokumen kerja: setiap bagiannya punya akibat yang bisa
diperiksa. Cara memakainya:

- **Seat 1 (Dyang)** memakai §4, §5, §7, dan §9, serta memelihara `docs/decisions.md`.
- **Seat 2 (Raissa)** memakai §7.2 dan §7.3 sebagai daftar kerja fitur.
- **Seat 3 (Billa)** memakai §7.1, §7.4, §7.5, dan §7.6.
- **Seat 4 (Yona)** memakai §6 dan §8, karena dia penjaga alat ukurnya.
- **Semua orang** wajib membaca §1, §2, dan §9.

Kalau isi dokumen ini bertentangan dengan repo resmi penyelenggara, **yang benar adalah repo resmi**.
Semua angka di sini diambil dari repo itu pada 24 Oktober 2026, dari commit `f8f2629`.

---

## 1. Apa yang sebenarnya kita kerjakan

Kita mengerjakan satu pertandingan LaLiga lengkap: **FC Barcelona vs Athletic Club**, LaLiga EA Sports
2024-25 matchday 2. Penyelenggara memberi kita rekaman dari dua kamera, pelacakan otomatis posisi setiap
pemain dan bola, penandaan taktik otomatis (Smart Tagging), serta pemetaan kamera ke lapangan
(homography).

Tugasnya bisa dirangkum dalam satu kalimat:

> **Untuk setiap frame pertandingan, tentukan tim mana yang sedang menguasai bola.**

Hasilnya satu file CSV: `frame,label`, **199.319 baris**, dengan frame `0` sampai `199318` dan label
`H` / `A` / `D` / `X`.

| Label | Artinya |
|---|---|
| `H` | Barcelona (home) menguasai bola, dan bola sedang hidup |
| `A` | Athletic (away) menguasai bola, dan bola sedang hidup |
| `D` | Bola mati, yaitu bola tidak sedang dalam permainan |
| `X` | Sistem tidak menjawab |

**Bagian ini paling sering disalahpahami:** tugas ini **bukan** tantangan computer vision, **bukan**
pelacakan banyak objek (multi-object tracking), dan **bukan** rekonstruksi keadaan permainan. Data
pelacakan, penandaan, dan pemetaan kamera sudah disediakan, jadi kita tidak perlu membangun deteksi,
pengenalan ulang pemain, atau kalibrasi kamera dari nol. Yang dinilai hanya satu hal: apa yang
ditunjukkan oleh posisi 22 pemain dan satu bola tentang siapa yang menguasai bola.

Yang lebih penting lagi, `CHALLENGE.md` menyatakan:

> *"The ground truth is derived from corrected tracking data — not from a human watching video, and not
> from event data. The derivation is mechanical: a frame is `D` where the corrected tracking marks the
> ball dead, and otherwise takes the team the tracking names as owning it. Nothing is smoothed,
> interpolated or hand-adjusted afterwards."*

Artinya: **ground truth (jawaban benar) bukan penilaian manusia tentang sepak bola.** Ground truth
adalah keluaran sistem pelacakan yang sudah dikoreksi. Jadi yang kalian kejar bukan "kebenaran dalam
sepak bola", melainkan **menebak apa yang akan dikatakan oleh data pelacakan terkoreksi itu**. Satu-satunya
jendela untuk memahami cara kerjanya adalah **5 menit ground truth publik** yang ada di repo.

---

## 2. Peta medan: angka-angka yang menentukan

| | |
|---|---|
| FPS (frame per detik) | 25 |
| Total frame video | 199.319 (0–199318) |
| **Frame yang dinilai** | **158.857** |
| Babak 1 yang dinilai | frame 11.185 – 90.651 (79.467 frame) |
| Babak 2 yang dinilai | frame 110.808 – 190.197 (79.390 frame) |
| Kick-off babak 2 | frame **113.742**, jadi 2.934 frame pertama babak 2 ikut dinilai dan **semuanya `D`** |
| Bola terdeteksi | 56,9% dari seluruh frame (113.488 / 199.319) · 59,3% dari frame yang dinilai (94.214 / 158.857) |
| **Bola tidak terdeteksi** | **41% dari frame yang dinilai**, 43% dari seluruh frame |
| Track slot | 46 (feed taktis) · 51 (broadcast) |
| Catatan tracker broadcast | 164.488 (timeline-nya sendiri, tidak sama dengan nomor frame feed taktis) |
| Smart Tagging | 638 fase |
| Homography yang valid | taktis 100% · broadcast 65,8% |
| Ukuran lapangan | 105,3 × 68,0 m (menurut `games.py`; metadata menulis 105,0 × 68,0) |
| Selisih nomor frame (frame offset) | `{1: 1702057, 2: 1702058}`, berbeda satu frame antar babak |
| `video_frame` | `= id_frame − 1` (data tracking mulai dari 1, submission mulai dari 0) |

**5 menit ground truth publik** (satu-satunya ground truth yang kita punya):

| | |
|---|---|
| Rentang | frame 11.185 – 18.684 |
| Frame yang dinilai | 7.500 |
| Possession | **17** · 21 segmen · rata-rata 14,2 detik |
| Komposisi | `H` 3.454 · `A` 2.577 · `D` 1.469 |

**Batas minimum yang harus dilewati** adalah `baseline_smooth50`, diukur pada pertandingan penuh:

| Baseline | macroF1 | spellF1 |
|---|---|---|
| `baseline_raw` | 0,6532 | 0,0486 |
| `baseline_smooth25` | **0,6752** | 0,1996 |
| `baseline_smooth50` | 0,6724 | **0,2433** ← batas minimum |
| `baseline_smooth125` | 0,6356 | 0,2242 |

Perhatikan tabel itu sekali lagi. Keempat baris itu adalah **algoritma yang sama, dijalankan empat
kali**: cari pemain yang terdekat ke bola, lalu ambil suara terbanyak (voting mayoritas) dalam sebuah
window. Satu-satunya yang berubah adalah lebar window. Namun `macroF1` hanya bergeser **0,04**, sedangkan
`spellF1` berubah **lima kali lipat**.

Itu bukan kebetulan. Itulah inti dari seluruh kompetisi ini.

---

## 3. Kenapa kita bisa menang, dan kenapa model bukan jawabannya

`spellF1` mengukur **seberapa terpecah-pecah** possession kita, bukan ketepatan tiap frame. Setiap
possession (rentang `H` atau `A` yang tidak terputus) diperlakukan sebagai satu objek. Possession itu
dipasangkan satu lawan satu dengan possession asli lewat **temporal IoU** (ukuran tumpang tindih
waktu), lalu F1-nya dirata-rata pada ambang 0,3 / 0,4 / 0,5 / 0,6 / 0,7.

Empat akibatnya yang menentukan strategi kita:

1. **Potongan kecil bukan "setengah benar". Potongan kecil itu salah sepenuhnya.** Scorer **tidak punya
   batas minimum panjang possession**, jadi satu frame pun dihitung sebagai satu possession utuh. Yang
   dihitung `fp` (positif palsu) bukan hanya possession hantu. Possession kita yang beririsan dengan
   possession asli tetapi IoU-nya di bawah ambang **juga** dihitung `fp`. Jadi memecah satu possession
   asli menjadi dua menghasilkan **1 `fp` dan 1 `fn` sekaligus**. "Jangan memecah possession" adalah
   hitungan matematika, bukan sekadar saran.
2. **Satu kesalahan bisa menggeser skor 6 poin.** Di jendela publik, satu possession yang meleset kira-kira
   mengurangi 6 poin `spellF1`. Pengaruhnya besar untuk setiap kesalahan.
3. **Terlambat 1 frame tidak apa-apa.** Terlambat 1 detik hanya menurunkan skor ke 0,6539. Artinya,
   **ketepatan di ujung batas tidak penting, tetapi memotong di tengah possession itu fatal.**
4. **Label yang sama untuk semua frame bernilai tepat 0.** Tidak ada jalan pintas yang aman.

**Buktinya** datang dari menjalankan scorer resmi pada 5 menit publik. Kolom `frag` adalah perbandingan
antara jumlah segmen prediksi dan 21 segmen yang benar:

| Versi baseline | `frag` | `spellF1` | possession yang dilaporkan (GT: 17) |
|---|---|---|---|
| `baseline_smooth125` | 0,81 | **0,4242** | 16 (−1) |
| `baseline_smooth50` | 1,43 | 0,3256 | 26 (+9) |
| `baseline_smooth25` | 1,90 | 0,2868 | 36 (+19) |
| `baseline_raw` | 6,52 | 0,0378 | 131 (+114) |

Kolom `frag` hampir bisa dipakai langsung untuk memperkirakan `spellF1`, dan hubungannya konsisten:
makin kecil `frag`, makin besar `spellF1`. Angka itu dicetak oleh evaluator resmi setiap kali kalian
menjalankan `tools/gate0.py`. **Pantau angka itu setiap hari, bukan `macroF1`.**

Kesimpulan yang harus dipegang seluruh tim sampai 17 November:

> Skor kita berasal dari **empat hal struktural**: deteksi bola mati, pengisian posisi bola yang hilang
> (imputasi), penentuan tim yang menguasai bola, dan penyusunan possession tanpa memecahnya. Tidak ada
> satu pun yang berupa "model yang lebih canggih". Keempatnya bisa dikerjakan dengan fitur, aturan, dan
> ambang batas, dan masing-masing bisa diuji sendiri-sendiri.

---

## 4. Pembagian tugas

Ada empat orang, empat seat, dan satu penanggung jawab untuk setiap hasil kerja. Kolom terakhir di
tabel ringkasan dipakai dalam rapat harian: kalau hasilnya belum ada, seat itu dianggap merah.

> **Semua seat di bawah ini masih sementara.** Isinya usulan yang dicocokkan dengan pengalaman masing-masing
> orang, bukan keputusan final. Rapat pertama yang mengunci pembagiannya. Setelah Gate 1 dimulai,
> mengubah pembagian ini menjadi mahal.
>
> **Peran PM sengaja dikosongkan** (lihat §4.5). Seat lainnya tetap harus ada namanya.
>
> **Seat 1 dan Seat 2 bisa ditukar.** Profil Dyang dan Raissa hampir sama: keduanya mengikuti Startup
> Campus Data Science Batch 5, keduanya punya pengalaman EDA, clustering, segmentation, dan dashboard,
> **dan keduanya sama-sama paham sepak bola.** Jadi pembagiannya sebaiknya ditentukan oleh **preferensi**,
> bukan kemampuan. Yang **tidak bisa** ditukar adalah Seat 3 (Billa satu-satunya yang punya pengalaman
> *sequence labelling*, yaitu memberi label pada data berurutan) dan Seat 4 (Yona satu-satunya yang
> pernah menulis kode berstandar produksi).

### Seat 1 — Domain, Aturan, dan Eksperimen · **Dyang** (`DyangPB`)

**Kenapa dia:** menonton LaLiga secara rutin (terutama Barça) dan menulis tentang sepak bola.

**Tugas:**

*Fase 1 — domain (3–4 hari pertama, pekerjaan paling depan):*
- Membedah 5 menit GT publik frame demi frame, memakai lembar kerja `docs/gt-public-transitions.md`.
  Pekerjaan ini dibagi dengan Raissa, yang juga paham sepak bola.
- Menuliskan aturan `D` dan `H`/`A` dalam bentuk yang bisa langsung diubah menjadi kode.

*Fase 2 — teknis (sisa waktu, berjalan terus):*
- **Menulis kode fitur bola mati (dead ball)** di `src/deculgirl/features/`. Aturan yang ditulis Dyang di
  `possession-rules.md` langsung menjadi fungsi di situ, dan **Dyang sendiri yang menuliskannya**, bukan
  Billa. Ini cara paling langsung untuk mengubah cara berpikir Dyang menjadi kode, dan tidak ada orang
  lain yang bisa menuliskannya lebih tepat. Billa membangun model **di atas** fitur itu, bukan
  menggantikannya.
- **Alat diagnosa dan harness eksperimen**, yaitu `metrics/diagnose.py` dan `metrics/compare.py`. Seluruh
  tim memakainya untuk melihat letak kesalahan (§8), dan Dyang yang menentukan bentuknya.
- **Menjalankan eksperimen.** Setiap perubahan yang bisa diukur dijalankan Dyang dan dicatat di
  `docs/experiments.md` lengkap dengan putusannya. Eksperimen yang gagal juga dicatat, bahkan **terutama**
  yang gagal, karena catatan itulah isi bagian *"tried and dropped"* (yang dicoba lalu dibuang) yang
  diwajibkan di dokumen teknis (§7.7).
- Pemilik kebijakan `X`: kapan sistem boleh tidak menjawab, dan kapan wajib menebak.

**Hasil yang bisa diperiksa:** `docs/possession-rules.md` · fitur bola mati di `src/deculgirl/features/` ·
`metrics/diagnose.py` · `docs/experiments.md`

**Definisi selesai:** Billa bisa membangun model bola mati **tanpa bertanya lagi** ke Dyang, karena
fiturnya sudah ada dan sudah didokumentasikan.
**Definisi selesai (untuk tugas eksperimen):** setiap perubahan yang masuk `main` punya catatan di
`docs/experiments.md`, lengkap dengan angka dan putusan ✅/❌/⚠️, bukan sekadar "rasanya lebih baik".

**Catatan risiko — direvisi 24 Oktober.** Rencana awal menganggap Dyang satu-satunya orang di tim yang
paham sepak bola, sehingga ia dianggap *single point of failure* (satu titik yang kalau hilang, semuanya
terhenti). **Anggapan itu keliru:** Raissa juga paham sepak bola. Risikonya turun dari satu orang
menjadi dua. Dampaknya ada dua: lembar 21 transisi bisa dibagi dua orang, dan tekanan untuk
"menuliskan semuanya secepat mungkin" jauh berkurang. Menuliskan aturan tetap wajib, tetapi sekarang
alasannya karena itu bagian dari hasil kerja ketiga (dokumen teknis), **bukan** karena takut tidak ada
yang bisa menggantikan.

---

### Seat 2 — Data dan Sinyal Bola · **Raissa** (`raisinmee`)

**Kenapa dia:** punya pengalaman EDA, clustering, segmentation, dan dashboard, yaitu pekerjaan yang
sebagian besar berisi membersihkan data dan memeriksa sebaran nilainya. **Dia juga paham sepak bola**,
sehingga dia ikut memegang domain bersama Dyang, bukan sekadar menerima aturan.

> Seat ini bisa ditukar dengan Seat 1. Dyang punya pengalaman EDA/clustering/segmentation/dashboard yang
> setara dan juga paham bola. Kalau kalian bertukar, tidak ada yang hilang. Yang berpindah hanya siapa
> yang memegang aturan dan siapa yang memegang fitur.

**Tugas:**
- Memuat ATD (XML EPTS dan txt mentah), Smart Tagging, dan homography, lalu **menyeragamkan** semuanya
  menjadi satu tabel dengan satu baris per frame.
- Menjaga penyelarasan nomor frame: `video_frame = id_frame − 1`, Smart Tagging memakai
  `round(detik × 25)`, dan kolom `frame` di homography sama dengan baris di submission.
- Membangun fitur per frame (§7.2 dan §7.3).
- **Ikut memegang domain:** memeriksa apakah aturan Dyang masuk akal **dari sudut pandang sepak bola**,
  dan mengambil separuh lembar 21 transisi (`docs/gt-public-transitions.md`). Dua orang yang membaca 21
  transisi itu akan melihat hal yang berbeda, dan perbedaan itulah gunanya.
- Pemilik diagnosa: sebaran label, panjang celah bola yang hilang, dan peta potongan possession.

**Hasil yang bisa diperiksa:** `src/deculgirl/features/` · tabel fitur per frame · laporan diagnosa

**Definisi selesai:** satu perintah menghasilkan `features.parquet` dengan tepat 199.319 baris, tanpa
`NaN` yang tidak dijelaskan, dan Billa bisa memakainya tanpa menyentuh file mentah.

---

### Seat 3 — Model Sekuensial dan Bola Mati · **Billa** (`nabilland`)

**Kenapa dia:** satu-satunya di tim yang punya pengalaman *sequence labelling* (LSTM / Bi-LSTM /
Bi-GRU). Tugas ini persis jenis masalah itu: 199.319 frame berurutan yang saling memengaruhi.

**Tugas:**
- Model bola mati yang berdiri sendiri (§7.1). **Inilah kelemahan terbesar baseline**, dan nilainya
  paling tinggi.
- Menentukan tim `H`/`A` untuk frame saat bola hidup (§7.3).
- Menyusun possession tanpa memecahnya (§7.4), yaitu mengubah probabilitas per frame menjadi rentang
  waktu.
- Model sekuensial di Gate 2 (§7.6).
- **Penulis utama dokumen teknis** (hasil kerja ketiga). Billa satu-satunya yang sudah punya publikasi
  ilmiah.

**Hasil yang bisa diperiksa:** `src/deculgirl/model/` · file label mentah · draf dokumen teknis

**Definisi selesai:** setiap perubahan konfigurasi bisa dijalankan ulang dan menghasilkan skor yang
jelas berbeda, bukan hasil yang tidak bisa dijelaskan.

---

### Seat 4 — Pengukuran, Validasi, dan Reproduksi Hasil · **Yona** (`yonakatitin`)

**Kenapa dia:** satu-satunya yang pernah menulis kode berstandar produksi (FastAPI, RAG pipeline, AWS
re/Start).

**Tugas:**
- Menjalankan scorer resmi di komputer lokal (§8). Ini **Gate 0, hari pertama**.
- Membuat regression suite dan bootstrap CI, supaya selisih 0,01 tidak disangka kemenangan.
- Menyiapkan `run.py`, satu perintah yang menghasilkan file submission yang **identik**.
- Mengunci versi semua dependensi (pin). Pemeriksaan validasi berjalan otomatis di setiap PR.
- Penjaga terakhir sebelum submit.

**Hasil yang bisa diperiksa:** `metrics/` · `run.py` · `.github/workflows/validate.yml` · `REPRODUCE.md`

**Definisi selesai:** Dyang bisa menghapus semua hasil, menjalankan satu perintah di laptopnya sendiri,
dan file yang dihasilkan identik byte demi byte dengan yang sebelumnya.

> **Catatan penting — Yona satu-satunya yang masih intern.** Seat 4 adalah jalur yang tidak boleh
> terputus. Kalau Yona tidak bisa dihubungi selama tiga hari di minggu terakhir, tidak ada yang bisa
> menghasilkan ulang submission. Karena itu, cara kerja pipeline dibangun berpasangan di Gate 0 lalu
> **dibekukan**, pemeriksaannya **diotomatiskan** (dikerjakan robot, bukan orang), dan tugas menjawab
> "apakah selisih ini nyata?" dipindahkan ke Raissa. Yona tetap pemilik metriknya, sedangkan Raissa
> pemilik keraguannya.

---

### 4.5 ⬜ PM — sengaja dikosongkan

Siapa yang menjadi PM **belum ditetapkan**, dan itu disengaja. Ini satu-satunya peran di dokumen ini
yang tidak dicocokkan dengan pengalaman siapa pun, karena PM bukan soal keahlian, melainkan soal
**kesediaan**. Tanyakan langsung di rapat. Jangan menunggu ada yang mengangkat tangan sendiri.

**PM adalah peran tambahan, bukan seat tersendiri.** Siapa pun yang memegangnya tetap mengerjakan seat
teknisnya. Jadi kalian **tidak** butuh orang kelima. Kalian hanya butuh satu dari empat orang ini yang
bersedia memegang dua tugas sekaligus.

| Tanggung jawab | Kalau tidak ada yang memegang |
|---|---|
| Memimpin rapat harian: "apa yang hijau, apa yang merah, apa yang menghalangi" | Tim remote akan berjalan sendiri-sendiri dalam empat hari, dan tidak ada yang menyadarinya |
| Memutuskan di akhir tiap gate: **lanjut atau perbaiki** | Gate hanya jadi hiasan, tanggalnya lewat tanpa ada yang memutuskan |
| **Pemilik file submission**: uji coba pengiriman 15 Nov, mengisi form, menyimpan bukti | Ini penyebab kegagalan paling umum, dan tidak bisa diselamatkan di menit terakhir |
| Memastikan `docs/decisions.md` terisi | Keputusan hilang dan dibahas ulang minggu depan |

**Batas waktunya: harus sudah ada yang memegang paling lambat di akhir Gate 1, yaitu Senin, 2 November.**

Sampai peran itu terisi, dua hal berjalan dengan cara sementara, dan keduanya sengaja tidak dipaksakan:

- `docs/decisions.md` diisi oleh **notulis bergilir**, yaitu siapa pun yang mencatat di rapat itu, bukan
  satu orang tetap.
- Kepemilikan file submission belum punya nama. Itu **wajar** di hari kedua, tetapi **tidak wajar** di
  hari kesepuluh.

Kalau sampai 2 November tidak ada yang bersedia, tugas ini jatuh ke **Dyang secara otomatis**. Alasannya
bukan karena itu bagian dari tugas domainnya, tetapi karena file submission harus punya satu nama dan
Dyang adalah pemilik repo.

---

## 5. Alur 25 hari: empat gate

Pekerjaan dibagi per **gate** (tahap), bukan per tanggal. **Setiap gate punya satu angka yang harus
hijau sebelum lanjut.** Kalau gatenya masih merah, jangan naik ke gate berikutnya. Perbaiki dulu.

Hari ini **Sabtu, 24 Oktober 2026**. Batas pengumpulan **Selasa, 17 November 2026**. Pendaftaran
ditutup **Selasa, 10 November 2026**.

### 🔴 GATE 0 — Pipeline dan pengaman · Sab 24 – Sen 26 Okt (3 hari)

**Angka hijau:** `run.py` menghasilkan file 199.319 baris yang **lolos `validate_submission.py`**, dan
kita punya skor `spellF1` yang terukur di jendela publik.

**Angka kedua:** kita sudah **terdaftar dan sudah memegang bundle data.**

Daftar pekerjaan:
1. **Unduh bundle ke `data\tactical\`** dengan nama file yang persis sama dengan aslinya. Yang
   dibutuhkan hanya empat file, karena `tactical.mp4` tidak dipakai pipeline kita sama sekali. Kalau
   Drive tidak mengizinkan unduhan, kirim email ke penyelenggara **hari ini juga**. Itu satu-satunya
   masalah di proyek ini yang tidak bisa diatasi dengan kerja keras.
2. **Sudah berjalan:** repo `mtah-DeculGirl` sudah publik dan commit pertama sudah di-push. Tinggal satu
   langkah, yaitu mengatur hak akses: **Dyang = owner**, **Billa = Admin** (admin kedua), **Raissa dan
   Yona = Write**. Adminnya dua orang, bukan satu, karena Admin adalah satu-satunya peran yang bisa
   mengubah Settings, mengatur akses, dan mengelola Actions. Kalau hanya satu orang yang memegangnya dan
   dia tidak bisa dihubungi di minggu terakhir, tim tidak bisa memperbaiki repo di saat yang paling
   berbahaya.
3. **Sudah disiapkan:** `tools/fetch_official.py`, yang mengunduh repo resmi pada commit `f8f2629` ke
   `third_party/`. Kalian tinggal menjalankannya.
4. **Sudah disiapkan dan sudah diuji:** `tools/gate0.py`, yang **sama sekali tidak butuh data
   pertandingan**. Alat ini membuktikan bahwa scorer, validator, dan GT publik berfungsi di komputer
   kalian.
5. **Sudah disambungkan:** versi pertama `submit.py` memakai **baseline resmi**. Itu bukan buatan kita,
   melainkan kode berlisensi MIT dari penyelenggara yang mereka sebut sendiri sebagai *"a starting
   point, not a constraint"* (titik awal, bukan batasan). Begitu data selesai diunduh, `python run.py`
   langsung menghasilkan submission yang sudah berskor. **Itulah pengaman kalian, dan karena itu
   langkah ini tidak boleh dilewati.** Setiap perbaikan ditambahkan sebagai varian baru, sehingga
   `main` selalu bisa menghasilkan submission yang valid.
6. Ekstrak data ke `data/` (**di drive D:, tidak masuk git**). Pastikan jumlah baris tracking = 199.319.
   Kalau jumlahnya berbeda, **jangan ditambah atau dipotong sendiri**. Cari tahu dulu kenapa berbeda.

> ### ⚠️ Kalau Gate 0 selesai, kalian sudah punya submission. Itu asuransi.
> Setelah ini, **tidak boleh ada yang menghapus file yang sudah valid.** Setiap perbaikan ditambahkan
> sebagai varian, dan `main` selalu bisa menghasilkan submission yang valid.

---

### 🟠 GATE 1 — Empat hal struktural · Sel 27 Okt – Sen 2 Nov (7 hari)

**Angka hijau:** `spellF1` di jendela publik melewati baseline buatan kita sendiri, dan `macroF1` untuk
kelas `D` naik dengan jelas.

Semua seat bekerja bersamaan tanpa saling menunggu. Rincian teknisnya ada di §7.

| Seat | Hasil kerja di gate ini |
|---|---|
| 1 (Dyang) | `docs/possession-rules.md` selesai dan sudah ditinjau Billa |
| 2 (Raissa) | `features.parquet` dan laporan diagnosa celah bola yang hilang |
| 3 (Billa) | Pengklasifikasi bola mati dan penyusunan possession tanpa memecah sudah berjalan |
| 4 (Yona) | Regression suite dan bootstrap CI selesai; Gate 0 dibekukan |

**Aturan gate ini:** setiap hal struktural harus bisa **dibuktikan sendiri-sendiri**. Kalau pendeteksi
bola mati memperbaiki `macroF1` kelas `D` **tanpa** merusak `spellF1`, berarti ia terbukti berfungsi.
Kalau skor naik tetapi kalian tidak tahu bagian mana penyebabnya, itu bukan hasil, melainkan
kebetulan, dan tidak bisa ditulis di dokumen teknis.

---

### 🟡 GATE 2 — Model sekuensial dan penyetelan yang jujur · Sel 3 – Sen 9 Nov (7 hari)

**Angka hijau:** model sekuensial mengalahkan versi berbasis aturan dengan **confidence interval yang
tidak saling tumpang tindih** (`--bootstrap 1000`). Kalau intervalnya tumpang tindih, **pertahankan
versi yang lebih sederhana** dan berhenti di situ. Itu bukan hal yang memalukan. Itulah riset yang
jujur.

**Peringatan paling mahal di seluruh proyek ini:** `EVALUATION.md` menunjukkan bahwa menyetel parameter
di 5 menit publik **memilih baseline yang salah**. `smooth125` menang di jendela publik (0,4242) tetapi
kalah di pertandingan penuh (0,2242). Padahal itu baru satu parameter pada baseline yang sangat
sederhana. Jangan pernah memilih versi berdasarkan jendela publik. Pakai jendela itu hanya untuk
memastikan pipeline-nya **benar**, tidak lebih.

Di gate ini juga: kalau `--bootstrap 1000` belum pernah dijalankan, lakukan sekali di sini. Apa pun
hasilnya, **catat di `docs/experiments.md`**, termasuk kalau ternyata selisihnya masih di dalam noise.
"Tidak terbukti lebih baik" adalah hasil yang sah, dan justru menjadi bahan untuk bagian keterbatasan di
dokumen teknis.

---

### 🟢 GATE 3 — Reproduksi hasil dan dokumen · Sel 10 – Sel 17 Nov (8 hari)

**Angka hijau:** orang yang bukan pemilik Seat 4 bisa menjalankan `run.py` di laptop yang bersih dan
mendapatkan file yang **identik**, hanya dengan membaca `REPRODUCE.md`.

| Tanggal | Pekerjaan |
|---|---|
| 10 – 13 Nov | Dokumen teknis (§7.7), `REPRODUCE.md`, dan merapikan repo |
| **14 Nov** | **FREEZE (kode dibekukan).** Tidak ada perubahan kode setelah tanggal ini. |
| 15 Nov | Uji coba pengiriman: isi form lengkap dengan file dan URL final. Pastikan file bisa dibuka. |
| 16 Nov | Cadangan waktu. Hanya untuk memperbaiki yang rusak. |
| **17 Nov** | **Kumpulkan.** |

> **Freeze bukan sekadar saran.** Kebanyakan poin dalam kompetisi seperti ini hilang di 72 jam
> terakhir, dan penyebabnya bukan skor. Penyebabnya adalah file yang tadinya valid menjadi tidak valid,
> atau repo yang tadinya berjalan menjadi tidak berjalan. Menurut `SUBMISSION.md`, file yang gagal
> validasi **"is skipped with a one-line reason and scores nothing"** (dilewati dengan satu baris alasan
> dan tidak mendapat nilai).

---

## 6. Cara mengelola proyek ini

### Kebiasaan rutin

| Kapan | Apa | Lama |
|---|---|---|
| Setiap hari, jam tetap | Rapat harian: **apa yang hijau, apa yang merah, apa yang menghalangi** | 20 menit |
| Setiap Minggu | Tinjauan gate: apakah angka hijaunya tercapai? Lanjut atau perbaiki? | 45 menit |
| Kapan saja | Kalau tersendat lebih dari 2 jam → **tulis di channel**, jangan diam saja | — |

Aturan rapat harian: **tidak ada laporan status yang panjang.** Cukup tiga kalimat: hijau, merah,
penghalang. Kalau butuh lebih dari 20 menit, berarti masalahnya belum dirumuskan dengan jelas, dan itu
sendiri sudah menjadi masalah.

### Repo

- **Tidak ada yang push langsung ke `main`.** Semua lewat branch dan PR, walaupun hanya dua baris.
  Nama branch: `dyang/rules`, `raissa/features`, `billa/model`, `yona/metrics`.
- **Semua PR melewati pemeriksaan otomatis** (`.github/workflows/validate.yml`). Kalau pemeriksaannya
  merah, jangan di-merge.
- **`docs/decisions.md` adalah satu-satunya sumber yang sah untuk keputusan.** Di tim remote, keputusan
  yang hanya diucapkan di chat akan hilang dalam dua hari dan dibahas lagi minggu depan. Satu keputusan =
  satu baris.
- **Commit kecil dan sering.** Riwayat commit adalah bukti pekerjaan yang bisa dilihat siapa pun yang
  membuka repo, termasuk juri Innovation Challenge nanti.

### Kenapa bekerja remote bukan masalah

Seluruh tugas ini berbentuk **berkas**: CSV, repo, dan dokumen. Tidak ada bagian yang mengharuskan
kalian berada di ruangan yang sama. Yang biasanya bermasalah di tim remote bukan hasil kerjanya,
melainkan tiga hal berikut, dan ketiganya sudah dicegah di atas: pekerjaan tidak meninggalkan jejak
(→ lewat PR), keputusan hilang (→ `decisions.md`), dan orang tersendat tanpa memberi tahu (→ aturan
2 jam).

---

## 7. Strategi teknis

Urutan kerja yang disarankan: **aturan dan fitur dulu, model belakangan.** Alasannya bukan karena ingin
aman. Alasannya karena **setiap hal struktural bisa dibuktikan sendiri-sendiri**, dan hanya dengan cara
itu kalian punya sesuatu yang benar-benar bisa ditulis di dokumen teknis.

### 7.1 Deteksi bola mati — bagian dengan nilai tertinggi

Baseline sama sekali tidak punya logika bola mati. Docstring `starter/baseline.py` mengakuinya sendiri:

> *"It has no notion of a dead ball beyond 'the tracking lost the ball', which is why its D class is weak."*

Satu-satunya tanda `D` di baseline adalah bola tidak ada di frame itu. Artinya, baseline hanya benar
saat memberi `D` kalau bola kebetulan sedang tidak terdeteksi **dan** bola memang sedang mati.

**Menghaluskan hasil malah memperburuk kelas `D`, bukan memperbaikinya.** Berikut F1 kelas `D` untuk
tiap varian, dari scorer resmi pada jendela publik:

| Versi | F1 `D` | presisi `D` | recall `D` |
|---|---|---|---|
| `baseline_raw` | **0,4197** | 0,5582 | 0,3363 |
| `baseline_smooth25` | 0,3857 | 0,6106 | 0,2818 |
| `baseline_smooth50` | 0,3225 | 0,6569 | 0,2138 |
| `baseline_smooth125` | 0,1464 | **1,0000** | **0,0790** |

Cara membacanya: `smooth125` **tidak pernah salah** saat menyebut `D`, jadi presisinya sempurna, tetapi
ia hanya menemukan **7,9%** dari frame bola mati yang sebenarnya. Dan keempat varian lebih buruk
daripada `raw` untuk kelas ini. Jadi pendeteksi bola mati yang lebih baik **bukan sekadar penyempurnaan
kecil di atas baseline**. Ini wilayah yang belum digarap sama sekali, dan setiap perbaikan di sini tidak
mengambil poin dari siapa pun.

Fitur yang tersedia dan belum dipakai siapa pun:

| Fitur | Kenapa relevan |
|---|---|
| Panjang celah bola yang hilang berturut-turut | Bola mati sering muncul sebagai celah yang panjang, bukan yang pendek |
| Kecepatan bola | Ada di file mentah sebagai angka **ketiga** di setiap kelompok (`x,y,speed`). Baseline hanya membaca dua angka pertama |
| Gerakan pemain | Saat bola mati, pemain berjalan (bukan berlari) atau berhenti |
| Sebaran dan kerapatan pemain | Posisi pemain saat memulai kembali permainan (kick-off, lemparan ke dalam) punya pola yang khas |
| Smart Tagging | **Setiap set piece adalah awal permainan kembali**, dan itu mengakhiri masa bola mati. Setiap fase juga punya tag tim |
| Jeda antar babak, sebelum kick-off | Babak 2 mulai dinilai dari frame 110.808, kick-off di 113.742. Ada 2.934 frame yang semuanya `D` |

> **Catatan kepatuhan untuk poin terakhir.** Fakta tentang 2.934 frame itu **diterbitkan di `FAQ.md`
> resmi**, jadi memakainya bukan pelanggaran. Tetapi `RULES.md` melarang *"rules and constants tied to
> specific frames of the game"* (aturan dan konstanta yang terikat pada frame tertentu) yang kalian
> **turunkan sendiri dari pengamatan**. Cara yang aman: bangun pendeteksi bola mati yang **bersifat
> umum**, lalu pakai fakta dari FAQ itu sebagai **alat pemeriksa**, yaitu apakah pendeteksimu memang
> menandai `D` di sana. Kalau kalian memutuskan untuk menuliskan angka itu langsung di kode
> (hardcode), **cantumkan beserta sumbernya** di dokumen teknis. Kalau ragu, tanyakan ke penyelenggara
> lewat issue. `FAQ.md` mengundang hal itu secara terbuka: *"If a rule is unclear or your approach sits
> near a line, ask before you build on it."*

### 7.2 Mengisi posisi bola yang hilang (imputasi)

Bola tidak terdeteksi di **41% frame yang dinilai**. Menurut `DATA.md`, hilangnya justru
*"disproportionately on the frames that matter"* (tidak seimbang: lebih sering di frame yang penting),
yaitu di kotak penalti yang penuh pemain, duel udara, dan tekel. Di data tidak ada indikator tingkat
keyakinan atau keterlihatan bola. `DATA.md` sendiri berpesan: *"design for it on day one."*
(rancang untuk hal ini sejak hari pertama).

Pendekatan bertahap, dari yang murah ke yang mahal:

1. **Celah pendek** (kurang dari ± 0,5 detik atau 12 frame): isi dengan interpolasi linear atau filter
   Kalman. Bola bergerak mulus, jadi mengisi celah pendek hampir selalu benar.
2. **Celah panjang**: **jangan diisi.** Biarkan tetap sebagai ketidakpastian dan pakai sebagai sinyal.
   Celah panjang itu sendiri sudah membawa informasi (lihat §7.1).
3. **Pemeriksaan geometri:** proyeksikan posisi bola hasil pengisian ke piksel lewat homography, lalu
   periksa apakah hasilnya masuk akal. Ini penggunaan homography yang paling langsung berguna, dan
   homography feed taktis **100% valid**.
4. **Satu gangguan ditambah satu tebakan buruk lebih mahal daripada satu celah.** Ingat bahwa `X` di
   tengah possession itu **tidak merugikan** (§7.5). Jadi tidak ada alasan memaksakan posisi bola yang
   tidak kalian yakini.

**Jangan pakai video.** GPU GTX 1650 Ti dengan VRAM 4 GB cukup untuk menjalankan model kecil.
Tetapi `RULES.md` melarang anotasi manual *"in any amount and for any purpose"* (berapa pun jumlahnya
dan untuk tujuan apa pun), termasuk untuk melatih model. Artinya kalian harus mengandalkan model yang
sudah dilatih pihak lain dan kebetulan bisa menemukan bola, lalu memvalidasinya tanpa ground truth.
Itu eksperimen, bukan rencana. Tidak ada bagiannya yang bisa kalian buktikan benar sebelum 17 November.

### 7.3 Menentukan tim yang menguasai bola

Baseline: pemain tracked yang paling dekat ke bola, memakai jarak Euclidean kuadrat dalam meter.
Hanya itu.

Fitur pengganti. Daftarnya panjang, tetapi semuanya murah dikerjakan:

- Jarak bola ke **2–3 pemain terdekat dari tiap tim**, lalu dibandingkan, bukan hanya pemain yang paling
  dekat secara keseluruhan.
- **Arah gerak:** apakah pemain bergerak **menuju** bola (hasil kali titik (dot product) antara
  kecepatan pemain dan vektor dari pemain ke bola). Pemain yang mendekati bola jauh lebih mungkin
  menguasainya daripada pemain yang kebetulan berada di dekatnya.
- **Konteks sebelum celah:** tim mana yang terakhir mengontrol bola sebelum bola menghilang.
- **Petunjuk dari Smart Tagging:** setiap fase punya tag tim. Dua peringatan dari dokumentasinya:
  `Team = N/A` pada **setiap lemparan ke dalam**, dan *"the intervals are phases, not possessions"*
  (rentang waktunya adalah fase permainan, bukan possession).
- **Kelanjutan dari frame sebelumnya adalah fitur, bukan masalah:** possession adalah *keadaan* yang
  bertahan, bukan keputusan yang dibuat terpisah di tiap frame. Sebuah frame berlabel `H` sebagian besar
  karena frame sebelumnya `H`.

### 7.4 Menyusun possession tanpa memecahnya

Langkah ini mengubah probabilitas per frame menjadi rentang waktu. Inilah bagian yang langsung
berhubungan dengan metriknya.

- **Panjang minimum possession.** Scorer tidak punya batas minimum panjang possession, jadi **kitalah**
  yang harus punya aturannya. Gabungkan potongan pendek ke tetangga yang dominan, atau buang. Setiap
  potongan yang dibuang berarti satu `fp` yang hilang.
- **HMM / Viterbi** dengan matriks transisi yang membuat perpindahan `H → A` mahal. Ini bentuk yang
  paling wajar untuk gagasan "possession itu keadaan yang bertahan, bukan keputusan yang berdiri
  sendiri".
- **Median filter** adalah versi termurah dari gagasan yang sama, dan baseline sudah membuktikan bahwa
  gagasan ini berhasil: hanya dengan melebarkan window, `spellF1` bergerak 5 kali lipat.
- **Perhatikan jumlah possession kalian.** `validate_submission.py` mencetak angkanya. Baseline `raw`
  melaporkan **131 possession** untuk 5 menit publik, padahal yang benar **17**. Itu berarti possession
  terpecah 7,7 kali lipat, dan itulah sebabnya `spellF1`-nya hanya 0,0378.

### 7.5 Kebijakan `X` — alat paling kuat yang kita punya

Sebelum menyusun possession, scorer mengganti setiap `X` dengan label terakhir yang bukan `X` **di babak
yang sama** (di awal babak, diisi dengan label non-`X` pertama yang ditemui). Jadi:

```
H H H X X X H H H   →   H H H H H H H H H   →   SATU possession
```

**`X` bukan tombol menyerah. `X` adalah tombol "sama seperti sebelumnya".**

Penerapannya:

| Situasi | Tindakan | Alasan |
|---|---|---|
| Bola hilang **di tengah** possession | Tulis `X` | Tidak merugikan. Possession tetap utuh. Lebih aman daripada tebakan yang bisa memecahnya |
| Saat **possession berpindah ke tim lawan** | **Wajib menebak** | `X` akan menarik label lama ke wilayah tim lawan. Ini sangat merugikan |
| Di luar waktu pertandingan | `X` | Sama sekali tidak dinilai |

Soal biayanya: `macroF1` menghitung `X` sebagai salah, tetapi `macroF1` hanya pemutus kalau seri.
`spellF1`, yang menentukan peringkat, tidak pernah melihatnya. Jadi dalam praktiknya **`X` itu murah**,
dan tidak ada alasan untuk sungkan memakainya.

### 7.6 Model sekuensial (Gate 2, bukan Gate 1)

Baru dikerjakan setelah keempat hal struktural berdiri dan terbukti. Bentuk yang paling masuk akal:
**CRF atau GRU/Bi-GRU di atas fitur per frame**, dengan empat hal struktural tadi sebagai fitur masukan,
bukan sebagai pengganti. Billa sudah pernah mengerjakan model seperti ini.

Aturan gate: kalau tidak mengalahkan versi aturan dengan confidence interval yang tidak tumpang tindih,
**pertahankan versi aturan.** Model sekuensial hanyalah bonus, bukan jalan keluar.

### 7.7 Dokumen teknis (hasil kerja ketiga)

`SUBMISSION.md` meminta *"a few pages"* (beberapa halaman). Susunan yang diminta, sebaiknya diikuti
persis:

1. **Pendekatan dan alasannya** — kenapa dipilih begitu, bukan hanya apa yang dikerjakan.
2. **Aset mana yang dipakai dan bagaimana** — termasuk **yang sudah dicoba lalu dibuang**. Bagian ini
   paling sering dilewatkan, padahal justru yang paling menunjukkan kesungguhan kalian. Isinya diambil
   apa adanya dari `docs/experiments.md`. **Itulah alasan file itu ada**, dan karena itu file tersebut
   harus diisi selama pekerjaan berlangsung, bukan disusun ulang di bulan November.
3. **Data latih** — setiap dataset berlabel, sumbernya, siapa yang melabeli, dan jumlahnya. Kalau tidak
   ada, tulis "tidak ada". Itu jawaban yang sah.
4. **Aturan possession yang diterapkan** — diambil dari `docs/possession-rules.md`.
5. **Keterbatasan** — tulis dengan jujur. Kejujuran menaikkan kredibilitas, bukan menurunkannya.
6. **Cara mereproduksi hasil** — satu perintah.

Lampirkan juga fakta mana dari dokumentasi resmi yang kalian pakai (§7.1), dan keputusan apa saja yang
bersifat kalibrasi atau dilakukan manual, kalau ada.

---

## 8. Cara mengukur tanpa menipu diri sendiri

**Scorer yang kalian jalankan di komputer sendiri adalah scorer yang menentukan peringkat kompetisi.**
Kata `EVALUATION.md`: *"Organisers run this exact script against the private full-match ground truth;
the published board is its output. There is no stricter version held back."* (Penyelenggara menjalankan
skrip yang persis sama terhadap ground truth pertandingan penuh yang dirahasiakan; papan skor yang
diterbitkan adalah keluarannya. Tidak ada versi yang lebih ketat yang disembunyikan.) Ini keuntungan
besar, jadi manfaatkan sepenuhnya.

```bash
python tools/gate0.py              # unduh repo resmi, jalankan evaluator resmi
python evaluation/validate_submission.py <file>   # SEBELUM setiap submission
```

Aturan pengukuran:

- **Noise `spellF1` di pertandingan penuh ≈ 0,04.** Selisih di bawah itu bukan perbaikan.
  Noise `macroF1` ≈ 0,01.
- **Selalu jalankan `--bootstrap 1000`** sebelum percaya bahwa satu versi lebih baik daripada versi
  lain. Biasanya intervalnya tumpang tindih.
- **Jendela publik 5 menit bukan leaderboard.** Isinya hanya 17 possession, dan satu possession yang
  meleset kira-kira berarti 6 poin. `EVALUATION.md` membuktikan bahwa menyetel parameter di situ
  memilih baseline yang salah. Pakai hanya untuk memastikan **pipeline-nya benar**, bukan untuk memilih
  versi.
- **Hasilnya harus selalu sama (deterministik).** Kalau skor berubah di antara dua kali menjalankan
  program yang sama, itu bug, bukan keberuntungan.
- **`reports/<nama>_transitions.csv`** dari evaluator resmi mendaftar setiap transisi sebagai
  `matched` (cocok), `missed` (terlewat), atau `spurious` (palsu) untuk setiap video frame. Ini alat
  debug terbaik yang kalian punya, dan tidak banyak yang tahu ada.

### Kolom papan skor yang wajib kalian baca

`tools/gate0.py` mencetak papan skor resminya. Selain `spellF1` dan `macroF1`, ada lima kolom yang jauh
lebih berguna untuk pekerjaan harian:

| Kolom | Artinya | Yang kalian cari |
|---|---|---|
| **`frag`** | jumlah segmen prediksi ÷ jumlah segmen yang benar | **Mendekati 1,0 atau sedikit di bawahnya.** Ini kolom terpenting di seluruh papan |
| **`poss`** | jumlah possession yang kalian laporkan | Yang benar **17** di jendela ini. 26 sudah mulai menyimpang; 131 itu tanda bahaya |
| **`dur`** | rata-rata durasi possession | Yang benar **14,2 detik**. Kalau terlalu pendek, berarti possession kalian terpecah |
| **`shareE`** | selisih porsi penguasaan tim home dibandingkan yang benar | Yang benar 0,5727: Barcelona menguasai 57% frame bola hidup di jendela ini |
| **`lat_f`** | rata-rata keterlambatan, dalam jumlah frame | Di bawah 25 frame masih murah (§3 poin 3); di atas itu mahal |

Laporan per submission (file `.txt` yang ditulis evaluator) lebih tajam lagi. Isinya matriks konfusi
4×4, presisi/recall/F1 per kelas, `alive/dead F1`, akurasi tim, dan, yang paling berkaitan dengan
§7.5, **berapa banyak frame `X` kalian yang jatuh pada frame yang dinilai.** Itu ukuran langsung dari
kebijakan tidak-menjawab yang kalian pakai. Evaluator juga menulis `scoreboard.csv`.

---

## 9. Larangan yang tidak boleh dilanggar

Daftar ini berisi hal-hal yang bisa membuat kerja tiga minggu bernilai nol. Ini bukan soal etika,
melainkan soal **apa yang dihitung**.

| ❌ Dilarang | Detail yang mudah terlewat |
|---|---|
| **Melabeli pertandingan ini secara manual** | *"in any amount and for any purpose"* (berapa pun jumlahnya dan untuk tujuan apa pun): untuk submission, **untuk melatih model, maupun untuk memvalidasi**. Termasuk memperbaiki keluaran algoritma dengan tangan, baik *frame demi frame, segmen demi segmen, maupun hanya di titik transisi* |
| **Data buatan manusia tentang pertandingan ini** | Data event (Opta, StatsBomb, Wyscout, LaLiga, atau siapa pun), tracking yang sudah dikoreksi, data possession, atau anotasi apa pun dari sumber mana pun |
| ⚠️ **Ingatan kalian sendiri tentang pertandingan ini** | Ini turunan dari larangan di atas, dan jebakan khusus bagi **Dyang** serta Raissa yang paham sepak bola. Kalau ada yang ingat skor akhir, menit gol, atau kejadian VAR, itu adalah **pengetahuan manusia tentang pertandingan ini**. Memakainya sebagai fitur, label, atau konstanta adalah pelanggaran. Yang boleh: memahami **arti** sepak bola. Yang tidak boleh: mengingat **pertandingan ini** |
| **Mengunggah data ke LLM cloud** | Syarat penggunaan (ToU) melarang mengunggah video, dataset, atau **potongan-potongannya** ke LLM pihak ketiga berbasis cloud. Memakai AI untuk menulis kode tetap boleh; yang dilarang adalah mengirim isi datanya |
| **Menyebarkan data** | Jangan commit `data/` ke repo publik. Jangan menerbitkan turunan yang bisa dipakai untuk merekonstruksi data |
| **Repo yang tidak bisa mereproduksi file** | *"A private in-house model or an unavailable internal dataset is the one thing this rules out"* (model internal yang tidak dipublikasikan atau dataset internal yang tidak tersedia adalah satu-satunya hal yang dilarang) |
| **Menyetel parameter di 5 menit publik** | Ini aturan, bukan saran. Dan terbukti merugikan (§8) |

**Yang justru diizinkan**, dan mungkin belum kalian sadari:

- Memperbaiki atau **mengganti** data tracking yang diberikan, asalkan dilakukan **oleh algoritma**,
  bukan oleh tangan.
- Memakai model yang sudah dilatih pihak lain, LLM apa pun, dan framework apa pun.
- Memakai data dari luar, **asalkan tentang pertandingan lain**.
- Melabeli secara manual **pertandingan lain**, sebanyak apa pun.
- Memakai Smart Tagging. FAQ menjawab kecurigaan ini langsung: *"Use it — that is why it is there."*
  (Pakailah, memang untuk itu ia disediakan.)
- Memakai model buatan sendiri: pendeteksi, pelacak, atau pengenal kejadian. *"If it produces a better
  answer, it is a better answer."* (Kalau hasilnya lebih baik, berarti jawabannya lebih baik.)

---

## 10. Sepuluh hal penentu — dari yang paling sering diabaikan

1. **Pemenangnya bukan yang modelnya paling canggih.** Keempat baseline di repo memakai algoritma
   **yang sama** dengan window berbeda: `macroF1` bergeser 0,04, sedangkan `spellF1` berbeda 11 kali
   lipat di jendela publik (5 kali lipat di pertandingan penuh).
2. **`X` adalah tombol "ulangi jawaban sebelumnya".** Tidak menjawab di tengah possession itu tidak
   merugikan; tidak menjawab saat possession berpindah ke tim lawan itu bencana. Satu kebijakan, dua
   arah yang berlawanan.
3. **Scorer tidak punya batas minimum panjang possession.** Potongan kecil bukan "setengah benar". Ia
   adalah `fp` murni, dan memecah satu possession menjadi dua menghasilkan `fp` dan `fn` sekaligus.
4. **Kelas `D` adalah kelemahan terbesar.** Baseline mengakuinya sendiri. Smart Tagging memberi tag tim
   dan tanda set piece secara gratis, dan **belum ada yang memakainya**.
5. **Bola tidak terdeteksi di 41% frame yang dinilai, dan hilangnya tepat di frame yang penting.** Ini
   bukan gangguan yang harus ditoleransi. Ini adalah soalnya.
6. **5 menit publik tidak bisa dipakai untuk meranking siapa pun.** `smooth125` menang di jendela
   publik tetapi kalah di pertandingan penuh. Padahal itu hanya satu parameter pada baseline yang
   sederhana.
7. **Kebanyakan poin hilang di urusan administrasi.** File yang gagal validasi dinilai **nol**, dan repo
   yang tidak bisa mereproduksi file membuat tim gugur. `validate_submission.py` hanya butuh dua detik.
8. **Di luar kedua babak, label kalian tidak berpengaruh apa pun.** `macroF1` hanya menghitung frame
   yang dinilai, dan `spellF1` hanya menyusun possession di dalam rentang yang dinilai. Jangan
   buang waktu untuk bagian jeda.
9. **2.934 frame pertama babak 2 semuanya `D`**, dan itu diterbitkan resmi di `FAQ.md`. Pakai sebagai
   alat pemeriksa pendeteksi bola mati kalian, dan cantumkan sumbernya.
10. **Semua yang kalian hasilkan akan dibaca.** Dua dari tiga hasil kerja bukan angka, yaitu repo dan
    dokumen. Keduanya ikut menentukan nasib kalian di Innovation Challenge, yang penilaiannya sangat
    berbeda: ada juri, ada presentasi, dan ada desain.

---

## 11. Daftar periksa pengumpulan

Dijalankan pada **15 November**, tidak boleh lebih lambat.

**File CSV**
- [ ] `DeculGirl.csv` — tepat **199.319** baris data, header `frame,label`
- [ ] Kolom `frame` berisi 0…199318, berurutan, tanpa duplikat
- [ ] Tidak ada sel yang kosong — tulis `X` kalau sistem tidak menjawab
- [ ] `python evaluation/validate_submission.py DeculGirl.csv` → **`Valid.`**
- [ ] Jumlah possession yang dilaporkan masuk akal (bandingkan dengan 17 pada 5 menit publik; 131 itu
      tanda bahaya)
- [ ] Kolom `frag` mendekati 1,0 atau sedikit di bawahnya, bukan 2 ke atas
- [ ] Baris `abstained ... frames of X on graded ground truth` di laporan sesuai dengan kebijakan `X`
      kalian, bukan 0% dan bukan 100%

**Repo publik**
- [ ] `mtah-DeculGirl` berstatus **public**, dan URL-nya bisa dibuka di jendela incognito
- [ ] Folder `data/` **tidak ada** di repo
- [ ] `run.py` menghasilkan file yang identik, sudah diuji di laptop orang lain
- [ ] Versi dependensi dikunci (`requirements.txt` dengan nomor versi)
- [ ] `README.md` menjelaskan cara menjalankan dengan bahasa yang bisa diikuti orang luar

**Dokumen teknis**
- [ ] `DeculGirl.pdf` atau `.md`, beberapa halaman, mengikuti susunan di §7.7
- [ ] Menyebut aset yang dicoba **lalu dibuang**, bukan hanya yang dipakai
- [ ] Menyebut ada atau tidaknya data latih, lengkap dengan sumbernya
- [ ] Mencantumkan fakta resmi yang dipakai sebagai kalibrasi

**Form**
- [ ] Satu tanggapan per tim. **Tanggapan terakhir sebelum batas waktu yang akan dinilai.**
- [ ] Nama tim: `DeculGirl` · file: `DeculGirl.csv`, `DeculGirl.pdf`
- [ ] Butuh akun Google · tidak ada leaderboard langsung dan tidak ada umpan balik
- [ ] Simpan tangkapan layar bukti pengiriman di tempat yang bisa diakses keempat anggota

---

## 12. Setelah 17 November

Hasil diumumkan **sebelum 26 November**. Kalau masuk **top 20**, kalian lanjut ke Innovation Challenge
(**26 Nov – 14 Jan**, online) dengan dataset **10 pertandingan profesional**, tantangan desain yang
terbuka, dan bimbingan teknis. Kalau masuk **top 5** di sana, kalian tampil di Final Pitch pada
**2 Maret 2027** di Talent Arena Barcelona. Biaya perjalanan dan akomodasi ditanggung, dan kalian
mendapat jersey resmi Barça serta pengalaman eksklusif. Tidak ada hadiah uang.

Kalau tidak lolos pun, kalian tetap punya repo publik berisi analisis satu pertandingan LaLiga yang
nyata, dengan pipeline yang bisa direproduksi, dokumen teknis yang bisa dibaca orang lain, dan empat
orang yang sudah terbukti sanggup menyelesaikan pekerjaan bersama secara remote dalam tiga minggu. Itu
bukan hasil yang kecil.

**Penilaian berubah total di fase berikutnya.** Phase 1 murni dinilai dari angka tanpa juri, jadi ide
yang bagus tidak mendapat nilai. Innovation Challenge justru menilai desain, interpretasi, dan cara
bercerita. Karena itu, selama 25 hari ini: **kejar skornya dulu, ceritanya belakangan.** Tetapi mulai
sekarang, catat setiap keputusan di `docs/decisions.md`. Bahan cerita itu tidak bisa disusun ulang di
bulan Desember.
