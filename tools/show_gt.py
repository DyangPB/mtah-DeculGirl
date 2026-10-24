#!/usr/bin/env python3
"""Tunjukkan 5 menit contoh jawaban — supaya kelihatan apa yang harus ditebak.

    python tools/show_gt.py

Ini SATU-SATUNYA contoh jawaban yang kita punya: 5 menit pertama permainan,
lengkap dengan jawaban benarnya. Menampilkan 21 segmen di dalamnya — 17 possession
dan 4 blok bola mati.

Gunanya: pekerjaan Seat 1 bukan "membangun model". Pekerjaanmu adalah melihat
transisi ke `D` di tabel ini, membuka file tracking di sekitar frame itu, dan
menjawab pertanyaan "kenapa frame ini bola mati?" — lalu menuliskannya sebagai
aturan yang bisa dikodekan.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

# Windows: konsol default (cp1252) tidak bisa mencetak karakter non-ASCII.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except (AttributeError, OSError):
        pass

ROOT = Path(__file__).resolve().parents[1]
GT = (ROOT / "third_party" / "mtah2027" / "evaluation" / "gt"
      / "BAR-ATH_possession_gt_public.csv")

FPS = 25
ARAH = {"H": "H  Barcelona menguasai", "A": "A  Athletic menguasai", "D": "D  BOLA MATI"}


def main() -> int:
    if not GT.exists():
        print(
            "File contoh jawaban belum ada.\n\n"
            "  python tools/fetch_official.py\n",
            file=sys.stderr,
        )
        return 1

    df = pd.read_csv(GT, dtype={"label": str})

    dinilai = df[df["label"] != "X"]
    if dinilai.empty:
        print("file contoh jawaban tidak berisi frame yang dinilai.", file=sys.stderr)
        return 1

    pertama = int(dinilai["frame"].iloc[0])
    terakhir = int(dinilai["frame"].iloc[-1])

    jendela = df[(df["frame"] >= pertama) & (df["frame"] <= terakhir)]
    frames = jendela["frame"].to_numpy()
    labels = jendela["label"].to_numpy()

    detik_jendela = len(labels) / FPS
    print()
    print(f"Contoh jawaban: frame {pertama:,} sampai {terakhir:,}")
    print(f"  {len(labels):,} frame dinilai  =  {detik_jendela:.0f} detik  =  {detik_jendela/60:.1f} menit")
    print(f"  di luar jendela ini, semua jawabannya 'X' (tidak dinilai)")
    print()
    print("  #   label  frame mulai   frame akhir    durasi   waktu mulai")
    print("  --- ----- -------------  -------------  -------  -----------")

    segmen: list[tuple[str, int, int, int]] = []
    awal = 0
    for i in range(1, len(labels) + 1):
        if i == len(labels) or labels[i] != labels[awal]:
            segmen.append((labels[awal], int(frames[awal]), int(frames[i - 1]), i - awal))
            awal = i

    for nomor, (label, mulai, akhir, panjang) in enumerate(segmen, start=1):
        detik = mulai / FPS
        menit = int(detik // 60)
        sisa = detik - menit * 60
        tanda = " <<<" if label == "D" else ""
        print(
            f"  {nomor:>3} {ARAH[label]:<24} {mulai:>7,}  {akhir:>13,}"
            f"  {panjang/FPS:>6.1f}s  {menit:>2}:{sisa:04.1f}{tanda}"
        )

    possession = [s for s in segmen if s[0] in ("H", "A")]
    mati = [s for s in segmen if s[0] == "D"]

    print()
    print(f"  {len(segmen)} segmen: {len(possession)} possession dan {len(mati)} blok bola mati.")
    print(f"  Rata-rata {sum(s[3] for s in possession)/len(possession)/FPS:.1f} detik per possession."
          f"  Yang terpendek {min(s[3] for s in possession)/FPS:.2f} detik.")
    print()
    print("  Empat blok bertanda <<< itulah pertanyaanmu. Untuk masing-masing:")
    print("    1. Buka data/tactical/BAR-ATH_tactical_atd.txt di sekitar frame itu.")
    print("    2. Tanya: apa yang beda di situ? Bola hilang? Bola diam? Pemain berhenti?")
    print("    3. Tulis jawabannya di docs/possession-rules.md sebagai aturan yang bisa dikodekan.")
    print()
    print("  Kalau kamu bisa menjelaskan kenapa 4 blok itu 'D' tanpa melihat video dan tanpa")
    print("  mengingat pertandingannya, kamu sudah melakukan pekerjaan Seat 1.")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
