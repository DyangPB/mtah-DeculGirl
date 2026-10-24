#!/usr/bin/env python3
"""Ambil repo resmi penyelenggara, di-pin ke satu commit.

    python tools/fetch_official.py
    python tools/fetch_official.py --force     # hapus lalu ambil ulang

Hasilnya masuk ke ``third_party/mtah2027/`` (gitignored, diambil ulang saat
dibutuhkan).

KENAPA DI-PIN
-------------
``evaluation/possession_metrics.py`` **adalah** spesifikasi metriknya.
``EVALUATION.md`` mengatakannya sendiri:

    "If this document and that file ever disagree, the file is right."

Kalau upstream mengubah file itu di tengah kompetisi, angka lokal kalian ikut
berubah tanpa kalian sadari -- dan kalian akan mengejar hantu. Pin mencegahnya:
setiap orang di tim, dan setiap kali dijalankan, mendapat kode penilai yang
persis sama.

Kalau kalian memang mau menarik versi terbaru, ubah ``PINNED_SHA`` di bawah
lalu tulis alasannya di ``docs/decisions.md``.
"""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

# Windows: konsol default (cp1252) tidak bisa mencetak karakter non-ASCII dan
# akan crash. Paksa UTF-8 sebelum apa pun dicetak.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except (AttributeError, OSError):
        pass

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "third_party" / "mtah2027"

UPSTREAM = "https://github.com/metrica-sports/more-than-a-hack-2027.git"

#: Commit yang di-pin. Diambil 24 Oktober 2026 -- commit terakhir saat itu,
#: "Clarifying the guidelines for annotating the provided video."
PINNED_SHA = "f8f2629ff1e0985f81d7e59d8413678514ee1530"


def _rmtree(path: Path) -> None:
    """Hapus folder yang mungkin berisi file read-only (objek git di Windows)."""

    def on_error(func, target, _exc_info):  # type: ignore[no-untyped-def]
        try:
            os.chmod(target, stat.S_IWRITE)
            func(target)
        except Exception:  # noqa: BLE001
            pass

    shutil.rmtree(path, onerror=on_error)


def _git(args: list[str], cwd: Path | None = None) -> None:
    printable = " ".join(args)
    print(f"  $ git {printable}")
    subprocess.run(["git", *args], cwd=cwd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--force",
        action="store_true",
        help="hapus third_party/mtah2027 dulu, lalu ambil ulang",
    )
    args = parser.parse_args()

    if shutil.which("git") is None:
        print("git tidak ada di PATH. Install Git dulu.", file=sys.stderr)
        return 1

    if DEST.exists():
        if not args.force:
            print(f"sudah ada: {DEST.relative_to(ROOT)}")
            print("ambil ulang dengan:  python tools/fetch_official.py --force")
            return 0
        print(f"menghapus {DEST.relative_to(ROOT)} ...")
        _rmtree(DEST)

    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.mkdir(parents=True)

    print(f"mengambil {UPSTREAM}")
    print(f"          @ {PINNED_SHA}\n")

    try:
        _git(["init", "--quiet"], cwd=DEST)
        _git(["remote", "add", "origin", UPSTREAM], cwd=DEST)
        # --depth 1 + SHA langsung: cepat, dan mengunci persis satu commit.
        _git(["fetch", "--quiet", "--depth", "1", "origin", PINNED_SHA], cwd=DEST)
        _git(["checkout", "--quiet", "FETCH_HEAD"], cwd=DEST)
    except subprocess.CalledProcessError:
        print(
            "\ngagal mengambil repo resmi.\n"
            "  - cek koneksi internet\n"
            "  - cek git bisa mengakses github.com\n"
            "  - lalu jalankan lagi\n"
            "Folder setengah jadi dibiarkan supaya bisa diperiksa; "
            "pakai --force untuk membersihkannya.",
            file=sys.stderr,
        )
        return 1

    scorer = DEST / "evaluation" / "run_evaluation.py"
    gt = DEST / "evaluation" / "gt" / "BAR-ATH_possession_gt_public.csv"
    if not scorer.exists() or not gt.exists():
        print(
            "\nrepo terambil tapi file kuncinya tidak ada "
            f"({scorer.name}, {gt.name}).\n"
            "Mungkin upstream berubah. Cek manual sebelum lanjut.",
            file=sys.stderr,
        )
        return 1

    print(f"\nok: {DEST.relative_to(ROOT)}  @ {PINNED_SHA[:8]}")
    print("langkah berikutnya:  python run.py")
    print("lalu:                python tools/gate0.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
