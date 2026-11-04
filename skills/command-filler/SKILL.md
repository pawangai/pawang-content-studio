---
name: command-filler
description: Isi otomatis semua isian {kurung kurawal} pada command prompt (gambar, video, teks, jadwal) berdasarkan topik yang diberikan user, sehingga command langsung siap ditempel ke ChatGPT atau Google Flow. User cukup memberi topik dan command (ditempel, atau nama command dari file command yang diunggah); skill memilih opsi yang tepat, menulis headline, subteks, aksi, dan latar yang konkret sesuai batas kata, menjaga konsistensi antar-command untuk satu topik, dan menandai data yang harus dari user (kutipan, nama klien, harga, tanggal) sebagai [ISI SENDIRI] alih-alih mengarangnya. Gunakan skill ini setiap kali user menempelkan atau menyebut command seperti /pw-carousel, /pw-igpost, /pw-v-hello, /pw-t-reels yang masih berisi {…}, meminta "isikan command ini", "lengkapi placeholder", "siap tempel", atau punya topik dan ingin command-nya langsung terisi, bahkan jika user tidak menyebut kata "skill".
---

# Command Filler

Mengubah command yang masih berisi `{...}` menjadi command siap tempel untuk satu topik. User memberi **topik** dan **command**; Anda menentukan isi tiap `{...}`; skrip menerapkannya dan memeriksa bahwa teks di luar kurung tidak berubah dan batas kata terpenuhi.

Dua hal yang membuat hasilnya bagus: (1) satu **brief** per topik yang dipakai ulang di semua command supaya headline, hook, dan pesan konsisten, dan (2) isian yang **konkret**, bukan generik.

## Alur kerja

1. **Terima input.** Butuh topik dan daftar command.
   - Command boleh ditempel langsung, atau disebut namanya (mis. "carousel, igstory, og") bila user mengunggah/menempel file command. Jika hanya nama dan tidak ada file atau teks command, minta user menempelkan commandnya; jangan menebak isi command dari ingatan.
   - Jika user menempel Brand Lock atau brand board, pakai sebagai sumber suara brand, warna, dan CTA.
2. **Ekstrak isian.** Simpan command ke file teks/md lalu jalankan `python scripts/fill.py extract <file> templates.json`. Skrip menampilkan tiap command (`c001`, `c002`, ...), varian Singkat/Detail, dan isiannya lengkap dengan batas kata, daftar opsi, serta penanda `DATA DARI USER`.
   - Jika file command punya Singkat dan Detail, isi varian yang diminta user. Bila tidak disebut, isi **Detail** (hasil lebih terarah) dan tawarkan Singkat.
3. **Buat brief satu kali per topik** (lihat `references/placeholder-guide.md`): topik, audiens, pesan kunci, headline (maks 8 kata), subteks (maks 15 kata), hook, CTA, konsep visual, nada. Semua command yang berasal dari topik yang sama harus memakai brief yang sama.
4. **Tanya satu kali bila ada data yang wajib dari user** dan belum diberikan (kutipan atau nama klien, harga, tanggal/periode promo, nomor, email, metrik hasil, nama file gambar). Kumpulkan semuanya dalam **satu** pesan pendek. Jika user ingin cepat atau tidak menjawab, tulis `[ISI SENDIRI: keterangan]` (kurung siku). Jangan pernah mengarang testimoni, angka hasil, harga, atau klaim.
5. **Tulis `values.json`**: `{"brief": {...}, "only": [id yang diminta], "values": {"c001": ["nilai 1", "nilai 2"], ...}}` dengan nilai berurutan sesuai isian. Aturan isi ada di `references/placeholder-guide.md`.
6. **Terapkan**: `python scripts/fill.py apply templates.json values.json /mnt/user-data/outputs/command_siap_tempel.md`. Perbaiki semua **Galat** (nilai kosong, melebihi batas kata, jumlah nilai salah, kurung kurawal tersisa) dan baca **Peringatan**; ulangi sampai bersih.
7. **Serahkan.**
   - 1-3 command: tampilkan langsung di balasan, masing-masing dalam code block, tanpa file.
   - 4 command atau lebih: simpan file `.md` dan `present_files`.
   - Selalu sebutkan: brief singkat yang dipakai, daftar **[ISI SENDIRI]** yang masih perlu dilengkapi, dan urutan pakai (mis. carousel satu slide per permintaan; gambar dulu, baru video).

## Prinsip pengisian

- **Konkret mengalahkan generik.** `{pose / aksi}` diisi "mengangkat satu tangan melambai dua kali sambil tersenyum", bukan "pose bagus".
- **Pilih satu opsi.** Untuk `{A / B / C}` berupa pilihan nyata (rasio, platform, mode, latar), pilih satu yang paling cocok dengan topik dan tulis persis salah satu opsi, tanpa garis miring. Bila opsi hanya contoh kategori (`{pose / aksi}`), tulis nilai konkret sendiri.
- **Patuhi batas dalam kurung**: `maks 8 kata`, `6-9 kata`, dan sejenisnya adalah batas keras yang diperiksa skrip.
- **Teks pada gambar pendek dan dieja persis**, karena model gambar sering salah eja teks panjang. Tulis dengan ejaan final, tanpa tanda kutip ganda di dalam nilai.
- **Jangan menyentuh teks di luar kurung.** Anda hanya mengisi isian; skrip memastikan sisanya tidak berubah.
- **Satu topik, satu cerita.** Hook di carousel, story, OG, dan video harus terasa sebagai variasi pesan yang sama.
- **Tidak mengarang data.** Hasil, angka, harga, testimoni, nama klien: dari user atau `[ISI SENDIRI]`.

## File

- `scripts/fill.py` - `extract`, `apply`, `--example-values`
- `references/placeholder-guide.md` - cara mengisi tiap jenis isian, format brief, contoh
