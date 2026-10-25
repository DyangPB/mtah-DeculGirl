# Catatan Eksperimen — DeculGirl

**Pemilik: Seat 1 (Dyang)** · Alat ukurnya dijalankan bersama Seat 4 (Yona)

> Ini bukan catatan formalitas. Fungsinya **ada dua**: supaya tim tahu apa saja yang sudah dicoba, dan
> sebagai bahan mentah untuk bagian wajib di dokumen teknis.
>
> `SUBMISSION.md` meminta dokumen teknis menyebutkan *"which assets used and how — **including which
> were tried and dropped**"* (aset mana yang dipakai dan bagaimana, **termasuk yang dicoba lalu
> dibuang**). Bagian itu **tidak bisa dikarang di bulan November**. Satu-satunya cara agar ada isinya
> adalah mencatatnya selama pekerjaan berlangsung. File ini tempatnya.

---

## Cara mencatat

Ada tiga aturan, dan aturan ketiga yang paling sering dilanggar:

1. **Tulis hipotesisnya SEBELUM menjalankan eksperimen.** Cukup satu baris: "Saya kira mengubah X akan
   menaikkan `spellF1`, karena Y". Eksperimen tanpa hipotesis hanya menghasilkan angka, bukan
   pengetahuan.
2. **Tulis hasilnya apa adanya.** Termasuk yang jelek, dan termasuk yang tidak berubah sama sekali.
3. **Jangan pernah menghapus catatan eksperimen yang gagal.** Justru yang dibuang itulah isi bagian
   *"tried and dropped"* di dokumen teknis, dan bagian itu yang paling menunjukkan kesungguhan kalian.
   Tim yang hanya melaporkan keberhasilan terlihat seperti tim yang tidak pernah gagal, dan itu tidak
   dipercaya.

**Setiap catatan harus punya angka, bukan kesan.** "Rasanya lebih baik" bukan hasil eksperimen.
Jalankan `python tools/gate0.py` dan salin angkanya.

**Selalu jalankan `--bootstrap 1000` sebelum menyimpulkan bahwa satu versi lebih baik.** Selisih yang
masih di dalam batas noise (`spellF1` ≈ 0,04 di pertandingan penuh) tidak berarti apa-apa. Di jendela
publik 5 menit, batas noise-nya lebih lebar lagi karena possession-nya hanya 17.

---

## Catatan 0 — kalibrasi · 24 Oktober 2026

Dijalankan oleh Dyang saat menyiapkan kerangka proyek, **sebelum ada data pertandingan sama sekali.**
Tujuannya bukan mengejar skor, melainkan memastikan alat ukurnya berfungsi dan mengetahui di mana batas
minimumnya.

`python tools/gate0.py` pada 5 menit ground truth publik:

| Versi | `macroF1` | `spellF1` | `frag` | possession yang dilaporkan | rata-rata durasi |
|---|---|---|---|---|---|
| `baseline_raw` | 0,5972 | 0,0378 | **6,52** | 131 | 2,0 s |
| `baseline_smooth25` | 0,6200 | 0,2868 | 1,90 | 36 | 7,6 s |
| `baseline_smooth50` | **0,6207** | 0,3256 | 1,43 | 26 | 10,8 s |
| `baseline_smooth125` | 0,5812 | **0,4242** | **0,81** | 16 | 18,5 s |
| `DeculGirl` (placeholder) | 0,0000 | 0,0000 | 0,05 | 0 | 0,0 s |

*Yang benar: 17 possession, 21 segmen, rata-rata 14,2 detik.*

**Yang kita pelajari, dan ini mengubah cara kerja kita:**

- **`frag` hampir bisa dipakai langsung untuk memperkirakan `spellF1`,** dan hubungannya konsisten:
  0,81 → 0,4242 · 1,43 → 0,3256 · 1,90 → 0,2868 · 6,52 → 0,0378. Jadi angka yang dipantau setiap hari
  adalah `frag`, **bukan** `macroF1`, yang hanya bergeser 0,04 di seluruh percobaan ini.
