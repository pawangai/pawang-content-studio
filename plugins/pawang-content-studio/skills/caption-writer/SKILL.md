---
name: caption-writer
description: Tulis caption siap unggah untuk konten sosial media (carousel, reel/short/TikTok, foto, story, testimoni, promo, thumbnail) di banyak platform sekaligus (Instagram, TikTok, LinkedIn, X, Threads, Facebook, Pinterest, YouTube Shorts, WhatsApp Status) dengan hook, isi, CTA, hashtag, alt text, komentar pertama, dan alternatif hook, disesuaikan dengan suara brand. Skill ini memeriksa batas karakter tiap platform, panjang hook sebelum "selengkapnya", jumlah hashtag, link yang tidak bisa diklik di Instagram/TikTok, klaim berlebihan, dan caption yang terlalu mirip antar-platform. Gunakan setiap kali user meminta caption, deskripsi postingan, kata-kata untuk posting, hashtag, alt text, atau "tulis teks untuk diunggah", terutama setelah gambar/video/jadwal siap, bahkan jika user tidak menyebut kata "skill".
---

# Caption Writer

Menulis caption yang siap salin dan unggah, satu versi per platform (bukan satu caption yang ditempel di mana-mana). Anda penulisnya; skrip `scripts/captions.py` memeriksa batas dan kualitas dasar, lalu menyusun file hasil.

## Alur kerja

1. **Kumpulkan input.**
   - Konten: topik, jenis (carousel, reel, foto, story, testimoni, promo), dan isinya bila ada (teks carousel, naskah reel, hook). Jika user memberi teks konten, caption harus konsisten dengannya dan tidak mengulang seluruh isi slide.
   - Platform tujuan. Jika tidak disebut, tanyakan satu kali; bila user ingin cepat, pakai Instagram dan TikTok.
   - Tujuan (edukasi, simpan/bagikan, konsultasi, penjualan), CTA brand, dan suara brand (pakai Brand Lock / Voice Lock bila ditempel; kalau tidak, simpulkan dari konten dan sebutkan asumsinya).
2. **Tulis per platform** mengikuti `references/caption-guide.md`: hook di baris pertama, 2-3 kalimat nilai, CTA, hashtag. Tiap platform punya sudut dan panjang yang berbeda.
3. **Data yang harus dari user** (kutipan klien, nama, harga, tanggal/periode promo, nomor, metrik hasil): jangan dikarang. Pakai `[ISI SENDIRI: keterangan]`, atau tanyakan dalam satu pesan singkat.
4. **Tulis `captions.json`** (`python scripts/captions.py --example` untuk skema) lalu jalankan `python scripts/captions.py render captions.json /mnt/user-data/outputs/caption_<topik>.md`.
   - Perbaiki semua **Galat** (melebihi batas, caption kosong, kurung kurawal, hashtag salah format).
   - Baca **Peringatan** dan perbaiki yang beralasan: hook terlalu panjang, jumlah hashtag, link yang tidak bisa diklik (ubah ke "link di bio"), klaim berlebihan, tidak ada CTA, caption mirip antar-platform. Peringatan boleh dibiarkan bila ada alasan, tetapi sebutkan alasannya.
5. **Serahkan.** Satu atau dua platform: tampilkan caption langsung di balasan dalam code block. Tiga platform atau lebih: simpan file `.md` dan `present_files`. Cantumkan daftar `[ISI SENDIRI]` yang tersisa dan catatan yang perlu diketahui (mis. link di bio).

## Prinsip

- **Hook dulu.** Baris pertama harus membuat orang berhenti sebelum "selengkapnya" (Instagram sekitar 125 karakter, LinkedIn sekitar 140). Sediakan 2 alternatif hook untuk platform utama.
- **Sesuaikan, jangan salin.** Instagram: hangat dan ringkas; TikTok: sangat pendek, mengikuti video; LinkedIn: profesional dan berstruktur; X: satu pernyataan; Pinterest: kata kunci yang dicari orang; YouTube Shorts: judul jelas. Skrip menandai caption yang >85% mirip.
- **CTA lembut dan tunggal.** Satu ajakan utama per caption (simpan, bagikan, komentar, konsultasi). Di Instagram dan TikTok link di caption tidak bisa diklik, jadi arahkan ke "link di bio".
- **Hashtag sedikit dan relevan** (sekitar 3-5 di Instagram, TikTok, LinkedIn; 0-2 di X dan Facebook). Campur satu-dua yang luas dengan yang spesifik niche. Di TikTok hashtag ikut dihitung dalam batas karakter.
- **Alt text** untuk gambar/carousel: satu kalimat yang menjelaskan isi visual, tanpa "gambar dari".
- **Tidak mengarang dan tidak melebih-lebihkan**: tanpa "dijamin", "pasti", "100%", angka hasil, atau testimoni yang tidak diberikan user.
- **Batas karakter bisa berubah.** Angka di skrip adalah batas aman konservatif dari sumber publik yang tidak seragam (mis. TikTok dilaporkan 2.200 atau 4.000, Pinterest 500 atau 800). Jika user menanyakan batas terkini, cari sumber resmi platform.

## File

- `scripts/captions.py` - `render`, `check`, `--example`, `--limits`
- `references/caption-guide.md` - struktur caption, rumus hook, aturan per platform, alt text, contoh per jenis konten
