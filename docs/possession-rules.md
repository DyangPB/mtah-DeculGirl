# Aturan Possession — DeculGirl

**Pemilik: Seat 1 (Dyang)** · Ditinjau: Seat 3 (Billa) · Status: `DRAFT`

> Ini dokumen yang paling penting di repo ini. Tugasnya satu: **memindahkan pemahaman bola dari kepala
> Dyang ke dalam repo**, supaya Billa bisa mengimplementasikannya tanpa bertanya lagi.
>
> Kalau Billa masih harus bertanya "ini maksudnya apa?", dokumen ini belum selesai — bukan karena
> Billa kurang paham, tapi karena kalimatnya belum cukup tajam.

**Cara mengisi:** setiap aturan harus bisa ditulis sebagai `jika ... maka ...`, dan setiap aturan harus
punya nomor. Nomor itu dipakai di pesan commit dan di `docs/decisions.md`, supaya kalau ada yang berubah
kita tahu apa yang berubah.

---

## 1. Ruang lingkup

Tiga state saja. Tidak ada "contested", tidak ada "transisi", tidak ada "tidak diketahui".

| Label | Definisi operasional |
|---|---|
| `H` | Barcelona menguasai bola **dan** bola hidup |
| `A` | Athletic menguasai bola **dan** bola hidup |
| `D` | Bola mati |

`X` bukan state keempat — `X` adalah keputusan sistem untuk tidak menjawab. Lihat §5.

**Yang sengaja tidak ditanyakan:** kepemilikan bola saat bola mati. Tracking akan tetap menamai satu
tim bahkan saat bola keluar (siapa yang akan me-restart, atau yang terakhir menyentuh), tapi GT
membuang informasi itu. Saat bola mati, jawabannya `D`. Titik.

---

## 2. Definisi "bola hidup" dan "bola mati"

*[Isi setelah membedah GT publik. Yang harus dijawab: apa bukti paling awal yang tersedia di data
untuk memisahkan keduanya?]*

**R-2.1** Bola hidup ketika ...

**R-2.2** Bola mati ketika ...

**R-2.3** ⚠️ **Bola mati tidak selalu pendek.** Di 5 menit GT publik ada tiga bola mati berdurasi
**20,4 detik**, **18,3 detik**, dan **14,5 detik** — totalnya 17,7% jendela dinilai. Lemparan ke dalam
normal cuma 5–8 detik, jadi rentang sepanjang ini kemungkinan besar cedera, pergantian pemain, atau
VAR. Aturan apa pun yang berbunyi "bola akan segera hidup kembali" **salah** dan merusak tiga momen
paling mencolok di jendela itu.

**R-2.4** Bobot kelas: `H` 46%, `A` 34%, `D` 20% dari frame dinilai. Kelas `D` cuma **4 segmen** dari
21, tapi 1.469 frame. Artinya satu kesalahan `D` merusak **tiga** possession sekaligus — dua yang
terpotong dan satu yang tercipta dari ketiadaan. Perlakukan `D` sebagai kelas berisiko tertinggi.

---

## 3. Definisi "menguasai bola"

`CHALLENGE.md` menyebut ini bagian yang ambigu, dan menawarkan proxy:

- pemain menahan bola selama beberapa detik
- sebuah tim menyelesaikan lebih dari dua operan berturut-turut

**R-3.1** *[Pilih satu definisi operasional dan tulis di sini. Harus bisa dihitung dari koordinat +
kecepatan, karena tidak ada data event. Ingat: tidak boleh memakai data event eksternal apa pun.]*

**R-3.2** Yang **bukan** perubahan possession — dari `CHALLENGE.md`:

- sentuhan sekilas tanpa kontrol
- defleksi operan yang tidak memotongnya
- duel udara yang dimenangkan tanpa kontrol lanjutan oleh tim itu

**R-3.3** *[Bagaimana ketiga hal itu dikenali dari tracking saja? Ini pertanyaan tersulit di dokumen ini,
dan jawabannya kemungkinan besar "tidak selalu bisa" — kalau begitu, tulis itu, dan jelaskan apa yang
dilakukan sistem saat tidak bisa.]*

---

## 4. Kemampuan bertahan possession

Possession adalah **state yang bertahan**, bukan keputusan per frame. Frame ini `H` sebagian besar karena
frame sebelumnya `H`.

