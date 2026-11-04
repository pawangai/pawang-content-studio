# Pemecahan Masalah

| Gejala | Kemungkinan penyebab | Tindakan |
|---|---|---|
| Skill tidak muncul atau abu-abu | Code execution and file creation belum aktif | Aktifkan di Settings > Capabilities (individu) atau pengaturan organisasi (Team/Enterprise) |
| Unggahan ditolak | ZIP berisi lebih dari satu skill, nama folder tidak sama dengan `name`, atau ukuran terlalu besar | Unggah **satu skill per ZIP** dari `dist/`; jangan ubah nama folder |
| Unggahan ditolak karena deskripsi | Ada dokumentasi yang menyebut batas deskripsi 200 karakter di Claude.ai (spesifikasi umum 1024) | Pakai `dist-short/` (deskripsi di bawah 200 karakter) |
| Skill tidak terpicu otomatis | Deskripsi tidak cocok dengan cara Anda meminta | Sebut nama skill secara eksplisit |
| Skrip gagal: modul tidak ada | Pustaka (Pillow, numpy, OpenCV) tidak ada di lingkungan | `asset-qa` tetap bisa dipakai sebagian (visual oleh Claude); minta Claude melewati langkah itu |
| OCR salah baca | Font dekoratif, OCR hanya bahasa Inggris | Baca dengan mata; OCR bukan penentu |
| Konektor tidak muncul | Belum dipasang atau izin belum diberikan | Pasang di pengaturan konektor, lalu minta Claude memeriksa daftar alat |
| Claude berkata berhasil menulis ke Drive tetapi tidak ada | Konektor tidak tersedia atau gagal | Minta bukti (nama berkas/tautan); bila tidak ada, gunakan unduhan manual |
| Pemeriksa duplikat melewatkan topik yang sama | Kata-kata berbeda jauh | Bandingkan manual; isi kolom Hook dan Slug |
| Kalender melapor "bukan hari Senin" | `start` di brand.json salah | Ganti ke Senin terdekat |
| Hasil gambar warna melenceng | Palet tidak dikunci | Tempel Brand Lock lengkap dengan hex; sebut "hanya warna ini" |
| Teks video berubah bentuk | Teks di dalam video AI | Buat ulang tanpa teks; tambah di CapCut |
| Kontras warna gagal | Pasangan warna tidak memenuhi WCAG | Ikuti tabel kontras profil; pakai warna aksen hanya untuk tombol/ikon |
