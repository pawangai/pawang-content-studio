# Tips dan Trik

## Cara bicara dengan Claude
- **Sebut nama skill bila tidak terpicu**: "Gunakan skill `command-filler` untuk mengisi command ini."
- **Satu tahap per percakapan** supaya konteks tetap bersih. Mulai percakapan baru dengan: "Baca `profile.json` ini" dan unggah profil.
- **Tempel hanya yang dibutuhkan**: satu atau dua command, bukan seluruh file.
- **Sebut format tujuan** ("story 9:16", "reels", "feed 4:5") agar QA dan layout tepat.
- **Minta ringkasan asumsi** di akhir; periksa sebelum memakai.

## Data dan brand
- `profile.json` adalah **satu sumber kebenaran**. Ubah di sana, ekspor ulang; jangan mengedit file turunan satu per satu.
- Periksa **tabel kontras** profil: aksen oranye di atas krem biasanya gagal untuk teks. Pakai aksen untuk tombol dan ikon, teks tetap gelap.
- **Prefix unik** (`pw`, `ks`) agar command tidak bentrok antar-brand.
- **Brand baru = folder dan profil baru**; salin struktur folder, bukan isinya.
- Data yang tidak Anda berikan akan ditandai `[ISI SENDIRI]`, bukan dikarang. Itu fitur: isi, jangan hapus penandanya sebelum yakin.

## Gambar (ChatGPT)
- Tempel **Brand Lock** di Project/Custom Instructions; unggah brand board sekali di tiap percakapan baru.
- **Carousel satu slide per permintaan**, lalu "lanjut slide berikutnya, gaya identik".
- **Teks gambar pendek** dan dieja persis. Teks panjang hampir selalu salah eja; tambahkan di Canva.
- **Logo resmi** tempel dari file aslinya; AI boleh membuat variasi, bukan pengganti file master.
- Salah eja? Ketik `Perbaiki teks saja menjadi: "..." . Jangan ubah elemen lain.`

## Video (Flow)
- **Satu klip, satu aksi, satu gerakan kamera.**
- **Tanpa teks di dalam video**; teks ditambah di CapCut.
- Karakter harus sama? Pakai **Ingredients** dengan gambar acuan yang sama.
- Sambung adegan dengan frame terakhir klip sebelumnya sebagai frame awal klip berikutnya.
- Hasil buruk: ulangi dengan **satu** perubahan kecil, bukan semuanya.
- Uji **satu klip** sebelum membuat empat, supaya kredit tidak terbuang.

## Jadwal
- Mulai **Ringan** (3 konten utama per minggu), naik ke Standar setelah 4 minggu konsisten.
- **Produksi batch**: satu blok kerja untuk seminggu konten; jadwalkan postingan sekali.
- **Jam posting adalah hipotesis.** Uji selama 4 minggu dengan Insights akun Anda sendiri, ubah satu variabel pada satu waktu.
- Satu topik, banyak konten: carousel, reel, 3 story, kartu tips, thread, pin (lihat bagian daur ulang di kalender).
- Cek tanggal hari besar sendiri (11.11, Ramadan, libur); tanggalnya bergeser.

## Anti duplikat
- Jalankan cek duplikat **sebelum produksi**, bukan sesudah.
- Isi kolom **Hook** dan **Slug** di Content Log; pemeriksa memakainya.
- **MIRIP bukan larangan**: ubah sudut, platform, atau format.
- Catat konten yang **sudah terbit** segera, supaya log selalu terbaru.

## Kualitas (QA)
- Baca teks pada gambar **dengan mata**; OCR hanya pembantu.
- Urutan prioritas: ejaan > logo/karakter > anatomi > zona aman > warna > ukuran dan kontras > rasio.
- Dua kali perbaikan gagal = buat ulang dengan prompt lebih ketat.

## Konten panjang dan Quora
- Bahan nyata dulu, riset kemudian: pengalaman Anda adalah pembeda; skill tidak akan mengarang studi kasus atau angka.
- Satu artikel -> carousel, reel, kartu tips, post Threads, jawaban Quora, newsletter. Jadwalkan dalam 10 hari agar tidak menumpuk.
- Quora: jawab dulu pertanyaannya, ungkapkan hubungan dengan brand bila disebut, paling banyak satu tautan, hindari menempel jawaban yang sama.
- Periksa aturan platform tentang bantuan AI (Medium, LinkedIn, komunitas); sunting draf sendiri sebelum terbit.
- Skrip YouTube: hook 30 detik, bab minimal tiga dengan tiap bab >= 10 detik, sekitar 150 kata per menit.

## Percakapan dengan calon klien
- Balas komentar singkat, **pindah ke DM** untuk detail; keluhan di DM, bukan debat di publik.
- Jangan sebut harga final di komentar; tawarkan konsultasi.
- Jangan pernah meminta atau menyimpan kata sandi/OTP lewat chat.
- Pesan otomatis hanya untuk di luar jam layanan dan kata kunci; jangan untuk harga atau komplain.

## Evaluasi
- Median lebih jujur daripada rata-rata; satu posting viral jangan mengubah strategi.
- Metrik terdekat dengan bisnis: **pesan masuk** dan konsultasi, bukan jangkauan.
- Format kuat di jangkauan tetapi lemah di pesan masuk: perbaiki CTA dulu sebelum mengurangi.

## Perawatan repo
- `python scripts/smoke_test.py` setelah mengubah skill, untuk memastikan alur masih tersambung.
- `python scripts/build_all.py` untuk validasi dan kemas ulang; unggah ulang `.skill` yang berubah (hapus versi lama dulu).
- Catat perubahan penting di `CHANGELOG.md` (buat sendiri bila perlu).
- Simpan `dist/` dan `profile.json` sebagai cadangan.
