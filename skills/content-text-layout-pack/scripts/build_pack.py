#!/usr/bin/env python3
"""Render panduan teks, layout, dan waktu konten (Canva/CapCut) dari brand.json, atau validasi file.

Pemakaian:
  python build_pack.py brand.json out.md        # render + validasi + lint contoh
  python build_pack.py --check out.md [prefix]  # validasi file saja
  python build_pack.py --example                # cetak contoh brand.json
"""
import json
import re
import sys
from pathlib import Path

EXAMPLE = {
    "brand": "Pawang.dev", "prefix": "pw",
    "tagline": "Digitalmu liar? Serahkan ke Pawang.",
    "cta": "Konsultasi Gratis -> pawang.dev", "url": "pawang.dev",
    "tone": "tenang, paham, jinak; hangat, ramah, tidak menakut-nakuti dengan istilah teknis",
    "avoid": "janji berlebihan, angka karangan, istilah teknis tanpa penjelasan, jargon",
    "colors": [
        {"role": "dark", "name": "Biru Malam", "hex": "#14213D"},
        {"role": "accent", "name": "Api Dupa", "hex": "#FF8A3D"},
        {"role": "light", "name": "Krem", "hex": "#FFF6E9"},
        {"role": "support", "name": "Hijau Sage", "hex": "#A7C4A0"},
        {"role": "offwhite", "name": "Putih Tulang", "hex": "#FAFAF7"},
    ],
    "fonts": {"heading": "Plus Jakarta Sans", "body": "Inter"},
    "mascot": {"name": "Si Liar"},
    "examples": {
        "topic": "tanda data bisnis sudah liar",
        "carousel": [
            "Data bisnismu sudah liar?\nCek 4 tandanya. Geser ->",
            "Cari satu angka,\nbuka lima file.\nKedengaran akrab?",
            "1\nSatu angka, banyak versi\nPenjualan bulan lalu beda di tiap file. Tidak ada yang yakin mana yang benar.",
            "2\nLaporan dibuat manual\nTiap minggu menyalin angka berjam-jam. Rawan salah dan bikin lelah.",
            "3\nPesan pelanggan tercecer\nWhatsApp, email, DM. Ada yang terlewat tanpa disadari.",
            "4\nHanya satu orang yang paham\nKalau dia cuti, semua berhenti.",
            "Jinakkan sebelum makin liar.\n[ Konsultasi Gratis ]\npawang.dev",
        ],
        "story": [
            {"tujuan": "Hook / pertanyaan", "teks": "Laporan bisnismu masih disalin manual?"},
            {"tujuan": "Masalah", "teks": "Rawan salah. Makan waktu. Bikin pusing."},
            {"tujuan": "Solusi", "teks": "Pawang Sheet: angka berantakan jadi dashboard rapi."},
            {"tujuan": "CTA", "teks": "Mau dicoba? Konsultasi Gratis -> pawang.dev"},
        ],
        "reels": {
            "title": "Si Liar Menjinakkan Data", "duration": 24,
            "rows": [
                {"waktu": "0:00-0:03", "visual": "Klip 1: tokoh terlilit kabel dan kertas", "teks": "Data bisnismu juga liar begini?", "posisi": "Tengah atas (di bawah 250 px)", "animasi": "Pop membesar, 100 px"},
                {"waktu": "0:03-0:06", "visual": "Klip 1 (lanjut)", "teks": "Satu angka, lima file.", "posisi": "Bawah tengah, di atas 450 px", "animasi": "Fade in, 56 px"},
                {"waktu": "0:06-0:09", "visual": "Klip 2: cahaya oranye menyala", "teks": "Lalu ketemu Pawang.", "posisi": "Tengah atas", "animasi": "Geser dari kiri, 90 px"},
                {"waktu": "0:09-0:12", "visual": "Klip 2 (lanjut)", "teks": "Kami pahami dulu masalahnya.", "posisi": "Bawah tengah", "animasi": "Fade in, 52 px"},
                {"waktu": "0:12-0:15", "visual": "Klip 3: layar kusut tertata", "teks": "Paham -> Tenang -> Jinak", "posisi": "Tengah", "animasi": "Muncul satu per satu"},
                {"waktu": "0:15-0:18", "visual": "Klip 3 (lanjut)", "teks": "Data kusut jadi dashboard rapi.", "posisi": "Bawah tengah", "animasi": "Fade in"},
                {"waktu": "0:18-0:21", "visual": "Klip 4: tokoh tenang melambai", "teks": "Rapi. Tenang. Jalan sendiri.", "posisi": "Tengah atas", "animasi": "Pop"},
                {"waktu": "0:21-0:24", "visual": "Klip 4 (penutup)", "teks": "Tombol Konsultasi Gratis + pawang.dev + logo", "posisi": "Tengah bawah, di atas 450 px", "animasi": "Tombol muncul memantul"},
            ],
        },
        "foto": {
            "headline": "Website jinak: cepat, rapi, mudah diurus.",
            "subteks": "Pawang Web untuk usaha yang ingin tampil tenang di dunia digital.",
            "formulas": [
                ["Masalah -> solusi", "Laporan berantakan? Jadikan dashboard."],
                ["Angka", "4 tanda data bisnismu sudah liar"],
                ["Pertanyaan", "Digitalmu liar?"],
                ["Janji", "Dari kusut jadi rapi, tanpa istilah ribet."],
            ],
        },
        "hooks": [
            ["Pertanyaan", "Laporan bisnismu masih disalin manual?"],
            ["Kejutan", "Ini yang terjadi kalau data dibiarkan liar."],
            ["Angka", "3 tanda websitemu bikin pelanggan pergi."],
            ["Kontras", "Sebelum vs sesudah dijinakkan."],
            ["Tantangan", "Coba hitung: berapa file untuk satu laporan?"],
        ],
        "ctas": [
            "Konsultasi Gratis -> pawang.dev",
            "Chat kami, kita jinakkan bareng.",
            "Simpan video ini, kirim ke temanmu yang datanya liar.",
            "Komentar 'INFO' dan kami kirim detailnya.",
        ],
        "thumbnails": {"thumbnail": "DATA LIAR? JINAKKAN.", "og": "5 Cara Membuat Laporan Bisnis Otomatis", "pinterest": "Checklist: Apakah Data Bisnismu Sudah Jinak?"},
        "caption": "Cari satu angka, buka lima file? Itu tanda data bisnismu mulai liar.\nKabar baiknya, bisa dijinakkan tanpa istilah teknis yang bikin pusing.\nGeser untuk 4 tandanya, lalu cek mana yang kamu alami.\nMau dibantu? Konsultasi Gratis -> pawang.dev\n#digitalbisnis #otomasiusaha #dashboardbisnis #umkmdigital",
    },
}
REQUIRED = ["brand", "prefix", "tagline", "cta", "url", "colors", "fonts", "examples"]


