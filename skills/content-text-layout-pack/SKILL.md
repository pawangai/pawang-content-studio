---
name: content-text-layout-pack
description: Buat file Markdown panduan teks, layout, dan waktu untuk konten sosial media yang diedit di Canva atau CapCut — mencakup teks apa yang diisi, posisi dan ukuran font, zona aman, serta detik keberapa teks muncul untuk carousel, story IG/WA, post foto, Reels/TikTok/Shorts, thumbnail, OG image, caption, plus command prompt (/prefix-t-...) untuk membuat teks sesuai topik. Gunakan skill ini setiap kali user bingung "teks apa yang harus ditulis", "layout-nya seperti apa", "di menit/detik berapa teks muncul", ingin template teks carousel/story/reel/short setelah gambar atau video dibuat di ChatGPT dan Google Flow, atau ingin panduan Canva/CapCut berbasis brand, bahkan jika user tidak menyebut kata "skill".
---

# Content Text Layout Pack

Menghasilkan satu file `.md` yang menjawab tiga pertanyaan editor: **teks apa**, **di mana**, **kapan**. Gambar dan video dibuat tanpa teks (ChatGPT, Flow); teks ditambahkan di Canva/CapCut memakai file ini. Semua teks contoh dan prompt ada di code block agar bisa disalin.

Bagian generik (aturan kata, ukuran font, zona aman, rumus durasi teks, pola layout, langkah Canva/CapCut, command `/prefix-t-...`) disusun skrip. Bagian yang menentukan mutu adalah **contoh isi yang Anda tulis** khusus brand dan topik user.

## Alur kerja

1. **Ambil brand** dari input (brand board, deskripsi, atau `brand.json` dari skill `brand-command-pack` / `flow-video-command-pack`; pakai ulang awalan dan palet yang sama). Skema: `references/brand-json.md`.
2. **Tulis `examples` dengan serius.** Ini inti pekerjaan Anda:
   - `topic`: satu topik nyata untuk brand ini
   - `carousel`: tepat 7 slide (hook, masalah, 4 poin, CTA); hook maksimal 8 kata
   - `story`: 3-5 story dengan `tujuan` dan `teks`
   - `reels`: tabel detik demi detik (`waktu` format `0:00-0:03`, tanpa celah, `visual`, `teks`, `posisi`, `animasi`). Selaraskan dengan klip Flow bila user memakai `flow-video-command-pack` (satu baris atau dua per klip)
   - `foto`, `hooks`, `ctas`, `thumbnails`, `caption`
   Jangan mengarang data, angka, atau testimoni; pakai pernyataan umum yang bisa dipertanggungjawabkan, atau placeholder `{...}` jika butuh data user.
3. **Tanya hanya jika perlu**: satu pertanyaan ringkas jika brand atau topik tidak bisa disimpulkan. Selain itu asumsikan dan sebutkan.
4. **Render**: `python scripts/build_pack.py brand.json /mnt/user-data/outputs/<brand>_panduan_teks_layout.md`. Skrip memvalidasi struktur dan **lint isi contoh**: hook > 8 kata, teks video > 6 kata per baris, teks tampil lebih singkat dari rumus `1 detik + 0,3 detik x kata`, celah waktu, dan total durasi tidak cocok. Perbaiki `examples` sampai lint bersih, lalu render ulang.
5. **Tinjau**: baca tabel reels dan carousel seolah-olah Anda editornya. Apakah posisi dan animasi masuk akal, apakah CTA muncul di 3-4 detik terakhir, apakah hook sebelum detik ke-3.
6. **Serahkan** dengan `present_files`. Balasan singkat: bagian isi, asumsi, dan catatan bahwa angka zona aman adalah patokan umum yang perlu diuji satu konten dulu karena tampilan aplikasi berubah.

## Prinsip

- Hook sebelum detik ke-3, CTA di 3-4 detik terakhir, ganti teks atau visual setiap 2-4 detik.
- Teks maksimal 6 kata per baris di video, minimal 48 px agar terbaca di ponsel.
- Teks tidak ditaruh di zona yang tertutup UI aplikasi (atas sekitar 250 px, bawah sekitar 340 px story / 450 px video).
- Warna teks hanya dari palet brand; satu atau dua kata penekanan per layar.
- Teks selalu ditambahkan di editor, bukan di dalam gambar atau video AI, karena teks AI sering salah eja atau berubah bentuk.

## File

- `scripts/build_pack.py` - render, validasi, dan lint (`--example`, `--check`)
- `references/brand-json.md` - skema `brand.json` dan panduan menulis `examples`
