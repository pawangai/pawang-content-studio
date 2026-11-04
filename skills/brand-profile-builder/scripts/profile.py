#!/usr/bin/env python3
"""Profil brand tunggal (profile.json): validasi, kontras warna, ekspor ke skill lain, Brand/Voice Lock.

Pemakaian:
  python profile.py --example                          # contoh profile.json lengkap
  python profile.py validate profile.json              # validasi + tabel kontras
  python profile.py export profile.json --for TARGET out.json [--start 2026-10-26]
        TARGET: command-pack | flow-video | text-layout | calendar | caption | reply | quora | longform
  python profile.py lock profile.json                  # Brand Lock + Voice Lock siap tempel
  python profile.py from-spec brand-spec.md out.json   # draf profil dari Brand Spec (skill brandboard-standard)
  python profile.py colors gambar.png [--n 6]          # warna dominan dari brand board (bantuan, bukan pengganti membaca hex di board)
"""
import json
import re
import sys
from pathlib import Path

SCHEMA = "brand-profile/1"
ROLES = ["dark", "accent", "light", "support", "offwhite"]
REQUIRED = ["brand", "prefix", "tagline", "cta", "url", "logo_desc", "colors", "fonts"]
# kunci wajib per target (setelah dipetakan dari profil)
TARGET_REQ = {
    "command-pack": ["brand", "prefix", "tagline", "cta", "url", "colors", "fonts", "logo_desc"],
    "flow-video": ["brand", "prefix", "tagline", "cta", "url", "logo_desc", "colors"],
    "text-layout": ["brand", "prefix", "tagline", "cta", "url", "colors", "fonts", "examples"],
    "calendar": ["brand", "prefix", "cta", "url", "start", "weeks_plan"],
    "caption": ["brand", "cta"],
    "reply": ["brand", "prefix", "cta", "url", "address", "tone"],
    "quora": ["brand", "tone", "author"],
    "longform": ["brand", "tone", "audience", "author"],
}
COMMON = ["brand", "brand_short", "prefix", "tagline", "cta", "cta_short", "url", "handle", "quote", "tone", "style", "avoid",
          "audience", "logo_desc", "pattern_elements", "colors", "fonts", "mascot", "services", "packages", "author", "seo"]

