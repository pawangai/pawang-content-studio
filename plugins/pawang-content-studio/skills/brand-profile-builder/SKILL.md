---
name: brand-profile-builder
description: Ubah brand board, logo, foto, atau deskripsi brand menjadi satu profil brand baku (profile.json) yang menjadi sumber tunggal bagi semua skill konten lain (command gambar, video Flow, teks dan layout, jadwal, caption, balasan, QA). Mengekstrak nama, tagline, CTA, palet warna dengan role dan hex, font, deskripsi logo, maskot, layanan, paket, nada suara, dan hal yang dihindari; memeriksa kontras warna (WCAG) untuk menemukan pasangan warna yang tidak boleh dipakai sebagai teks; menghasilkan Brand Lock dan Voice Lock siap tempel; dan mengekspor profil ke format yang dibutuhkan tiap skill. Gunakan setiap kali user mengunggah brand board atau logo, mengatakan "ini brand saya", ingin memulai dari nol, ingin konsistensi antar-skill tanpa mengisi ulang data, atau mengganti/memperbarui data brand, bahkan jika user tidak menyebut kata "profil" atau "skill".
---

# Brand Profile Builder

Satu `profile.json` menjadi sumber kebenaran brand. Skill lain tidak perlu membaca ulang brand board; cukup memakai hasil ekspor dari profil ini sehingga nama, warna, tagline, dan nada selalu sama di gambar, video, teks, jadwal, caption, dan balasan.

## Alur kerja

1. **Baca brand dengan teliti.**
   - Dari **Brand Spec** (hasil skill `brandboard-standard`, file Markdown `Brand Spec: NAMA`): jalankan `python scripts/profile.py from-spec brand-spec.md profile.json`. Skrip menyusun draf profil (nama, tagline, palet beserta role, font, maskot, layanan, paket, tone) dan mencetak daftar yang harus dikonfirmasi: role warna adalah heuristik, nama maskot, prefix usulan, harga paket, URL, kontak, serta section bertanda `[ASUMSI]`. Brand Spec adalah sumber yang lebih kuat daripada gambar board karena hex, font, dan copy di dalamnya sudah baku.
   - Dari gambar brand board: baca langsung nama brand (termasuk domain), tagline persis, nama dan kode hex warna, font judul dan isi, bentuk logo, maskot, nilai/filosofi (untuk nada), layanan, paket, dan CTA. Jika hex tidak tertulis, jalankan `python scripts/profile.py colors board.png` untuk memperkirakan warna dominan, cocokkan dengan yang terlihat, dan **sebutkan bahwa itu perkiraan**.
   - Dari teks/deskripsi user: ambil apa adanya. Jangan menambah layanan, harga, atau klaim yang tidak disebut.
2. **Tentukan `prefix`**: 2-3 huruf kecil dari nama brand (mis. `pw`), tidak sama dengan singkatan platform.
3. **Isi `profile.json`** (`python scripts/profile.py --example`; penjelasan field di `references/profile-schema.md`). Tentukan role warna: `dark` (utama gelap), `accent` (CTA/aksen), `light` (latar terang), `support` (pendukung), `offwhite` (teks di latar gelap).
4. **Tanya satu kali** bila ada hal penting yang tidak bisa disimpulkan: nomor WhatsApp, email, tautan booking, harga paket, jam layanan, audiens utama. Jika tidak dijawab, biarkan kosong; skill lain menandainya `[ISI SENDIRI]`.
5. **Validasi**: `python scripts/profile.py validate profile.json`. Perbaiki galat. Baca tabel kontras; pasangan yang **TIDAK LOLOS** (mis. aksen oranye di atas krem) dicatat sebagai larangan: dipakai hanya untuk ikon atau tombol dengan teks gelap, bukan untuk teks.
6. **Keluarkan Brand Lock dan Voice Lock**: `python scripts/profile.py lock profile.json` (siap tempel ke ChatGPT).
7. **Ekspor sesuai kebutuhan**: `python scripts/profile.py export profile.json --for TARGET out.json` dengan TARGET `command-pack`, `flow-video`, `text-layout`, `calendar` (tambah `--start YYYY-MM-DD`), `caption`, `reply`, `quora`, atau `longform`. Skrip melaporkan field yang belum lengkap untuk target itu (mis. `examples` untuk `text-layout`, `weeks_plan` untuk `calendar`); lengkapi lewat skill terkait, lalu simpan kembali ke `profile.json` agar profil tetap menjadi sumber tunggal.
8. **Serahkan** `profile.json` dengan `present_files`, ringkasan satu paragraf (nama, prefix, palet beserta role, font, maskot, layanan), daftar asumsi/perkiraan, hasil kontras, dan petunjuk memakai ekspor di skill lain.

## Prinsip

- **Salin persis, jangan memperbaiki.** Tagline, nama, dan ejaan diambil sesuai brand board, termasuk huruf besar-kecil dan tanda baca.
- **Tidak mengarang.** Harga, layanan, jam, kontak, dan klaim hanya dari user atau board. Field yang tidak diketahui dikosongkan, bukan ditebak.
- **Satu sumber.** Jika user mengganti data (warna, CTA, layanan), ubah `profile.json` dan ekspor ulang; jangan mengedit tiap file turunan secara terpisah.
- **Kontras itu data.** Laporkan angka kontras (rasio) dan aturan pakai, bukan sekadar "kurang bagus".
- **Pembaruan**: bila user memberi versi brand baru, bandingkan dengan profil lama dan tampilkan apa saja yang berubah sebelum menimpa.

## File

- `scripts/profile.py` - `--example`, `from-spec`, `validate`, `export`, `lock`, `colors`
- `references/profile-schema.md` - skema, role warna, target ekspor, daftar periksa pembacaan brand board
