# Struktur Folder Google Drive (satu folder per brand)

```
<Nama Brand>/
├── 00-Brand/
│   ├── profile.json              # sumber tunggal brand (brand-profile-builder)
│   ├── brand-spec.md             # hasil brandboard-standard
│   ├── brand-board.png           # gambar acuan untuk ChatGPT
│   └── logo/                     # logo asli (vektor/PNG) dan maskot acuan
├── 01-Kalender/
│   ├── Content Log (Sheet)       # semua konten: rencana, status, tautan   <- dipakai cek konten ganda
│   └── jadwal-<bulan>.md         # kalender dari content-calendar-pack
├── 02-Aset/
│   └── 2026-10/                  # satu folder per bulan
│       ├── 2026-10-26_carousel_4-tanda-data-liar/
│       │   ├── slide-1.png ...  
│       │   └── caption.md
│       └── 2026-10-27_reel_satu-angka-lima-file/
│           ├── klip-1.mp4 ...
│           └── final.mp4
├── 03-Command/                   # file command (gambar, video, teks)
├── 04-Insights/                  # ekspor CSV Insights per bulan (performance-analyzer)
├── 05-Leads/
│   └── Lead Tracker (Sheet)
└── 06-Laporan/                   # laporan performa dan QA
```

Aturan penamaan aset: `YYYY-MM-DD_format_slug-topik/`. Satu konten = satu folder. Status di Content Log memakai: ide, rencana, draf, qa, jadi, terjadwal, terbit, arsip.
