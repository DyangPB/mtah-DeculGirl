#!/usr/bin/env python3
"""Satu perintah yang menghasilkan file submission.

    python run.py                        # pipeline sungguhan
    python run.py --placeholder          # submission kosong, untuk uji rantai
    python run.py --window 25            # ganti konfigurasi baseline

Menulis ``results/DeculGirl.csv`` dengan tepat 199.319 baris data.

Ini entry point yang dipakai semua orang. Kalau kamu mengubah cara kerja
pipeline, **jangan ubah perintah ini** -- ganti isi ``src/deculgirl/submit.py``.
Reproducibility itu syarat penilaian, dan satu perintah yang tidak pernah
berubah adalah cara termurah untuk menjaganya.

PERINGATAN soal ``--placeholder``: file yang dihasilkannya **lolos validasi
tapi skornya 0,0000**. Jangan pernah ini yang disubmit. Gunanya cuma untuk
menguji rantai sebelum bundle data ada -- dan itu sebabnya ia harus diminta
secara eksplisit, bukan jadi perilaku default. Kalau data tidak ketemu,
perintah ini akan gagal dengan jelas, bukan diam-diam memberi kalian file
kosong.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Windows: code page konsol default (cp1252) tidak bisa mencetak karakter
# non-ASCII dan akan CRASH di tengah pipeline. Paksa UTF-8 di sini supaya
# kesalahan sepele ini tidak pernah membunuh proses yang sudah jalan lama.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except (AttributeError, OSError):
        pass

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from deculgirl import N_VIDEO_FRAMES  # noqa: E402
from deculgirl.submit import (  # noqa: E402
    DEFAULT_DATA_DIR,
    DEFAULT_WINDOW,
    build_labels,
    build_placeholder,
    write_submission,
)

OUT = ROOT / "results" / "DeculGirl.csv"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--placeholder",
        action="store_true",
        help="tulis submission kosong (semua 'X'). Skornya 0,0000. "
             "Hanya untuk menguji rantai tanpa data",
    )
    parser.add_argument(
        "--window",
        type=int,
        default=DEFAULT_WINDOW,
        help=f"half-width window voting mayoritas, dalam frame (default: {DEFAULT_WINDOW})",
    )
    parser.add_argument(
        "--data-dir",
        default=None,
        help=f"lokasi bundle pertandingan (default: {DEFAULT_DATA_DIR})",
    )
    args = parser.parse_args()

    OUT.parent.mkdir(parents=True, exist_ok=True)

    try:
        labels = (
            build_placeholder()
            if args.placeholder
            else build_labels(data_dir=args.data_dir, window=args.window)
        )
    except (FileNotFoundError, IOError, OSError) as error:
        print(f"\nGAGAL membangun label:\n\n{error}\n", file=sys.stderr)
        print(
            "Kalau kamu cuma ingin menguji bahwa rantainya tersambung, dan "
            "bundle data belum ada:\n\n"
            "    python run.py --placeholder\n\n"
            "File yang dihasilkan akan valid tapi berskor 0,0000.\n",
            file=sys.stderr,
        )
        return 1

    if len(labels) != N_VIDEO_FRAMES:
        print(
            f"build_labels() mengembalikan {len(labels)} label, "
            f"seharusnya {N_VIDEO_FRAMES}.",
            file=sys.stderr,
        )
        return 1

    write_submission(labels, OUT)

    print(f"\nditulis: {OUT.relative_to(ROOT)}")
    print(f"baris  : {len(labels)}")
    if args.placeholder:
        print("\n  PERINGATAN: PLACEHOLDER -- semua 'X'. Valid, tapi skornya 0,0000.")
        print("              Jangan ini yang disubmit.")
    print("\nlangkah berikutnya:  python tools/gate0.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
