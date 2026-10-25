# More than a Hack 2027 — Phase 1: Ball Possession

Tantangan dari Metrica Sports, FC Barcelona, dan Mobile World Capital: memberi satu label penguasaan
bola untuk **setiap frame** dalam satu pertandingan LaLiga (Barça vs Athletic).

Glosarium ini menetapkan istilah baku yang dipakai di dokumen, kode, dan percakapan tim. Kalau ragu
sebuah istilah berarti apa, cari di sini dulu. Bagian _Hindari_ berisi kata yang sering dipakai untuk
hal yang sama tetapi menimbulkan salah paham.

## Waktu dan nomor frame

**Video frame** (nomor frame video):
Nomor urut frame pada video taktis, dengan kecepatan 25 frame per detik (fps), dari 0 sampai 199318.
Inilah isi kolom `frame` pada file submission.
_Hindari_: frame_id, timestamp, "detik"

**ID frame**:
Nomor urut frame pada file tracking ATD. Dimulai dari 1, jadi rentangnya 1–199319.
Rumus pengubahnya: `video_frame = id_frame - 1`.
_Hindari_: "frame" saja tanpa keterangan

**Half** (babak):
Babak 1 atau babak 2. Scorer mengganti label `X` per babak; penggantian tidak pernah melewati batas babak.

**Graded frame** (frame yang dinilai):
Frame yang punya ground truth, sehingga ikut dihitung dalam skor. Jumlahnya 158.857 dari 199.319 frame,
yaitu isi kedua babak. Jeda dan waktu di luar pertandingan tidak dinilai.

**Public window** (jendela publik):
5 menit pertama permainan: video frame 11185–18684, berisi 7.500 frame yang dinilai dan 17 possession.
Hanya ini ground truth yang dipegang tim. Gunanya untuk memeriksa bahwa pipeline kita benar. Jangan
dipakai untuk meranking versi, sebagai data latih, atau untuk menyetel parameter.

**Private ground truth** (ground truth privat):
Ground truth seluruh pertandingan, yang hanya dipegang penyelenggara. Inilah yang menentukan peringkat.

## Status dan label

**Possession** (penguasaan bola):
Rentang frame berurutan yang labelnya sama (`H` atau `A`) selama bola hidup, dan terputus kalau label
berubah. Possession adalah satuan yang dihitung `spellF1`.
_Hindari_: spell, phase, sequence

**Controlled possession** (penguasaan yang sah):
Penguasaan bola yang diakui. Sentuhan sekilas, bola yang hanya membelok, atau duel udara tanpa
kontrol lanjutan tidak termasuk.

**Change of possession** (pergantian penguasaan):
Saat bola berpindah ke tim lawan, yaitu ketika pemain lawan mendapat penguasaan yang sah.

**Dead ball** (bola mati, label `D`):
Bola tidak sedang dalam permainan. Ini masa berhenti, bukan possession. Siapa yang memegang bola
saat bola mati sengaja tidak ditanyakan.

**Ball alive** (bola hidup):
Bola sedang dalam permainan. Setiap frame yang dinilai dan bolanya hidup harus berlabel `H` atau `A`.

**Stoppage** (masa berhenti):
Periode bola mati. Masa ini memisahkan dua possession: `H H D D H H` adalah dua possession, bukan satu.

**Abstention** (tidak menjawab, label `X`):
Sistem memilih tidak menjawab untuk frame itu. `macroF1` menganggap `X` sebagai jawaban salah. `spellF1`
mengganti `X` dengan label terakhir yang bukan `X` di babak yang sama.

**macroF1**:
Rata-rata F1 untuk tiga kelas `H`, `A`, dan `D` pada frame yang dinilai. Skor ini dilaporkan
berdampingan dengan `spellF1` dan dipakai sebagai pemutus pertama kalau `spellF1` seri.
Noise sekitar 0,01; skor terendah yang mungkin sekitar 0,16.

**spellF1**:
Metrik yang menentukan peringkat. Cara hitungnya: possession prediksi dipasangkan satu lawan satu
dengan possession asli berdasarkan temporal IoU, lalu F1-nya dirata-rata pada lima ambang
(0,3 / 0,4 / 0,5 / 0,6 / 0,7). Noise sekitar 0,04 pada pertandingan penuh. Label yang sama untuk
semua frame selalu bernilai tepat 0.

**Temporal IoU**:
Perbandingan antara panjang waktu yang tumpang tindih dan panjang gabungan dua rentang waktu. Ukuran
ini menunjukkan seberapa pas satu possession prediksi menimpa satu possession asli.

## Aset data

**ATD** (automatic tracking data):
Data pelacakan otomatis dari Metrica dalam format FIFA/EPTS: satu file XML berisi metadata dan satu
file txt berisi data mentah. Isinya 25 catatan per detik, dengan koordinat yang dinormalisasi ke
rentang 0–1 (bukan meter) dan tanpa identitas pemain. Ada 199.319 catatan untuk feed taktis dan
164.488 untuk feed broadcast.
_Hindari_: "data tracking" tanpa keterangan

**Track slot**:
Satu "tempat" di ATD (`Track 1`…`Track 46` pada feed taktis; 51 pada feed broadcast). Slot bukan orang
tertentu dan bukan nomor punggung; pemain yang menempati slot itu bisa berganti dari frame ke frame.
_Hindari_: player, shirt number

**Smart Tagging**:
Anotasi taktis otomatis (XML SportsCode, 638 fase) dengan tag seperti `BUILD UP`, `SET PIECES`, dan
`BALL IN THE BOX`. Isinya fase permainan, bukan possession.
_Hindari_: event, possession label

**Homography**:
Matriks 3×3 untuk setiap frame yang mengubah koordinat lapangan ternormalisasi menjadi koordinat piksel
pada gambar, lengkap dengan penanda `valid`. Pada feed taktis 100% valid; pada feed broadcast hanya 65,8%.

**Feed taktis** dan **feed broadcast**:
Dua video yang disediakan. Timeline feed taktis menjadi acuan submission. Feed broadcast punya
timeline sendiri (ada potongan gambar dan tayangan ulang), sehingga nomor framenya tidak sama dengan
feed taktis.
_Hindari_: "video utama" tanpa menyebut yang mana

**Baseline floor** (batas minimum baseline):
`baseline_smooth50` dengan `spellF1` 0,2433 pada pertandingan penuh. Ini angka minimum yang harus
dilewati.
