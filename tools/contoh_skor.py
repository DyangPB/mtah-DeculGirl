"""Contoh mini dari awal sampai akhir: data posisi -> tebakan -> possession -> skor.

Skrip ini untuk BELAJAR, bukan bagian dari pipeline submission. Datanya rekaan
(14 frame), supaya semua langkah bisa dibaca dan dihitung dengan tangan.

    python tools/contoh_skor.py                  # dengan perapian (min-spell 2)
    python tools/contoh_skor.py --min-spell 1    # tanpa perapian, lihat skornya jatuh
    python tools/contoh_skor.py --min-spell 3    # perapian lebih agresif

Alurnya sama dengan yang sebenarnya:

    data posisi -> fitur -> tebakan tiap frame -> rapikan jadi possession
                -> isi X (dilakukan penilai) -> hitung spellF1

Cara menghitung skornya meniru logika penilai resmi
(``third_party/mtah2027/evaluation/possession_metrics.py``): possession dicocokkan
satu lawan satu dengan tim yang sama, urut dari IoU terbesar, dan dianggap cocok
kalau IoU >= ambang. Penilai resmi tetap yang menentukan angka sebenarnya.
"""

import argparse
import sys

# Windows sering memakai encoding bawaan yang bukan UTF-8.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

AMBANG_IOU = (0.3, 0.4, 0.5, 0.6, 0.7)

# --- 1. Data rekaan ----------------------------------------------------------
# Satu baris per frame:
#   (bola_terdeteksi, tim_pemain_terdekat, kecepatan_bola, pemain_berjalan)
# Di data asli ini berasal dari ATD (posisi x, y bola dan pemain per frame).
DATA = [
    (True,  "H", 5.0, False),   # frame 0
    (True,  "H", 5.0, False),   # frame 1
    (False, None, None, None),  # frame 2: bola tidak terdeteksi
    (True,  "H", 5.0, False),   # frame 3
    (True,  "A", 5.0, False),   # frame 4: pemain Athletic kebetulan lewat
    (True,  "H", 5.0, False),   # frame 5
    (True,  "H", 5.0, False),   # frame 6
    (True,  "H", 0.1, True),    # frame 7: bola hampir diam, pemain berjalan
    (True,  "A", 0.1, True),    # frame 8
    (True,  "A", 0.1, True),    # frame 9
    (True,  "A", 5.0, False),   # frame 10
    (True,  "A", 5.0, False),   # frame 11
    (True,  "A", 5.0, False),   # frame 12
    (True,  "A", 5.0, False),   # frame 13
]

# Jawaban asli. Di kompetisi, ini disimpan penyelenggara dan tidak kita lihat.
JAWABAN_ASLI = list("HHHHHHH" + "DDD" + "AAAA")


# --- 2. Aturan (inilah yang ditulis Dyang di possession-rules.md) -------------
def tebak_satu_frame(bola_terdeteksi, tim_terdekat, kecepatan_bola, pemain_berjalan):
    """Jika bola hilang -> X. Jika bola hampir diam dan pemain berjalan -> D.
    Selain itu, tim pemain terdekat yang menguasai bola."""
    if not bola_terdeteksi:
        return "X"          # tidak menebak; penilai akan mengisinya dengan label sebelumnya
    if kecepatan_bola < 1.0 and pemain_berjalan:
        return "D"
    return tim_terdekat


# --- 3. Merapikan (bagian Billa: anti-fragmentasi) ----------------------------
def segmen(label):
    """Daftar (awal, akhir, label), akhir tidak ikut dihitung. Label sama berurutan = satu segmen."""
    hasil, awal = [], 0
    for i in range(1, len(label) + 1):
        if i == len(label) or label[i] != label[awal]:
            hasil.append((awal, i, label[awal]))
            awal = i
    return hasil


def isi_x(label):
    """Meniru penilai: X diganti label bukan-X sebelumnya; di awal diisi label bukan-X pertama."""
    hasil = list(label)
    pertama = next((x for x in hasil if x != "X"), None)
    terakhir = pertama
    for i, x in enumerate(hasil):
        if x == "X":
            hasil[i] = terakhir
        else:
            terakhir = x
    return hasil


def rapikan(label, min_spell):
    """Possession pendek yang diapit tim lawannya diubah mengikuti tim yang mengapitnya.

    Hanya mengubah H/A yang diapit dua segmen dengan tim yang sama. Bola mati (D)
    tidak pernah diubah. min_spell=1 berarti tidak merapikan apa pun.

    Catatan: di data asli ada possession sependek 19 frame yang memang nyata, jadi
    nilai min_spell sungguhan harus kecil, dan idealnya memakai kekuatan bukti,
    bukan panjang saja.
    """
    hasil = isi_x(label)
    segs = segmen(hasil)
    for i in range(1, len(segs) - 1):
        awal, akhir, tim = segs[i]
        sebelum, sesudah = segs[i - 1][2], segs[i + 1][2]
        if tim in "HA" and akhir - awal < min_spell and sebelum == sesudah and sebelum in "HA":
            for k in range(awal, akhir):
                hasil[k] = sebelum
    # X yang asli tetap ditulis X di file; penilai yang mengisinya.
    return [("X" if asli == "X" else baru) for asli, baru in zip(label, hasil)]