**R-4.1** *[Berapa lama possession bertahan setelah bukti terakhir mendukungnya? Ini parameter yang
paling berpengaruh pada `spellF1` — karena ia yang menentukan seberapa sering possession terpecah.]*

**R-4.2** *[Apa yang mengalahkan persistensi? Dengan kata lain, bukti sekuat apa yang dibutuhkan untuk
membalik `H` → `A`? Petunjuk: perpindahan ini harus MAHAL, karena setiap perpindahan yang salah
menghasilkan dua possession cacat.]*

---

## 5. Kebijakan `X`

Scorer mengganti setiap `X` dengan label non-`X` terakhir **di babak yang sama**, sebelum possession
disusun. Jadi `H H H X X X H H H` dihitung sebagai **satu** possession `H` sepanjang sembilan frame.

**`X` bukan tombol menyerah. `X` adalah tombol "sama seperti sebelumnya".**

| Situasi | Tindakan | Alasan |
|---|---|---|
| Bola hilang **di tengah** possession | `X` | Gratis. Possession tetap utuh. Lebih aman dari tebakan yang bisa memecahnya |
| Di titik **hand-over** | **Wajib menebak** | `X` menarik label lama ke wilayah tim lawan — mahal sekali |
| Di luar jendela dinilai (frame < 11.185, jeda, > 190.197) | `X` | Tidak dihitung sama sekali |

**R-5.1** Bagaimana sistem tahu ia sedang **di tengah possession** dan bukan **di titik hand-over**?
*[Ini pertanyaan inti seat ini. Jawabannya menentukan kebijakan abstain seluruh sistem.]*

**R-5.2** Catatan biaya: `macroF1` menghitung `X` sebagai salah, tapi `macroF1` hanya **tie-break**.
`spellF1` — yang menentukan ranking — tidak pernah melihatnya. Jadi `X` itu murah, dan tidak ada alasan
untuk pelit memakainya.

---

## 6. Minimum spell ⚠️

**Temuan yang bisa langsung menyelamatkan skor kalian:**

> Possession terpendek di GT publik adalah **19 frame (0,76 detik)** — dan itu possession **sungguhan**.
> Yang kedua terpendek 33 frame (1,32 detik).

Scorer **tidak** menggabungkan possession pendek. Kalau kalian memasang minimum spell yang agresif —
"gabungkan apa pun di bawah 1 detik", "buang di bawah 30 frame" — kalian akan **menghapus possession
yang benar-benar ada**, dan satu possession yang hilang ≈ **6 poin** `spellF1` di jendela ini.

Untuk perbandingan: `baseline_raw` melaporkan **131 possession** untuk 5 menit ini. Kebenarannya **17**.

**R-6.1** Ambang minimum spell kami: ______ frame. Alasan: ______

**R-6.2** Serpihan yang lebih pendek dibuang, atau digabung ke tetangga? ______

**R-6.3** Apakah penggabungan boleh lintas tim (`H → A`)? ______ *[Hati-hati: menggabungkan dua
possession tim berbeda menjadi satu akan selalu salah.]*

---

## 7. Kasus yang belum diputuskan

Setiap kali Billa menemukan keadaan yang tidak tercakup di atas, **jangan improvisasi di kode** —
tulis di sini, lalu putuskan bersama.

| # | Kasus | Frame contoh | Keputusan | Tanggal |
|---|---|---|---|---|
| | | | | |

---

## 8. Batas kepatuhan

Aturan di dokumen ini **tidak boleh** berasal dari:

- ❌ ingatan siapa pun tentang pertandingan Barça–Athletic yang asli
- ❌ laporan pertandingan, berita, atau ringkasan mana pun
- ❌ data event dari penyedia mana pun (Opta, StatsBomb, Wyscout, LaLiga, siapa pun)
- ❌ anotasi manual atas frame mana pun

Yang boleh menjadi sumber: **tracking, Smart Tagging, homography yang diberikan · 5 menit GT publik ·
pemahaman umum tentang cara sepak bola bekerja.**

Kalau ada aturan yang terasa "berasal dari ingatan", tulis di `docs/decisions.md` dan tanyakan lewat
issue resmi sebelum dipakai. `FAQ.md` mengundang itu secara eksplisit:

> *"If a rule is unclear or your approach sits near a line, ask before you build on it."*
