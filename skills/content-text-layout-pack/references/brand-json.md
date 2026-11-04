# brand.json untuk content-text-layout-pack

`python scripts/build_pack.py --example` mencetak contoh lengkap.

## Wajib
`brand`, `prefix`, `tagline`, `cta` (boleh `->`), `url`, `colors` (role `dark`, `accent`, `light`; opsional `support`, `offwhite`), `fonts` {`heading`,`body`}, `examples`.

## Opsional
`tone`, `avoid` (daftar hal yang dihindari di Voice Lock), `mascot` {`name`}.

## examples
| Field | Isi |
|---|---|
| `topic` | Topik contoh (frasa pendek) |
| `carousel` | 7 string; baris dipisah `\n`. Slide 3-6 diawali nomor poin |
| `story` | 3-5 objek `{tujuan, teks}` |
| `reels` | `{title, duration, rows:[{waktu, visual, teks, posisi, animasi}]}`; waktu berurutan tanpa celah dan berakhir tepat di `duration` |
| `foto` | `{headline, subteks, formulas:[[label, teks], ...]}` |
| `hooks` | `[[label, teks], ...]` maksimal 8 kata per hook |
| `ctas` | daftar string |
| `thumbnails` | `{thumbnail, og, pinterest}` |
| `caption` | string multi-baris dengan hashtag |

## Menyelaraskan dengan video Flow
Jika user memakai `flow-video-command-pack`, satu klip Flow biasanya 4-8 detik. Buat 2 baris tabel per klip (satu teks utama di atas, satu teks pendukung di bawah) dan sesuaikan `visual` dengan nama klip.
