# brand.json untuk flow-video-command-pack

Jalankan `python scripts/build_pack.py --example` untuk contoh lengkap. Skema dasar sama dengan skill `brand-command-pack`.

## Wajib
`brand`, `prefix` (2-3 huruf, tanpa `/` dan `-`), `tagline`, `cta`, `url`, `logo_desc`, `colors` (role `dark`, `accent`, `light`; opsional `support`).

## Opsional
- `mascot` {`name`,`desc`}: mengaktifkan `hello`, `dialog`, `ganti-sudut` dan Character Lock. Tanpa ini dipakai Visual Lock dan placeholder `{objek utama}`.
- `services` [{`name`}]: dipakai di `layanan`.
- `tone`, `style`: masuk ke Lock dan kalimat gaya.

## Bagian `video`
| Field | Fungsi | Contoh |
|---|---|---|
| `world` | Latar khas brand | "hutan sage lembut dengan cahaya senja hangat" |
| `problem` | Kekacauan yang bisa digambar | "spreadsheet kusut, kabel liar, notifikasi bertubi-tubi" |
| `solution` | Hasil akhir yang bisa digambar | "tampilan rapi Biru Malam dan Api Dupa" |
| `story_theme` | Tema cerita 4 adegan | "Si Liar menjinakkan data yang kacau" |
| `scenes` | 4 adegan kustom | `[{"title":"Masalah","image":"/pw-mascot ... rasio 9:16","motion":"Adegan 1. ..."}]` |

Aturan menulis `scenes`: `image` selalu diawali command gambar brand, rasio 9:16, tanpa teks; `motion` satu aksi, satu gerakan kamera, ada baris Audio, dan mengingatkan agar desain tidak berubah.
