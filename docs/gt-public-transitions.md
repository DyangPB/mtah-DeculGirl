# Lembar Kerja — 21 Transisi di 5 Menit GT Publik

**Pemilik: Seat 1 (Dyang).** Ini pekerjaan hari pertama, dan paling menentukan seluruh 25 hari
berikutnya.

Sumber: `evaluation/gt/BAR-ATH_possession_gt_public.csv` dari repo resmi (commit `f8f2629`).
Jendela yang dinilai: **frame 11.185 – 18.684** (7.500 frame). Di luar jendela itu labelnya `X`.

Semua angka di bawah sudah **dicocokkan silang** dengan `BAR-ATH_possession_gt_public_meta.json`:
jumlah `H` = 3.454, `A` = 2.577, `D` = 1.469, total = 7.500. Semuanya cocok.

---

## Kenapa lembar ini ada

`CHALLENGE.md` menyatakan bahwa GT-nya **bukan penilaian manusia**. GT diturunkan secara mekanis dari
data *corrected tracking* (tracking yang sudah dikoreksi) yang tidak kita pegang. Yang kita punya hanya
5 menit itu. Jadi pekerjaan pertama bukan "membangun model", melainkan **merekonstruksi cara kerja
tracking terkoreksi itu dari 21 titik transisi**.

Hanya ada 21 transisi untuk seluruh 5 menit. Membacanya cuma butuh lima menit kalau kalian tahu apa yang
dicari, tetapi bisa menghabiskan seharian kalau mulai dari "buka CSV lalu lihat-lihat saja".

---

## Tabel 1 — 21 transisi, berurutan

Kolom **Alasan** diisi manual oleh Seat 1. Kolom **Sinyal** diisi dengan dugaan fitur yang bisa
mendeteksinya. Isi kolom itu nanti diteruskan ke Billa (§7.1 playbook).

| # | Frame | Transisi | Detik (±) | Alasan (diisi) | Sinyal / fitur (diisi) |
|---|---|---|---|---|---|
| 1 | 11.185 | `X → A` | 447,4 | awal jendela yang dinilai, bukan transisi sungguhan | — |
| 2 | 11.351 | `A → H` | 454,0 | | |
| 3 | 11.553 | `H → A` | 462,1 | | |
| 4 | 11.624 | `A → H` | 465,0 | | |
| 5 | 12.665 | `H → A` | 506,6 | | |
| 6 | **12.851** | **`A → D`** | 514,0 | | |
| 7 | **12.989** | **`D → H`** | 519,6 | | |
| 8 | 13.704 | `H → A` | 548,2 | | |
| 9 | 13.785 | `A → H` | 551,4 | | |
| 10 | 14.846 | `H → A` | 593,8 | | |
| 11 | 15.346 | `A → H` | 613,8 | ⚠️ possession hanya **19 frame (0,76 detik)** | |
| 12 | 15.365 | `H → A` | 614,6 | | |
| 13 | 15.766 | `A → H` | 630,6 | ⚠️ possession hanya **33 frame (1,32 detik)** | |
| 14 | 15.799 | `H → A` | 632,0 | | |
| 15 | **15.889** | **`A → D`** | 635,6 | | |
| 16 | **16.400** | **`D → A`** | 656,0 | ⚠️ bola mati **511 frame = 20,4 detik** | |
| 17 | 17.293 | `A → H` | 691,7 | | |
| 18 | **17.380** | **`H → D`** | 695,2 | | |
| 19 | **17.838** | **`D → A`** | 713,5 | ⚠️ bola mati **458 frame = 18,3 detik** | |
| 20 | **18.027** | **`A → D`** | 721,1 | | |
| 21 | **18.389** | **`D → H`** | 735,6 | ⚠️ bola mati **362 frame = 14,5 detik** | |
| — | 18.685 | `H → X` | 747,4 | akhir jendela yang dinilai, bukan transisi sungguhan | |

---

## Tabel 2 — 17 possession yang sebenarnya

Inilah yang dibandingkan oleh `spellF1`. Perhatikan durasinya: **dua possession terpanjang (41,6 detik dan
42,4 detik) dan dua possession terpendek (0,76 detik dan 1,32 detik) dihitung sama beratnya.** Satu
possession dihitung sebagai satu objek. Itulah sebabnya metrik ini mengukur seberapa terpecah-pecah
possession kita.

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

**Total: `H` 3.454 · `A` 2.577 · `D` 1.469 = 7.500 frame. Rata-rata durasi possession 14,19 detik.** ✅

---

## Baris mentah di sekitar setiap transisi `D`

Diambil apa adanya dari file GT, supaya kalian bisa melihat sendiri bahwa transisinya bersih: tidak ada
frame campuran dan tidak ada perubahan bertahap.

```
12848,A          12986,D          18386,D          18682,H
12849,A          12987,D          18387,D          18683,H
12850,A          12988,D          18388,D          18684,H
12851,D          12989,H          18389,H          18685,X
12852,D          12990,H          18390,H          18686,X
12853,D          12991,H          18391,H          18687,X
```

Dan awal file, untuk memastikan kalian benar-benar membaca baris yang sama:

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

Ini bukan daftar bacaan. Ini daftar **keputusan**. Jawabannya dimasukkan ke `docs/possession-rules.md`,
lalu Billa yang membuat kodenya.

### 1. Kenapa frame 12.851 berlabel `D`, dan kenapa frame 12.989 kembali ke `H`?

