"""Seat 2 (Raissa) -- data dan sinyal bola.

Isi folder ini: memuat aset yang diberikan, mengkanonikalisasinya, dan
membangun fitur per frame.

Tiga hal yang harus benar sebelum apa pun yang lain:

1. **Alignment.** ``video_frame = id_frame - 1`` untuk ATD. Smart Tagging
   dalam detik --> ``round(seconds * 25)``. Homography sudah per ``frame``.
   Kalau ini salah, semua fitur kalian benar tapi tidak ada gunanya.

2. **Bentuk tabel.** Satu baris per video frame, tepat 199.319 baris,
   indeks 0..199318. Kalau jumlahnya beda, **jangan di-pad atau di-trim** --
   cari tahu kenapa bedanya (FAQ.md melarang menyesuaikan; "work out why the
   counts differ").

3. **Bola.** Ada di 56,9% seluruh frame dan 59,3% frame yang dinilai, dan
   tidak ada indikator kepercayaan apa pun. ``DATA.md`` bilang hilangnya
   "disproportionately on the frames that matter". Rancang untuk itu
   **sejak hari pertama** -- itu instruksi mereka, bukan saran.

Aset yang tersedia:

    data/tactical/BAR-ATH_tactical_atd.xml + _atd.txt   tracking (EPTS)
    data/tactical/BAR-ATH_tactical_smart_tagging.xml    tagging taktis
    data/tactical/BAR-ATH_tactical_homography.csv       geometri kamera
    data/tactical/BAR-ATH_tactical.mp4                  video (TIDAK dipakai)

Detail lengkapnya di ``DATA.md`` repo resmi, dan helper pembacanya di
``third_party/mtah2027/starter/`` (``load_atd.py``, ``load_smart_tagging.py``,
``load_homography.py``) -- semua MIT, memang disediakan untuk dipakai.

Fitur yang dibutuhkan Seat 3 ada di ``docs/PLAYBOOK.md`` bagian 7.1-7.3.
"""
