"""Seat 3 (Billa) -- model sekuensial, dead-ball, dan segmentasi.

Isi folder ini: dari fitur per frame menjadi label per frame.

BENTUK MASALAHNYA
Ini masalah *sequence labelling*: 199.319 frame berurutan yang saling
bergantung, dan satu label untuk setiap frame. Empat baseline di repo resmi
memakai pendekatan per frame lalu menghaluskannya; kalian bisa melangkah lebih
jauh dengan model yang memang melihat urutan.

URUTAN PENGERJAAN -- jangan dibalik
  1. **Dead-ball dulu** (bagian 7.1). Ini lubang terbesar di baseline, dan
     docstring baseline-nya mengakuinya sendiri:
       "It has no notion of a dead ball beyond 'the tracking lost the ball',
        which is why its D class is weak."
  2. Atribusi ``H``/``A`` untuk frame bola hidup (bagian 7.3).
  3. Segmentasi anti-fragmentasi (bagian 7.4) -- dari probabilitas per frame jadi
     interval.
  4. Baru model sekuensial (bagian 7.6), dan hanya kalau mengalahkan versi aturan
     pada confidence interval yang tidak tumpang tindih.

DUA ANGKA YANG MENENTUKAN SELURUH PEKERJAAN DI FOLDER INI
  - Scorer **tidak punya minimum panjang possession**. Satu frame dihitung
    possession utuh. Satu serpihan = satu false positive.
  - ``fp`` juga dihitung untuk possession kalian yang overlap dengan possession
    asli tapi IoU-nya di bawah ambang. Jadi memecah satu possession asli jadi
    dua menghasilkan **1 FP + 1 FN sekaligus**.

  Dan yang berlawanan arah, yang mudah terlewat: possession terpendek di GT
  publik adalah **19 frame (0,76 detik)** dan itu possession SUNGGUHAN. Jadi
  minimum spell kalian harus konservatif. Detailnya di
  ``docs/gt-public-transitions.md`` pertanyaan 3.

ATURAN YANG TIDAK BISA DITAWAR
  Semua label harus keluar dari algoritma. Tidak ada hand label pada
  pertandingan ini, dalam jumlah berapa pun, untuk tujuan apa pun -- termasuk
  untuk melatih atau memvalidasi model. Lihat ``docs/PLAYBOOK.md`` bagian 9.
"""
