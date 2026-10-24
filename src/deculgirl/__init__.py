"""Konstanta pertandingan dan kontrak submission.

Semua angka di sini berasal dari repo resmi penyelenggara pada commit
``f8f2629``. Kalau ada yang bertentangan dengan repo resmi, **repo resmi yang
benar** -- lalu perbarui file ini.

Istilahnya ada di ``GLOSSARY.md`` di root repo. Pakai istilah dari sana di
kode dan di dokumen, supaya tidak ada ambiguitas "possession" vs "spell".
"""

from __future__ import annotations

# --- Bentuk pertandingan ----------------------------------------------------

#: Jumlah frame video taktis. Ini juga jumlah baris data yang wajib ada
#: di file submission -- selalu, tidak peduli apa pun.
N_VIDEO_FRAMES = 199_319

#: Frame per detik. 25 baris tracking = 1 detik.
FPS = 25

#: Ukuran pitch dalam meter, dari ``games.py`` repo resmi.
#: (Metadata menulis 105.0 x 68.0; selisih 30 cm itu cuma penting kalau
#: kalian menghitung jarak meter. Baseline resmi memakai angka ini.)
PITCH_M = (105.3, 68.0)

# --- Kontrak label ----------------------------------------------------------

#: Satu-satunya label yang sah. Tidak ada yang lain, dalam bentuk apa pun.
LABELS = ("H", "A", "D", "X")

#: Label yang dihitung sebagai possession oleh spellF1. ``D`` adalah stoppage,
#: ``X`` bukan state.
POSSESSION_LABELS = ("H", "A")

# --- Frame yang dinilai -----------------------------------------------------
#
# Rentang half-open [start, stop), persis seperti ``valid_runs()`` di repo
# resmi: (11185, 90652) dan (110808, 190198).
#
# CATATAN PENTING: babak 2 dinilai mulai frame 110.808, tapi kick-off-nya baru
# 113.742 -- jadi 2.934 frame pertama babak 2 dinilai dan SEMUANYA ``D``.
# Ini diterbitkan resmi di FAQ.md, bukan tebakan. Kalau kalian memakainya
# untuk mengkalibrasi detektor dead-ball, cantumkan sumbernya di dokumen
# teknis (RULES.md melarang konstanta hasil pengamatan sendiri).
GRADED_RUNS = ((11_185, 90_652), (110_808, 190_198))

#: Di luar rentang di atas, label kalian tidak berpengaruh sama sekali:
#: macroF1 hanya menghitung frame yang dinilai, dan spellF1 hanya menyusun
#: possession di dalam rentang yang dinilai.
N_GRADED_FRAMES = 158_857

# --- Jendela ground truth publik --------------------------------------------

#: Satu-satunya ground truth yang kita pegang. Untuk memverifikasi bahwa
#: pipeline BENAR -- bukan untuk ranking, bukan data latih, bukan set tuning.
PUBLIC_GT_RUNS = ((11_185, 18_685),)
PUBLIC_GT_FRAMES = 7_500
PUBLIC_GT_POSSESSIONS = 17

# --- Kalibrasi: jarak antar-babak -------------------------------------------

#: ``video_frame = id_frame - 1`` untuk ATD.
ID_FRAME_OFFSET = 1

#: Offset jarak antar babak di Smart Tagging, dari ``games.py``.
#: Kedua babak berbeda satu frame, jadi tidak ada satu offset tunggal yang
#: eksak.
FRAME_OFFSETS = {1: 1_702_057, 2: 1_702_058}

# --- Ambang metrik ----------------------------------------------------------
#
# Jangan dibandingkan di bawah angka ini; itu noise, bukan kemajuan.

#: Noise band spellF1 pada pertandingan penuh.
SPELL_F1_NOISE = 0.04

#: Noise band macroF1.
MACRO_F1_NOISE = 0.01

#: Lantai yang harus dilewati: baseline_smooth50 pada pertandingan penuh.
BASELINE_FLOOR_SPELL_F1 = 0.2433