- **Jangan percaya urutan versi ini untuk pertandingan penuh.** `smooth125` menang di sini (0,4242)
  tetapi kalah di pertandingan penuh (0,2242). Jendela publik tidak bisa dipakai untuk meranking apa
  pun.

### Rincian kelas `D` — temuan paling berguna di catatan ini

| Versi | F1 `D` | presisi `D` | recall `D` |
|---|---|---|---|
| `baseline_raw` | **0,4197** | 0,5582 | 0,3363 |
| `baseline_smooth25` | 0,3857 | 0,6106 | 0,2818 |
| `baseline_smooth50` | 0,3225 | 0,6569 | 0,2138 |
| `baseline_smooth125` | 0,1464 | **1,0000** | **0,0790** |

Menghaluskan hasil **memperburuk** kelas `D`, bukan memperbaikinya. `smooth125` tidak pernah salah saat
menyebut `D`, jadi presisinya sempurna, tetapi hanya menemukan 7,9% dari frame bola mati yang
sebenarnya.

**Hipotesis yang muncul dari sini, untuk Gate 1:** pendeteksi bola mati yang memakai **kecepatan bola**
(kolom ketiga di file mentah, yang belum dibaca baseline mana pun) ditambah **gerakan pemain** akan
menaikkan recall `D` jauh di atas 0,34 **tanpa** menurunkan presisinya di bawah ± 0,60. Wilayah ini
belum digarap siapa pun, jadi tidak ada yang mengambil poin dari tim lain.

---

## Templat catatan baru

Salin blok ini setiap kali kalian mencoba sesuatu yang bisa diukur.

```markdown
## Catatan N — <nama singkat> · <tanggal>

**Hipotesis:** <satu baris: mengubah apa, dan kenapa saya kira itu menaikkan spellF1>
**Yang diubah:** <file dan baris, atau parameternya. Kalau ada, sebutkan nama branch-nya>
**Perintah:** `python tools/gate0.py --file results/<nama-varian>.csv`
**Bootstrap:** <berapa kali pengambilan sampel, kalau dipakai>

| Versi | macroF1 | spellF1 | frag | poss | dur |
|---|---|---|---|---|---|
| <pembanding> | | | | | |
| <varian baru> | | | | | |

**Hasil:** <apa adanya. Kalau tidak berubah, tulis "tidak berubah">
**Apakah selisihnya di atas batas noise?** <ya / tidak / tumpang tindih — lihat hasil bootstrap>
**Putusan:** ✅ dipakai · ❌ dibuang · ⚠️ belum jelas, perlu diuji ulang
**Alasan putusan:** <satu atau dua baris>
```

## Arti tanda putusan

| Tanda | Artinya | Masuk dokumen teknis? |
|---|---|---|
| ✅ **dipakai** | Sudah ada di `main` dan ikut menghasilkan file submission | Ya, di bagian "aset dan pendekatan yang dipakai" |
| ❌ **dibuang** | Sudah dicoba, tetapi hasilnya tidak dipakai | **Ya**, ini justru isi bagian *"tried and dropped"* |
| ⚠️ **belum jelas** | Selisihnya masih di dalam batas noise, atau hasilnya tidak konsisten | Ya, tulis sebagai keterbatasan |

## Kenapa pekerjaan ini layak dipertanggungjawabkan

Menjalankan eksperimen terdengar seperti pekerjaan pendukung. Padahal yang terjadi di sini justru
sebaliknya: **ini satu-satunya cara tim tahu apakah sebuah perubahan benar-benar perbaikan.** Tanpa
catatan ini, setiap anggota akan mengikuti perasaannya masing-masing, dua orang akan sama-sama
mengklaim versinya lebih baik, dan tidak ada yang bisa memutuskan karena tidak ada angka, hanya ingatan.

Dan di bulan Desember, kalau kalian lolos ke Innovation Challenge, file ini menjadi arsip cara berpikir
tim kalian. Itu bahan yang tidak bisa disusun ulang dari ingatan.
