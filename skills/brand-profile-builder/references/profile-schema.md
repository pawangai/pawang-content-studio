# Skema profile.json (brand-profile/1)

## Identitas
| Field | Wajib | Catatan |
|---|---|---|
| `brand` | ya | persis seperti logo, termasuk domain (Pawang.dev) |
| `brand_short` | tidak | nama pendek (Pawang) |
| `prefix` | ya | 2-3 huruf kecil untuk command (`pw`) |
| `tagline` | ya | salin persis |
| `cta`, `cta_short` | ya / tidak | boleh `->` |
| `url`, `handle` | ya / tidak | domain tanpa https |
| `quote` | tidak | kalimat filosofi brand |
| `audience` | tidak | siapa target utama |
| `tone` | disarankan | nada suara dari nilai/filosofi brand |
| `style` | disarankan | gaya visual dari mockup/board |
| `avoid` | disarankan | **daftar** kata yang dihindari (klaim berlebihan) |
| `address` | untuk balasan | sapaan ke pelanggan: Kak, Bapak/Ibu, Anda |

## Visual
| Field | Wajib | Catatan |
|---|---|---|
| `logo_desc` | ya | satu kalimat bentuk logo dan posisi wordmark |
| `colors` | ya | `[{role,name,hex,use}]`; role: dark, accent, light wajib; support, offwhite disarankan |
| `fonts` | ya | `{heading, body}` |
| `mascot` | tidak | `{name, desc}` |
| `pattern_elements` | tidak | elemen khas untuk pola latar |

## Bisnis
`services` `[{name, benefit}]`, `packages` `[{name, color, desc, price}]`, `channels` `{platforms[], whatsapp, email, booking_url}`, `hours` `{layanan, respons_target}`, `faq` `[{q, a}]`.

## Konten (diisi lewat skill terkait)
`video` `{world, problem, solution, story_theme}`; `content` `{package, pillars[], rhythm[], extras[], weeks_plan[], topic_bank{}, momen[], start}`; `examples` (teks dan layout).

## Ekspor
| Target | Dipakai oleh | Yang harus ada |
|---|---|---|
| `command-pack` | brand-command-pack | identitas, colors, fonts, logo_desc |
| `flow-video` | flow-video-command-pack | + `video` |
| `text-layout` | content-text-layout-pack | + `examples` |
| `calendar` | content-calendar-pack | + `content.weeks_plan`, `--start` |
| `caption` | caption-writer | kerangka captions.json (brief dan items diisi skill itu) |
| `reply` | inbound-reply-pack | + `address`, `channels`, `hours`, `faq` |
| `quora` | quora-answer-writer | + `author.name`, `author.role`, `seo`, `avoid` |
| `longform` | longform-writer | + `audience`, `author.name`, `author.role`, `seo`, `avoid` |

`asset-qa` membaca `profile.json` langsung lewat `--profile`.

## Daftar periksa membaca brand board
- [ ] Nama dan domain persis (tanda baca dan huruf besar)
- [ ] Tagline persis
- [ ] Setiap warna: nama, hex, fungsi, lalu role
- [ ] Font judul dan isi
- [ ] Logo: bentuk, warna, posisi wordmark, versi (horizontal, ikon, gelap)
- [ ] Maskot: nama, ciri visual yang harus tetap sama
- [ ] Nilai/filosofi -> `tone`
- [ ] Mockup (ponsel, topi, profil sosmed) -> `style`
- [ ] Layanan dan paket (nama persis, tanpa menambah)
- [ ] CTA standar

## Aturan kontras (WCAG 2.x)
Rasio >= 4,5:1: aman untuk teks normal. 3,0-4,5:1: hanya teks besar (>= 24 px) atau tombol. < 3,0:1: jangan untuk teks (hanya dekorasi).
