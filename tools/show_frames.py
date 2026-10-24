#!/usr/bin/env python3
"""Lihat isi file tracking untuk beberapa frame, dalam bentuk yang bisa dibaca manusia.

    python tools/show_frames.py 12840 12900

File `BAR-ATH_tactical_atd.txt` isinya 199.319 baris angka yang tidak enak dibaca
langsung. Skrip ini menerjemahkannya jadi tabel: di setiap frame, bolanya di mana,
seberapa cepat, sudah bergerak sejauh apa sejak frame sebelumnya, dan pemain mana
yang paling dekat.

Gunanya untuk Seat 1: menjawab "kenapa frame ini bola mati?" tanpa membuka video.
Cukup lihat: apakah bolanya diam? Apakah pemainnya berhenti? Apakah bolanya hilang?
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Windows: konsol default (cp1252) tidak bisa mencetak karakter non-ASCII.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except (AttributeError, OSError):
        pass

ROOT = Path(__file__).resolve().parents[1]
DATA_TACTICAL = ROOT / "data" / "tactical"
RAW = DATA_TACTICAL / "BAR-ATH_tactical_atd.txt"
META = DATA_TACTICAL / "BAR-ATH_tactical_atd.xml"

FPS = 25
PITCH = (105.3, 68.0)      # meter, sama seperti games.py repo resmi
MISSING = "N"              # huruf pertama dari "NaN"
HOME, AWAY = 0, 1


def team_of_each_track(meta_path: Path) -> list[int]:
    """Untuk setiap slot track: 0 kalau tim home, 1 kalau tim away.

    Cara bacanya sama persis dengan `starter/baseline.py` di repo resmi: elemen
    <Team> pertama di file adalah tim home (konvensi FIFA/EPTS).
    """
    root = ET.parse(meta_path).getroot()
    ids = [t.get("id") for t in root.iter("Team")]
    if len(ids) != 2:
        raise ValueError(f"{meta_path}: harusnya 2 tim, ketemu {len(ids)}")
    home_id = ids[0]
    return [HOME if p.get("teamId") == home_id else AWAY for p in root.iter("Player")]


def parse_group(text: str) -> tuple[float, float, float] | None:
    """'x,y,speed' -> (x, y, speed). None kalau grup itu kosong/NaN."""
    if not text or text[0] == MISSING:
        return None
    pieces = text.split(",")
    if len(pieces) < 2:
        return None
    try:
        x = float(pieces[0])
        y = float(pieces[1])
        speed = float(pieces[2]) if len(pieces) > 2 else 0.0
    except ValueError:
        return None
    return x, y, speed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("mulai", type=int, help="frame awal (0-based, seperti di submission)")
    parser.add_argument("selesai", type=int, nargs="?", default=None,
                        help="frame akhir (default: 60 frame setelah 'mulai')")
    args = parser.parse_args()

    awal = args.mulai
    akhir = args.selesai if args.selesai is not None else awal + 59

    if not RAW.exists():
        print(
            f"File tracking belum ada di:\n  {RAW}\n\n"
            "Pakai nama file yang persis seperti aslinya, dan taruh di folder itu.\n",
            file=sys.stderr,
        )
        return 1
    if not META.exists():
        print(f"File metadata belum ada di:\n  {META}\n", file=sys.stderr)
        return 1

    tim = team_of_each_track(META)
    panjang, lebar = PITCH
    nama_tim = {HOME: "Barcelona", AWAY: "Athletic"}

    print()
    print(f"Frame {awal:,} sampai {akhir:,}   ({awal/FPS:.1f}s sampai {akhir/FPS:.1f}s)")
    print("Frame di file itu 1-based, jadi kita mulai baca dari baris ke-", awal + 1)
    print()
    print("  frame   bola_x  bola_y   kec     geser   n   pemain terdekat")
    print("  ------  ------  ------  ------  ------  ---  ----------------------")

    sebelumnya: tuple[float, float] | None = None
    baris_tercetak = 0

    with RAW.open() as handle:
        for line in handle:
            parts = line.split(":")
            if len(parts) != 3:
                continue
            try:
                id_frame = int(parts[0])
            except ValueError:
                continue

            if id_frame > akhir + 1:
                break

            bola = parse_group(parts[2])
            frame = id_frame - 1     # id_frame 1-based -> video frame 0-based

            if awal <= frame <= akhir:
                if bola is None:
                    print(f"  {frame:>6,}  {'--':>6}  {'--':>6}  {'--':>6}  {'--':>6}  "
                          f"{'nd':>3}  BOLA TIDAK TERDETEKSI")
                    sebelumnya = None
                    baris_tercetak += 1
                    continue

                bx, by, kecepatan = bola
                mx = bx * panjang
                my = by * lebar

                if sebelumnya is None:
                    geser = "--"
                else:
                    px, py = sebelumnya
                    d = ((bx - px) * panjang) ** 2 + ((by - py) * lebar) ** 2
                    geser = f"{d ** 0.5:.2f}"

                pemain = parts[1].split(";")
                terdekat_jarak = None
                terdekat_tim = None
                terdekat_slot = None
                hidup = 0

                for slot, grup in enumerate(pemain):
                    p = parse_group(grup)
                    if p is None:
                        continue
                    hidup += 1
                    px_ = p[0] * panjang
                    py_ = p[1] * lebar
                    jarak = ((px_ - mx) ** 2 + (py_ - my) ** 2) ** 0.5
                    if terdekat_jarak is None or jarak < terdekat_jarak:
                        terdekat_jarak = jarak
                        terdekat_tim = tim[slot] if slot < len(tim) else None
                        terdekat_slot = slot + 1

                if terdekat_jarak is None:
                    info = "tidak ada pemain terdeteksi"
                else:
                    timnya = nama_tim.get(terdekat_tim, "?")
                    info = f"{timnya} (slot {terdekat_slot}, {terdekat_jarak:.1f} m)"

                print(f"  {frame:>6,}  {bx:>6.3f}  {by:>6.3f}  {kecepatan:>6.2f}  "
                      f"{geser:>6}  {hidup:>3}  {info}")
                sebelumnya = (bx, by)
                baris_tercetak += 1

    print()
    if baris_tercetak == 0:
        print("  Tidak ada frame di rentang itu yang terbaca dari file.")
        print(f"  File-nya berisi berapa baris? Cek dulu -- harusnya 199.319.")
    else:
        print("  Bacanya: 'geser' adalah berapa meter bola berpindah sejak frame sebelumnya.")
        print("  Bola diam (geser 0.00 terus) hampir selalu berarti bola mati.")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
