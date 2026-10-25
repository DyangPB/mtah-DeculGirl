# DeculGirl — More than a Hack 2027, Phase 1

Memberi label penguasaan bola **untuk setiap frame** pada satu pertandingan LaLiga lengkap
(**FC Barcelona vs Athletic Club**, LaLiga EA Sports 2024-25 matchday 2).

Tantangan dari [Metrica Sports](https://metrica-sports.com), FC Barcelona (Barça Innovation Hub), dan
[Mobile World Capital Barcelona](https://www.mwcbarcelona.com) untuk
[More than a Hack 2027](https://landing.mobileworldcapital.com/more-than-a-hack-2027).

Hasil akhirnya satu file `frame,label` berisi **199.319 baris**, dengan label `H` / `A` / `D` / `X`.
Penilaian dilakukan otomatis memakai **`spellF1`**, dibandingkan dengan ground truth (jawaban benar)
seluruh pertandingan yang dirahasiakan penyelenggara.

---

## Tim

| Seat | Nama | GitHub | Tanggung jawab |
|---|---|---|---|
| 1 | Dyang | [@DyangPB](https://github.com/DyangPB) | Domain sepak bola, aturan possession, PM, pemilik repo |
| 2 | Raissa | [@raisinmee](https://github.com/raisinmee) | Data dan sinyal bola — fitur |
| 3 | Billa | [@nabilland](https://github.com/nabilland) | Model sekuensial dan dead ball, dokumen teknis |
| 4 | Yona | [@yonakatitin](https://github.com/yonakatitin) | Pengukuran, validasi, dan reproduksi hasil |

**Mulai dari sini:** **[`docs/SUMMARY.md`](docs/SUMMARY.md)** — satu halaman, cukup 5 menit untuk
membacanya. Penjelasan lengkap ada di **[`docs/PLAYBOOK.md`](docs/PLAYBOOK.md)**.

Semua dokumen juga bisa dibaca sebagai halaman web (GitHub Pages) setelah Pages diaktifkan.
Caranya ada di [`docs/_config.yml`](docs/_config.yml).

---

## Cara menjalankan

Butuh **Python 3.9 atau lebih baru**. Semua perintah memakai Python agar sama persis di Windows, macOS,
dan Linux. Tidak ada shell script.

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt

python tools/fetch_official.py    # unduh repo resmi (dikunci pada commit tertentu)
python run.py                     # hasilkan results/DeculGirl.csv
python tools/gate0.py             # periksa dan beri skor pada file itu
```

**`python tools/gate0.py` bisa dijalankan tanpa data pertandingan.** Perintah ini memakai 5 menit ground
truth publik yang ada di repo resmi. Jadi kalian bisa memastikan seluruh rangkaian `CSV → validasi →
skor` sudah berjalan, bahkan sebelum data pertandingan selesai diunduh.

### Data pertandingan

Data **tidak ada di repo ini dan memang tidak boleh ada**. Taruh bundle data di folder `data/`, atau
arahkan variabel lingkungan `MTAH_DATA_DIR` ke folder lain. Susunannya:

```
data/tactical/BAR-ATH_tactical.mp4 | _atd.xml | _atd.txt | _homography.csv | _smart_tagging.xml
data/broadcast/BAR-ATH_broadcast.mp4 | _atd.xml | _atd.txt | _homography.csv
```

Folder `data/` sudah masuk `.gitignore`. Jangan pernah meng-commit isinya.

---

## Susunan folder

```
docs/
  SUMMARY.md               ringkasan satu halaman — mulai dari sini kalau cuma punya 5 menit
  PLAYBOOK.md              rencana lengkap 25 hari
  AGENDA.md                agenda rapat perdana
  possession-rules.md      ATURAN: kapan D, kapan H/A. Milik Seat 1
  experiments.md           CATATAN EKSPERIMEN: apa yang dicoba, angkanya, putusannya. Milik Seat 1
  gt-public-transitions.md lembar kerja 21 transisi di GT publik. Seat 1 + Seat 2
  decisions.md             catatan keputusan. Satu keputusan = satu baris
src/deculgirl/
  submit.py                data -> CSV submission
  features/                Seat 2: pembaca data, penyeragaman format, fitur per frame
  model/                   Seat 3: dead ball, penentuan tim, penyusunan possession
metrics/                   Seat 4: alat ukur, uji regresi, bootstrap
tools/
  fetch_official.py        unduh repo resmi pada commit yang dikunci
  gate0.py                 periksa dan beri skor (memakai GT publik)
results/                   hasil submission (tidak masuk git)
third_party/mtah2027/      repo resmi hasil unduhan (tidak masuk git)
data/                      bundle pertandingan (tidak masuk git)
```

`GLOSSARY.md` di folder utama berisi istilah baku. Pakailah istilah dari sana di kode, dokumen, dan
chat, supaya tidak ada salah paham, misalnya antara "possession" dan "spell".

---

## Aturan kerja

- **Hak akses repo:** Dyang = owner · **Billa = Admin** (admin kedua) · Raissa dan Yona = Write.
  Adminnya sengaja dua orang. Hanya Admin yang bisa mengubah Settings dan mengatur siapa boleh
  mengakses repo, jadi jangan menggantungkannya pada satu orang.
- **Tidak ada yang push langsung ke `main`.** Semua perubahan lewat branch dan pull request (PR).
- **`docs/decisions.md` adalah satu-satunya sumber yang sah untuk keputusan.** Keputusan yang tidak
  tertulis di sana dianggap belum ada.
- **Pemeriksaan otomatis berjalan di setiap PR** (`.github/workflows/validate.yml`).
- **Dilarang memberi label secara manual, dalam bentuk apa pun dan untuk tujuan apa pun.** Baca
  [`docs/PLAYBOOK.md`](docs/PLAYBOOK.md) §9 sebelum menyentuh data.

---

## Lisensi

Kode di repo ini berlisensi MIT. **Data pertandingan tidak termasuk di dalamnya.** Data itu dilisensikan
terpisah, hanya untuk kompetisi ini, dengan syarat yang disetujui saat pendaftaran.

`third_party/mtah2027/` adalah salinan repo resmi penyelenggara (berlisensi MIT) yang dikunci pada
commit `f8f2629ff1e0985f81d7e59d8413678514ee1530`. Salinan itu diunduh dengan
`tools/fetch_official.py`.
