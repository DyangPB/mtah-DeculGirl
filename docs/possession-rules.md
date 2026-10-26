# Aturan Possession — DeculGirl

**Pemilik: Seat 1 (Dyang)** · Ditinjau oleh: Seat 3 (Billa) · Status: `DRAFT`

> Ini dokumen terpenting di repo ini. Tugasnya hanya satu: **memindahkan pemahaman tentang sepak bola
> dari kepala Dyang ke dalam repo**, supaya Billa bisa membuat kodenya tanpa harus bertanya lagi.
>
> Kalau Billa masih harus bertanya "maksudnya apa?", berarti dokumen ini belum selesai. Penyebabnya
> bukan Billa kurang paham, melainkan kalimatnya belum cukup jelas.

**Cara mengisi:** setiap aturan harus bisa ditulis dalam bentuk `jika ... maka ...`, dan setiap aturan
harus punya nomor. Nomor itu dipakai di pesan commit dan di `docs/decisions.md`, sehingga kalau ada
yang berubah, kita tahu persis apa yang berubah.

---

## 1. Ruang lingkup

Hanya ada tiga keadaan. Tidak ada "diperebutkan", tidak ada "peralihan", dan tidak ada "tidak diketahui".

| Label | Definisi yang bisa diterapkan dalam kode |
|---|---|
| `H` | Barcelona menguasai bola **dan** bola hidup |
| `A` | Athletic menguasai bola **dan** bola hidup |
| `D` | Bola mati |

`X` bukan keadaan keempat. `X` adalah keputusan sistem untuk tidak menjawab. Lihat bagian 5.

**Yang sengaja tidak ditanyakan:** siapa yang memegang bola saat bola mati. Data tracking tetap
menyebut satu tim saat bola keluar lapangan (misalnya tim yang akan memulai kembali permainan, atau
tim yang terakhir menyentuh bola). Namun ground truth membuang informasi itu. Saat bola mati, jawabannya
`D`. Titik.

---

## 2. Arti "bola hidup" dan "bola mati"

> **Status bagian ini: HIPOTESIS.** R-2.1 dan R-2.2 berasal dari pemahaman umum tentang sepak bola,
> belum diverifikasi ke data tracking, karena bundle ATD belum diunduh. Verifikasinya: buka tracking di
> sekitar tiap blok `D` pada GT publik (lihat `docs/gt-public-transitions.md`), lalu ubah atau buang
> aturan yang tidak cocok. Semua angka ambang ada di tabel parameter di akhir bagian 6.

**R-2.1** Jika bola terdeteksi, bergerak dengan kecepatan di atas `v_diam`, dan ada pemain dalam
jarak `d_kontrol` darinya atau sedang bergerak antar pemain, maka bola **hidup**.

**R-2.2** Bola **mati** jika salah satu syarat ini terpenuhi:

- (a) posisi bola berada di luar batas lapangan (di luar rentang koordinat 0–1) → `D`
- (b) kecepatan bola di bawah `v_diam` selama sedikitnya `T_diam` frame berturut-turut, dan pemain
  di sekitarnya bergerak pelan atau tersebar (ciri bola dipasang untuk tendangan bebas, gawang, atau
  lemparan) → `D`

Bola yang tidak terdeteksi **bukan** bukti bola mati. Lihat R-5.1.

**R-2.3** ⚠️ **Bola mati tidak selalu sebentar.** Di 5 menit GT publik ada tiga bola mati yang
berlangsung **20,4 detik**, **18,3 detik**, dan **14,5 detik**, dengan total 17,7% dari jendela yang
dinilai. Lemparan ke dalam yang normal hanya 5–8 detik, jadi bola mati sepanjang itu kemungkinan besar
karena cedera, pergantian pemain, atau pemeriksaan VAR. Aturan apa pun yang berbunyi "bola akan segera
hidup kembali" **salah**, dan akan merusak tiga momen yang paling mencolok di jendela itu.