def col(b, role, fb=()):
    by = {c["role"]: c for c in b["colors"]}
    for r in (role, *fb):
        if r in by:
            return by[r]
    raise SystemExit(f"brand.json: warna role '{role}' tidak ada (wajib: dark, accent, light)")


def words(s):
    return len(re.findall(r"\S+", s))


def sec(ts):
    m, s = ts.split(":")
    return int(m) * 60 + int(s)


def lint(b):
    """Peringatan kualitas isi contoh (tidak menggagalkan render)."""
    w = []
    ex = b["examples"]
    if len(ex.get("carousel", [])) != 7:
        w.append("examples.carousel harus berisi tepat 7 slide.")
    else:
        hook = ex["carousel"][0].split("\n")[0]
        if words(hook) > 8:
            w.append(f"Hook carousel lebih dari 8 kata: '{hook}'")
    if len(ex.get("story", [])) < 3:
        w.append("examples.story minimal 3 story.")
    r = ex.get("reels", {})
    rows = r.get("rows", [])
    if not rows:
        w.append("examples.reels.rows kosong.")
    last_end = None
    for row in rows:
        try:
            a, z = row["waktu"].split("-")
            d = sec(z) - sec(a)
        except Exception:
            w.append(f"Format waktu salah: {row.get('waktu')} (pakai 0:00-0:03)")
            continue
        if last_end is not None and sec(a) != last_end:
            w.append(f"Celah/tumpang tindih waktu di {row['waktu']}")
        last_end = sec(z)
        for line in re.split(r"\n| / ", row["teks"]):
            if words(line) > 6 and "+" not in line:
                w.append(f"Teks video lebih dari 6 kata per baris di {row['waktu']}: '{line}'")
        need = 1 + 0.3 * words(row["teks"])
        if d + 0.2 < need and "+" not in row["teks"]:
            w.append(f"Teks terlalu cepat di {row['waktu']}: {d}s < {need:.1f}s (rumus 1s + 0,3s/kata)")
    if rows and r.get("duration") and last_end != int(r["duration"]):
        w.append(f"Durasi total {r['duration']}s tidak sama dengan akhir tabel ({last_end}s).")
    for h in ex.get("hooks", []):
        if words(h[1]) > 8:
            w.append(f"Hook lebih dari 8 kata: '{h[1]}'")
    return w


