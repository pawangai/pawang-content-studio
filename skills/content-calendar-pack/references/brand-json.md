# brand.json untuk content-calendar-pack

`python scripts/build_pack.py --example` mencetak contoh lengkap (Pawang.dev, 4 minggu).

## Wajib
`brand`, `prefix`, `cta` (boleh `->`), `url`, `start` (`YYYY-MM-DD`, harus hari Senin), `weeks_plan`.

## Opsional
| Field | Default | Catatan |
|---|---|---|
| `package` | - | `Ringan` atau `Standar`; Standar mewajibkan 7 hari terisi per minggu |
| `audience` | audiens utama di Indonesia (WIB) | frasa pendek |
| `pillars` | Edukasi 35, Solusi 25, Bukti 20, Karakter 15, Ajakan 5 | `[{name, goal, share, formats}]`, total 100 |
| `rhythm` | 7 hari bawaan (Sen carousel 09:00 ... Min rekap 19:30) | `[{hari, format, platform, jam, pilar, minimal}]` |
| `extras` | story, WA Status, LinkedIn, X, Pinterest, blog | `[[platform, frekuensi, jam, isi]]` |
| `topic_bank` | - | `{pilar: [topik, ...]}`, dinomori otomatis |
| `momen` | - | daftar momen; tanggal harus diverifikasi |

Jika `pillars` diganti dengan nama khas brand, `rhythm` dan setiap baris `weeks_plan` yang menyebut `pilar` harus memakai nama yang sama (lint akan melapor nama yang tidak dikenal).

## weeks_plan
```json
[{"tema": "Tema minggu", "rows": [
  {"hari": "Senin", "topik": "Judul spesifik", "command": "/pw-carousel + /pw-t-carousel"},
  {"hari": "Selasa", "topik": "...", "command": "/pw-v-reels-hook + /pw-t-reels", "pilar": "Jinak", "jam": "12:00"}
]}]
```
Baris tanpa `jam`, `platform`, `format`, `pilar`, `minimal` mewarisi dari `rhythm` pada hari itu. Command dipisah ` + ` dan harus berawalan `/<prefix>-`.

## Menulis topik yang baik
- Judul bisa langsung dipakai sebagai hook (maksimal 8 kata) atau mudah diubah jadi hook.
- Setiap topik menyebut masalah audiens atau layanan konkret, bukan label umum.
- Beri tanda "(isi dengan data nyata)" pada testimoni, studi kasus, dan angka.
- Variasikan format antar-hari dan seimbangkan pilar sesuai porsi.
