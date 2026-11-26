---
name: flow-video-command-pack
description: Buat file Markdown berisi kumpulan "command" prompt video siap salin untuk Google Flow (Veo) dari brand board, maskot, atau gambar hasil ChatGPT milik user. Mencakup intro logo, outro, Reels/TikTok hook, WA/IG story vertikal, cerita multi-adegan, penjelasan layanan, before-after, testimoni, produk, perpanjangan dan transisi klip, plus paket kerja 4 klip berpasangan (prompt gambar ChatGPT + prompt gerakan Flow). Gunakan skill ini setiap kali user ingin membuat konten video pendek, cerita, animasi maskot, atau menganimasikan gambar dengan Google Flow/Veo, meminta "command Flow", "prompt video untuk brand saya", atau melanjutkan dari kumpulan command gambar (brand-command-pack) ke video, bahkan jika user tidak menyebut kata "skill".
---

# Flow Video Command Pack

Membuat satu file `.md` berisi command bergaya `/prefix-v-nama` untuk Google Flow. Alurnya: user membuat gambar di ChatGPT (command `/prefix-...` dari skill `brand-command-pack` bila ada), mengunggahnya ke Flow sebagai Frames atau Ingredients, lalu menempel prompt gerakan dari file ini. Semua prompt ada di code block agar bisa disalin satu klik.

Skrip menyusun prompt dan memvalidasi format; tugas Anda adalah memahami brand, mengisi `brand.json`, dan menyesuaikan hasil.

## Alur kerja

1. **Ambil brand** dari input user (brand board, logo, deskripsi, atau file command sebelumnya). Skema `brand.json` sama dengan `brand-command-pack` (lihat `references/brand-json.md`); jika user sudah punya `brand.json` atau file command gambar untuk brand yang sama, pakai ulang isinya dan awalan yang sama.
2. **Isi bagian `video`** pada `brand.json`; ini yang membuat hasil terasa khas brand, bukan generik:
   - `world`: latar visual khas (mis. "hutan sage lembut dengan cahaya senja hangat")
   - `problem`: kekacauan yang diselesaikan brand, dalam bentuk visual yang bisa digambar
   - `solution`: bentuk visual hasil akhirnya
   - `story_theme`: tema cerita 4 adegan
   - `scenes` (disarankan): 4 adegan buatan Anda, masing-masing `{title, image, motion}`. `image` adalah prompt gambar untuk ChatGPT (diawali command gambar, mis. `/pw-mascot ...`, rasio 9:16, tanpa teks); `motion` adalah prompt gerakan Flow yang satu aksi per klip. Bila dikosongkan, skrip memakai adegan bawaan berpola masalah, solusi, penyelesaian, hasil.
3. **Tanya hanya jika perlu**: satu pertanyaan ringkas bila nama brand atau palet tidak bisa disimpulkan. Selain itu asumsikan dan sebutkan asumsinya.
4. **Render**: `python scripts/build_pack.py brand.json /mnt/user-data/outputs/<brand>_command_flow_video.md`. Skrip memvalidasi sendiri.
5. **Tinjau dan sesuaikan**: baca bagian Character/Visual Lock, `reels-hook`, `penjelasan`, dan paket 4 adegan. Pastikan aksi realistis untuk klip pendek dan sesuai karakter. Setelah mengedit file, jalankan `python scripts/build_pack.py --check <file> <prefix>`.
6. **Serahkan** dengan `present_files`. Balasan singkat: jumlah command, bagian isi, asumsi, dan latihan pertama (satu gambar, `/prefix-v-hello` atau `logoreveal`).

## Prinsip yang membuat hasil Flow bagus

- **Satu klip, satu aksi**: klip pendek (sekitar 4-8 detik) gagal jika memuat banyak aksi. Karena itu setiap prompt hanya punya satu gerakan utama dan satu gerakan kamera.
- **Prompt melengkapi gambar, bukan menentangnya**: model mengikuti gambar acuan; prompt yang meminta warna atau pose berbeda membuat hasil kacau.
- **Teks jangan dianimasikan**: teks dalam video AI sering berubah bentuk. Prompt meminta ruang kosong untuk teks, dan user menambahkan teks serta logo di CapCut/Canva.
- **Konsistensi karakter**: Character Lock dan mode Ingredients dipakai agar maskot tidak berubah di antar klip.
- **Rasio sama** antara gambar dan video (9:16 story/Reels, 16:9 YouTube).
- Command `hello`, `dialog`, dan `ganti-sudut` hanya dibuat jika brand punya maskot; tanpa maskot, prompt memakai placeholder `{objek utama}` untuk diisi user, jadi pertimbangkan menulis `scenes` sendiri.

## Hal yang disampaikan ke user

- Nama menu dan jumlah kredit Flow bisa berbeda menurut akun dan wilayah; verifikasi di halaman resmi Flow bila ditanya, jangan menjanjikan fitur tertentu.
- Audio buatan model (musik, efek, dialog) perlu diperiksa; kualitas dialog berbahasa Indonesia bisa bervariasi.
- Jangan membuat prompt yang meniru orang nyata tertentu.

## File

- `scripts/build_pack.py` - render dan validasi (`--example`, `--check`)
- `scripts/catalog.py` - katalog command; edit di sini untuk menambah command permanen
- `references/brand-json.md` - skema `brand.json` dan bagian `video`
