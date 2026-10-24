#!/usr/bin/env python3
"""Validasi dan skor file submission, memakai alat resmi.

    python tools/gate0.py
    python tools/gate0.py --file results/DeculGirl_v2.csv
    python tools/gate0.py --bootstrap 1000     # interval kepercayaan

GATE INI TIDAK BUTUH DATA PERTANDINGAN. Skornya dihitung pada 5 menit ground
truth publik yang ada di dalam repo resmi, jadi ia bisa jalan sejak menit
pertama kalian memulai -- sebelum bundle data turun.

APA YANG DILAKUKANNYA
  1. Menjalankan ``evaluation/validate_submission.py`` -- **pemeriksaan yang
     persis sama** dengan yang dijalankan scorer resmi. File yang gagal di
     sini akan dinilai nol kalau disubmit.
  2. Menjalankan ``evaluation/run_evaluation.py`` -- scorer resminya.

PERINGATAN YANG WAJIB DIINGAT
  Angka dari gate ini dihitung pada **17 possession**. Satu possession meleset
  menggerakkan spellF1 sekitar **6 poin**. ``EVALUATION.md`` membuktikan bahwa
  menuning di jendela ini memilih baseline yang SALAH: ``smooth125`` menang di
  sini (0,4242) tapi kalah di pertandingan penuh (0,2242).

  Jadi: pakai gate ini untuk memverifikasi bahwa pipeline kalian **benar**
  (frame selaras, file sesuai kontrak, labelnya berarti apa yang kalian kira).
  Jangan pakai untuk memilih versi.
"""

from __future__ import annotations

import argparse
import shutil
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
OFFICIAL = ROOT / "third_party" / "mtah2027"
DEFAULT_FILE = ROOT / "results" / "DeculGirl.csv"


def _run(cmd: list[str], cwd: Path) -> int:
    pretty = " ".join(str(part) for part in cmd)
    print(f"  $ {pretty}\n", flush=True)
    return subprocess.run([str(part) for part in cmd], cwd=cwd).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--file",
        default=str(DEFAULT_FILE),
        help="file submission yang diperiksa (default: results/DeculGirl.csv)",
    )
    parser.add_argument(
        "--bootstrap",
        type=int,
        default=0,
        metavar="N",
        help="jumlah draw bootstrap untuk interval kepercayaan (mis. 1000)",
    )
    args = parser.parse_args()

    if not (OFFICIAL / "evaluation" / "run_evaluation.py").exists():
        print(
            "Repo resmi belum ada.\n\n  python tools/fetch_official.py\n",
            file=sys.stderr,
        )
        return 1

    submission = Path(args.file).resolve()
    if not submission.exists():
        print(
            f"File submission tidak ada: {submission}\n\n  python run.py\n",
            file=sys.stderr,
        )
        return 1

    # 1. Validasi -- pakai fungsi yang persis sama dengan scorer resmi.
    print(f"=== 1/2  VALIDASI  {submission.name} ===\n")
    rc = _run(
        [sys.executable, "evaluation/validate_submission.py", str(submission)],
        cwd=OFFICIAL,
    )
    if rc != 0:
        print(
            "\nVALIDASI GAGAL. File ini akan dinilai NOL kalau "
            "disubmit.\nKontrak filenya ada di SUBMISSION.md; penyebab paling "
            "umum adalah off-by-one di awal/akhir file, header hilang, dan sel "
            "kosong yang seharusnya berisi 'X'.",
            file=sys.stderr,
        )
        return rc

    # 2. Skor. Scorer membaca semua *.csv di evaluation/results/.
    results_dir = OFFICIAL / "evaluation" / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(submission, results_dir / submission.name)

    print("\n=== 2/2  SKOR  (5 menit ground truth publik) ===\n")
    cmd = [sys.executable, "evaluation/run_evaluation.py"]
    if args.bootstrap:
        cmd += ["--bootstrap", str(args.bootstrap)]
    rc = _run(cmd, cwd=OFFICIAL)

    print(
        "\nLantai yang harus dilewati: spellF1 0,2433 pada pertandingan penuh "
        "(baseline_smooth50).\nAngka di atas berasal dari 17 possession -- 1 "
        "possession meleset ~ 6 poin. Bukan leaderboard."
    )
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
