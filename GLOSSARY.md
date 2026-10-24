# More than a Hack 2027 — Phase 1: Ball Possession

Domain untuk tantangan Metrica Sports / FC Barcelona / Mobile World Capital: memberi satu label
penguasaan bola untuk **setiap frame** dari satu pertandingan LaLiga (Barça vs Athletic).
Glosarium ini menetapkan istilah kanonik yang dipakai di dokumen, kode, dan percakapan tim.

## Waktu & indeks

**Video frame** (frame video):
Indeks frame di timeline video taktis, 25 fps, mencakup 0–199318. Inilah nilai kolom `frame` di submission.
_Avoid_: frame_id, timestamp, "detik"

**ID frame**:
Indeks frame di file tracking ATD, 1-based, mencakup 1–199319. `video_frame = id_frame - 1`.
_Avoid_: frame

**Half**:
Babak 1 atau 2. Pengisian label `X` oleh scorer dilakukan per half, tidak lintas babak.

**Graded frame**:
Frame yang punya ground truth dan ikut dinilai: 158.857 dari 199.319 frame (isi kedua babak, di luar jeda dan di luar pertandingan).

**Public window**:
5 menit pertama permainan (video frame 11185–18684; 7.500 frame dinilai; 17 possession) — satu-satunya ground truth yang dipegang tim.
Untuk memverifikasi pipeline itu benar, bukan untuk ranking, bukan data latih, bukan set tuning.

**Private ground truth**:
Ground truth seluruh pertandingan, hanya dipegang penyelenggara. Inilah yang menentukan ranking.

## State & label

**Possession**:
Run maksimal frame berlabel sama (`H` atau `A`) selama bola hidup. Ini unit yang dihitung spellF1.
_Avoid_: spell, phase, sequence

**Controlled possession**:
Penguasaan bola yang dianggap sah — bukan sentuhan sekilas, defleksi, atau duel udara tanpa kontrol lanjutan.

**Change of possession**:
Momen possession berpindah ke tim lawan, yaitu saat pemain lawan memperoleh controlled possession.

**Dead ball** (`D`):
Bola tidak dalam permainan. Ini stoppage, bukan possession. Kepemilikan bola saat dead ball sengaja tidak ditanyakan.

**Ball alive**:
Kondisi bola sedang dalam permainan. Setiap graded frame dengan bola hidup harus `H` atau `A`.

**Stoppage**:
Periode bola mati; memisahkan dua possession. `H H D D H H` adalah dua possession, bukan satu.

**Abstention** (`X`):
Sistem memilih tidak menjawab. macroF1 menghitungnya sebagai salah; spellF1 menggantinya dengan label non-`X` terakhir di babak itu.

**macroF1**:
Rata-rata F1 per kelas `H`/`A`/`D` atas graded frame. Dilaporkan berdampingan dengan spellF1 dan menjadi tie-break pertama. Noise ~0,01; lantai ~0,16.

**spellF1**:
Metrik ranking. Possession prediksi dipasangkan satu-ke-satu dengan possession asli lewat temporal IoU, lalu F1-nya dirata-rata pada threshold 0,3/0,4/0,5/0,6/0,7. Noise ~0,04 di full match. Label konstan bernilai tepat 0.

**Temporal IoU**:
Rasio durasi irisan terhadap gabungan dua rentang waktu — ukuran seberapa pas satu possession prediksi menimpa satu possession asli.

## Aset data

**ATD** (automatic tracking data):
Ekspor FIFA/EPTS dari Metrica: XML metadata + txt raw. 25 record per detik, koordinat ternormalisasi 0–1 (bukan meter), tanpa identitas pemain. 199.319 record untuk feed taktis, 164.488 untuk broadcast.
_Avoid_: "data tracking" generik

**Track slot**:
Slot di ATD (`Track 1`…`Track 46` pada taktis; 51 pada broadcast). Slot bukan orangnya dan bukan nomor punggung; identitas bisa berpindah antar frame.
_Avoid_: player, shirt number

**Smart Tagging**:
Anotasi taktis otomatis (SportsCode XML, 638 fase) seperti `BUILD UP`, `SET PIECES`, `BALL IN THE BOX`. Ini phase, bukan possession.
_Avoid_: event, possession label

**Homography**:
Matriks 3×3 per frame yang memetakan koordinat pitch ternormalisasi ke piksel gambar, disertai flag `valid`. Feed taktis 100% valid; broadcast hanya 65,8%.

**Feed taktis** / **feed broadcast**:
Dua video yang disediakan. Timeline taktis adalah referensi submission; broadcast punya timeline sendiri (ada cut dan replay) dan tidak selaras frame dengannya.
_Avoid_: "video utama" tanpa menyebut yang mana

**Baseline floor**:
`baseline_smooth50`, spellF1 0,2433 di full match — angka minimum yang harus dilewati.
