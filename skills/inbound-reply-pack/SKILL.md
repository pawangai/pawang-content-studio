---
name: inbound-reply-pack
description: Siapkan paket balasan untuk komentar publik, DM Instagram, dan WhatsApp agar calon klien yang menghubungi ditangani dengan baik dari pesan pertama sampai konsultasi. Berisi alur 8 tahap, 30 lebih template balasan siap salin (pujian, tanya harga, INFO, tanya layanan atau paket, portofolio, durasi, nego, penjadwalan, pengingat, follow-up D+1/D+3/D+7, penolakan, di luar layanan, data sensitif, komplain, minta testimoni), aturan eskalasi, format pencatatan lead, dan command pembuat balasan khusus untuk pesan yang sedang dihadapi. Template memeriksa batas panjang, klaim berlebihan, dan larangan meminta kata sandi atau data pribadi. Gunakan setiap kali user bertanya cara membalas komentar/DM/WhatsApp, calon klien bertanya harga, ada keluhan, ingin template balasan, alur penanganan lead, follow-up, atau auto-reply, bahkan jika user tidak menyebut kata "skill" atau "template".
---

# Inbound Reply Pack

Konten hanya berguna jika pesan yang masuk dibalas dengan baik. Skill ini membuat satu file `.md` berisi template balasan, alur, dan aturan eskalasi yang sesuai suara brand, serta membantu menulis balasan untuk pesan nyata yang ditempel user.

## Mode 1: membuat paket balasan

1. **Ambil data** dari profil brand (skill `brand-profile-builder`: `profile.py export profile.json --for reply reply.json`) atau dari user langsung: nama brand, `prefix`, sapaan (`address`: Kak / Bapak/Ibu / Anda), nada, CTA, URL, layanan (nama dan manfaat), paket (harga bila sudah ditetapkan), kontak (WhatsApp, email, tautan booking), jam layanan, target respons, FAQ resmi.
2. **Jangan mengarang kebijakan.** Harga, durasi, diskon, tautan portofolio, tautan booking, dan jawaban FAQ yang belum diberikan user dibiarkan kosong; skrip menandainya `[ISI SENDIRI: ...]`. Tanyakan sekali, singkat, untuk yang paling penting (nomor WhatsApp, tautan booking, jam layanan, harga paket jika ada); sisanya boleh menyusul.
3. **Render**: `python scripts/build_replies.py reply.json /mnt/user-data/outputs/<brand>_paket_balasan.md`. Skrip menyusun alur 8 tahap, template per kanal, eskalasi, pencatatan lead, dan command, lalu memvalidasi: batas karakter (komentar 220, DM 700), klaim berlebihan (dijamin, pasti, 100%, terbaik), template yang meminta data sensitif (kata sandi, OTP, KTP, kartu), dan token tersisa.
4. **Sesuaikan dengan bisnis**: ubah contoh `{masalah}` pada template layanan menjadi situasi umum yang nyata, tambah FAQ dari pertanyaan yang sering diterima user, dan pastikan sapaan konsisten. Setelah mengedit, jalankan `python scripts/build_replies.py --check file.md`.
5. **Serahkan** dengan `present_files` dan balasan singkat: isi paket, daftar `[ISI SENDIRI]` yang harus dilengkapi (termasuk yang harus diputuskan pemilik, seperti kebijakan diskon), dan tiga langkah memulai (atur balasan otomatis, simpan template di fitur balasan cepat, mulai catat lead).

## Mode 2: membalas pesan nyata

Jika user menempel pesan atau percakapan, tulis balasan langsung (tanpa membuat file):
1. Tentukan kanal (komentar/DM/WA), tahap alur (1-8), dan niat pesan (tanya harga, komplain, siap beli, dll.).
2. Tulis **dua pilihan** balasan, singkat dan lebih lengkap, sesuai Voice Lock dan sapaan brand, dengan **satu** ajakan. Jangan menjanjikan harga, tanggal, atau hasil yang belum ditetapkan user.
3. Tandai `[ISI SENDIRI]` untuk hal yang harus diputuskan user.
4. Jika pesan berisi keluhan serius, ancaman, data sensitif, atau permintaan di luar kewenangan, katakan perlu eskalasi dan beri saran langkah (lihat bagian eskalasi di `references/reply-principles.md`).
5. Untuk beberapa pesan sekaligus, buat tabel: Pesan | Niat | Balasan | Tindak lanjut.

## Prinsip

- **Empati dulu, solusi kemudian.** Pada keluhan, akui dulu, jangan membela diri, jangan menyalahkan.
- **Satu ajakan per pesan**, tanpa tekanan ("stok terbatas", "hari ini saja") kecuali benar-benar terjadi dan dikonfirmasi user.
- **Pahami dulu, tawarkan kemudian**: maksimal tiga pertanyaan kualifikasi.
- **Publik ringkas, DM rinci**: komentar dijawab pendek dan dipindah ke DM; keluhan diselesaikan di DM.
- **Keamanan data**: tidak pernah meminta atau menyimpan kata sandi, OTP, KTP, atau nomor kartu lewat chat; bila klien mengirimnya, ingatkan dan hapus bila mungkin.
- **Jujur tentang batas**: di luar layanan, katakan terus terang daripada menjanjikan.
- **Waktu respons** adalah hipotesis kemampuan tim; jangan menjanjikan "24 jam" bila tim tidak sanggup.

## File

- `scripts/build_replies.py` - render paket balasan dan validasi (`--example`, `--check`)
- `references/reply-principles.md` - nada, struktur balasan, eskalasi, contoh, kesalahan umum