def render(b):
    for k in REQUIRED:
        if not b.get(k):
            raise SystemExit(f"brand.json: field wajib '{k}' kosong atau tidak ada")
    ex = b["examples"]
    pre = "/" + b["prefix"].strip("/-") + "-t-"
    cta = b["cta"].replace("->", "\u2192")
    dark, acc, light = col(b, "dark"), col(b, "accent", ()), col(b, "light")
    sup = col(b, "support", ("accent",))
    off = col(b, "offwhite", ("light",))
    H, B = b["fonts"]["heading"], b["fonts"]["body"]
    m = b.get("mascot", {}).get("name")
    visual = m if m else "visual utama"
    topic = ex.get("topic", "{topik}")
    o = []
    w = o.append

    def C(c): return f"{c['name']} {c['hex']}"

    w(f"# Panduan Teks, Layout, dan Waktu {b['brand']} (Canva & CapCut)\n")
    w("Menjawab tiga pertanyaan: **teks apa yang diisi**, **ditaruh di mana**, dan **muncul di detik berapa**.")
    w("Gambar/video dibuat di ChatGPT dan Flow **tanpa teks**; semua tulisan ditambahkan di Canva atau CapCut memakai panduan ini.\n")
    w("Cara pakai cepat:")
    w("1. Pilih format di Bagian 2-6 (carousel, story, foto, reel/short, thumbnail).")
    w(f"2. Salin teks contoh, atau jalankan command `{pre}...` di Bagian 8 untuk membuat teks sesuai topik Anda.")
    w("3. Ikuti tabel posisi dan waktu, lalu atur di Canva/CapCut (Bagian 9).\n")
    w("---\n")
    w("## 1. Aturan Dasar (berlaku untuk semua format)\n")
    w("### 1.1 Gaya teks brand\n")
    w("| Elemen | Aturan |\n|---|---|")
    w(f"| Font judul | {H}, ExtraBold/Bold |")
    w(f"| Font isi | {B}, Regular/Medium |")
    w(f"| Warna teks di latar gelap | {C(off)} |")
    w(f"| Warna teks di latar terang | {C(dark)} |")
    w(f"| Kata penekanan | {C(acc)} (maksimal 1-2 kata per layar) |")
    w(f"| Tombol/CTA | Latar {C(acc)}, teks {C(dark)} |")
    w(f"| Latar kartu/pendukung | {C(light)}, {C(sup)} |")
    w(f"| Logo | Kecil di pojok, jangan menutupi {visual} |\n")
    w(f"Kontras: teks {off['name']} di atas {dark['name']}, atau {dark['name']} di atas {light['name']}. Hindari {acc['name']} sebagai warna teks panjang di atas {light['name']}.\n")
    w("### 1.2 Batas jumlah kata\n")
    w("| Jenis teks | Maksimal |\n|---|---|\n| Hook / judul utama | 6-8 kata |\n| Subteks | 12-15 kata |\n| Isi slide carousel | 25-30 kata |\n| Teks di video per layar | 6 kata per baris, maksimal 2 baris |\n| Tombol CTA | 2-4 kata |\n")
    w("### 1.3 Ukuran font (patokan, kanvas lebar 1080 px)\n")
    w("| Elemen | Ukuran |\n|---|---|\n| Judul utama | 72-110 px |\n| Subjudul | 44-56 px |\n| Isi | 36-44 px |\n| Teks kecil (nomor, handle) | 26-32 px |\n| Teks video di ponsel | tidak kurang dari 48 px |\n")
    w("Tes cepat: perkecil layar ke ukuran ponsel; jika masih terbaca, ukuran sudah aman.\n")
    w("### 1.4 Zona aman (agar tidak tertutup tampilan aplikasi)\n")
    w("Angka berikut patokan umum; tampilan aplikasi bisa berubah, jadi lihat panduan resmi platform bila ragu.\n")
    w("| Format | Atas | Bawah | Samping |\n|---|---|---|---|\n| IG Story / WA Status (1080x1920) | kosongkan ±250 px | kosongkan ±340 px | ±60 px |\n| Reels / TikTok / Shorts (1080x1920) | kosongkan ±250 px | kosongkan ±450 px | kanan ±140 px (ikon suka/komentar) |\n| Post / carousel IG (1080x1350) | ±90 px | ±90 px | ±90 px |\n| OG image (1200x630) | ±60 px | ±60 px | ±80 px |\n")
    w("### 1.5 Waktu tampil teks di video\n")
    w("Rumus: **durasi tampil minimal = 1 detik + 0,3 detik x jumlah kata.**\nContoh: 6 kata = 1 + 1,8 = **±2,8 detik**. Jangan menaruh teks di bawah 1,5 detik.\n")
    w("---\n")

    # 2 carousel
    w("## 2. Carousel Instagram (1080x1350, 7 slide)\n")
    w("### 2.1 Pola layout 7 slide\n")
    w("| Slide | Isi | Layout | Latar |\n|---|---|---|---|")
    w(f"| 1 | Hook | Judul 90-110 px di sepertiga atas; subteks kecil di bawah judul; logo kecil pojok kiri atas; panah geser pojok kanan bawah | {dark['name']} |")
    w(f"| 2 | Masalah | Kalimat besar 70-80 px di tengah; ikon kecil {sup['name']} | {light['name']} |")
    w(f"| 3-6 | Satu poin per slide | Angka besar ({acc['name']}, 160 px) di kiri atas; judul poin 64 px; penjelasan 40 px maksimal 2 kalimat; nomor \"3/7\" pojok kanan atas | Bergantian {light['name']} dan {dark['name']} |")
    w(f"| 7 | CTA | Kalimat ajakan 72 px; tombol {acc['name']} di tengah bawah; handle/URL di bawah tombol; logo di atas | {dark['name']} |\n")
    w("Footer semua slide: logo kecil (lebar ±120 px) kiri bawah, nomor slide kanan atas, margin 90 px.\n")
    w(f"### 2.2 Contoh isi teks (topik: {topic})\n")
    names = ["Hook", "Masalah", "", "", "", "", "CTA"]
    for i, t in enumerate(ex["carousel"], 1):
        lab = f"Slide {i}" + (f" ({names[i-1]})" if names[i - 1] else "")
        w(f"**{lab}**")
        w("```\n" + t + "\n```")
    w("\n### 2.3 Cara menaruhnya di Canva\nBuat satu desain 1080x1350, duplikat halaman untuk tiap slide, lalu ubah teks saja. Simpan logo, nomor, dan panah sebagai elemen yang sama di semua halaman. Unduh sebagai PNG.\n")
    w("---\n")

    # 3 story
    w("## 3. Story (IG, WA Status) 1080x1920\n")
    w("### 3.1 Pola layout 3 zona\n")
    w(f"| Zona | Posisi | Isi |\n|---|---|---|\n| Atas (250 px kosong) | tidak ada teks | area UI aplikasi |\n| Zona judul | sepertiga atas, di bawah 250 px | judul 80-100 px, maksimal 8 kata |\n| Zona visual | tengah | {visual} atau gambar utama |\n| Zona aksi | di atas 340 px dari bawah | tombol/stiker/CTA |\n| Bawah (340 px kosong) | tidak ada teks | area balas pesan |\n")
    w(f"### 3.2 Urutan {len(ex['story'])} story (satu hari)\n")
    w("| Story | Tujuan | Teks contoh |\n|---|---|---|")
    for i, s in enumerate(ex["story"], 1):
        w(f"| {i} | {s['tujuan']} | `{s['teks']}` |")
    w("\n### 3.3 Stiker interaktif\nTaruh stiker polling/pertanyaan di zona aksi, satu per story. Contoh format: `{pertanyaan singkat}? Ya / Tidak` atau `Tanya seputar {topik}`.\n")
    w("### 3.4 WhatsApp Status\nSama seperti story, tetapi teks lebih besar (judul 100-120 px) dan CTA berbentuk ajakan chat: `Balas \"INFO\" untuk konsultasi gratis`.\n")
    w("---\n")

    # 4 foto
    f = ex.get("foto", {})
    w("## 4. Post Foto / Gambar Tunggal (1080x1350)\n")
    w(f"| Zona | Isi |\n|---|---|\n| Sepertiga atas | Headline 80-100 px, maksimal 8 kata |\n| Tengah | Visual ({visual}, ilustrasi layanan, dashboard) |\n| Bawah | Subteks 40 px, lalu logo kecil dan `{b['url']}` |\n")
    if f:
        w("Contoh teks:")
        w("```\nHeadline: " + f.get("headline", "") + "\nSubteks: " + f.get("subteks", "") + "\nFooter: " + b["url"] + "\n```\n")
        if f.get("formulas"):
            w("Pilihan headline (rumus):")
            w("```\n" + "\n".join(f'{a}: "{t}"' for a, t in f["formulas"]) + "\n```\n")
    w("---\n")

    # 5 reels
    r = ex["reels"]
    rows = r["rows"]
    w("## 5. Reels / TikTok / Shorts (9:16)\n")
    w("### 5.1 Struktur waktu\n")
    w("| Durasi total | Hook | Masalah | Solusi | Bukti/hasil | CTA |\n|---|---|---|---|---|---|\n| 15 detik | 0:00-0:02 | 0:02-0:05 | 0:05-0:10 | 0:10-0:13 | 0:13-0:15 |\n| 24 detik | 0:00-0:03 | 0:03-0:08 | 0:08-0:15 | 0:15-0:20 | 0:20-0:24 |\n| 30-45 detik | 0:00-0:03 | 0:03-0:12 | 0:12-0:28 | 0:28-0:38 | 0:38-0:45 |\n")
    w("Aturan: hook muncul **sebelum detik ke-3**; CTA tampil **3-4 detik terakhir**; ganti visual atau teks setiap 2-4 detik.\n")
    w(f"### 5.2 Contoh lengkap {r.get('duration', '')} detik: \"{r.get('title', '')}\"\n")
    w("| Waktu | Visual | Teks di layar | Posisi | Animasi teks |\n|---|---|---|---|---|")
    for x in rows:
        w(f"| {x['waktu']} | {x['visual']} | `{x['teks']}` | {x['posisi']} | {x['animasi']} |")
    w("\nSubtitle suara (jika ada narasi): bawah tengah, 48 px, " + off["name"] + " dengan bayangan lembut, maksimal 2 baris.\n")
    hooks = ex.get("hooks") or []
    if hooks:
        w("### 5.3 Bank hook (3 detik pertama)\n")
        w("```\n" + "\n".join(f'{a}: "{t}"' for a, t in hooks) + "\n```\n")
    ctas = ex.get("ctas") or [cta]
    w("### 5.4 Bank CTA\n")
    w("```\n" + "\n".join(f'"{c.replace("->", chr(0x2192))}"' for c in ctas) + "\n```\n")
    w("### 5.5 Pengaturan audio dan caption\n- Musik pelan; narasi atau efek bunyi lebih keras daripada musik.\n- Aktifkan caption otomatis di CapCut untuk narasi, lalu perbaiki ejaan manual.\n- Taruh caption di zona aman bawah (di atas 450 px dari tepi bawah).\n")
    w("---\n")

    # 6 thumb
    th = ex.get("thumbnails", {})
    w("## 6. Thumbnail, OG Image, dan Feature Image\n")
    w(f"| Format | Teks | Layout |\n|---|---|---|\n| YouTube thumbnail 1280x720 | maksimal 4 kata, 110-150 px | teks kiri, {visual} kanan, kontras tinggi, satu kata {acc['name']} |\n| OG image 1200x630 | judul maksimal 8 kata | judul kiri, logo kiri atas, visual kanan bawah, URL kiri bawah, margin 80 px |\n| Feature image artikel 1600x900 | judul 2 baris | judul kiri, visual kanan, tanpa teks tambahan |\n| Pinterest 1000x1500 | judul 6-9 kata, 90 px | judul sepertiga atas, visual tengah, URL bawah |\n| Facebook post 1200x630 | pesan maksimal 12 kata, 80 px | teks kiri, visual kanan, margin 60 px |\n| Threads post 1080x1350 | satu pernyataan maksimal 10 kata, 90 px | teks tengah, satu kata aksen, gaya percakapan |\n")
    if th:
        w("Contoh:")
        w("```\n" + "\n".join(f"{k.capitalize()}: \"{v}\"" for k, v in th.items()) + "\n```\n")
    w("---\n")

    # 7 caption
    w("## 7. Caption dan Hashtag (di luar gambar)\n")
    w("### 7.1 Struktur caption (Instagram)\n")
    w("```\nBaris 1 (hook, ulangi ide gambar): ...\nBaris 2-4 (nilai: 2-3 kalimat pendek): ...\nBaris 5 (CTA): " + cta + "\nBaris 6: 3-5 hashtag relevan\n```\n")
    if ex.get("caption"):
        w("Contoh:")
        w("```\n" + ex["caption"].replace("->", "\u2192") + "\n```\n")
    w("### 7.2 Panjang caption\nReels/TikTok/Shorts: 1-3 baris. Carousel: 4-6 baris. Story: tanpa caption, cukup stiker.\n")
    w("---\n")

    # 8 commands
    w("## 8. Command untuk Membuat Teks (jalankan di ChatGPT atau Claude)\n")
    w("Tempel dulu **Voice Lock** ini sekali per chat:\n")
    avoid = b.get("avoid", "janji berlebihan, angka karangan, jargon tanpa penjelasan")
    if isinstance(avoid, list):
        avoid = ", ".join(a.strip() for a in avoid)
    w("```\nVOICE LOCK - " + b["brand"] + "\nSuara brand: " + b.get("tone", "ramah dan profesional") + ".\nTagline: \"" + b["tagline"] + "\"\nCTA standar: \"" + cta + "\"\nBahasa Indonesia santai-profesional, kalimat pendek.\nHindari: " + avoid + ".\nAturan: hook maksimal 8 kata, teks video maksimal 6 kata per baris, jangan mengarang data atau testimoni.\n```\n")
    cmds = [
        ("carousel", f"Buat isi teks carousel Instagram 7 slide tentang \"{{topik}}\" untuk audiens {{pemilik UMKM / tim operasional / ...}}. Output berupa tabel dengan kolom: Slide | Teks (persis seperti akan ditulis) | Posisi di layar | Ukuran font | Catatan visual. Slide 1 hook maksimal 8 kata, slide 2 masalah, slide 3-6 satu poin per slide (angka, judul 5-7 kata, penjelasan maksimal 2 kalimat), slide 7 CTA. Setelah tabel, tulis caption Instagram 4-6 baris dan 4 hashtag. Jangan mengarang data."),
        ("story", f"Buat urutan {{3 / 4 / 5}} story Instagram atau WhatsApp Status tentang \"{{topik}}\". Output tabel: Story | Tujuan | Teks judul | Teks pendukung | Stiker interaktif yang disarankan | Posisi teks. Ikuti zona aman 250 px atas dan 340 px bawah. Story terakhir berisi CTA \"{cta}\"."),
        ("reels", f"Buat naskah teks di layar untuk video {{15 / 24 / 30}} detik tentang \"{{topik}}\", memakai {{4}} klip visual: {{jelaskan isi tiap klip}}. Output tabel: Waktu (detik) | Visual | Teks di layar (maksimal 6 kata per baris) | Posisi | Animasi teks | Audio/narasi. Hook muncul sebelum detik ke-3, CTA di 3-4 detik terakhir, durasi tampil teks mengikuti rumus 1 detik + 0,3 detik per kata. Sertakan 3 pilihan hook alternatif dan caption 1-3 baris."),
        ("foto", "Buat 5 pilihan headline (maksimal 8 kata) dan satu subteks (maksimal 15 kata) untuk post gambar tunggal Instagram tentang \"{topik}\". Beri tiap pilihan label rumus (masalah-solusi / angka / pertanyaan / janji / kontras) dan sarankan posisi teks pada layout 1080x1350."),
        ("hook", "Beri 10 hook 3 detik pertama untuk video tentang \"{topik}\". Maksimal 8 kata, bervariasi: pertanyaan, kejutan, angka, kontras, tantangan. Tandai 2 yang paling kuat dan jelaskan alasannya dalam satu kalimat."),
        ("thumbnail", f"Beri 6 pilihan teks thumbnail (maksimal 4 kata, huruf kapital) dan teks OG image (maksimal 8 kata) untuk konten \"{{judul}}\". Sebutkan kata mana yang diberi warna {acc['name']} pada tiap pilihan."),
        ("caption", "Buat caption {Instagram / TikTok / LinkedIn / X} untuk konten \"{ringkasan konten}\" dengan struktur: hook, 2-3 kalimat nilai, CTA, hashtag. Sesuaikan panjang dan nada dengan platform. Jangan mengarang klaim."),
        ("cta", f"Beri 8 variasi CTA pendek (maksimal 4 kata untuk tombol, maksimal 12 kata untuk kalimat) untuk tujuan \"{{konsultasi / simpan / bagikan / komentar / klik link}}\" dengan nada {b['brand']} yang hangat, tanpa tekanan."),
        ("lengkap", "Untuk topik \"{topik}\", buat paket teks lengkap: (1) 3 pilihan hook, (2) isi carousel 7 slide, (3) urutan 4 story, (4) naskah teks video 24 detik, (5) caption IG dan hashtag, (6) teks thumbnail/OG. Pakai format tabel dengan kolom posisi, ukuran font, dan waktu. Konsisten dengan Voice Lock."),
    ]
    for name, text in cmds:
        w(f"### {pre}{name}")
        w("```\n" + f"{pre}{name} {text}" + "\n```\n")
    w("---\n")

    # 9 teknis
    w("## 9. Langkah Teknis di Canva dan CapCut\n")
    w("### 9.1 Canva")
    w(f"1. Buat **Brand Kit**: tambahkan warna brand ({', '.join(c['name'] + ' ' + c['hex'] for c in b['colors'])}) dan font {H} + {B}.")
    w("2. Buat desain kustom sesuai ukuran di Bagian 1.4 (1080x1350 untuk carousel, 1080x1920 untuk story).")
    w("3. Tarik **panduan** (penggaris) untuk margin 90 px, atau 250/340 px untuk story.")
    w("4. Unggah gambar dari ChatGPT, taruh teks di layer atas sesuai tabel.")
    w("5. Simpan template (duplikat) agar topik berikutnya cukup mengganti teks.")
    w("6. Unduh PNG (carousel/story) atau MP4 (video).\n")
    w("### 9.2 CapCut")
    w("1. Proyek baru, rasio **9:16**, impor klip Flow berurutan di lini masa.")
    w(f"2. Tambah teks: pilih font mendekati {H} (atau impor font), ukuran tidak kurang dari 48 px, warna sesuai palet.")
    w("3. Atur durasi tiap teks di lini masa mengikuti tabel waktu (Bagian 5.2).")
    w("4. Beri animasi masuk sederhana (pop, fade, geser) 0,3-0,5 detik; hindari animasi berlebihan.")
    w("5. Tambahkan logo sebagai stiker/overlay di akhir video.")
    w("6. Caption otomatis untuk narasi, lalu koreksi manual.")
    w("7. Ekspor 1080p, 30 fps.\n")
    w("### 9.3 Daftar periksa sebelum unggah")
    for x in ["Hook muncul sebelum detik ke-3", "Teks tidak masuk zona UI (atas 250 px, bawah 450 px untuk video)", "Setiap teks tampil sesuai rumus durasi", "Warna hanya dari palet brand", "Ejaan dan angka sudah diperiksa", "CTA dan URL jelas di akhir", f"Logo tidak menutupi {visual}"]:
        w(f"- [ ] {x}")
    return "\n".join(o) + "\n"