EXAMPLE = {
    "schema": SCHEMA,
    "brand": "Pawang.dev", "brand_short": "Pawang", "prefix": "pw",
    "tagline": "Digitalmu liar? Serahkan ke Pawang.",
    "cta": "Konsultasi Gratis -> pawang.dev", "cta_short": "Konsultasi Gratis",
    "url": "pawang.dev", "handle": "pawang.dev",
    "quote": "Karena digital yang jinak adalah digital yang berguna.",
    "audience": "pemilik UMKM dan tim operasional di Indonesia (WIB)",
    "tone": "tenang, paham, jinak; hangat, ramah, tidak menakut-nakuti dengan istilah teknis",
    "style": "flat modern hangat, ilustrasi bersih, sudut membulat, banyak ruang kosong, sedikit tekstur lembut",
    "avoid": ["dijamin", "pasti ", "100%", "terbaik", "nomor 1", "garansi"],
    "address": "Kak",
    "logo_desc": "huruf P dengan lingkaran oranye dan percikan bintang, wordmark \"Pawang\" dengan \".dev\" lebih kecil di bawah kanan",
    "pattern_elements": "percikan bintang oranye kecil, daun sage, dan siluet P",
    "colors": [
        {"role": "dark", "name": "Biru Malam", "hex": "#14213D", "use": "utama, tenang, tepercaya"},
        {"role": "accent", "name": "Api Dupa", "hex": "#FF8A3D", "use": "aksen, CTA, energi"},
        {"role": "light", "name": "Krem", "hex": "#FFF6E9", "use": "latar, ramah"},
        {"role": "support", "name": "Hijau Sage", "hex": "#A7C4A0", "use": "pendukung, segar"},
        {"role": "offwhite", "name": "Putih Tulang", "hex": "#FAFAF7", "use": "teks di latar gelap, bersih"},
    ],
    "fonts": {"heading": "Plus Jakarta Sans", "body": "Inter"},
    "mascot": {"name": "Si Liar", "desc": "makhluk berbulu biru malam, syal oranye, tongkat kayu, daun hijau sage; ekspresif, imut, tidak menyeramkan"},
    "services": [
        {"name": "Pawang Web", "benefit": "Website yang jinak: cepat, rapi, mudah diurus"},
        {"name": "Pawang Sheet", "benefit": "Angka berantakan jadi dashboard rapi"},
        {"name": "Pawang Otomasi", "benefit": "Kerja berulang dikerjakan sendiri"},
        {"name": "Pawang Rawat", "benefit": "Setelah proyek selesai, tetap ada yang jaga"},
    ],
    "packages": [
        {"name": "Jinak", "color": "hijau", "desc": "paket dasar", "price": ""},
        {"name": "Piawai", "color": "oranye", "desc": "fitur lebih lengkap", "price": ""},
        {"name": "Sakti", "color": "ungu", "desc": "custom penuh", "price": ""},
    ],
    "author": {"name": "Contoh Penulis", "role": "Pendiri Pawang.dev (data contoh, ganti dengan data nyata)", "bio": "", "experience": [], "ai_disclosure": "Draf dibantu AI dan sudah saya periksa dan sunting sendiri."},
    "seo": {"primary_keywords": [], "audience_questions": [], "blog_url": ""},
    "channels": {"platforms": ["instagram", "tiktok", "linkedin", "x", "whatsapp"], "whatsapp": "", "email": "", "booking_url": ""},
    "hours": {"layanan": "Senin-Jumat 09:00-17:00 WIB", "respons_target": "dalam jam kerja secepatnya"},
    "video": {
        "world": "hutan sage lembut dengan cahaya senja hangat",
        "problem": "spreadsheet kusut, kabel liar, dan notifikasi bertubi-tubi",
        "solution": "tampilan rapi dan tenang dengan warna Biru Malam dan Api Dupa",
        "story_theme": "Si Liar menjinakkan data bisnis yang kacau",
    },
    "content": {
        "package": "Ringan",
        "pillars": [
            {
                "name": "Paham",
                "goal": "Membuktikan Pawang memahami masalah",
                "share": 35,
                "formats": "carousel, reels tips"
            },
            {
                "name": "Jinak",
                "goal": "Menjelaskan layanan",
                "share": 25,
                "formats": "carousel layanan, before-after"
            },
            {
                "name": "Tenang",
                "goal": "Testimoni, FAQ, paket",
                "share": 20,
                "formats": "kartu testimoni, FAQ"
            },
            {
                "name": "Si Liar",
                "goal": "Hiburan dan karakter",
                "share": 15,
                "formats": "reel maskot"
            },
            {
                "name": "Ajakan",
                "goal": "Mendatangkan konsultasi",
                "share": 5,
                "formats": "story promo"
            }
        ],
        "weeks_plan": [
            {
                "tema": "Kenali Data yang Liar",
                "rows": [
                    {
                        "hari": "Senin",
                        "topik": "4 tanda data bisnismu sudah liar",
                        "command": "/pw-carousel + /pw-t-carousel"
                    },
                    {
                        "hari": "Selasa",
                        "topik": "\"Satu angka, lima file.\" Hook Si Liar terlilit",
                        "command": "/pw-v-reels-hook + /pw-t-reels"
                    },
                    {
                        "hari": "Rabu",
                        "topik": "Seberapa sering salah angka di laporan? (polling)",
                        "command": "/pw-igstory + /pw-t-story"
                    },
                    {
                        "hari": "Kamis",
                        "topik": "Pawang Sheet: dari spreadsheet kusut ke dashboard rapi",
                        "command": "/pw-carousel + /pw-wacatalog"
                    },
                    {
                        "hari": "Jumat",
                        "topik": "Tips: satu sumber data, bukan lima file",
                        "command": "/pw-tips + /pw-t-foto"
                    },
                    {
                        "hari": "Sabtu",
                        "topik": "Si Liar bukan seram, liar itu cuma belum dipahami",
                        "command": "/pw-v-hello + /pw-t-reels"
                    },
                    {
                        "hari": "Minggu",
                        "topik": "Rencana pekan depan + ajakan konsultasi gratis",
                        "command": "/pw-igstory + /pw-t-cta",
                        "pilar": "Ajakan"
                    }
                ]
            },
            {
                "tema": "Website yang Jinak",
                "rows": [
                    {
                        "hari": "Senin",
                        "topik": "Hal-hal yang membuat pengunjung meninggalkan website usaha",
                        "command": "/pw-carousel + /pw-t-carousel"
                    },
                    {
                        "hari": "Selasa",
                        "topik": "Landing page lama vs landing page jinak",
                        "command": "/pw-v-beforeafter + /pw-t-reels",
                        "pilar": "Jinak"
                    },
                    {
                        "hari": "Rabu",
                        "topik": "Website kamu sudah cepat dibuka di ponsel? (kotak tanya)",
                        "command": "/pw-igstory + /pw-t-story"
                    },
                    {
                        "hari": "Kamis",
                        "topik": "Pawang Web: cepat, rapi, mudah diurus",
                        "command": "/pw-carousel + /pw-t-carousel"
                    },
                    {
                        "hari": "Jumat",
                        "topik": "Tips: judul halaman dan tombol WhatsApp yang jelas",
                        "command": "/pw-tips"
                    },
                    {
                        "hari": "Sabtu",
                        "topik": "Si Liar menata halaman web yang berantakan",
                        "command": "/pw-v-penjelasan"
                    },
                    {
                        "hari": "Minggu",
                        "topik": "Testimoni klien (isi dengan data nyata)",
                        "command": "/pw-testimoni"
                    }
                ]
            },
            {
                "tema": "Otomasi dan Persiapan 11.11",
                "rows": [
                    {
                        "hari": "Senin",
                        "topik": "Persiapan 11.11 untuk toko online: stok, pesanan, chat",
                        "command": "/pw-carousel + /pw-t-carousel"
                    },
                    {
                        "hari": "Selasa",
                        "topik": "Pahlawan tak terlihat di balik bisnis: sistem yang jalan sendiri",
                        "command": "/pw-v-story + /pw-t-reels"
                    },
                    {
                        "hari": "Rabu",
                        "topik": "11.11: pesanan membludak, siapa yang balas chat? (polling)",
                        "command": "/pw-igstory + /pw-t-story",
                        "pilar": "Jinak"
                    },
                    {
                        "hari": "Kamis",
                        "topik": "Pawang Otomasi: 3 contoh notifikasi WhatsApp otomatis",
                        "command": "/pw-carousel + /pw-wacatalog"
                    },
                    {
                        "hari": "Jumat",
                        "topik": "Tips: balasan otomatis untuk pertanyaan yang sama",
                        "command": "/pw-tips"
                    },
                    {
                        "hari": "Sabtu",
                        "topik": "Si Liar dikejar notifikasi, lalu dijinakkan",
                        "command": "/pw-v-reels-hook"
                    },
                    {
                        "hari": "Minggu",
                        "topik": "Persiapan 12.12: konsultasi gratis sebelum ramai",
                        "command": "/pw-promo + /pw-igstory",
                        "pilar": "Ajakan"
                    }
                ]
            },
            {
                "tema": "Dijaga dan Paket",
                "rows": [
                    {
                        "hari": "Senin",
                        "topik": "Pawang Rawat: website sudah jadi, siapa yang menjaga?",
                        "command": "/pw-carousel + /pw-t-carousel",
                        "pilar": "Jinak"
                    },
                    {
                        "hari": "Selasa",
                        "topik": "Update yang ditunda bisa jadi masalah (tanpa menakut-nakuti)",
                        "command": "/pw-v-penjelasan"
                    },
                    {
                        "hari": "Rabu",
                        "topik": "Kapan terakhir website kamu diperbarui? (polling)",
                        "command": "/pw-igstory"
                    },
                    {
                        "hari": "Kamis",
                        "topik": "Paket Jinak, Piawai, Sakti: mana yang cocok?",
                        "command": "/pw-paket + /pw-t-carousel",
                        "pilar": "Tenang"
                    },
                    {
                        "hari": "Jumat",
                        "topik": "5 pertanyaan yang sering ditanyakan calon klien",
                        "command": "/pw-faq",
                        "pilar": "Tenang",
                        "format": "Carousel FAQ"
                    },
                    {
                        "hari": "Sabtu",
                        "topik": "Si Liar Menjinakkan Data (paket 4 adegan)",
                        "command": "/pw-v-cerita"
                    },
                    {
                        "hari": "Minggu",
                        "topik": "Rekap 4 minggu + ajakan Konsultasi Gratis",
                        "command": "/pw-igstory + /pw-t-cta",
                        "pilar": "Ajakan"
                    }
                ]
            }
        ],
        "start": "2026-10-26"
    },
    "examples": {
        "topic": "tanda data bisnis sudah liar",
        "carousel": [
            "Data bisnismu sudah liar?\nCek 4 tandanya. Geser ->",
            "Cari satu angka,\nbuka lima file.\nKedengaran akrab?",
            "1\nSatu angka, banyak versi\nPenjualan bulan lalu beda di tiap file. Tidak ada yang yakin mana yang benar.",
            "2\nLaporan dibuat manual\nTiap minggu menyalin angka berjam-jam. Rawan salah dan bikin lelah.",
            "3\nPesan pelanggan tercecer\nWhatsApp, email, DM. Ada yang terlewat tanpa disadari.",
            "4\nHanya satu orang yang paham\nKalau dia cuti, semua berhenti.",
            "Jinakkan sebelum makin liar.\n[ Konsultasi Gratis ]\npawang.dev"
        ],
        "story": [
            {
                "tujuan": "Hook / pertanyaan",
                "teks": "Laporan bisnismu masih disalin manual?"
            },
            {
                "tujuan": "Masalah",
                "teks": "Rawan salah. Makan waktu. Bikin pusing."
            },
            {
                "tujuan": "Solusi",
                "teks": "Pawang Sheet: angka berantakan jadi dashboard rapi."
            },
            {
                "tujuan": "CTA",
                "teks": "Mau dicoba? Konsultasi Gratis -> pawang.dev"
            }
        ],
        "reels": {
            "title": "Si Liar Menjinakkan Data",
            "duration": 24,
            "rows": [
                {
                    "waktu": "0:00-0:03",
                    "visual": "Klip 1: tokoh terlilit kabel dan kertas",
                    "teks": "Data bisnismu juga liar begini?",
                    "posisi": "Tengah atas (di bawah 250 px)",
                    "animasi": "Pop membesar, 100 px"
                },
                {
                    "waktu": "0:03-0:06",
                    "visual": "Klip 1 (lanjut)",
                    "teks": "Satu angka, lima file.",
                    "posisi": "Bawah tengah, di atas 450 px",
                    "animasi": "Fade in, 56 px"
                },
                {
                    "waktu": "0:06-0:09",
                    "visual": "Klip 2: cahaya oranye menyala",
                    "teks": "Lalu ketemu Pawang.",
                    "posisi": "Tengah atas",
                    "animasi": "Geser dari kiri, 90 px"
                },
                {
                    "waktu": "0:09-0:12",
                    "visual": "Klip 2 (lanjut)",
                    "teks": "Kami pahami dulu masalahnya.",
                    "posisi": "Bawah tengah",
                    "animasi": "Fade in, 52 px"
                },
                {
                    "waktu": "0:12-0:15",
                    "visual": "Klip 3: layar kusut tertata",
                    "teks": "Paham -> Tenang -> Jinak",
                    "posisi": "Tengah",
                    "animasi": "Muncul satu per satu"
                },
                {
                    "waktu": "0:15-0:18",
                    "visual": "Klip 3 (lanjut)",
                    "teks": "Data kusut jadi dashboard rapi.",
                    "posisi": "Bawah tengah",
                    "animasi": "Fade in"
                },
                {
                    "waktu": "0:18-0:21",
                    "visual": "Klip 4: tokoh tenang melambai",
                    "teks": "Rapi. Tenang. Jalan sendiri.",
                    "posisi": "Tengah atas",
                    "animasi": "Pop"
                },
                {
                    "waktu": "0:21-0:24",
                    "visual": "Klip 4 (penutup)",
                    "teks": "Tombol Konsultasi Gratis + pawang.dev + logo",
                    "posisi": "Tengah bawah, di atas 450 px",
                    "animasi": "Tombol muncul memantul"
                }
            ]
        },
        "foto": {
            "headline": "Website jinak: cepat, rapi, mudah diurus.",
            "subteks": "Pawang Web untuk usaha yang ingin tampil tenang di dunia digital.",
            "formulas": [
                [
                    "Masalah -> solusi",
                    "Laporan berantakan? Jadikan dashboard."
                ],
                [
                    "Angka",
                    "4 tanda data bisnismu sudah liar"
                ],
                [
                    "Pertanyaan",
                    "Digitalmu liar?"
                ],
                [
                    "Janji",
                    "Dari kusut jadi rapi, tanpa istilah ribet."
                ]
            ]
        },
        "hooks": [
            [
                "Pertanyaan",
                "Laporan bisnismu masih disalin manual?"
            ],
            [
                "Kejutan",
                "Ini yang terjadi kalau data dibiarkan liar."
            ],
            [
                "Angka",
                "3 tanda websitemu bikin pelanggan pergi."
            ],
            [
                "Kontras",
                "Sebelum vs sesudah dijinakkan."
            ],
            [
                "Tantangan",
                "Coba hitung: berapa file untuk satu laporan?"
            ]
        ],
        "ctas": [
            "Konsultasi Gratis -> pawang.dev",
            "Chat kami, kita jinakkan bareng.",
            "Simpan video ini, kirim ke temanmu yang datanya liar.",
            "Komentar 'INFO' dan kami kirim detailnya."
        ],
        "thumbnails": {
            "thumbnail": "DATA LIAR? JINAKKAN.",
            "og": "5 Cara Membuat Laporan Bisnis Otomatis",
            "pinterest": "Checklist: Apakah Data Bisnismu Sudah Jinak?"
        },
        "caption": "Cari satu angka, buka lima file? Itu tanda data bisnismu mulai liar.\nKabar baiknya, bisa dijinakkan tanpa istilah teknis yang bikin pusing.\nGeser untuk 4 tandanya, lalu cek mana yang kamu alami.\nMau dibantu? Konsultasi Gratis -> pawang.dev\n#digitalbisnis #otomasiusaha #dashboardbisnis #umkmdigital"
    },
    "faq": [{"q": "Berapa lama pengerjaan?", "a": ""}],
}


