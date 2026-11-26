---
name: longform-writer
description: Tulis konten format panjang berbasis riset dan suara brand, yaitu artikel blog (SEO), artikel Medium atau LinkedIn Articles, newsletter, dan skrip video panjang YouTube lengkap dengan bab, catatan visual, dan deskripsi. Alur brief, riset bersumber, kerangka, draf, pemeriksaan otomatis (judul, meta deskripsi, slug, struktur H2, keterbacaan, kata kunci, alt text, tautan, angka tanpa sumber, kecepatan bicara per bab), paket daur ulang ke carousel, reel, Threads, Quora, dan caption, serta baris Content Log. Gunakan setiap kali user meminta artikel, blog, tulisan panjang, newsletter, naskah atau skrip YouTube, riset topik untuk tulisan, atau mengubah topik kalender menjadi konten mendalam, bahkan jika user tidak menyebut kata "skill".
---

# Longform Writer

Konten panjang adalah tempat brand menunjukkan keahlian. Hasil terbaik berasal dari **pengalaman dan data nyata user** ditambah **riset bersumber**, bukan dari teks umum yang bisa ditulis siapa saja.

## Prinsip

- **Jangan mengarang**: fakta, statistik, kutipan, studi kasus, dan klaim pengalaman hanya dari user atau sumber yang ditemukan dan dapat ditautkan. Bila tidak ada sumber, tulis pernyataan umum atau `[ISI SENDIRI: ...]`.
- **Jawaban dulu**: paragraf pembuka langsung memberi inti dan janji isi artikel.
- **Bermanfaat sebelum menjual**: satu CTA lembut di akhir, bukan di setiap bagian.
- **Suara brand**: ikuti Voice Lock/`profile.json` (`tone`, `avoid`).
- **Pengungkapan bantuan AI**: sebagian platform dan komunitas meminta pengungkapan. Cek aturan platform tujuan saat ini lewat pencarian; bila diminta, tambahkan catatan singkat (`author.ai_disclosure` di profil). Draf harus dibaca dan disunting user sebelum terbit.

## Alur kerja

1. **Brief.** Tanyakan atau simpulkan dalam satu pesan singkat: format (blog, Medium, LinkedIn Article, newsletter, skrip YouTube), topik (boleh dari kalender), audiens dan masalahnya, tujuan, panjang, CTA, serta **bahan nyata** (pengalaman, contoh, data, studi kasus yang boleh dipakai). Ambil `tone`, `avoid`, `author`, `seo` dari `profile.json` bila ada. Untuk SEO, usulkan 2-3 kata kunci kandidat berdasarkan bahasa audiens; **jangan mengklaim volume pencarian** tanpa data dari alat yang user miliki.
2. **Riset bersumber.** Cari fakta dan data terbaru dengan pencarian web; baca halaman utamanya; catat sumber (judul, penerbit, tanggal, tautan). Lihat 3-5 artikel teratas untuk topik itu guna menemukan celah, tanpa menyalin struktur atau kalimatnya. Hanya pakai angka yang ada di sumber, dan tautkan.
3. **Kerangka.** Buat judul kerja, H2 (4-7), poin tiap bagian, contoh/gambar yang diperlukan, FAQ (dari pertanyaan nyata audiens), dan CTA. Untuk tulisan di atas sekitar 1.500 kata atau skrip di atas 8 menit, tampilkan kerangka dan minta persetujuan singkat sebelum menulis penuh, kecuali user sudah meminta langsung.
4. **Draf** memakai templat di `templates/` (front matter untuk artikel; penanda `## [mm:ss]` untuk skrip; subjek dan preheader untuk newsletter). Kalimat pendek, paragraf maksimal sekitar 100 kata, subjudul yang bisa dipindai, contoh konkret, daftar bernomor untuk langkah. Jangan menaruh URL karangan; tautan internal hanya ke halaman yang user sebutkan.
5. **Periksa.**
   - Artikel/newsletter: `python scripts/article_check.py artikel.md --keyword "..." --target-words N --site domain.com [--disclosure]`
   - Skrip: `python scripts/script_check.py skrip.md --duration 8:00 --chapters`
   Perbaiki semua **Galat**, pertimbangkan **Peringatan** (kata kunci terlalu rapat, angka tanpa sumber, tautan generik, kecepatan bicara tidak wajar, bab di bawah 10 detik).
6. **Paket penerbitan**: judul akhir (maksimal sekitar 60 karakter), meta deskripsi (120-160), slug, alt text gambar, prompt gambar fitur (pakai command `/xx-feature` dari `brand-command-pack`), dan untuk video: daftar bab untuk deskripsi, judul, thumbnail (`/xx-ytthumb`).
7. **Rencana daur ulang** (satu artikel menjadi banyak konten): carousel 7 slide, reel 15-24 detik, kartu tips, thread atau post Threads, post LinkedIn, jawaban Quora (`quora-answer-writer`), caption (`caption-writer`), dan dua-tiga story. Beri hari dan jam dari kalender, serta baris **Content Log** (Format = Artikel/Skrip YouTube, Hook = judul).
8. **Serahkan**: simpan artikel sebagai berkas `.md` (satu berkas per tulisan) dan `present_files`; balasan singkat berisi ringkasan, daftar sumber, daftar `[ISI SENDIRI]`, hasil pemeriksaan, dan langkah berikutnya.

## Format dan platform

Ringkasan per format ada di `references/longform-guide.md`: blog SEO, Medium dan LinkedIn Articles (tanpa meta SEO, judul dan subjudul menarik, pengungkapan sesuai kebijakan), newsletter (subjek, preheader, satu CTA), dan skrip YouTube (hook, bab, kecepatan bicara, deskripsi). Aturan angka di skrip pemeriksa adalah patokan keterbacaan, bukan aturan mutlak.

## File

- `scripts/article_check.py` - pemeriksa artikel dan newsletter
- `scripts/script_check.py` - pemeriksa skrip video, kecepatan bicara, pembuat daftar bab
- `templates/article-template.md`, `templates/newsletter-template.md`, `templates/youtube-script-template.md`
- `references/longform-guide.md` - panduan format, riset, SEO jujur, daur ulang, daftar periksa
