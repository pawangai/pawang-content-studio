# Panduan Mengisi Isian {...}

## 1. Brief satu topik (tulis dulu, pakai ulang)

```
topik        : frasa topik dari user
audiens      : siapa, masalahnya apa
pesan_kunci  : satu kalimat inti yang ingin diingat
headline     : maks 8 kata, bisa dibaca sebagai hook
subteks      : maks 15 kata, menjelaskan headline
hook_video   : maks 6 kata per baris, muncul sebelum detik ke-3
cta          : sesuai brand (mis. Konsultasi Gratis -> pawang.dev)
konsep_visual: satu adegan/objek yang mewakili topik
nada         : dari Brand/Voice Lock
```

Jika user tidak memberi audiens atau tujuan, simpulkan dari brand dan topik, lalu sebutkan asumsinya.

## 2. Jenis isian dan cara mengisi

| Contoh isian | Cara mengisi |
|---|---|
| `{topik}`, `{tema}` | Frasa topik dari user, apa adanya atau dirapikan |
| `{judul}`, `{judul maks 6 kata}`, `{headline maks 8 kata}` | Turunan brief.headline sesuai batas kata |
| `{subteks maks 15 kata}` | brief.subteks |
| `{pesan}`, `{pesan singkat}`, `{kalimat maks 12 kata}` | Satu kalimat dari brief.pesan_kunci, patuhi batas |
| `{teks CTA}`, `{judul tombol}` | 2-4 kata: "Cek 4 tandanya", "Konsultasi Gratis" |
| `{pose / aksi}`, `{aksi tunggal}`, `{aksi berikutnya yang wajar}` | Satu aksi fisik konkret, bisa digambar dan dianimasikan |
| `{kondisi kacau}` / `{kondisi rapi}` | Gambaran visual spesifik sesuai topik (benda, jumlah, suasana) |
| `{tempat}`, `{latar}` | Latar konkret yang cocok dengan topik dan palet brand |
| `{krem / biru malam}`, `{[warna] / [warna]}` | Pilih satu; kontras dengan elemen lain |
| `{9:16 / 16:9}`, `{1:1 / 9:16}` | Pilih sesuai platform di command; ikuti yang sudah tertulis di command bila ada |
| `{Instagram / X / LinkedIn / ...}`, `{platform}` | Platform yang disebut user; jika tidak disebut, pilih yang paling cocok dengan topik dan beri tahu |
| `{Frames / Ingredients / Text to Video}` | Frames bila ada satu gambar awal; Ingredients bila karakter/objek sama di banyak klip; Text to Video bila tanpa gambar |
| `{static / slow push-in / pan / orbit}` | Satu gerakan kamera; static untuk teks/logo, slow push-in untuk fokus emosi |
| `{efek / musik / dialog "..." / tanpa suara}` | Satu pilihan audio yang cocok suasana |
| `{senang / bingung / bangga}` | Ekspresi yang sesuai alur cerita |
| `{Q1}` ... `{Q5}`, `{poin 1}` ... | Isi dengan pertanyaan atau poin spesifik topik, satu kalimat pendek |
| `{jumlah}`, `{nomor}` pada urutan/seri | Angka urut yang jelas; bila `{nomor}` berupa telepon, itu data user |

## 3. Data yang harus dari user (jangan dikarang)

Kutipan atau testimoni, nama klien, jabatan, nama usaha klien, nomor WhatsApp, email, harga, diskon, periode/tanggal promo, syarat promo, metrik hasil ("hemat 10 jam"), nama file gambar, handle akun.
- Jika user sudah memberikannya: pakai persis.
- Jika belum: tanyakan dalam **satu** pesan; bila tidak dijawab, tulis `[ISI SENDIRI: keterangan singkat]`.
- Skrip mencantumkannya di bagian "Data dari Anda (periksa kebenarannya)" dan "Yang Masih Perlu Anda Isi".

## 4. Contoh lengkap

Topik: "4 tanda data bisnis sudah liar".

Command: `/pw-igpost Post Instagram 4:5. Headline "{headline maks 8 kata}", subteks "{subteks maks 15 kata}". Visual {Si Liar / ilustrasi layanan}. Latar {krem / biru malam}...`

Nilai: `["Data bisnismu sudah liar? Cek 4 tandanya", "Cari satu angka, buka lima file. Kedengaran akrab? Geser untuk tahu tandanya.", "Si Liar", "biru malam"]`

Hasil: headline 7 kata (lolos), subteks 13 kata (lolos), visual dan latar dipilih dari opsi.

## 5. Kesalahan umum
- Menulis `{pose / aksi}` menjadi "pose / aksi" atau membiarkan garis miring.
- Headline melebihi batas karena menambahkan tanda tanya dan penjelasan; pangkas.
- Memakai tanda kutip ganda di dalam nilai yang sudah berada dalam tanda kutip command.
- Mengisi testimoni palsu "supaya terlihat lengkap".
- Headline berbeda untuk tiap command dari topik yang sama.