DEFAULT_RHYTHM = [
    {"hari": "Senin", "format": "Carousel edukasi", "platform": "Instagram (+ LinkedIn)", "jam": "09:00", "pilar": 0, "minimal": True},
    {"hari": "Selasa", "format": "Reels/Short pendek", "platform": "Instagram Reels, TikTok, YouTube Shorts", "jam": "12:00", "pilar": 0, "minimal": False},
    {"hari": "Rabu", "format": "Story interaktif (polling/tanya)", "platform": "Instagram Story, WA Status", "jam": "19:30", "pilar": 0, "minimal": False},
    {"hari": "Kamis", "format": "Carousel layanan / bukti", "platform": "Instagram (+ LinkedIn)", "jam": "09:30", "pilar": 1, "minimal": True},
    {"hari": "Jumat", "format": "Kartu tips cepat", "platform": "Instagram, X", "jam": "12:00", "pilar": 0, "minimal": False},
    {"hari": "Sabtu", "format": "Reel/cerita karakter", "platform": "Reels, TikTok, Shorts", "jam": "19:00", "pilar": 3, "minimal": True},
    {"hari": "Minggu", "format": "Testimoni / rekap pekan / ajakan", "platform": "Instagram Story, WA Status", "jam": "19:30", "pilar": 2, "minimal": False},
]


