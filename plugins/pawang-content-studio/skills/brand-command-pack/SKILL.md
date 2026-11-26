---
name: brand-command-pack
description: Buat file Markdown berisi kumpulan "command" prompt gambar siap salin untuk ChatGPT (logo, carousel IG, story IG/WA, OG image, feature image artikel, X/Twitter, LinkedIn, Pinterest, iklan, testimoni, mockup, dll) dari brand board, logo, foto, atau deskripsi brand yang diberikan user. Gunakan skill ini setiap kali user mengunggah brand identity board/logo/foto brand lalu meminta "buatkan command", "kumpulan prompt konten", "prompt sosmed", "command seperti /scrapbook tapi untuk brand saya", "template prompt carousel/story/og image", atau ingin satu file yang bisa dipakai berulang untuk membuat konten marketing dengan gaya brand yang konsisten, bahkan jika user tidak menyebut kata "skill" atau "markdown".
---

# Brand Command Pack

Mengubah identitas brand (gambar brand board, logo, foto, atau teks) menjadi satu file `.md` berisi 35-40 command bergaya `/prefix-nama`. User mengunggah brand board ke ChatGPT, menempel **Brand Lock**, lalu menyalin command yang dibutuhkan. Semua prompt ada di code block agar bisa disalin satu klik.

Pekerjaan berulang (menyusun ratusan baris prompt, mengganti warna/nama/CTA, memeriksa format) dikerjakan skrip supaya hasilnya konsisten. Tugas Anda: membaca brand dengan teliti, mengisi `brand.json` dengan benar, menjalankan skrip, lalu menyesuaikan hasilnya.

## Alur kerja

1. **Ekstrak brand** dari input. Baca `references/brand-extraction.md` untuk daftar field dan cara mengisinya. Jika input berupa gambar, baca teks, kode hex, font, dan deskripsi visual langsung dari gambar. Jika kode hex tidak tertulis, perkirakan dari gambar dan sebutkan bahwa itu perkiraan.
2. **Tanya hanya jika perlu.** Satu pertanyaan ringkas bila nama brand, palet warna, atau tagline benar-benar tidak bisa disimpulkan. Selain itu asumsikan, lalu tulis asumsi di balasan akhir.
3. **Tulis `brand.json`** (contoh: `python scripts/build_pack.py --example`). Field `mascot`, `services`, `packages` boleh dihilangkan: command yang bergantung padanya otomatis dilewati, dan kalimat visual berganti ke versi tanpa maskot.
4. **Render**: `python scripts/build_pack.py brand.json /mnt/user-data/outputs/<nama-brand>_command_konten.md`. Skrip memvalidasi sendiri (code block, token tersisa, awalan command).
5. **Tinjau hasil** dengan membuka beberapa command (carousel, og, hero, testimoni). Perbaiki kalimat yang janggal untuk brand ini langsung di file, misalnya mengganti contoh generik dengan konteks bisnis user. Jalankan `python scripts/build_pack.py --check <file> <prefix>` setelah mengedit.
6. **Tambah command khusus** bila user minta (mis. `/xx-menu` untuk kafe). Ikuti format yang sama: heading `### /prefix-nama`, deskripsi satu baris, lalu `**Singkat:**` dan `**Detail:**` masing-masing di code block yang diawali nama command.
7. **Serahkan** dengan `present_files`, lalu balas singkat: jumlah command, bagian yang ada, asumsi yang dibuat, dan cara pakai (upload board, tempel Brand Lock, salin command).

## Prinsip format

- Setiap prompt berada di code block dan diawali nama command, karena user menyalinnya apa adanya ke ChatGPT.
- Placeholder untuk isian user memakai `{kurung kurawal}`; token internal `[[...]]` tidak boleh tersisa di hasil akhir.
- Palet dikunci ke warna brand lengkap dengan hex di Brand Lock, karena model gambar cenderung mengarang warna jika tidak dibatasi.
- Teks pada gambar dibuat pendek dan dieja persis; model gambar sering salah eja pada teks panjang. Itu sebabnya aturan teks ada di Brand Lock dan carousel dibuat satu slide per permintaan.
- Awalan command: 2-3 huruf dari nama brand (mis. `pw` untuk Pawang.dev), supaya tidak bentrok dengan command umum seperti `/logo`.

## Bahasa

Katalog bawaan berbahasa Indonesia. Jika user menulis dalam bahasa lain, terjemahkan hasil render setelah skrip selesai, tetapi biarkan nama command, token placeholder `{...}`, dan kode hex tidak berubah.

## Batasan yang perlu disampaikan ke user

- Ukuran piksel hanya perkiraan; model gambar memilih rasio terdekat. Resize/crop di Canva atau Figma.
- Logo resmi sebaiknya tetap memakai file asli; command `logo` cocok untuk variasi, bukan pengganti file master.
- Foto orang nyata: jangan menulis prompt yang meminta meniru wajah tertentu selain yang user sendiri unggah dan miliki hak pakainya.

## File

- `scripts/build_pack.py` - render dan validasi (`--example`, `--check`)
- `scripts/catalog.py` - katalog command dan token; edit di sini untuk menambah command permanen
- `references/brand-extraction.md` - panduan mengisi `brand.json` dari gambar/teks