**R-2.4** Bobot tiap kelas: `H` 46%, `A` 34%, `D` 20% dari frame yang dinilai. Kelas `D` hanya **4
segmen** dari 21, tetapi berisi 1.469 frame. Artinya, satu kesalahan pada `D` merusak **tiga**
possession sekaligus: dua yang terpotong dan satu yang muncul begitu saja. Perlakukan `D` sebagai kelas
dengan risiko tertinggi.

---

## 3. Arti "menguasai bola"

`CHALLENGE.md` mengakui bahwa bagian ini kurang jelas, dan menawarkan dua pendekatan:

- pemain menahan bola selama beberapa detik
- satu tim menyelesaikan lebih dari dua operan berturut-turut

**R-3.1** Kami memilih definisi pertama: **pemain menahan bola**. Definisi "lebih dari dua operan"
ditolak karena butuh mendeteksi operan, dan itu berarti membangun data event, yang tidak kita punya.

Satu tim **menguasai** bola pada sebuah frame jika:

- pemain terdekat ke bola berasal dari tim itu, **dan**
- jaraknya ke bola `<= d_kontrol`, **dan**
- kondisi itu bertahan sedikitnya `K_kontrol` frame berturut-turut.

Jarak dihitung dalam meter (koordinat 0–1 dikali ukuran lapangan 105,3 × 68,0). Untuk membandingkan dua
tim, pakai jarak 2–3 pemain terdekat dari tiap tim, bukan hanya satu pemain terdekat secara keseluruhan.
Pemain yang bergerak **menuju** bola lebih diutamakan daripada yang kebetulan lewat.

**R-3.2** Yang **bukan** pergantian possession (dari `CHALLENGE.md`):

- sentuhan sekilas tanpa kontrol
- operan yang hanya membelok (defleksi) tanpa berhasil dipotong
- duel udara yang dimenangkan tanpa kontrol lanjutan oleh tim yang menang

**R-3.3** Dari data tracking, ketiga hal itu tidak selalu bisa dikenali.

| Hal | Bisa dikenali? | Yang dilakukan sistem |
|---|---|---|
| Sentuhan sekilas | Sebagian. Kontaknya lebih pendek dari `K_kontrol` | Diabaikan oleh R-3.1 |
| Defleksi | Sebagian. Bola lewat dengan kecepatan tinggi tanpa melambat | Tidak dihitung sebagai kontrol |
| Duel udara | **Tidak.** Koordinat bola tidak menyimpan ketinggian | Label lama dipertahankan (R-4.1) sampai bukti tim baru bertahan `N_pindah` frame |

Dengan kata lain: sistem tidak berusaha mengenali duel udara. Ia hanya menolak berpindah terlalu cepat.

---

## 4. Possession harus bertahan

Possession adalah **keadaan yang bertahan**, bukan keputusan yang dibuat terpisah di setiap frame.
Sebuah frame berlabel `H` sebagian besar karena frame sebelumnya `H`.

**R-4.1** Jika tidak ada bukti yang cukup dari tim lawan, maka label **tetap sama** dengan frame
sebelumnya, tanpa batas waktu. Possession tidak berakhir karena waktu, hanya karena bukti tim lawan
(R-4.2) atau bola mati (R-2.2). Saat dua tim berimbang jaraknya (selisih di bawah `margin_jarak`),
pemilik sebelumnya dipertahankan.

**R-4.2** Jika kandidat dari tim lawan (menurut R-3.1) muncul **terus-menerus selama `N_pindah`
frame**, maka label berpindah. Satu frame atau beberapa frame yang terputus tidak cukup. `N_pindah`
harus **di bawah 19**, karena possession asli terpendek di GT publik adalah 19 frame.

**R-4.3** Saat perpindahan sudah terkonfirmasi oleh R-4.2, awal possession baru **dimundurkan ke frame
pertama dari rangkaian bukti**, bukan ke frame konfirmasi. Tanpa ini, setiap perpindahan terlambat
`N_pindah` frame, dan possession pendek (misalnya 19 frame) kehilangan separuh isinya sehingga IoU-nya
jatuh di bawah ambang. Ini aman karena pemrosesan dilakukan offline atas seluruh pertandingan.

