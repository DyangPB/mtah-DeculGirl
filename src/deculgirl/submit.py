"""data -> CSV submission.

KONTRAK ``build_labels()``
--------------------------
- mengembalikan array numpy 1-D berisi string, panjangnya **tepat**
  ``deculgirl.N_VIDEO_FRAMES``
- setiap elemen harus salah satu dari ``"H"``, ``"A"``, ``"D"``, ``"X"``
- indeks ``i`` adalah ``video_frame`` bernilai ``i`` (0-based)
- tidak boleh ada elemen kosong -- tulis ``"X"`` untuk abstain

Kalau kontrak ini dilanggar, ``validate_submission.py`` menolak file dan
submission kalian **dinilai nol**. Itu penyebab kegagalan paling umum di
kompetisi ini.


===========================================================================
STATUS: FAIL-SAFE, BELUM CERDAS.
===========================================================================

Yang berjalan sekarang adalah **baseline resmi** (pemain tracked terdekat ke
bola + voting mayoritas), diimpor langsung dari
``third_party/mtah2027/starter/baseline.py``. Itu bukan curang dan bukan
kemalasan: kode itu MIT, dan penyelenggara sendiri menyebutnya *"a starting
point, not a constraint"* -- sekaligus cara tercepat punya submission valid.

Ini asuransi kalian. Begitu data turun dan ``python run.py`` jalan, kalian
sudah memegang submission yang berskor (±0,32 di jendela publik, 0,2433 di
pertandingan penuh). **Jangan pernah menghapus keadaan ini.** Setiap perbaikan
ditambahkan sebagai varian, dan `main` selalu bisa menghasilkan submission
yang valid.

CARA MENGGANTINYA -- GATE 1, satu pilar sekaligus
-------------------------------------------------
Ganti ``build_labels()`` supaya memanggil pipeline kalian sendiri, lalu
kerjakan empat pilar di ``src/deculgirl/features/`` dan ``src/deculgirl/model/``
(lihat ``docs/PLAYBOOK.md`` bagian 7):

  1. Deteksi dead-ball   -- pilar bernilai tertinggi. Baseline tidak punya
                            logika dead ball sama sekali
  2. Imputasi bola       -- bola hilang di 41% frame yang dinilai
  3. Atribusi tim        -- lebih kaya dari "pemain terdekat"
  4. Segmentasi          -- jangan memecah possession jadi serpihan

Aturan yang tidak boleh dilanggar di file ini: **tidak ada label yang boleh
berasal dari tangan manusia.** Semua label harus keluar dari algoritma. Tidak
untuk submission, tidak untuk melatih model, tidak untuk memvalidasi.
Lihat ``docs/PLAYBOOK.md`` bagian 9.

Ingat juga: label di luar ``GRADED_RUNS`` tidak berpengaruh apa pun pada skor.
Jangan buang waktu menyempurnakan jeda babak.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from . import LABELS, N_VIDEO_FRAMES

ROOT = Path(__file__).resolve().parents[2]
OFFICIAL = ROOT / "third_party" / "mtah2027"

#: Di mana bundle pertandingan ditaruh. Sama dengan konvensi repo resmi:
#: variabel lingkungan ``MTAH_DATA_DIR`` menang, kalau tidak ada pakai
#: ``data/`` di root repo ini.
DEFAULT_DATA_DIR = Path(os.environ.get("MTAH_DATA_DIR") or (ROOT / "data"))

#: Half-width window voting mayoritas, dalam frame. 50 = jendela +/- 2 detik,
#: dan itu konfigurasi yang menghasilkan lantai yang diterbitkan (spellF1
#: 0,2433 di pertandingan penuh).
#:
#: JANGAN tuning angka ini di jendela publik 5 menit. EVALUATION.md
#: membuktikan bahwa tuning di situ memilih nilai yang SALAH: window 125
#: menang di publik (0,4242) tapi kalah di pertandingan penuh (0,2242).
DEFAULT_WINDOW = 50


def _load_official_baseline():
    """Impor ``starter/baseline.py`` dari repo resmi.

    Diimpor, bukan disalin, supaya kalau kalian memperbarui repo resmi
    (``tools/fetch_official.py --force``) kalian juga mendapat perbaikan
    mereka -- dan supaya jelas bahwa yang berjalan di sini adalah kode mereka,
    bukan rekaan kita. Lisensinya MIT.
    """
    starter = OFFICIAL / "starter"
    if not starter.is_dir():
        raise FileNotFoundError(
            f"Repo resmi tidak ada di {OFFICIAL}.\n"
            "  jalankan dulu:  python tools/fetch_official.py"
        )
    # baseline.py sendiri menambahkan root repo resmi ke sys.path saat diimpor;
    # kita tambahkan keduanya supaya urutannya tidak bergantung padanya.
    for path in (OFFICIAL, starter):
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))

    import baseline  # noqa: PLC0415  (sengaja: impornya butuh sys.path di atas)

    return baseline


def build_labels(data_dir: Path | str | None = None, window: int = DEFAULT_WINDOW) -> np.ndarray:
    """Membangun satu label untuk setiap frame video.

    Ini fungsi yang kalian ganti di Gate 1. Kontraknya ada di docstring modul.
    """
    baseline = _load_official_baseline()
    codes = baseline.build(data_dir=str(data_dir or DEFAULT_DATA_DIR))
    return baseline.smooth(codes, window)


def build_placeholder() -> np.ndarray:
    """Submission legal yang tidak menjawab apa pun. Skornya 0,0000.

    Gunanya cuma satu: membuktikan rantai ``build -> write -> validate ->
    score`` tersambung SEBELUM data pertandingan kalian ada. Jangan pernah
    ini yang disubmit.

    Perhatikan: file ini tetap **lolos validasi**. Itu pelajaran yang layak
    dilihat sekali -- validitas file dan kebenaran isinya dua hal yang
    berbeda, dan scorer hanya menghukum yang kedua.
    """
    return np.full(N_VIDEO_FRAMES, "X", dtype="<U1")


def write_submission(labels: np.ndarray, path: Path | str) -> None:
    """Menulis file submission sesuai kontrak, lalu memeriksanya sendiri.

    Jangan ubah fungsi ini. Kalau ada yang salah dengan bentuk filenya, itu
    bug di ``build_labels()``, bukan di sini.
    """
    labels = np.asarray(labels)

    if labels.ndim != 1:
        raise ValueError(f"labels harus 1-D, dapat {labels.ndim}-D")
    if len(labels) != N_VIDEO_FRAMES:
        raise ValueError(f"labels harus {N_VIDEO_FRAMES} elemen, dapat {len(labels)}")

    labels = np.char.upper(np.char.strip(labels.astype(str)))

    empty = int(np.sum(labels == ""))
    if empty:
        raise ValueError(
            f"{empty} label kosong. Sel kosong ditolak validator -- tulis 'X' "
            "untuk abstain, jangan biarkan kosong."
        )

    bad = sorted(set(labels.tolist()) - set(LABELS))
    if bad:
        raise ValueError(f"label di luar {list(LABELS)}: {bad[:5]}")

    frame = pd.DataFrame(
        {
            "frame": np.arange(N_VIDEO_FRAMES, dtype=np.int64),
            "label": labels,
        }
    )

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # newline="" + lineterminator="\n": pastikan filenya identik di Windows dan
    # Linux. Reproducibility itu syarat penilaian, bukan bonus.
    with open(path, "w", newline="", encoding="utf-8") as handle:
        frame.to_csv(handle, index=False, lineterminator="\n")
