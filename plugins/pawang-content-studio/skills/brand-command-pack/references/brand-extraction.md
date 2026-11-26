# Mengisi brand.json dari brand board, logo, atau teks

Jalankan `python scripts/build_pack.py --example` untuk melihat contoh lengkap.

## Field wajib
| Field | Cara mengisi |
|---|---|
| `brand` | Nama persis seperti di logo, termasuk domain (mis. `Pawang.dev`). |
| `prefix` | 2-3 huruf dari nama brand, huruf kecil (mis. `pw`). Hindari `logo`, `ai`, dan awalan umum. |
| `tagline` | Salin persis, termasuk tanda baca. |
| `cta` | Ajakan utama. Boleh pakai `->` (otomatis jadi panah). |
| `url` | Domain tanpa `https://`. |
| `colors` | Minimal tiga: role `dark`, `accent`, `light`. Opsional `support`, `offwhite`. Isi `name` dan `hex` persis dari board; bila hex tak tertulis, perkirakan dari gambar dan beri tahu user. |
| `fonts` | `heading` dan `body`. Jika tak terbaca, pilih pasangan yang paling mirip dan beri tahu user. |
| `logo_desc` | Satu kalimat deskripsi bentuk logo dan posisi wordmark; dipakai di command `logo`. |

## Field opsional (menambah command)
| Field | Efek |
|---|---|
| `mascot` {`name`,`desc`} | Mengaktifkan `mascot`, `stickerpack`, dan kalimat visual berisi maskot. Tanpa ini, visual memakai ilustrasi konseptual dan ikon logo. |
| `services` [{`name`}] | Mengaktifkan `wacatalog`, mengisi ikon di banner LinkedIn dan label highlight. |
| `packages` [{`name`,`color`,`desc`}] | Mengaktifkan `paket` dan label paket di katalog. |
| `quote` | Kalimat filosofi brand untuk `quote`. Default: tagline. |
| `tone`, `style` | Karakter suara dan gaya visual; masuk ke Brand Lock. Ambil dari bagian filosofi/nilai brand di board. |
| `handle`, `brand_short`, `cta_short`, `pattern_elements` | Menyempurnakan teks; ada default bila kosong. |

## Tips membaca brand board
- Bagian "Warna" biasanya memuat nama dan hex; bagian "Tipografi" memuat font judul dan isi.
- Nilai brand dan filosofi menentukan `tone`.
- Mockup (ponsel, topi, profil sosmed) menunjukkan gaya visual yang diharapkan; rangkum di `style`.
- Jangan mengarang layanan atau paket yang tidak tertulis; hilangkan field-nya.