def default_rhythm(pillars):
    """Ritme bawaan dengan indeks pilar dipetakan ke nama pilar brand (urutan: edukasi, solusi, bukti, karakter, ajakan)."""
    names = [x["name"] for x in pillars]
    out = []
    for r in DEFAULT_RHYTHM:
        i = min(r["pilar"], len(names) - 1)
        out.append(dict(r, pilar=names[i]))
    return out


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(rgb):
    c = []
    for v in rgb:
        v /= 255
        c.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = lum(hex2rgb(a)), lum(hex2rgb(b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def by_role(p):
    return {c["role"]: c for c in p.get("colors", []) if "role" in c}


def contrast_table(p):
    r = by_role(p)
    pairs = [("offwhite", "dark", "teks utama di latar gelap"), ("dark", "light", "teks utama di latar terang"),
             ("accent", "light", "teks/tombol aksen di latar terang"), ("accent", "dark", "teks aksen di latar gelap"),
             ("dark", "accent", "teks gelap pada tombol aksen"), ("dark", "support", "teks gelap di latar pendukung"),
             ("light", "dark", "teks terang di latar gelap")]
    rows = []
    for fg, bg, label in pairs:
        if fg in r and bg in r:
            ratio = contrast(r[fg]["hex"], r[bg]["hex"])
            level = "AA (teks normal)" if ratio >= 4.5 else "AA hanya teks besar/tombol" if ratio >= 3 else "TIDAK LOLOS"
            rows.append((label, r[fg]["name"], r[bg]["name"], round(ratio, 2), level))
    return rows


def validate(p):
    errs, warns = [], []
    if p.get("schema") != SCHEMA:
        errs.append(f"Field schema harus '{SCHEMA}' (ditemukan: '{p.get('schema')}').")
    for k in REQUIRED:
        if not p.get(k):
            errs.append(f"Field wajib kosong: {k}")
    if p.get("prefix") and not re.fullmatch(r"[a-z]{2,3}", p["prefix"]):
        errs.append("prefix harus 2-3 huruf kecil tanpa '/' atau '-'.")
    if p.get("prefix") in {"ai", "ig", "wa", "fb", "tt", "yt"}:
        warns.append(f"prefix '{p['prefix']}' mirip singkatan platform; pilih yang unik untuk brand.")
    seen = set()
    for c in p.get("colors", []):
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", c.get("hex", "")):
            errs.append(f"Hex salah: {c.get('name')} '{c.get('hex')}'")
        if c.get("role") not in ROLES:
            warns.append(f"Role '{c.get('role')}' tidak standar (pakai: {', '.join(ROLES)}).")
        if c.get("role") in seen:
            errs.append(f"Role ganda: {c['role']}")
        seen.add(c.get("role"))
    for need in ("dark", "accent", "light"):
        if need not in seen:
            errs.append(f"Warna role '{need}' wajib ada.")
    if "support" not in seen:
        warns.append("Role 'support' tidak ada; skill lain akan memakai 'accent' sebagai pengganti.")
    if "offwhite" not in seen:
        warns.append("Role 'offwhite' tidak ada; skill lain akan memakai 'light' sebagai pengganti.")
    for row in contrast_table(p):
        if row[4] == "TIDAK LOLOS":
            warns.append(f"Kontras rendah: {row[0]} ({row[1]} di {row[2]}) = {row[3]}:1; jangan dipakai untuk teks.")
    pl = p.get("content", {}).get("pillars")
    if pl and sum(x.get("share", 0) for x in pl) != 100:
        errs.append(f"Total porsi pilar {sum(x.get('share', 0) for x in pl)}%, harus 100%.")
    for pk in p.get("packages", []):
        if not pk.get("price"):
            warns.append(f"Paket {pk.get('name')}: harga kosong (balasan harga akan memakai [ISI SENDIRI]).")
    if p.get("mascot") and not p["mascot"].get("desc"):
        warns.append("Deskripsi maskot kosong; Character Lock akan lemah.")
    au = p.get("author") or {}
    if not au.get("name") or not au.get("role"):
        warns.append("author.name/role kosong; diperlukan untuk jawaban Quora dan artikel (isi dengan keahlian dan pengalaman yang benar-benar ada).")
    ch = p.get("channels", {})
    if not ch.get("whatsapp"):
        warns.append("Nomor WhatsApp kosong; template balasan akan memakai [ISI SENDIRI].")
    return errs, warns


def export(p, target, start=None):
    if target not in TARGET_REQ:
        raise SystemExit(f"Target tidak dikenal: {target} (pilih: {', '.join(TARGET_REQ)})")
    out = {k: p[k] for k in COMMON if k in p}
    out["cta"] = p.get("cta", "")
    if target == "flow-video":
        out["video"] = p.get("video", {})
    elif target == "text-layout":
        out["examples"] = p.get("examples", {})
    elif target == "calendar":
        c = p.get("content", {})
        out.update(start=start or c.get("start"), package=c.get("package", "Ringan"), weeks_plan=c.get("weeks_plan"),
                   pillars=c.get("pillars"), rhythm=c.get("rhythm"), extras=c.get("extras"),
                   topic_bank=c.get("topic_bank"), momen=c.get("momen"))
        if out.get("pillars") and not out.get("rhythm"):
            out["rhythm"] = default_rhythm(out["pillars"])
        out = {k: v for k, v in out.items() if v not in (None, [], {})}
    elif target == "caption":
        out = {"brand": p["brand"], "cta": p["cta"], "avoid": p.get("avoid", []), "brief": {"topik": "", "tujuan": "", "konten": ""}, "items": []}
    elif target in ("quora", "longform"):
        out["author"] = p.get("author", {})
        out["seo"] = p.get("seo", {})
        out["avoid"] = p.get("avoid", [])
    elif target == "reply":
        out["address"] = p.get("address", "Kak")
        out["channels"] = p.get("channels", {})
        out["hours"] = p.get("hours", {})
        out["faq"] = p.get("faq", [])
    missing = [k for k in TARGET_REQ[target] if not out.get(k)]
    if target in ("quora", "longform"):
        au = out.get("author") or {}
        missing = [m for m in missing if m != "author"]
        for f in ("name", "role"):
            if not au.get(f):
                missing.append(f"author.{f}")
    return out, missing


def locks(p):
    r = by_role(p)
    colors = "\n".join(f"- {c['name']} {c['hex']} ({c.get('use', c['role'])})" for c in p["colors"])
    m = p.get("mascot")
    bl = ["BRAND LOCK - " + p["brand"], "Selalu ikuti brand board yang saya upload. Jangan mengubah logo, maskot, warna, atau font.", "",
          f"Brand: {p['brand']}", f"Tagline: \"{p['tagline']}\"", f"Karakter brand: {p.get('tone', '')}."]
    if m:
        bl.append(f"Maskot: \"{m['name']}\" - {m['desc']}.")
    bl += ["", "Warna (hanya ini):", colors, "", f"Tipografi: {p['fonts']['heading']} (judul, tebal), {p['fonts']['body']} (isi).",
           f"Logo: {p['logo_desc']}.", f"Gaya visual: {p.get('style', '')}."]
    if p.get("services"):
        bl.append("Layanan: " + ", ".join(s["name"] for s in p["services"]) + ".")
    if p.get("packages"):
        bl.append("Paket: " + ", ".join(f"{x['name']} ({x.get('color', '')})" for x in p["packages"]) + ".")
    bl += [f"CTA standar: \"{p['cta'].replace('->', chr(0x2192))}\"", "Bahasa: Indonesia santai-profesional, kalimat pendek.", "",
           "Aturan teks pada gambar:", "- Tulis teks seminimal mungkin, besar, dan terbaca.", "- Eja persis seperti yang saya berikan. Jangan menambah/mengubah kata.",
           "- Jaga margin aman 6% dari tepi.", "- Jangan pakai warna di luar palet."]
    vl = ["VOICE LOCK - " + p["brand"], f"Suara brand: {p.get('tone', '')}.", f"Tagline: \"{p['tagline']}\"",
          f"CTA standar: \"{p['cta'].replace('->', chr(0x2192))}\"", "Bahasa Indonesia santai-profesional, kalimat pendek.",
          "Hindari: " + ", ".join(a.strip() for a in p.get("avoid", [])) + ".",
          "Aturan: hook maksimal 8 kata, teks video maksimal 6 kata per baris, jangan mengarang data atau testimoni."]
    return "\n".join(bl), "\n".join(vl)


def md_table(text, heading):
    """Ambil baris tabel Markdown pertama setelah heading yang memuat `heading`."""
    m = re.search(r"^#{2,4}\s*[^\n]*" + re.escape(heading) + r"[^\n]*\n(.*?)(?=^#{2,4}\s|\Z)", text, re.S | re.M)
    if not m:
        return []
    rows = []
    for ln in m.group(1).splitlines():
        if ln.strip().startswith("|") and not re.match(r"^\|\s*-", ln.strip()):
            rows.append([c.strip() for c in ln.strip().strip("|").split("|")])
    return rows[1:] if rows else []


def clean(x):
    return re.sub(r"\s*\[ASUMSI\]\s*", " ", x).replace("`", "").strip()


def bullet(text, key):
    m = re.search(r"^[-*]\s*" + re.escape(key) + r"[^:\n]*:\s*(.+)$", text, re.M | re.I)
    return clean(m.group(1)) if m else ""


def from_spec(md):
    """Draf profile.json dari Brand Spec (format skill brandboard-standard). Hasil WAJIB dikonfirmasi."""
    notes = []
    name = (re.search(r"^#\s*Brand Spec:\s*(.+)$", md, re.M) or [None, ""])[1].strip()
    letters = re.sub(r"[^a-z]", "", name.lower())
    explicit_pre = bullet(md, "Prefix").lower()
    pre = explicit_pre if re.fullmatch(r"[a-z]{2,3}", explicit_pre) else ("pw" if name.lower().startswith("pawang") else (letters[:2] or "xx"))
    url = bullet(md, "URL") or bullet(md, "Website") or (name.lower() if "." in name and " " not in name else "")
    handle = bullet(md, "Handle") or url
    cta = bullet(md, "CTA")
    style = bullet(md, "Gaya visual")
    pattern = bullet(md, "Elemen pola")
    prof = {"schema": SCHEMA, "brand": name, "brand_short": name.split(".")[0], "prefix": pre,
            "tagline": bullet(md, "Tagline"), "cta": cta, "url": url, "handle": handle,
            "quote": bullet(md, "Kalimat pendamping"), "audience": bullet(md, "Target audiens"),
            "tone": bullet(md, "Tone") or bullet(md, "Karakter"), "style": style,
            "avoid": ["dijamin", "pasti ", "100%", "terbaik", "nomor 1", "garansi"], "address": "Kak"}
    if pattern:
        prof["pattern_elements"] = pattern
    if not explicit_pre:
        notes.append(f"prefix '{prof['prefix']}' hanya usulan dari huruf awal; ganti bila bentrok.")
    # logo
    for r in md_table(md, "Variasi Logo"):
        if r and r[0].lower().startswith("horizontal") and len(r) > 1:
            prof["logo_desc"] = clean(r[1])
    prof.setdefault("logo_desc", "")
    # warna
    cols = []
    for r in md_table(md, "Palet Warna"):
        hx = re.search(r"#[0-9A-Fa-f]{6}", r[1] if len(r) > 1 else "")
        if hx:
            cols.append({"name": clean(r[0]), "hex": hx.group(0).upper(), "peran": clean(r[2]).lower() if len(r) > 2 else "",
                         "use": clean(r[2]) if len(r) > 2 else ""})
    used = set()
    final = []

    def take(pred, role):
        for c in cols:
            if id(c) not in used and pred(c):
                used.add(id(c))
                final.append({"role": role, "name": c["name"], "hex": c["hex"], "use": c["use"]})
                return True
        return False
    L = lambda c: lum(hex2rgb(c["hex"]))
    take(lambda c: "aksen" in c["peran"] or "cta" in c["peran"], "accent")
    take(lambda c: ("utama" in c["peran"] or "teks gelap" in c["peran"]) and L(c) < 0.25, "dark")
    take(lambda c: "latar" in c["peran"] and L(c) > 0.5, "light")
    if not any(f["role"] == "dark" for f in final):
        take(lambda c: L(c) < 0.15, "dark")
    for c in sorted([c for c in cols if id(c) not in used], key=lambda c: -L(c)):
        role = "offwhite" if L(c) > 0.9 and not any(f["role"] == "offwhite" for f in final) else \
               "support" if not any(f["role"] == "support" for f in final) else None
        if role:
            used.add(id(c))
            final.append({"role": role, "name": c["name"], "hex": c["hex"], "use": c["use"]})
    prof["colors"] = final
    left = [c["name"] for c in cols if id(c) not in used]
    if left:
        notes.append("warna tanpa role (tidak dimasukkan): " + ", ".join(left))
    notes.append("role warna ditentukan heuristik dari kolom Peran dan kecerahan; periksa dark/accent/light/support/offwhite.")
    # font
    fonts = {}
    for r in md_table(md, "Tipografi"):
        if len(r) > 1:
            k = r[0].lower()
            if k.startswith("judul"):
                fonts["heading"] = clean(r[1])
            elif k.startswith("isi"):
                fonts["body"] = clean(r[1])
            elif "kode" in k:
                fonts["code"] = clean(r[1])
    prof["fonts"] = fonts
    # maskot
    mt = md_table(md, "Maskot")
    if mt:
        desc = next((clean(r[2]) for r in mt if r and r[0].lower().startswith("utama") and len(r) > 2), "")
        mname = bullet(md, "Nama maskot") or bullet(md, "Maskot")
        prof["mascot"] = {"name": mname, "desc": desc}
        if not mname:
            notes.append("nama maskot tidak ditemukan di Brand Spec; isi mascot.name.")
    # layanan dan paket
    sv = [{"name": clean(r[0]), "benefit": clean(r[1]) if len(r) > 1 else ""} for r in md_table(md, "Layanan") if r and clean(r[0])]
    if sv:
        prof["services"] = sv
    pk = [{"name": clean(r[0]), "color": clean(r[1]) if len(r) > 1 else "", "desc": clean(r[2]) if len(r) > 2 else "", "price": ""}
          for r in md_table(md, "Paket") if r and clean(r[0])]
    if pk:
        prof["packages"] = pk
        notes.append("harga paket tidak ada di Brand Spec; isi packages[].price bila sudah ditetapkan.")
    # microcopy CTA
    for r in md_table(md, "Gaya Bahasa"):
        if r and r[0].lower().startswith("tombol cta") and len(r) > 1:
            prof["cta_short"] = clean(r[1]).strip('"')
    if not prof.get("cta") and prof.get("cta_short"):
        prof["cta"] = f"{prof['cta_short']} -> {prof['url']}" if prof.get("url") else prof["cta_short"]
    role_order = {r: i for i, r in enumerate(ROLES)}
    prof["colors"].sort(key=lambda c: role_order.get(c.get("role"), 99))
    notes.append("channels, hours, dan video belum ada di Brand Spec; lengkapi bila diperlukan.")
    missing = [k for k in ("tagline", "logo_desc") if not prof.get(k)] + [k for k in ("heading", "body") if k not in fonts]
    if missing:
        notes.append("kosong: " + ", ".join(missing))
    assumed = sorted(set(re.findall(r"^#{2,4}\s*([^\n]*?)\s*\[ASUMSI\]", md, re.M)))
    if assumed:
        notes.append("section bertanda [ASUMSI] di Brand Spec (belum dikonfirmasi): " + "; ".join(assumed))
    return prof, notes


def dominant_colors(path, n=6):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    im.thumbnail((200, 200))
    q = im.quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:n * 3]
    tot = sum(c for c, _ in q.getcolors())
    return [("#%02X%02X%02X" % tuple(pal[i * 3:i * 3 + 3]), round(100 * c / tot, 1)) for c, i in sorted(q.getcolors(), reverse=True)]


def main(a):
    if len(a) >= 2 and a[1] == "--example":
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False))
        return 0
    if len(a) == 3 and a[1] == "validate":
        p = json.loads(Path(a[2]).read_text(encoding="utf-8"))
        e, w = validate(p)
        print("Tabel kontras warna (WCAG):")
        for r in contrast_table(p):
            print(f"  {r[0]:<42} {r[1]} di {r[2]}: {r[3]}:1  {r[4]}")
        print("Galat: " + ("tidak ada" if not e else "\n" + "\n".join("- " + x for x in e)))
        print("Peringatan: " + ("tidak ada" if not w else "\n" + "\n".join("- " + x for x in w)))
        return 1 if e else 0
    if len(a) >= 6 and a[1] == "export" and a[3] == "--for":
        p = json.loads(Path(a[2]).read_text(encoding="utf-8"))
        start = a[a.index("--start") + 1] if "--start" in a else None
        out, missing = export(p, a[4], start)
        Path(a[5]).write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Ditulis: {a[5]} (target {a[4]})")
        if missing:
            print("Belum lengkap untuk target ini, isi dulu di profile.json: " + ", ".join(missing))
            return 1
        print("Lengkap untuk target ini.")
        return 0
    if len(a) == 3 and a[1] == "lock":
        p = json.loads(Path(a[2]).read_text(encoding="utf-8"))
        b, v = locks(p)
        print("```\n" + b + "\n```\n\n```\n" + v + "\n```")
        return 0
    if len(a) == 4 and a[1] == "from-spec":
        prof, notes = from_spec(Path(a[2]).read_text(encoding="utf-8"))
        Path(a[3]).write_text(json.dumps(prof, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Draf profil ditulis: {a[3]}\nKonfirmasi dengan user:")
        for n in notes:
            print("  - " + n)
        return 0
    if len(a) >= 3 and a[1] == "colors":
        n = int(a[a.index("--n") + 1]) if "--n" in a else 6
        for h, pct in dominant_colors(a[2], n):
            print(f"{h}  {pct}%")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
