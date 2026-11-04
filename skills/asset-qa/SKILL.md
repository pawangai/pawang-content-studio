---
name: asset-qa
description: Periksa kualitas gambar dan video hasil ChatGPT/Google Flow/AI lain terhadap brand dan platform, lalu tulis prompt perbaikan siap tempel. Mengecek ejaan teks pada gambar, kepatuhan warna terhadap palet brand, teks yang masuk zona tidak aman (tertutup UI story/reels/feed), ukuran dan kontras teks, rasio dan resolusi, logo atau karakter yang berubah dari acuan, anatomi janggal, serta pada video meliputi lonjakan atau glitch antar-frame, drift warna, teks yang berubah bentuk, audio, dan durasi. Gunakan setiap kali user mengunggah gambar atau video hasil AI dan bertanya "sudah benar belum", "cek hasil ini", "ada yang salah?", "kenapa teksnya aneh", meminta QA, review, atau perbaikan hasil, bahkan jika user tidak menyebut kata "QA" atau "skill".
---

# Asset QA

Memeriksa hasil AI sebelum diunggah, lalu menulis perintah perbaikan yang bisa langsung ditempel. Pemeriksaan terbaik adalah gabungan **mata Anda** (membaca gambar langsung) dan **skrip** (angka yang tidak bisa dilihat mata: persentase warna di luar palet, posisi teks terhadap zona aman, kontras, lonjakan antar-frame).

## Alur kerja

1. **Terima input**: gambar/video hasil, format tujuan (story, reels, feed, square, og, wide, pinterest; `python scripts/qa_image.py --formats`), brand (palet warna dari `profile.json` atau `--colors`), teks yang seharusnya tertulis (daftar kalimat persis), dan gambar acuan logo/karakter bila ada. Jika format tujuan tidak disebut, simpulkan dari rasio gambar dan sebutkan asumsinya.
2. **Lihat dengan mata dulu.** Buka gambar (atau lembar kontak video) dan baca teksnya sendiri. Catat: ejaan tiap kata terhadap teks yang diharapkan, logo, karakter, jumlah jari/anggota tubuh, benda aneh, teks acak, tepi terpotong. OCR hanya pelengkap (bahasa Inggris, font dekoratif sering salah baca), jadi **konfirmasi visual selalu menang** atas OCR.
3. **Jalankan skrip.**
   - Gambar: `python scripts/qa_image.py hasil.png --format story --profile profile.json --expect "Kalimat 1|Kalimat 2"`
   - Video: `python scripts/qa_video.py klip.mp4 --format reels --profile profile.json --expect-duration 24` (atau `--colors "Nama=#HEX,..."`) lalu **lihat `contact.jpg`** dan frame yang ditandai.
   - Logo/karakter: `python scripts/logo_compare.py acuan.png hasil.png [--crop x0,y0,x1,y1]`; skor tinggi cukup meyakinkan, skor rendah pada logo datar sederhana bukan bukti berbeda, jadi bandingkan berdampingan.
4. **Susun laporan** dengan tabel: Pemeriksaan | Hasil (lolos/perlu perbaikan) | Temuan | Perbaikan. Urutkan dari yang paling merusak (ejaan, logo/karakter, teks tertutup UI) ke yang kosmetik. Jangan melaporkan lolos pada hal yang tidak benar-benar Anda periksa; tulis "tidak diperiksa" bila datanya tidak ada.
5. **Tulis prompt perbaikan**: isi `issues.json` lalu `python scripts/fixprompts.py issues.json fix.md` (tipe: spelling, palette, logo, character, safe_zone, small_text, contrast, extra_text, ratio, anatomy, video_text, video_glitch). Satu masalah per prompt; ChatGPT dan Flow lebih stabil jika diubah satu hal per percobaan. Rujuk `references/qa-checklist.md` untuk urutan prioritas dan strategi.
6. **Serahkan**: laporan singkat di balasan, prompt perbaikan dalam code block (1-3 prompt langsung di balasan; lebih dari itu simpan file `.md` dan `present_files`). Sebutkan keputusan akhir: **layak unggah / perbaiki dulu / buat ulang**.

## Aturan keputusan

- **Layak unggah**: tidak ada salah eja, logo/karakter sesuai, tidak ada teks di zona tertutup UI, warna masuk palet.
- **Perbaiki dulu**: satu atau dua masalah lokal (ejaan, satu warna, posisi).
- **Buat ulang**: karakter/logo berubah menyeluruh, anatomi rusak, atau banyak masalah sekaligus; lebih cepat membuat ulang dengan prompt yang lebih ketat.
- **Video dengan teks di dalamnya**: sarankan membuang teks dari video dan menambahkannya di CapCut/Canva; teks dalam video AI jarang stabil.

## Batas yang perlu jujur disampaikan

- OCR tidak mengenali semua font; "tidak ditemukan" pada teks dekoratif belum tentu salah, dan teks yang terbaca benar oleh OCR tetap perlu dicek mata.
- Pemeriksaan palet memakai selisih warna rata-rata; pencahayaan dan gradasi membuat warna bergeser sedikit dan itu wajar.
- Zona aman adalah patokan umum; tampilan aplikasi berubah, jadi uji satu postingan dulu.
- Skrip tidak menilai keindahan atau kecocokan pesan; itu penilaian Anda.

## File

- `scripts/qa_image.py` - rasio, palet, OCR, zona aman, ukuran dan kontras teks, ejaan terhadap `--expect`
- `scripts/qa_video.py` - info teknis, frame, lembar kontak, lonjakan, drift warna, audio, durasi
- `scripts/logo_compare.py` - perbandingan logo/karakter dengan acuan
- `scripts/fixprompts.py` - prompt perbaikan siap tempel
- `references/qa-checklist.md` - daftar periksa dan strategi perbaikan
