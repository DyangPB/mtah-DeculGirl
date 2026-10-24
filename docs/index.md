# DeculGirl — dokumen kerja

**More than a Hack 2027 · Phase 1: Ball Possession**
Metrica Sports × FC Barcelona (Barça Innovation Hub) × Mobile World Capital Barcelona

Deadline submission: **17 November 2026**

---

## Mulai dari sini

| Dokumen | Isi | Untuk siapa |
|---|---|---|
| **[Ringkasan](SUMMARY.md)** | Satu halaman, 5 menit. Baca ini dulu | semua orang |
| **[Agenda rapat](AGENDA.md)** | Urutan rapat perdana, keputusan yang harus diambil, pembagian tugas | semua orang |
| **[Playbook](PLAYBOOK.md)** | Dokumen lengkap: strategi, job desk, flow 25 hari, cara mengukur, garis merah | semua orang |
| **[Catatan keputusan](decisions.md)** | Satu keputusan = satu baris. Sumber kebenaran tunggal | semua orang |

## Dokumen per seat

| Dokumen | Isi | Pemilik |
|---|---|---|
| **[Aturan possession](possession-rules.md)** | Aturan `D` vs `H`/`A` yang bisa dikodekan | Seat 1 — Dyang |
| **[Lembar transisi GT publik](gt-public-transitions.md)** | 21 transisi + 17 possession, lengkap dengan durasinya | Seat 1 — Dyang |
| **[Glosarium](../GLOSSARY.md)** | Istilah kanonik: possession, dead ball, spellF1, ATD | semua orang |
| **[Catatan metrik](../metrics/README.md)** | Cara mengukur tanpa menipu diri sendiri | Seat 4 — Yona |

---

## Kalau kamu cuma punya 5 menit

Baca **[Ringkasan](SUMMARY.md)**. Isinya delapan angka yang menentukan, kenapa skor datang dari empat
hal struktural dan bukan dari model yang lebih canggih, siapa mengerjakan apa, dan lima hal yang harus
terjadi malam ini.

## Kalau kamu mau menyumbang kode

Mulai dari **[`../README.md`](../README.md)** — di situ ada cara menjalankan pipeline dan struktur
foldernya. Perintahnya tiga:

```
python tools/fetch_official.py
python run.py
python tools/gate0.py
```

---

> **Satu aturan yang berlaku untuk semua orang di sini:** tidak ada hand label, dalam bentuk apa pun,
> untuk tujuan apa pun — termasuk **ingatan kalian sendiri tentang pertandingan aslinya**. Semua label
> harus keluar dari algoritma. Detailnya di **[Playbook §9](PLAYBOOK.md#9-garis-merah)**.