---

## 5. Kebijakan `X`

Scorer mengganti setiap `X` dengan label terakhir yang bukan `X` **di babak yang sama**, sebelum
possession disusun. Jadi `H H H X X X H H H` dihitung sebagai **satu** possession `H` sepanjang sembilan
frame.

**`X` bukan tombol menyerah. `X` adalah tombol "sama seperti sebelumnya".**

| Situasi | Tindakan | Alasan |
|---|---|---|
| Bola hilang **di tengah** possession | `X` | Tidak merugikan. Possession tetap utuh. Lebih aman daripada tebakan yang bisa memecahnya |
| Saat **possession berpindah ke tim lawan** | **Wajib menebak** | `X` menarik label lama ke wilayah tim lawan, dan itu sangat merugikan |
| Di luar jendela yang dinilai (frame < 11.185, jeda, > 190.197) | `X` | Sama sekali tidak dihitung |

**R-5.1** Sistem tahu ia di tengah possession atau saat berpindah dengan **membandingkan dua ujung
celah** (periode bola tidak terdeteksi):

- Ambil pemilik **sebelum** celah (`T_sebelum`) dan kandidat pertama **sesudah** celah (`T_sesudah`).
- Jika `T_sebelum == T_sesudah` → tulis `X` untuk seluruh celah. Itu di tengah possession.
- Jika `T_sebelum != T_sesudah` → perpindahan terjadi **di dalam** celah. Wajib menebak. Sementara,
  frame di paruh pertama celah diberi `T_sebelum` dan paruh kedua `T_sesudah` (titik tengah celah).
- Jika salah satu ujung tidak punya pemilik (misalnya awal babak) → tulis `X`.

Titik tengah adalah tebakan paling lemah di dokumen ini. Dicatat di bagian 7 supaya diperbaiki lebih
dulu begitu ada data posisi pemain sekitar celah yang bisa dipakai.

**R-5.2** Catatan biaya: `macroF1` menghitung `X` sebagai salah, tetapi `macroF1` hanya pemutus kalau
seri. `spellF1`, yang menentukan peringkat, tidak pernah melihatnya. Jadi `X` itu murah, dan tidak ada
alasan untuk pelit memakainya.

---

## 6. Panjang minimum possession ⚠️

**Temuan yang bisa langsung menyelamatkan skor kalian:**

> Possession terpendek di GT publik adalah **19 frame (0,76 detik)**, dan itu possession **yang
> sungguhan**. Possession terpendek kedua adalah 33 frame (1,32 detik).

Scorer **tidak** menggabungkan possession yang pendek. Kalau kalian memasang batas minimum yang agresif,
misalnya "gabungkan apa pun yang di bawah 1 detik" atau "buang yang di bawah 30 frame", kalian akan
**menghapus possession yang memang ada**. Satu possession yang hilang ≈ **6 poin** `spellF1` di jendela
ini.

Sebagai perbandingan, `baseline_raw` melaporkan **131 possession** untuk 5 menit ini, padahal yang benar
**17**.

**R-6.1** Batas minimum panjang possession yang kami pilih: **12 frame (0,48 detik)**. Alasan: harus
jauh di bawah 19 frame supaya possession pendek yang nyata tidak terhapus, tetapi cukup besar untuk
membuang kedipan 1–5 frame akibat pemain yang kebetulan lewat.

**R-6.2** Potongan yang lebih pendek dari batas itu **digabung**, bukan dibuang, dan hanya jika
diapit dua possession dari tim yang sama (pola `H A H` menjadi `H H H`). Jika diapit tim yang berbeda
atau oleh `D`, potongan itu **dibiarkan**.

**R-6.3** Penggabungan **tidak boleh melintasi tim**. Dua possession `H` dan `A` yang bersebelahan
tidak pernah digabung. Pada pola `H A H`, yang berubah hanya potongan `A` yang pendek. Bola mati `D`
tidak pernah diubah.

