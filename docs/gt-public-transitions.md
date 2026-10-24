# Lembar Kerja — 21 Transisi di 5 Menit GT Publik

**Pemilik: Seat 1 (Dyang).** Ini pekerjaan hari pertama, dan ini pekerjaan yang paling menentukan
seluruh 25 hari berikutnya.

Sumber: `evaluation/gt/BAR-ATH_possession_gt_public.csv` dari repo resmi (commit `f8f2629`).
Jendela yang dinilai: **frame 11.185 – 18.684** (7.500 frame). Di luar itu labelnya `X`.

Semua angka di bawah sudah **kuvalidasi silang** terhadap `BAR-ATH_possession_gt_public_meta.json`:
jumlah `H` = 3.454, `A` = 2.577, `D` = 1.469. Total = 7.500. Cocok.

---

## Kenapa lembar ini ada

`CHALLENGE.md` bilang GT-nya **bukan penilaian manusia** — GT diturunkan secara mekanis dari *corrected
tracking* yang tidak kita pegang. Yang kita punya cuma 5 menit itu. Jadi pekerjaan pertama bukan
"membangun model", tapi **merekonstruksi logika tracking terkoreksi itu dari 21 titik transisi**.

21 transisi untuk seluruh 5 menit. Itu lima menit kerja membaca kalau kalian tahu harus mencari apa —
dan seharian kalau mulai dari "buka CSV dan lihat".

---

## Tabel 1 — 21 transisi, berurutan

Kolom **Alasan** diisi tangan oleh Seat 1. Kolom **Sinyal** diisi hipotesis fitur apa yang bisa
mendeteksinya — itu yang nanti diteruskan ke Billa (§7.1 playbook).

| # | Frame | Transisi | Detik (±) | Alasan (isi) | Sinyal / fitur (isi) |
|---|---|---|---|---|---|
| 1 | 11.185 | `X → A` | 447,4 | awal jendela dinilai — bukan transisi sungguhan | — |
| 2 | 11.351 | `A → H` | 454,0 | | |
| 3 | 11.553 | `H → A` | 462,1 | | |
| 4 | 11.624 | `A → H` | 465,0 | | |
| 5 | 12.665 | `H → A` | 506,6 | | |
| 6 | **12.851** | **`A → D`** | 514,0 | | |
| 7 | **12.989** | **`D → H`** | 519,6 | | |
| 8 | 13.704 | `H → A` | 548,2 | | |
| 9 | 13.785 | `A → H` | 551,4 | | |
| 10 | 14.846 | `H → A` | 593,8 | | |
| 11 | 15.346 | `A → H` | 613,8 | ⚠️ possession cuma **19 frame (0,76 detik)** | |
| 12 | 15.365 | `H → A` | 614,6 | | |
| 13 | 15.766 | `A → H` | 630,6 | ⚠️ possession cuma **33 frame (1,32 detik)** | |
| 14 | 15.799 | `H → A` | 632,0 | | |
| 15 | **15.889** | **`A → D`** | 635,6 | | |
| 16 | **16.400** | **`D → A`** | 656,0 | ⚠️ bola mati **511 frame = 20,4 detik** | |
| 17 | 17.293 | `A → H` | 691,7 | | |
| 18 | **17.380** | **`H → D`** | 695,2 | | |
| 19 | **17.838** | **`D → A`** | 713,5 | ⚠️ bola mati **458 frame = 18,3 detik** | |
| 20 | **18.027** | **`A → D`** | 721,1 | | |
| 21 | **18.389** | **`D → H`** | 735,6 | ⚠️ bola mati **362 frame = 14,5 detik** | |
| — | 18.685 | `H → X` | 747,4 | akhir jendela dinilai — bukan transisi sungguhan | |

---

## Tabel 2 — 17 possession yang sebenarnya

Ini yang dibandingkan `spellF1`. Perhatikan durasinya: **dua possession terpanjang (41,6 s dan 42,4 s)
dan dua possession terpendek (0,76 s dan 1,32 s) dihitung sama beratnya** — satu possession, satu objek.
Itulah kenapa metrik ini metrik fragmentasi.

