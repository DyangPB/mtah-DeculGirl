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

*[Isi setelah membedah GT publik. Pertanyaan yang harus dijawab: tanda paling awal apa yang tersedia di
data untuk membedakan keduanya?]*

**R-2.1** Bola hidup ketika ...

**R-2.2** Bola mati ketika ...

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

**R-3.1** *[Pilih satu definisi dan tulis di sini. Definisi itu harus bisa dihitung dari koordinat dan
kecepatan, karena kita tidak punya data event. Ingat: tidak boleh memakai data event dari luar dalam
bentuk apa pun.]*

**R-3.2** Yang **bukan** pergantian possession (dari `CHALLENGE.md`):

- sentuhan sekilas tanpa kontrol
- operan yang hanya membelok (defleksi) tanpa berhasil dipotong
- duel udara yang dimenangkan tanpa kontrol lanjutan oleh tim yang menang

**R-3.3** *[Bagaimana ketiga hal itu dikenali hanya dari data tracking? Ini pertanyaan tersulit di
dokumen ini, dan jawabannya kemungkinan besar "tidak selalu bisa". Kalau begitu, tulis apa adanya, lalu
jelaskan apa yang dilakukan sistem saat tidak bisa mengenalinya.]*

---

## 4. Possession harus bertahan

Possession adalah **keadaan yang bertahan**, bukan keputusan yang dibuat terpisah di setiap frame.
Sebuah frame berlabel `H` sebagian besar karena frame sebelumnya `H`.

**R-4.1** *[Berapa lama possession bertahan setelah bukti terakhir yang mendukungnya? Ini parameter yang
paling memengaruhi `spellF1`, karena menentukan seberapa sering possession terpecah.]*

**R-4.2** *[Apa yang bisa mengalahkan kecenderungan bertahan itu? Dengan kata lain, seberapa kuat bukti
yang dibutuhkan untuk membalik `H` menjadi `A`? Petunjuk: perpindahan ini harus MAHAL, karena setiap
perpindahan yang salah menghasilkan dua possession yang cacat.]*

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

**R-5.1** Bagaimana sistem tahu bahwa ia sedang **di tengah possession** dan bukan **saat possession
berpindah ke tim lawan**? *[Ini pertanyaan inti seat ini. Jawabannya menentukan kebijakan tidak-menjawab
untuk seluruh sistem.]*

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

**R-6.1** Batas minimum panjang possession yang kami pilih: ______ frame. Alasan: ______

**R-6.2** Potongan yang lebih pendek dari batas itu dibuang, atau digabung ke possession di sebelahnya? ______

**R-6.3** Bolehkah penggabungan melintasi tim (`H → A`)? ______ *[Hati-hati: menggabungkan dua
possession dari tim yang berbeda menjadi satu pasti selalu salah.]*

---

## 7. Kasus yang belum diputuskan

Setiap kali Billa menemukan keadaan yang tidak tercakup di atas, **jangan berimprovisasi di kode**.
Tulis dulu di sini, lalu putuskan bersama.

| # | Kasus | Contoh frame | Keputusan | Tanggal |
|---|---|---|---|---|
| | | | | |

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