Bola mati **5,5 detik** setelah possession `A` yang hanya berlangsung 7,4 detik. Permainan dimulai
kembali 5,5 detik kemudian dan dikuasai `H`, bukan `A`. Artinya, kemungkinan besar ini bukan pelanggaran
oleh `A`. Bisa jadi tendangan gawang, atau lemparan ke dalam oleh pihak lawan. Periksa: apakah Smart
Tagging punya fase di rentang 12.851–12.988?

### 2. Ada tiga bola mati yang panjang: 20,4 detik, 18,3 detik, dan 14,5 detik. Apa ini?

Lemparan ke dalam biasanya hanya 5–8 detik. **20 detik** bukan lemparan ke dalam. Itu kemungkinan
cedera, pergantian pemain, atau pemeriksaan VAR. Ini penting, karena kalau kalian menganggap "bola mati
itu pasti sebentar", pendeteksi kalian akan salah di tiga momen yang paling mencolok di jendela ini.
**Ketiga momen ini berjumlah 1.331 frame, atau 17,7% dari seluruh jendela yang dinilai.**

### 3. ⚠️ Possession sependek 19 frame itu nyata. Apa artinya bagi batas minimum possession kita?

Ini temuan terpenting di lembar ini, dan bisa langsung menyelamatkan skor kalian:

> Possession terpendek di GT adalah **19 frame (0,76 detik)**, dan itu **possession yang sungguhan**,
> bukan kesalahan data. Yang terpendek kedua 33 frame (1,32 detik).

Artinya, **scorer tidak menggabungkan possession yang pendek.** Kalau kalian memasang batas minimum yang
terlalu agresif, misalnya "gabungkan apa pun yang di bawah 1 detik" atau "buang yang di bawah 30
frame", kalian akan **menghapus possession yang benar-benar ada**, dan setiap possession yang hilang ≈
**6 poin** `spellF1` di jendela ini.

**Jadi batas minimum kalian harus konservatif**, dan itu berlawanan dengan naluri. Jawab: berapa batas
yang kalian pilih, dan kenapa. (Petunjuk: `baseline_raw` melaporkan **131 possession** untuk 5 menit
ini, padahal yang benar **17**.)

### 4. Aturan `D` atau aturan `H`/`A` — mana yang lebih menentukan?

Perhatikan komposisinya: `H` 46%, `A` 34%, `D` **20%**. Kelas `D` mengambil 20% frame dan hanya 4 segmen
(1.469 frame). Kalau pendeteksi `D` kalian meleset, kesalahannya langsung memecah possession di kedua
sisinya. Satu kesalahan `D` bisa merusak **tiga** possession sekaligus: dua yang terpotong dan satu yang
muncul begitu saja. Tuliskan ini sebagai aturan yang eksplisit.

### 5. Kapan sistem boleh menulis `X`?

Polanya diambil dari `EVALUATION.md`:

| Situasi | Tindakan | Alasan |
|---|---|---|
| Bola hilang **di tengah** possession | Tulis `X` | Scorer mengganti `X` dengan label terakhir, sehingga possession tetap **satu**. Tidak merugikan |
| Saat **possession berpindah ke tim lawan** | **Wajib menebak** | `X` menarik label lama ke wilayah tim lawan. Sangat merugikan |
| Di luar jendela yang dinilai | `X` | Tidak dihitung |

Pertanyaan yang harus kalian jawab: **bagaimana sistem tahu bahwa ia sedang berada di tengah possession
atau saat possession berpindah?** Ini pertanyaan teknis sekaligus pertanyaan sepak bola, dan itulah
alasan seat ini ada.

### 6. Bola terdeteksi di 59,3% frame yang dinilai. Ke mana sisanya?

Kalian punya `ball_x` dan `ball_y` di 94.214 frame yang dinilai, dan **tidak ada di 64.643 frame
lainnya**. Tidak ada indikator tingkat keyakinan dan tidak ada penanda apa pun. `DATA.md` menyebut bola
hilang *"disproportionately on the frames that matter"* (tidak seimbang: lebih sering di frame yang
penting).

Pertanyaannya: dari 4 segmen `D` di jendela ini, **berapa yang memiliki celah bola yang hilang berturut-turut
di dalamnya?** Kalau hubungannya kuat, celah bola itu sendiri adalah fitur `D` terkuat yang kalian
punya, dan didapat gratis. Kalau lemah, artinya bola mati justru terjadi **saat bola masih terdeteksi**
(bola menggelinding keluar, atau diam di titik pelanggaran), dan itu masalah yang jauh lebih sulit.

---

## Cara mengisi lembar ini

1. Jalankan `python tools/fetch_official.py`, lalu `python run.py --placeholder` dan
   `python tools/gate0.py` untuk memastikan rangkaiannya berjalan dan GT publiknya terbaca.
2. Gambar grafik posisi bola per frame di rentang 11.185–18.684, dengan warna latar belakang sesuai
   label GT.
3. Untuk setiap transisi `D`: lihat 2 detik sebelum dan sesudahnya. Tanyakan *"apa yang terjadi di
   sini?"*
4. **Tulis apa yang kalian amati, bukan kesimpulannya.** "Pemain berhenti dan bola diam" lebih berguna
   bagi Billa daripada "bola mati".
5. Setiap temuan yang bisa dijadikan kode → masukkan ke `docs/possession-rules.md`.
6. Setiap temuan yang masih meragukan → catat di `docs/decisions.md` sebagai keputusan, lengkap dengan
   alasannya.

**Jangan** mengisi kolom Alasan dengan ingatan tentang pertandingan aslinya. Kalau kalian ingat ada
pelanggaran di menit ke-20, itu tidak boleh dimasukkan. Yang boleh hanya apa yang kalian **lihat di
grafik dan di data**. Lihat `PLAYBOOK.md` §9.
