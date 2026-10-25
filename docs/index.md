# DeculGirl — dokumen kerja

**More than a Hack 2027 · Phase 1: Ball Possession**
Metrica Sports × FC Barcelona (Barça Innovation Hub) × Mobile World Capital Barcelona

Batas pengumpulan: **17 November 2026**

---

## Mulai dari sini

| Dokumen | Isi | Untuk siapa |
|---|---|---|
| **[Ringkasan](SUMMARY.md)** | Satu halaman, cukup 5 menit. Baca ini dulu | semua orang |
| **[Agenda rapat](AGENDA.md)** | Urutan rapat perdana, keputusan yang harus diambil, pembagian tugas | semua orang |
| **[Playbook](PLAYBOOK.md)** | Dokumen lengkap: strategi, pembagian tugas, alur 25 hari, cara mengukur, larangan | semua orang |
| **[Catatan keputusan](decisions.md)** | Satu keputusan = satu baris. Satu-satunya sumber yang sah untuk keputusan | semua orang |

## Dokumen per seat

| Dokumen | Isi | Pemilik |
|---|---|---|
| **[Aturan possession](possession-rules.md)** | Aturan `D` dan `H`/`A` yang bisa dijadikan kode | Seat 1 — Dyang |
| **[Catatan eksperimen](experiments.md)** | Apa yang dicoba, angkanya, dan putusannya, termasuk yang gagal | Seat 1 — Dyang |
| **[Lembar transisi GT publik](gt-public-transitions.md)** | 21 transisi dan 17 possession, lengkap dengan durasinya | Seat 1 + Seat 2 |
| **[Glosarium](https://github.com/DyangPB/mtah-DeculGirl/blob/main/GLOSSARY.md)** | Istilah baku: possession, dead ball, spellF1, ATD | semua orang |
| **[Catatan metrik](https://github.com/DyangPB/mtah-DeculGirl/blob/main/metrics/README.md)** | Cara mengukur tanpa menipu diri sendiri | Seat 4 — Yona |

> **Kenapa dua tautan terakhir mengarah ke github.com, bukan tautan biasa?** Karena file-nya berada di
> luar folder `docs/`, sedangkan Jekyll hanya bisa menampilkan file di dalam folder itu. Tautan biasa
> ke `../` akan mati di halaman ini. Jadi keduanya sengaja diarahkan ke GitHub, tempat keduanya tampil
> dengan rapi. Kalau nama repo berubah, tiga alamat di file ini perlu diperbarui.

---

## Kalau hanya punya 5 menit

Baca **[Ringkasan](SUMMARY.md)**. Isinya delapan angka penting, alasan kenapa skor datang dari empat
hal struktural dan bukan dari model yang lebih canggih, siapa mengerjakan apa, dan lima hal yang harus
terjadi sekarang.

## Kalau mau menyumbang kode

Mulai dari **[`README.md`](https://github.com/DyangPB/mtah-DeculGirl/blob/main/README.md)**. Di sana ada
cara menjalankan pipeline dan susunan folder. Hanya ada tiga perintah:

```
python tools/fetch_official.py
python run.py
python tools/gate0.py
```

---

> **Satu aturan yang berlaku untuk semua orang di sini:** tidak ada pelabelan manual, dalam bentuk apa
> pun dan untuk tujuan apa pun, termasuk **ingatan kalian sendiri tentang pertandingan aslinya**. Semua
> label harus dihasilkan oleh algoritma. Detailnya ada di **[Playbook bagian 9](PLAYBOOK.md#9-larangan-yang-tidak-boleh-dilanggar)**.