| # | Tim | Frame | Durasi (frame) | Durasi (detik) |
|---|---|---|---|---|
| 1 | **A** | 11.185 – 11.350 | 166 | 6,64 |
| 2 | H | 11.351 – 11.552 | 202 | 8,08 |
| 3 | **A** | 11.553 – 11.623 | 71 | 2,84 ← terpendek milik A |
| 4 | H | 11.624 – 12.664 | 1.041 | 41,64 ← terpanjang |
| 5 | **A** | 12.665 – 12.850 | 186 | 7,44 |
| — | *D* | *12.851 – 12.988* | *138* | *5,52* |
| 6 | H | 12.989 – 13.703 | 715 | 28,60 |
| 7 | **A** | 13.704 – 13.784 | 81 | 3,24 |
| 8 | H | 13.785 – 14.845 | 1.061 | 42,44 ← terpanjang |
| 9 | **A** | 14.846 – 15.345 | 500 | 20,00 |
| 10 | H | 15.346 – 15.364 | **19** | **0,76** ← TERPENDEK |
| 11 | **A** | 15.365 – 15.765 | 401 | 16,04 |
| 12 | H | 15.766 – 15.798 | **33** | **1,32** |
| 13 | **A** | 15.799 – 15.888 | 90 | 3,60 |
| — | *D* | *15.889 – 16.399* | *511* | *20,44* ← terpanjang |
| 14 | **A** | 16.400 – 17.292 | 893 | 35,72 |
| 15 | H | 17.293 – 17.379 | 87 | 3,48 |
| — | *D* | *17.380 – 17.837* | *458* | *18,32* |
| 16 | **A** | 17.838 – 18.026 | 189 | 7,56 |
| — | *D* | *18.027 – 18.388* | *362* | *14,48* |
| 17 | H | 18.389 – 18.684 | 296 | 11,84 |

**Total: `H` 3.454 · `A` 2.577 · `D` 1.469 = 7.500 frame. Rata-rata possession 14,19 detik.** ✅

---

## Baris mentah di sekitar setiap transisi `D`

Diambil apa adanya dari file GT, biar kalian bisa lihat sendiri bahwa transisinya bersih — tidak ada
frame campuran, tidak ada gradasi.

```
12848,A          12986,D          18386,D          18682,H
12849,A          12987,D          18387,D          18683,H
12850,A          12988,D          18388,D          18684,H
12851,D          12989,H          18389,H          18685,X
12852,D          12990,H          18390,H          18686,X
12853,D          12991,H          18391,H          18687,X
```

Dan awal file, buat memastikan kalian benar-benar membaca baris yang sama:

```
frame,label
0,X
1,X
2,X
3,X
4,X
```

---

## Enam pertanyaan yang wajib dijawab Seat 1

Ini bukan daftar bacaan. Ini daftar **keputusan**. Jawabannya masuk ke `docs/possession-rules.md`,
dan Billa akan mengimplementasikannya.

### 1. Kenapa frame 12.851 `D`, dan kenapa 12.989 balik ke `H`?

Bola mati **5,5 detik** setelah possession `A` yang cuma 7,4 detik. Restart 5,5 detik kemudian
dikuasai `H`, bukan `A`. Artinya ini kemungkinan besar bukan pelanggaran `A` — mungkin tendangan gawang,
atau lemparan ke dalam dari pihak lain. Cek: apakah Smart Tagging punya fase di rentang 12.851–12.988?

### 2. Ada tiga bola mati panjang: 20,4 s, 18,3 s, dan 14,5 s. Apa ini?

Lemparan ke dalam biasanya 5–8 detik. **20 detik** itu bukan lemparan — itu cedera, pergantian pemain,
atau pemeriksaan VAR. Ini penting karena kalau kalian mengasumsikan "bola mati = pendek", detektor
kalian akan salah di tiga momen paling mencolok di jendela ini. **Dan tiga momen ini 1.331 frame —
17,7% dari seluruh jendela dinilai.**

### 3. ⚠️ Possession 19 frame itu nyata. Apa artinya untuk minimum spell kita?

Ini temuan paling penting di lembar ini, dan bisa langsung menyelamatkan skor kalian:

> Possession terpendek di GT adalah **19 frame (0,76 detik)** — dan itu **possession sungguhan**,
> bukan artefak. Yang kedua terpendek 33 frame (1,32 detik).

Artinya: **scorer tidak menggabungkan possession pendek.** Kalau kalian memasang minimum spell yang
terlalu agresif — misalnya "gabungkan apa pun di bawah 1 detik" atau "buang di bawah 30 frame" —
kalian akan **menghapus possession yang benar-benar ada**, dan setiap possession yang hilang ≈ **6 poin**
`spellF1` di jendela ini.

**Jadi minimum spell kalian harus konservatif**, dan itu berlawanan dengan insting. Jawab: berapa
ambang yang kalian pilih, dan kenapa. (Petunjuk: `baseline_raw` melaporkan **131 possession** untuk 5
menit ini; kebenarannya **17**.)

### 4. Aturan `D` vs aturan `H`/`A` — mana yang lebih menentukan?

Perhatikan komposisinya: `H` 46%, `A` 34%, `D` **20%**. Kelas `D` mengambil 20% frame dan 4 segmen
(1.469 frame). Kalau detektor `D` kalian meleset, kesalahannya langsung membelah possession di
sebelah-sebelahnya — artinya satu kesalahan `D` bisa merusak **tiga** possession sekaligus (dua yang
dipotong, satu yang dibuat-buat). Tuliskan ini sebagai aturan eksplisit.

### 5. Kapan sistem boleh menulis `X`?

Polanya dari `EVALUATION.md`:

| Situasi | Tindakan | Alasan |
|---|---|---|
| Bola hilang **di tengah** possession | Tulis `X` | Scorer mengisi `X` dengan label terakhir → possession tetap **satu**. Gratis |
| Di titik **hand-over** | **Wajib menebak** | `X` menarik label lama ke wilayah tim lawan. Mahal sekali |
| Di luar jendela dinilai | `X` | Tidak dihitung sama sekali |

Pertanyaan yang harus kalian jawab: **bagaimana sistem tahu ia sedang di tengah possession atau di
titik hand-over?** Itu pertanyaan teknis sekaligus pertanyaan sepak bola — dan itu sebabnya seat ini
ada.

### 6. Bola ada di 59,3% frame dinilai. Sisanya ke mana?

Kalian punya `ball_x`, `ball_y` di 94.214 frame dinilai, dan **tidak ada di 64.643 frame lainnya**.
Tidak ada indikator kepercayaan, tidak ada flag. `DATA.md`: hilangnya *"disproportionately on the frames
that matter."*

Pertanyaan: dari 4 segmen `D` di jendela ini, **berapa banyak yang punya gap bola beruntun
di dalamnya?** Kalau korelasinya kuat, gap bola itu sendiri adalah fitur `D` terkuat yang kalian punya
— dan itu gratis. Kalau lemah, artinya bola mati justru terjadi **saat bola terdeteksi** (bola
menggelinding keluar, atau diam di titik pelanggaran), dan itu masalah yang jauh lebih sulit.

---

## Cara mengisi lembar ini

1. Jalankan `python tools/fetch_official.py`, lalu `python run.py --placeholder` dan
   `python tools/gate0.py` untuk memastikan rantainya jalan dan GT publiknya terbaca.
2. Plot bola per frame di rentang 11.185–18.684, warnai latar belakangnya dengan label GT.
3. Untuk setiap transisi `D`: lihat 2 detik sebelum dan sesudah. Tanya *"apa yang terjadi di sini?"*
4. **Tulis jawabannya, bukan kesimpulannya.** "Pemain berhenti dan bola diam" lebih berguna untuk Billa
   daripada "bola mati".
5. Setiap temuan yang bisa dikodekan → `docs/possession-rules.md`.
6. Setiap temuan yang ambigu → `docs/decisions.md` sebagai keputusan dengan alasannya.

**Jangan** mengisi kolom Alasan dengan ingatan soal pertandingan aslinya. Kalau kalian ingat ada
pelanggaran di menit 20, itu tidak boleh masuk. Yang boleh masuk: apa yang kalian **lihat di plot dan
di data**. Lihat `PLAYBOOK.md` §9.