# --- 4. Skor spellF1 ----------------------------------------------------------
def possession(label):
    return [s for s in segmen(label) if s[2] in "HA"]


def iou(a, b):
    irisan = min(a[1], b[1]) - max(a[0], b[0])
    gabungan = max(a[1], b[1]) - min(a[0], b[0])
    return irisan / gabungan


def skor_spell(asli, tebakan):
    """Mengembalikan (rata-rata F1, rincian per ambang). X sudah diisi sebelum dihitung."""
    gt, pred = possession(isi_x(asli)), possession(isi_x(tebakan))
    pasangan = sorted(
        ((iou(g, p), i, j)
         for i, g in enumerate(gt) for j, p in enumerate(pred)
         if g[2] == p[2] and p[1] > g[0] and g[1] > p[0]),
        key=lambda t: (-t[0], t[1], t[2]),
    )
    rincian, daftar_f1 = [], []
    for ambang in AMBANG_IOU:
        dipakai_gt, dipakai_pred = set(), set()
        for nilai, i, j in pasangan:
            if nilai < ambang:
                break
            if i in dipakai_gt or j in dipakai_pred:
                continue
            dipakai_gt.add(i)
            dipakai_pred.add(j)
        benar = len(dipakai_gt)
        salah = len(pred) - benar      # tebakan yang tidak punya pasangan (fp)
        terlewat = len(gt) - benar     # possession asli yang tidak terdeteksi (fn)
        f1 = 2 * benar / (2 * benar + salah + terlewat) if (2 * benar + salah + terlewat) else 0.0
        rincian.append((ambang, benar, salah, terlewat, f1))
        daftar_f1.append(f1)
    return sum(daftar_f1) / len(daftar_f1), rincian


# --- 5. Menjalankan semuanya --------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--min-spell", type=int, default=2,
                        help="possession lebih pendek dari ini (dan diapit tim yang sama) "
                             "dirapikan. 1 = tanpa perapian. Bawaan: 2")
    args = parser.parse_args()

    mentah = [tebak_satu_frame(*baris) for baris in DATA]
    akhir = rapikan(mentah, args.min_spell)

    print("LANGKAH 1-2. Data -> tebakan tiap frame")
    print("frame  bola   terdekat  kecepatan  jalan   tebakan  asli")
    for i, (baris, t, a) in enumerate(zip(DATA, mentah, JAWABAN_ASLI)):
        ada, tim, kec, jalan = baris
        print(f"{i:>5}  {'ya' if ada else 'TIDAK':<5}  {str(tim or '-'):<8}  "
              f"{str(kec if kec is not None else '-'):<9}  {str(jalan if jalan is not None else '-'):<6}  "
              f"{t:<7}  {a}")

    print("\nLANGKAH 3. Setelah dirapikan (min-spell =", args.min_spell, ")")
    print("tebakan mentah :", " ".join(mentah))
    print("dirapikan      :", " ".join(akhir))
    print("jawaban asli   :", " ".join(JAWABAN_ASLI))

    diisi = isi_x(akhir)
    benar_frame = sum(p == a for p, a in zip(diisi, JAWABAN_ASLI))
    print(f"\nAkurasi per frame (setelah X diisi): {benar_frame}/{len(diisi)} "
          f"= {benar_frame / len(diisi):.0%}")

    print("\nLANGKAH 4. Possession")
    print("possession asli   :", [f"{t}[{a}-{b - 1}]" for a, b, t in possession(JAWABAN_ASLI)])
    print("possession tebakan:", [f"{t}[{a}-{b - 1}]" for a, b, t in possession(diisi)])

    rata, rincian = skor_spell(JAWABAN_ASLI, akhir)
    print("\nLANGKAH 5. spellF1")
    print("ambang  benar  tebakan_salah  terlewat    F1")
    for ambang, benar, salah, terlewat, f1 in rincian:
        print(f"{ambang:>6}  {benar:>5}  {salah:>13}  {terlewat:>8}  {f1:.2f}")
    print(f"\nspellF1 = {rata:.4f}")

    print("\nFile CSV yang dikumpulkan akan berbentuk seperti ini:")
    print("frame,label")
    for i, x in enumerate(akhir):
        print(f"{i},{x}")


if __name__ == "__main__":
    main()
