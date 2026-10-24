# DeculGirl — More than a Hack 2027, Phase 1

Label penguasaan bola **per frame** untuk satu pertandingan LaLiga lengkap
(**FC Barcelona vs Athletic Club**, LaLiga EA Sports 2024-25 matchday 2).

Tantangan oleh [Metrica Sports](https://metrica-sports.com), FC Barcelona (Barça Innovation Hub), dan
[Mobile World Capital Barcelona](https://www.mwcbarcelona.com) untuk
[More than a Hack 2027](https://landing.mobileworldcapital.com/more-than-a-hack-2027).

Output: `frame,label` — **199.319 baris** — label `H` / `A` / `D` / `X`.
Dinilai otomatis pada **`spellF1`** terhadap ground truth pertandingan penuh yang bersifat privat.

---

## Tim

| Seat | Nama | GitHub | Tanggung jawab |
|---|---|---|---|
| 1 | Dyang | [@DyangPB](https://github.com/DyangPB) | Domain, aturan possession, PM, owner repo |
| 2 | Raissa | [@raisinmee](https://github.com/raisinmee) | Data & sinyal bola — fitur |
| 3 | Billa | [@nabilland](https://github.com/nabilland) | Model sekuensial & dead-ball, dokumen teknis |
| 4 | Yona | [@yonakatitin](https://github.com/yonakatitin) | Metrik, validasi, reproducibility |

**Mulai dari sini:** **[`docs/SUMMARY.md`](docs/SUMMARY.md)** — satu halaman, 5 menit, isi ringkasnya.
Detailnya di **[`docs/PLAYBOOK.md`](docs/PLAYBOOK.md)**.

Semua dokumen juga tersedia sebagai halaman web (GitHub Pages) setelah Pages-nya diaktifkan —
lihat [`docs/_config.yml`](docs/_config.yml) untuk cara mengaktifkannya.

---

## Menjalankan

Butuh **Python 3.9+**. Semua entry point ditulis dengan Python supaya perintahnya sama persis di
Windows, macOS, dan Linux — tidak ada shell script.

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt

python tools/fetch_official.py    # ambil repo resmi (di-pin ke commit tertentu)
python run.py                     # hasilkan results/DeculGirl.csv
python tools/gate0.py             # validasi + skor file itu
```

**`python tools/gate0.py` jalan tanpa data pertandingan.** Dia memakai 5 menit ground truth publik yang
ada di repo resmi, jadi kalian bisa membuktikan seluruh rantai `CSV → validasi → skor` bekerja sebelum
bundle data kalian turun.

### Data pertandingan

Data **tidak ada di repo ini** dan tidak boleh ada. Letakkan bundle di `data/` (atau arahkan
`MTAH_DATA_DIR` ke tempat lain):

```
data/tactical/BAR-ATH_tactical.mp4 | _atd.xml | _atd.txt | _homography.csv | _smart_tagging.xml
data/broadcast/BAR-ATH_broadcast.mp4 | _atd.xml | _atd.txt | _homography.csv
```

`data/` ada di `.gitignore`. Jangan pernah commit isinya.

---

## Struktur

```
docs/
  PLAYBOOK.md              rencana lengkap 25 hari — mulai dari sini
  AGENDA.md                agenda rapat perdana
  possession-rules.md      ATURAN: D vs H/A. Pemilik Seat 1
  gt-public-transitions.md lembar kerja 21 transisi GT publik. Pemilik Seat 1
  decisions.md             catatan keputusan. Satu keputusan = satu baris
src/deculgirl/
  submit.py                data -> CSV submission
  features/                Seat 2: loader, kanonikalisasi, fitur per frame
  model/                   Seat 3: dead-ball, atribusi, segmentasi
metrics/                   Seat 4: harness, regression suite, bootstrap
tools/
  fetch_official.py        clone repo resmi di commit yang di-pin
  gate0.py                 validasi + skor (pakai GT publik)
results/                   output submission (gitignored)
third_party/mtah2027/      repo resmi, hasil fetch (gitignored)
data/                      bundle pertandingan (gitignored)
```

`GLOSSARY.md` di root berisi istilah kanonik — pakai istilah dari situ di kode, dokumen, dan chat,
supaya tidak ada ambiguitas "possession" vs "spell".

---

## Cara kerja

- **Tidak ada yang push langsung ke `main`.** Semua lewat branch + PR.
- **`docs/decisions.md` sumber kebenaran tunggal.** Kalau sebuah keputusan tidak ada di sana, keputusan
  itu belum ada.
- **Gate validasi jalan otomatis** di setiap PR (`.github/workflows/validate.yml`).
- **Tidak ada hand label, dalam bentuk apa pun, untuk tujuan apa pun.** Baca
  [`docs/PLAYBOOK.md`](docs/PLAYBOOK.md) §9 sebelum menyentuh data.

---

## Lisensi

Kode di repo ini: MIT. **Data pertandingan tidak tercakup** — datanya dilisensikan terpisah untuk
kompetisi ini saja, di bawah syarat yang disetujui saat pendaftaran.

`third_party/mtah2027/` adalah salinan repo resmi penyelenggara (MIT) yang di-pin ke commit
`f8f2629ff1e0985f81d7e59d8413678514ee1530`, diambil ulang dengan `tools/fetch_official.py`.