REQUIRED_HEADS = ["## 1. Aturan Dasar", "## 2. Carousel", "## 3. Story", "## 4. Post Foto", "## 5. Reels", "## 6. Thumbnail", "## 7. Caption", "## 8. Command", "## 9. Langkah Teknis"]
REQUIRED_CMDS = ["carousel", "story", "reels", "foto", "hook", "thumbnail", "caption", "cta", "lengkap"]


def check(md, prefix=None):
    p = []
    if md.count("```") % 2:
        p.append("Jumlah code fence ``` ganjil.")
    if "[[" in md:
        p.append("Masih ada token [[...]].")
    for h in REQUIRED_HEADS:
        if h not in md:
            p.append(f"Bagian hilang: {h}")
    heads = re.findall(r"^### (/[\w-]+-t-([\w-]+))\s*$", md, re.M)
    names = {n for _, n in heads}
    for c in REQUIRED_CMDS:
        if c not in names:
            p.append(f"Command hilang: -t-{c}")
    for full, n in heads:
        if not re.search(rf"### {re.escape(full)}\n```\n{re.escape(full)} ", md):
            p.append(f"{full}: prompt tidak ada di code block atau tidak diawali nama command.")
        if prefix and not full.startswith("/" + prefix.strip("/-") + "-t-"):
            p.append(f"Prefix tidak konsisten: {full}")
    return p


def main(a):
    if len(a) >= 2 and a[1] == "--example":
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False))
        return 0
    if len(a) >= 3 and a[1] == "--check":
        p = check(Path(a[2]).read_text(encoding="utf-8"), a[3] if len(a) > 3 else None)
        print("OK" if not p else "\n".join("- " + x for x in p))
        return 1 if p else 0
    if len(a) != 3:
        print(__doc__)
        return 2
    b = json.loads(Path(a[1]).read_text(encoding="utf-8"))
    md = render(b)
    p = check(md, b["prefix"])
    warn = lint(b)
    Path(a[2]).parent.mkdir(parents=True, exist_ok=True)
    Path(a[2]).write_text(md, encoding="utf-8")
    print(f"Ditulis: {a[2]}")
    print("Validasi struktur: " + ("OK" if not p else "\n" + "\n".join("- " + x for x in p)))
    print("Lint isi contoh: " + ("OK" if not warn else "\n" + "\n".join("- " + x for x in warn)))
    return 1 if p else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
