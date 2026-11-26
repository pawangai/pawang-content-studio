# Pawang Content Studio

Rangkaian 14 skill yang tersambung lewat satu profile.json: identitas brand, command gambar dan video, panduan teks dan layout, jadwal bertanggal, caption, artikel dan skrip YouTube, jawaban Quora, QA aset, balasan DM, dan evaluasi performa.

Skill aktif otomatis saat permintaan cocok dengan deskripsinya. Bila tidak terpicu, sebut nama skill secara eksplisit, misalnya: *"Gunakan skill asset-qa untuk memeriksa gambar ini."*

## Skill

| Skill | Fungsi |
|---|---|
| `content-pipeline` | Pengarah alur konten end-to-end (pilih skill per tahap, cek konten ganda lewat Content Log, catat ke Drive/Sheets, jadwalkan ke Calendar). Pakai saat memulai sesi atau bingung langkah berikutnya. |
| `brand-profile-builder` | Ubah brand board, Brand Spec, atau deskripsi jadi profile.json tunggal, cek kontras warna, buat Brand/Voice Lock, ekspor ke skill lain. Pakai saat user bilang ini brand saya atau ganti data brand. |
| `brandboard-standard` | Buat, audit, atau samakan brand board satu halaman dengan 16 section standar, menghasilkan Brand Spec Markdown dan prompt gambar. Pakai saat user minta brand board atau brand guideline. |
| `brand-command-pack` | Buat file command prompt gambar siap salin untuk ChatGPT (logo, carousel, story, OG, feature image, X, Pinterest, iklan, mockup) dari brand board. Pakai saat user minta kumpulan command konten. |
| `content-text-layout-pack` | Buat panduan teks, layout, ukuran font, zona aman, dan detik tampil teks untuk carousel, story, reel, thumbnail di Canva atau CapCut, plus command pembuat teks. Pakai saat bingung teks dan layout. |
| `flow-video-command-pack` | Buat file command prompt video siap salin untuk Google Flow (hook reels, story, cerita 4 adegan, before-after, transisi) dari gambar ChatGPT. Pakai saat user mau video pendek atau animasi maskot. |
| `content-calendar-pack` | Buat jadwal konten bertanggal (hari, jam WIB, platform, format, pilar, topik, command), plus gudang topik dan evaluasi. Pakai saat user bingung posting apa, kapan, dan topiknya. |
| `caption-writer` | Tulis caption siap unggah per platform (Instagram, TikTok, LinkedIn, X, Pinterest, YouTube Shorts) dengan hook, CTA, hashtag, alt text, dan cek batas karakter. Pakai saat user minta caption. |
| `command-filler` | Isi semua isian kurung kurawal pada command prompt berdasarkan topik user sampai siap tempel, patuhi batas kata, tandai data wajib dari user. Pakai saat command masih berisi isian. |
| `longform-writer` | Tulis artikel blog SEO, Medium, LinkedIn Article, newsletter, dan skrip YouTube berbasis riset bersumber, dengan pemeriksa otomatis dan rencana daur ulang. Pakai saat user minta tulisan panjang. |
| `quora-answer-writer` | Tulis jawaban Quora yang bermanfaat dan jujur (cek kebijakan, struktur, pengungkapan brand, satu tautan) dengan pemeriksa tautan, promosi, dan klaim. Pakai saat user menyebut Quora atau Q&A. |
| `asset-qa` | Periksa gambar atau video hasil AI (ejaan, palet warna, zona aman, kontras, logo atau karakter berubah, glitch video), lalu tulis prompt perbaikan. Pakai saat user minta cek hasil. |
| `inbound-reply-pack` | Siapkan alur dan template balasan komentar, DM, dan WhatsApp sampai konsultasi, aturan eskalasi, pencatatan lead, dan balas pesan nyata. Pakai saat user tanya cara membalas calon klien. |
| `performance-analyzer` | Analisis data Insights 4 minggu (jam, hari, format, pilar terbaik) dengan median dan peringatan sampel kecil, lalu revisi kalender. Pakai saat user menempel data statistik posting. |

## Prasyarat

- `asset-qa` memakai Pillow dan numpy (opsional OpenCV, Tesseract, ffmpeg). Pasang dengan `pip install Pillow numpy opencv-python-headless pytesseract`.
- Skill lain hanya memakai pustaka standar Python 3.9+.