**Tabel parameter.** Semua angka di bawah ini adalah **titik awal berbasis penalaran, belum
diverifikasi**. Jangan disetel memakai skor 5 menit publik (hanya 17 possession; satu possession
meleset ≈ 6 poin). Verifikasi dengan pemeriksaan yang tidak butuh jawaban benar: jumlah possession
yang dilaporkan (baseline melaporkan 131 untuk 5 menit; yang benar 17), jumlah potongan di bawah 19
frame, dan perpindahan `H → A` yang tidak didukung data.

| Parameter | Titik awal | Dipakai di | Dasar |
|---|---|---|---|
| `d_kontrol` | ±2 m | R-2.1, R-3.1 | Jangkauan wajar pemain mengontrol bola. Perlu dilihat di data |
| `K_kontrol` | 5 frame (0,2 detik) | R-3.1 | Menyaring sentuhan sekilas |
| `N_pindah` | 10 frame (0,4 detik) | R-4.2 | Harus < 19 |
| `margin_jarak` | ±1 m | R-4.1 | Di bawah ini dianggap berimbang |
| `v_diam` | ±1 m/s | R-2.1, R-2.2 | Bola nyaris diam. Cek ke blok `D` pada GT |
| `T_diam` | 25 frame (1 detik) | R-2.2 | Membedakan bola diam sungguhan dari jeda sesaat |
| `min_possession` | 12 frame | R-6.1 | Harus jauh < 19 |

---

## 7. Kasus yang belum diputuskan

Setiap kali Billa menemukan keadaan yang tidak tercakup di atas, **jangan berimprovisasi di kode**.
Tulis dulu di sini, lalu putuskan bersama.

| # | Kasus | Contoh frame | Keputusan | Tanggal |
|---|---|---|---|---|
| 1 | Perpindahan tim terjadi di dalam celah bola hilang: di mana batasnya? | *(cari di data)* | Sementara titik tengah celah (R-5.1). **Belum diputuskan**; diperbaiki lebih dulu | 26 Okt 2026 |
| 2 | Duel udara: tidak bisa dikenali dari koordinat | *(cari di data)* | Tidak dikenali; dipertahankan lewat R-4.1 dan R-4.2 | 26 Okt 2026 |
| 3 | Dua tim berimbang jaraknya ke bola | *(cari di data)* | Pertahankan pemilik sebelumnya (R-4.1) | 26 Okt 2026 |
| 4 | Awal babak atau setelah bola mati: belum ada pemilik sebelumnya | *(cari di data)* | Pakai kandidat pertama yang memenuhi R-3.1 | 26 Okt 2026 |
| 5 | Bola mati yang panjang (14–20 detik) dengan bola masih terdeteksi | *(cari di GT publik)* | **Belum diputuskan.** R-2.2(b) mungkin tidak menangkapnya; periksa dulu di data | 26 Okt 2026 |

---

## 8. Batas kepatuhan

Aturan di dokumen ini **tidak boleh** berasal dari:

- ❌ ingatan siapa pun tentang pertandingan Barça–Athletic yang asli
- ❌ laporan pertandingan, berita, atau ringkasan apa pun
- ❌ data event dari penyedia mana pun (Opta, StatsBomb, Wyscout, LaLiga, atau siapa pun)
- ❌ anotasi manual pada frame mana pun

Sumber yang **boleh**: **data tracking, Smart Tagging, dan homography yang diberikan · 5 menit GT publik ·
pemahaman umum tentang cara kerja sepak bola.**

Kalau ada aturan yang terasa "berasal dari ingatan", catat di `docs/decisions.md` dan tanyakan lewat
issue resmi sebelum dipakai. `FAQ.md` mengundang hal itu secara terbuka:

> *"If a rule is unclear or your approach sits near a line, ask before you build on it."*
> (Kalau sebuah aturan kurang jelas atau pendekatanmu mendekati batas, bertanyalah sebelum kamu
> membangun di atasnya.)
