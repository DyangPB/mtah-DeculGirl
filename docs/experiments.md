# Catatan Eksperimen — DeculGirl

**Pemilik: Seat 1 (Dyang)** · Dijalankan bersama Seat 4 (Yona) untuk alat ukurnya

> Ini bukan catatan formalitas. Ini **dua hal sekaligus**: cara tim tahu apa yang sudah dicoba, dan
> bahan mentah untuk bagian wajib di dokumen teknis.
>
> `SUBMISSION.md` meminta dokumen teknis menyebutkan *"which assets used and how — **including which
> were tried and dropped**"*. Bagian itu **tidak bisa dikarang di bulan November**. Satu-satunya cara
> punya isi untuk itu adalah mencatatnya sementara kalian mengerjakannya. File ini tempatnya.

---

## Cara mencatat

Tiga aturan, dan aturan ketiga yang paling sering dilanggar:

1. **Tulis hipotesisnya SEBELUM menjalankan.** Satu baris: "saya kira mengubah X akan menaikkan
   `spellF1`, karena Y". Eksperimen tanpa hipotesis tidak menghasilkan pengetahuan, cuma angka.
2. **Tulis hasilnya apa adanya.** Termasuk yang jelek, termasuk yang tidak berubah sama sekali.
3. **Jangan pernah menghapus entri yang gagal.** Yang dibuang itu justru isi bagian *"tried and
   dropped"* di dokumen teknis — dan itu bagian yang paling menunjukkan kalian serius. Tim yang cuma
   melaporkan yang berhasil kelihatan seperti tim yang tidak pernah gagal, dan itu tidak dipercaya.

**Setiap entri harus punya angka, bukan kesan.** "Terasa lebih baik" bukan hasil eksperimen.
Jalankan `python tools/gate0.py` dan salin angkanya.

**Selalu jalankan `--bootstrap 1000` sebelum menyimpulkan satu versi lebih baik.** Di bawah noise band
(`spellF1` ≈ 0,04 di pertandingan penuh), selisihnya tidak berarti apa-apa. Di jendela publik 5 menit
band-nya lebih lebar lagi — 17 possession saja.

---

## Entri 0 — kalibrasi · 24 Oktober 2026

Dijalankan oleh Dyang saat menyiapkan scaffold, **sebelum ada data pertandingan sama sekali.**
Gunanya bukan mengejar skor — gunanya memastikan alat ukurnya bekerja dan mengukur di mana lantainya.

`python tools/gate0.py` pada 5 menit ground truth publik:

| Versi | `macroF1` | `spellF1` | `frag` | possession dilaporkan | rata-rata durasi |
|---|---|---|---|---|---|
| `baseline_raw` | 0,5972 | 0,0378 | **6,52** | 131 | 2,0 s |
| `baseline_smooth25` | 0,6200 | 0,2868 | 1,90 | 36 | 7,6 s |
| `baseline_smooth50` | **0,6207** | 0,3256 | 1,43 | 26 | 10,8 s |
| `baseline_smooth125` | 0,5812 | **0,4242** | **0,81** | 16 | 18,5 s |
| `DeculGirl` (placeholder) | 0,0000 | 0,0000 | 0,05 | 0 | 0,0 s |

*Kebenaran: 17 possession, 21 segmen, rata-rata 14,2 detik.*

**Yang kita pelajari, dan ini yang mengubah cara kerja kita:**

- **`frag` hampir menjadi prediktor langsung `spellF1`,** dan hubungannya monoton: 0,81 → 0,4242 ·
  1,43 → 0,3256 · 1,90 → 0,2868 · 6,52 → 0,0378. Jadi angka yang dipantau setiap hari adalah `frag`,
  **bukan** `macroF1` — yang cuma bergerak 0,04 di seluruh sapuan.
- **Jangan percaya urutan versi ini untuk pertandingan penuh.** `smooth125` menang di sini (0,4242)
  tapi kalah di pertandingan penuh (0,2242). Jendela publik tidak bisa meranking apa pun.

### Detail kelas `D` — temuan paling berguna di entri ini

| Versi | F1 `D` | presisi `D` | recall `D` |
|---|---|---|---|
| `baseline_raw` | **0,4197** | 0,5582 | 0,3363 |
| `baseline_smooth25` | 0,3857 | 0,6106 | 0,2818 |
| `baseline_smooth50` | 0,3225 | 0,6569 | 0,2138 |
| `baseline_smooth125` | 0,1464 | **1,0000** | **0,0790** |

Smoothing **memperburuk** kelas `D`, bukan memperbaikinya. `smooth125` tidak pernah salah ketika bilang
`D` — presisinya sempurna — tapi hanya menangkap 7,9% frame bola mati yang sesungguhnya.

**Hipotesis yang lahir dari sini, untuk Gate 1:** detektor dead-ball yang memakai **kecepatan bola**
(kolom ketiga di file mentah, yang belum dibaca baseline mana pun) plus **pergerakan pemain** akan
menaikkan recall `D` jauh di atas 0,34 **tanpa** menurunkan presisinya di bawah ~0,60. Ini wilayah yang
belum digarap siapa pun, jadi tidak ada yang diambil dari tim lain.

---

## Templat entri baru

Salin blok ini tiap kali kalian mencoba sesuatu yang bisa diukur.

```markdown
## Entri N — <nama singkat> · <tanggal>

**Hipotesis:** <satu baris: mengubah apa, dan kenapa saya kira itu menaikkan spellF1>
**Yang diubah:** <file + baris, atau parameter. Kalau ada, sebutkan nama branch-nya>
**Perintah:** `python tools/gate0.py --file results/<nama-varian>.csv`
**Bootstrap:** <berapa draw, kalau dipakai>

| Versi | macroF1 | spellF1 | frag | poss | dur |
|---|---|---|---|---|---|
| <pembanding> | | | | | |
| <varian baru> | | | | | |

**Hasil:** <apa adanya. Kalau tidak berubah, tulis "tidak berubah">
**Selisihnya di atas noise band?** <ya / tidak / tumpang tindih — lihat hasil bootstrap>
**Putusan:** ✅ dipakai · ❌ dibuang · ⚠️ ambigu, perlu diuji ulang
**Alasan putusan:** <satu atau dua baris>
```

## Konvensi putusan

| Tanda | Artinya | Masuk dokumen teknis? |
|---|---|---|
| ✅ **dipakai** | Ada di `main`, ikut menghasilkan file submission | Ya — bagian "aset dan pendekatan yang dipakai" |
| ❌ **dibuang** | Sudah dicoba, hasilnya tidak dipakai | **Ya** — ini justru isi bagian *"tried and dropped"* |
| ⚠️ **ambigu** | Selisihnya di dalam noise band, atau hasilnya tidak konsisten | Ya — tulis sebagai keterbatasan |

## Kenapa ini pekerjaan yang layak dipertanggungjawabkan

Menjalankan eksperimen terdengar seperti pekerjaan pendamping. Yang sebenarnya terjadi di sini:
**ini satu-satunya cara tim tahu apakah perubahannya benar-benar perbaikan.** Tanpa catatan ini,
setiap anggota tim akan mengejar perasaannya masing-masing, dua orang akan mengklaim versinya lebih
baik, dan tidak ada yang bisa memutuskan — karena tidak ada angka, cuma ingatan.

Dan di bulan Desember, kalau kalian lolos ke Innovation Challenge, file ini jadi arsip cara berpikir
tim kalian. Itu bahan yang tidak bisa direkonstruksi dari ingatan.
