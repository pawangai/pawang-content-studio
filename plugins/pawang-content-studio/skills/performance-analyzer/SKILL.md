---
name: performance-analyzer
description: Analisis data performa konten sosial media (Insights Instagram, TikTok, LinkedIn, YouTube, atau tabel pencatatan sendiri) setelah sekitar 4 minggu posting, lalu tunjukkan jam, hari, format, pilar, dan platform yang paling efektif, dan revisi kalender konten berdasarkan data. Memakai median, menandai sampel kecil, memperingatkan faktor yang tercampur (mis. jam dan format selalu berpasangan), dan hanya menyarankan perubahan yang cukup didukung data. Gunakan setiap kali user menempelkan atau mengunggah data statistik postingan (CSV/tabel/screenshot Insights), bertanya "jam posting terbaik saya kapan", "konten mana yang paling bagus", "kenapa jangkauan turun", "evaluasi 4 minggu", meminta analisis performa atau revisi jadwal, bahkan jika user tidak menyebut kata "analisis" atau "skill".
---

# Performance Analyzer

Mengubah angka Insights menjadi keputusan jadwal yang jujur. Skrip `scripts/analyze.py` menghitung agregat per format, pilar, platform, hari, dan waktu; Anda menafsirkan, memberi konteks, dan menulis rekomendasi yang realistis.

## Alur kerja

1. **Terima data.** Format yang diharapkan (`python scripts/analyze.py --template`): Tanggal, Jam, Platform, Format, Pilar, Topik, Jangkauan, Simpan, Bagikan, Komentar, Klik link, Pesan masuk. Jika user hanya punya screenshot Insights atau tabel di chat, baca angkanya dan ubah menjadi CSV; **tanyakan bila angka tidak terbaca jelas, jangan menebak**. Jika kolom pilar/format kosong, ambil dari kalender konten user (cocokkan tanggal). Data minimal 8 posting, ideal 20 atau lebih dari 4 minggu; jika kurang, katakan data belum cukup dan sarankan menunggu.
2. **Periksa kualitas data**: tanggal valid, jangkauan > 0, satuan seragam (mis. tayangan vs jangkauan jangan dicampur), periode tidak mencakup libur/momen khusus tanpa dicatat. Catat masalahnya di laporan.
3. **Jalankan**: `python scripts/analyze.py data.csv --out laporan.md --json saran.json [--min-n 4] [--lift 1.25]`. `--min-n` adalah sampel minimum per grup, `--lift` adalah selisih minimum antara grup terbaik dan kedua agar disebut pemenang.
4. **Tafsirkan** (lihat `references/interpretation-guide.md`):
   - Pisahkan tujuan: jangkauan (pintu masuk), simpan/bagikan (nilai konten), klik dan **pesan masuk** (hasil bisnis). Format dengan jangkauan tinggi belum tentu menghasilkan pesan.
   - Laporkan hanya yang melewati ambang; sisanya "belum jelas".
   - Beri tahu bila jam dan format tercampur, dan rancang uji: format yang sama di dua jam berbeda selama 2-4 minggu.
5. **Tulis rekomendasi**: maksimal 3 perubahan, masing-masing dengan alasan berbasis angka, tingkat keyakinan (rendah/sedang/tinggi), dan cara mengujinya. Ubah satu variabel pada satu waktu.
6. **Revisi kalender**: sesuaikan `rhythm` (jam), porsi pilar, atau frekuensi format di `profile.json`/`brand.json` skill `content-calendar-pack`, lalu render ulang kalender; sertakan ringkasan perubahan sebelum-sesudah.
7. **Serahkan** laporan (`laporan.md` lewat `present_files`, ringkasannya di balasan): temuan utama, apa yang belum bisa disimpulkan, rekomendasi, dan data yang perlu dikumpulkan berikutnya.

## Prinsip

- **Median, bukan rata-rata**; satu posting viral tidak boleh mengubah strategi. Tampilkan outlier terpisah.
- **Sampel kecil tidak disimpulkan.** Dengan n < 4 per grup, katakan "belum cukup data".
- **Korelasi bukan sebab.** Topik, momen (11.11, tanggal gajian, libur), dan kualitas visual ikut memengaruhi hasil; sebutkan.
- **Jam terbaik berasal dari pengikut Anda**, bukan dari artikel umum. Gunakan Insights "jam aktif pengikut" sebagai pelengkap untuk memilih jam uji.
- **Jangan mengarang** angka, tren, atau penyebab; bila tidak yakin, tulis hipotesis dan cara mengujinya.
- **Jangan terlalu cepat memangkas.** Format yang lemah di pesan masuk tetapi kuat di jangkauan mungkin berperan sebagai pintu masuk; perbaiki CTA dulu.

## File

- `scripts/analyze.py` - analisis agregat, deteksi faktor tercampur, laporan `.md`, saran `.json`
- `references/interpretation-guide.md` - cara membaca metrik, ambang keputusan, desain uji, templat laporan
