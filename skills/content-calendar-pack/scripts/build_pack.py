#!/usr/bin/env python3
"""Render jadwal konten (hari, jam, topik) dari brand.json, atau validasi file.

Pemakaian:
  python build_pack.py brand.json out.md        # render + validasi + lint
  python build_pack.py --check out.md [prefix]  # validasi file saja
  python build_pack.py --example                # cetak contoh brand.json
"""
import datetime as dt
import json
import re
import sys
from pathlib import Path

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
HARI3 = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]
BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

DEFAULT_PILLARS = [
    {"name": "Edukasi", "goal": "Membuktikan brand memahami masalah audiens", "share": 35, "formats": "carousel, reels tips"},
    {"name": "Solusi", "goal": "Menjelaskan produk/layanan dan cara kerjanya", "share": 25, "formats": "carousel layanan, before-after"},
    {"name": "Bukti", "goal": "Testimoni, studi kasus, FAQ, paket", "share": 20, "formats": "kartu testimoni, FAQ, perbandingan paket"},
    {"name": "Karakter", "goal": "Membangun ingatan brand lewat hiburan/maskot", "share": 15, "formats": "reel maskot, cerita pendek"},
    {"name": "Ajakan", "goal": "Mendatangkan konsultasi/pembelian", "share": 5, "formats": "story promo, ajakan konsultasi"},
]
DEFAULT_RHYTHM = [
    {"hari": "Senin", "format": "Carousel edukasi", "platform": "Instagram (+ LinkedIn)", "jam": "09:00", "pilar": "Edukasi", "minimal": True},
    {"hari": "Selasa", "format": "Reels/Short pendek", "platform": "Instagram Reels, TikTok, YouTube Shorts", "jam": "12:00", "pilar": "Edukasi", "minimal": False},
    {"hari": "Rabu", "format": "Story interaktif (polling/tanya)", "platform": "Instagram Story, WA Status", "jam": "19:30", "pilar": "Edukasi", "minimal": False},
    {"hari": "Kamis", "format": "Carousel layanan / bukti", "platform": "Instagram (+ LinkedIn)", "jam": "09:30", "pilar": "Solusi", "minimal": True},
    {"hari": "Jumat", "format": "Kartu tips cepat", "platform": "Instagram, X", "jam": "12:00", "pilar": "Edukasi", "minimal": False},
    {"hari": "Sabtu", "format": "Reel/cerita karakter", "platform": "Reels, TikTok, Shorts", "jam": "19:00", "pilar": "Karakter", "minimal": True},
    {"hari": "Minggu", "format": "Testimoni / rekap pekan / ajakan", "platform": "Instagram Story, WA Status", "jam": "19:30", "pilar": "Bukti", "minimal": False},
]
DEFAULT_EXTRAS = [
    ["Instagram Story", "2-4 per hari", "pagi 08:00, siang 12:30, malam 19:30", "cuplikan konten, polling, balas komentar"],
    ["WhatsApp Status", "1-2 per hari", "07:30 dan 19:30", "versi story promo/tips"],
    ["LinkedIn", "2 per minggu", "Selasa dan Kamis, 08:00-09:00", "versi profesional carousel/artikel"],
    ["X (Twitter)", "3 per minggu", "Senin, Rabu, Jumat, 12:00", "satu pernyataan kuat atau thread"],
    ["Pinterest", "3-5 pin per minggu", "malam hari, bebas", "pin checklist dan infografis"],
    ["Facebook", "3 per minggu", "siang 11:00-13:00 atau malam 19:00", "versi ramah dari carousel/kartu; link bisa diklik"],
    ["Threads", "3-5 per minggu", "siang 12:00 dan malam 20:00", "pernyataan singkat, pertanyaan, cuplikan proses"],
    ["Quora", "1-2 jawaban per minggu", "bebas (jawaban bertahan lama)", "jawaban bermanfaat atas pertanyaan nyata (skill quora-answer-writer)"],
    ["Blog / Medium / LinkedIn Artikel", "2 per bulan", "Selasa pagi 08:00", "artikel panjang dari tema carousel (skill longform-writer)"],
    ["YouTube panjang (opsional)", "1-2 per bulan", "akhir pekan sore", "video 6-12 menit dari tema artikel (skill longform-writer)"],
]


def example():
    P = lambda *a: dict(zip(["hari", "topik", "command", "pilar", "format", "minimal", "jam", "platform"], a))
    wk = [
        {"tema": "Kenali Data yang Liar", "rows": [
            P("Senin", "4 tanda data bisnismu sudah liar", "/pw-carousel + /pw-t-carousel"),
            P("Selasa", "\"Satu angka, lima file.\" Hook Si Liar terlilit", "/pw-v-reels-hook + /pw-t-reels"),
            P("Rabu", "Seberapa sering salah angka di laporan? (polling)", "/pw-igstory + /pw-t-story"),
            P("Kamis", "Pawang Sheet: dari spreadsheet kusut ke dashboard rapi", "/pw-carousel + /pw-wacatalog"),
            P("Jumat", "Tips: satu sumber data, bukan lima file", "/pw-tips + /pw-t-foto"),
            P("Sabtu", "Si Liar bukan seram, liar itu cuma belum dipahami", "/pw-v-hello + /pw-t-reels"),
            P("Minggu", "Rencana pekan depan + ajakan konsultasi gratis", "/pw-igstory + /pw-t-cta", "Ajakan"),
        ]},
        {"tema": "Website yang Jinak", "rows": [
            P("Senin", "Hal-hal yang membuat pengunjung meninggalkan website usaha", "/pw-carousel + /pw-t-carousel"),
            P("Selasa", "Landing page lama vs landing page jinak", "/pw-v-beforeafter + /pw-t-reels", "Solusi"),
            P("Rabu", "Website kamu sudah cepat dibuka di ponsel? (kotak tanya)", "/pw-igstory + /pw-t-story"),
            P("Kamis", "Pawang Web: cepat, rapi, mudah diurus", "/pw-carousel + /pw-t-carousel"),
            P("Jumat", "Tips: judul halaman dan tombol WhatsApp yang jelas", "/pw-tips"),
            P("Sabtu", "Si Liar menata halaman web yang berantakan", "/pw-v-penjelasan"),
            P("Minggu", "Testimoni klien (isi dengan data nyata)", "/pw-testimoni"),
        ]},
        {"tema": "Otomasi dan Persiapan 11.11", "rows": [
            P("Senin", "Persiapan 11.11 untuk toko online: stok, pesanan, chat", "/pw-carousel + /pw-t-carousel"),
            P("Selasa", "Pahlawan tak terlihat di balik bisnis: sistem yang jalan sendiri", "/pw-v-story + /pw-t-reels"),
            P("Rabu", "11.11: pesanan membludak, siapa yang balas chat? (polling)", "/pw-igstory + /pw-t-story", "Solusi"),
            P("Kamis", "Pawang Otomasi: 3 contoh notifikasi WhatsApp otomatis", "/pw-carousel + /pw-wacatalog"),
            P("Jumat", "Tips: balasan otomatis untuk pertanyaan yang sama", "/pw-tips"),
            P("Sabtu", "Si Liar dikejar notifikasi, lalu dijinakkan", "/pw-v-reels-hook"),
            P("Minggu", "Persiapan 12.12: konsultasi gratis sebelum ramai", "/pw-promo + /pw-igstory", "Ajakan"),
        ]},
        {"tema": "Dijaga dan Paket", "rows": [
            P("Senin", "Pawang Rawat: website sudah jadi, siapa yang menjaga?", "/pw-carousel + /pw-t-carousel", "Solusi"),
            P("Selasa", "Update yang ditunda bisa jadi masalah (tanpa menakut-nakuti)", "/pw-v-penjelasan"),
            P("Rabu", "Kapan terakhir website kamu diperbarui? (polling)", "/pw-igstory"),
            P("Kamis", "Paket Jinak, Piawai, Sakti: mana yang cocok?", "/pw-paket + /pw-t-carousel", "Bukti"),
            P("Jumat", "5 pertanyaan yang sering ditanyakan calon klien", "/pw-faq", "Bukti", "Carousel FAQ"),
            P("Sabtu", "Si Liar Menjinakkan Data (paket 4 adegan)", "/pw-v-cerita"),
            P("Minggu", "Rekap 4 minggu + ajakan Konsultasi Gratis", "/pw-igstory + /pw-t-cta", "Ajakan"),
        ]},
    ]
    ren = {"Solusi": "Jinak", "Bukti": "Tenang", "Karakter": "Si Liar", "Edukasi": "Paham"}
    for w in wk:
        w["rows"] = [{k: (ren.get(v, v) if k == "pilar" else v) for k, v in r.items() if v is not None} for r in w["rows"]]
    return {
        "brand": "Pawang.dev", "prefix": "pw", "cta": "Konsultasi Gratis -> pawang.dev", "url": "pawang.dev",
        "audience": "pemilik UMKM dan tim operasional di Indonesia (WIB)",
        "start": "2026-10-26", "package": "Ringan",
        "pillars": [
            {"name": "Paham", "goal": "Membuktikan Pawang memahami masalah", "share": 35, "formats": "carousel, reels tips"},
            {"name": "Jinak", "goal": "Menjelaskan Pawang Web / Sheet / Otomasi / Rawat", "share": 25, "formats": "carousel layanan, before-after"},
            {"name": "Tenang", "goal": "Testimoni, studi kasus, FAQ, paket", "share": 20, "formats": "kartu testimoni, FAQ, perbandingan paket"},
            {"name": "Si Liar", "goal": "Hiburan dan karakter maskot", "share": 15, "formats": "reel maskot, cerita 4 klip"},
            {"name": "Ajakan", "goal": "Mendatangkan konsultasi", "share": 5, "formats": "story promo, ajakan konsultasi"},
        ],
        "rhythm": [dict(r, pilar={"Edukasi": "Paham", "Solusi": "Jinak", "Karakter": "Si Liar", "Bukti": "Tenang"}[r["pilar"]]) for r in DEFAULT_RHYTHM],
        "weeks_plan": wk,
        "topic_bank": {
            "Paham": ["4 tanda data bisnis sudah liar", "Kenapa laporan manual rawan salah", "Spreadsheet vs dashboard: kapan pindah", "Checklist website usaha yang sehat", "3 hal yang bisa diotomasi tanpa coding"],
            "Jinak": ["Pawang Web: dari ide ke website jadi", "Pawang Sheet: dari kusut ke dashboard", "Pawang Otomasi: notifikasi WhatsApp otomatis", "Pawang Rawat: perawatan bulanan"],
            "Tenang": ["Kartu testimoni (data nyata)", "Studi kasus 5 slide", "FAQ calon klien", "Cara kerja Pawang: paham dulu, baru jinakkan"],
            "Si Liar": ["Si Liar menyapa", "Si Liar terlilit kabel", "Stiker Si Liar", "Si Liar vs notifikasi"],
            "Ajakan": ["Konsultasi Gratis minggu ini", "Ajakan kirim data liar untuk diaudit ringan"],
        },
        "momen": ["Musim belanja (11.11, 12.12, Ramadan, Lebaran, akhir tahun)", "Awal dan akhir bulan (laporan)", "Awal tahun (evaluasi dan target)"],
    }


REQUIRED = ["brand", "prefix", "cta", "url", "start", "weeks_plan"]


def fmt_date(d):
    return f"{HARI3[d.weekday()]} {d.day} {BULAN[d.month - 1]}"


def resolve(b):
    """Gabungkan weeks_plan dengan ritme -> baris lengkap dengan tanggal."""
    start = dt.date.fromisoformat(b["start"])
    rhythm = {r["hari"]: r for r in (b.get("rhythm") or DEFAULT_RHYTHM)}
    weeks = []
    for wi, w in enumerate(b["weeks_plan"]):
        rows = []
        for r in w["rows"]:
            i = HARI.index(r["hari"])
            base = rhythm.get(r["hari"], {})
            d = start + dt.timedelta(days=wi * 7 + i)
            rows.append({
                "date": d, "tanggal": fmt_date(d), "hari": r["hari"],
                "jam": r.get("jam", base.get("jam", "09:00")),
                "platform": r.get("platform", base.get("platform", "Instagram")),
                "format": r.get("format", base.get("format", "")),
                "pilar": r.get("pilar", base.get("pilar", "")),
                "topik": r["topik"], "command": r["command"],
                "minimal": r.get("minimal", base.get("minimal", False)),
            })
        weeks.append({"tema": w["tema"], "rows": rows})
    return start, weeks


def lint(b):
    w = []
    start = dt.date.fromisoformat(b["start"])
    if start.weekday() != 0:
        w.append(f"start {b['start']} bukan hari Senin (hari: {HARI[start.weekday()]}).")
    pre = "/" + b["prefix"].strip("/-") + "-"
    pillars = {p["name"]: p["share"] for p in (b.get("pillars") or DEFAULT_PILLARS)}
    total = sum(pillars.values())
    if total != 100:
        w.append(f"Total porsi pilar {total}%, seharusnya 100%.")
    names = [p for p in pillars]
    _, weeks = resolve(b)
    seen, count, n = {}, {k: 0 for k in names}, 0
    for wi, wk in enumerate(weeks, 1):
        days = [r["hari"] for r in wk["rows"]]
        if sorted(days, key=HARI.index) != HARI and (b.get("package") == "Standar"):
            w.append(f"Minggu {wi}: paket Standar butuh 7 hari terisi.")
        if sum(1 for r in wk["rows"] if r["minimal"]) < 3:
            w.append(f"Minggu {wi}: kurang dari 3 konten bertanda minimal.")
        for r in wk["rows"]:
            n += 1
            if r["pilar"] not in count:
                w.append(f"{r['tanggal']}: pilar '{r['pilar']}' tidak ada di daftar pilar.")
            else:
                count[r["pilar"]] += 1
            if not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", r["jam"]):
                w.append(f"{r['tanggal']}: format jam salah '{r['jam']}'.")
            elif not ("06:00" <= r["jam"] <= "22:30"):
                w.append(f"{r['tanggal']}: jam {r['jam']} di luar 06:00-22:30.")
            for c in re.findall(r"/[\w-]+", r["command"]):
                if not c.startswith(pre):
                    w.append(f"{r['tanggal']}: command {c} tidak berawalan {pre}")
            key = r["topik"].lower()
            if key in seen:
                w.append(f"Topik duplikat: '{r['topik']}' ({seen[key]} dan {r['tanggal']})")
            seen[key] = r["tanggal"]
    for k, v in count.items():
        share = round(100 * v / n) if n else 0
        if abs(share - pillars.get(k, 0)) > 15:
            w.append(f"Porsi pilar {k}: {share}% di kalender vs target {pillars.get(k)}%.")
    return w


def render(b):
    for k in REQUIRED:
        if not b.get(k):
            raise SystemExit(f"brand.json: field wajib '{k}' kosong atau tidak ada")
    pre = "/" + b["prefix"].strip("/-") + "-"
    cta = b["cta"].replace("->", "\u2192")
    pillars = b.get("pillars") or DEFAULT_PILLARS
    rhythm = b.get("rhythm") or DEFAULT_RHYTHM
    extras = b.get("extras") or DEFAULT_EXTRAS
    start, weeks = resolve(b)
    end = weeks[-1]["rows"][-1]["date"] if weeks[-1]["rows"] else start
    aud = b.get("audience", "audiens utama brand di Indonesia (WIB)")
    o = []
    w = o.append
    w(f"# Jadwal Konten {b['brand']}: Hari, Jam, dan Topik\n")
    w("Menjawab: **posting apa, hari apa, jam berapa, topik apa**. "
      f"Siap dipakai mulai **{HARI[start.weekday()]}, {start.day} {BULAN[start.month - 1]} {start.year}** ({len(weeks)} minggu), lalu diulang atau diperbarui dengan command di Bagian 7.\n")
    w(f"Asumsi: audiens {aud}, waktu **WIB**, tim kecil (1-2 orang).\n")
    w("---\n")
    w("## 1. Dua Paket Ritme (pilih satu)\n")
    w("| Paket | Frekuensi | Cocok untuk |\n|---|---|---|\n| **Ringan** | 3 konten utama per minggu (tanda ★ di kalender) + story | Mulai dari nol, tim 1 orang |\n| **Standar** | 5-7 konten utama per minggu + story harian | Sudah rutin, ingin tumbuh lebih cepat |\n")
    w("Aturan terpenting: **konsisten lebih penting daripada banyak.** Lebih baik 3 konten rutin selama 3 bulan daripada 7 konten lalu berhenti dalam 2 minggu.\n")
    w("---\n")
    w("## 2. Pilar Konten (supaya topik tidak habis dan seimbang)\n")
    w("| Pilar | Tujuan | Porsi | Contoh format |\n|---|---|---|---|")
    for p in pillars:
        w(f"| **{p['name']}** | {p['goal']} | {p['share']}% | {p.get('formats', '')} |")
    w(f"\nPrinsip: edukasi dulu, jualan sedikit. Hampir semua konten tetap diakhiri CTA lembut `{cta}`.\n")
    w("---\n")
    w("## 3. Ritme Mingguan dan Jam Posting\n")
    w("### 3.1 Jadwal per hari (jam dalam WIB)\n")
    w("| Hari | Konten utama | Platform | Jam | Pilar | ★ Ringan |\n|---|---|---|---|---|---|")
    for r in rhythm:
        w(f"| {r['hari']} | {r['format']} | {r['platform']} | {r['jam']} | {r['pilar']} | {'★' if r.get('minimal') else ''} |")
    w("\n### 3.2 Platform pendukung (di luar konten utama)\n")
    w("| Platform | Frekuensi | Jam | Isi |\n|---|---|---|---|")
    for e in extras:
        w("| " + " | ".join(e) + " |")
    w("\n### 3.3 Tentang jam posting\n")
    w("Panduan jam posting di internet **tidak konsisten dan kebanyakan berupa artikel blog**, bukan data resmi platform. Pola yang berulang: untuk konten bisnis/B2B, jam kerja pagi (sekitar 09:00-11:00) dan jam istirahat (12:00-15:00) di hari kerja; untuk TikTok/Reels, siang (11:00-13:00) dan malam (19:00-22:00). Karena itu jam di tabel ini adalah **hipotesis awal**, bukan kepastian. Cara memastikannya ada di Bagian 9 (evaluasi 4 minggu dengan Insights akun Anda sendiri).\n")
    w("Tips teknis: unggah beberapa menit sebelum jam target agar sempat diproses, dan gunakan penjadwalan bawaan (Meta Business Suite atau scheduler Instagram/TikTok) supaya jam tetap tepat.\n")
    w("---\n")
    w(f"## 4. Kalender {len(weeks)} Minggu ({fmt_date(start)} - {fmt_date(end)})\n")
    w(f"Kolom **Command** menunjuk ke command yang sudah dibuat: gambar (`{pre}...`), video (`{pre}v-...`), teks (`{pre}t-...`). ★ = minimal untuk paket Ringan.\n")
    for i, wk in enumerate(weeks, 1):
        a, z = wk["rows"][0]["date"], wk["rows"][-1]["date"]
        w(f"### Minggu {i}: {wk['tema']} ({a.day} {BULAN[a.month - 1]} - {z.day} {BULAN[z.month - 1]})\n")
        w("| Tanggal | Jam | Platform | Format | Pilar | Topik / judul | Command | ★ |\n|---|---|---|---|---|---|---|---|")
        for r in wk["rows"]:
            cmds = " + ".join(f"`{c.strip()}`" for c in r["command"].split("+"))
            w(f"| {r['tanggal']} | {r['jam']} | {r['platform']} | {r['format']} | {r['pilar']} | {r['topik']} | {cmds} | {'★' if r['minimal'] else ''} |")
        w("")
    w("Catatan: topik bertema tanggal bergantung pada kesesuaian dengan audiens Anda; ganti jika tidak relevan. Untuk klaim, angka, dan testimoni, **gunakan data nyata**, jangan mengarang.\n")
    w("---\n")
    w("## 5. Gudang Topik\n")
    n = 0
    for k, items in (b.get("topic_bank") or {}).items():
        w(f"### {k}")
        lines = []
        for t in items:
            n += 1
            lines.append(f"{n}. {t}")
        w("```\n" + "\n".join(lines) + "\n```")
    if b.get("momen"):
        w("\nMomen untuk dijadikan tema (verifikasi tanggalnya sendiri):")
        w("```\n" + "\n".join("- " + m for m in b["momen"]) + "\n```")
    w("\n---\n")
    w("## 6. Alur Produksi Mingguan (supaya tidak lembur tiap hari)\n")
    w("Satu hari kerja untuk membuat konten satu minggu (batch).\n")
    w("| Waktu | Kegiatan | Alat | Command |\n|---|---|---|---|")
    w(f"| Jumat sore (30 menit) | Pilih topik pekan depan dari kalender | Kalender Bagian 4 | `{pre}j-mingguan` |")
    w(f"| Senin pagi (1 jam) | Tulis teks: hook, carousel, naskah reel, caption | ChatGPT/Claude | `{pre}t-lengkap` |")
    w(f"| Senin siang (1,5 jam) | Buat gambar semua konten | ChatGPT | `{pre}...` |")
    w(f"| Selasa (1-2 jam) | Buat klip video | Google Flow | `{pre}v-...` |")
    w("| Rabu (1,5 jam) | Susun teks dan layout | Canva, CapCut | Panduan Teks & Layout |")
    w("| Rabu sore (30 menit) | Jadwalkan semua posting sesuai jam | Meta Business Suite / scheduler | Bagian 3 |")
    w("| Setiap hari (10 menit) | Balas komentar dan DM, posting story | Aplikasi | story |\n")
    w("Estimasi total sekitar 6-8 jam per minggu untuk paket Standar; paket Ringan bisa 3-4 jam.\n")
    w("---\n")
    w("## 7. Command Pembuat Jadwal (jalankan di ChatGPT atau Claude)\n")
    w("Tempel Brand Lock dan Voice Lock dulu (dari file sebelumnya).\n")
    pl = ", ".join(f"{p['name']} {p['share']}%" for p in pillars)
    cmds = [
        ("kalender", f"Buat kalender konten {{4 / 8 / 12}} minggu mulai {{tanggal Senin}} untuk {b['brand']}. Paket {{Ringan / Standar}}. Platform: {{Instagram, WhatsApp, TikTok/Reels, LinkedIn, X, Pinterest, blog}}. Gunakan pilar ({pl}). Setiap minggu punya satu tema. Output tabel per minggu: Tanggal | Jam (WIB) | Platform | Format | Pilar | Topik/judul | Command yang dipakai ({pre}, {pre}v-, {pre}t-) | Tanda minimal. Pertimbangkan momen {{11.11, 12.12, Ramadan, akhir tahun}} bila relevan dan tandai topik yang butuh data nyata dari saya. Jangan mengarang angka atau testimoni."),
        ("mingguan", "Dari kalender saya untuk minggu {tanggal}, buatkan paket kerja minggu itu: (1) daftar konten per hari dengan jam posting, (2) prompt pembuat teks yang siap ditempel untuk tiap konten, (3) daftar gambar dan video yang harus dibuat, (4) caption dan hashtag, (5) daftar periksa sebelum jadwalkan. Kalender: {tempel baris minggu itu}."),
        ("topik", "Beri 20 ide topik baru untuk pilar {nama pilar} yang belum ada di daftar berikut: {tempel topik yang sudah dipakai}. Untuk tiap ide: judul (maksimal 8 kata), format terbaik (carousel/reel/story/kartu), dan alasan satu kalimat. Hindari klaim yang tidak bisa dibuktikan."),
        ("daur", "Untuk topik \"{topik}\", buat rencana daur ulang: carousel IG, reel, 3 story, kartu tips, thread X, post LinkedIn, pin Pinterest, status WhatsApp, dan outline artikel blog. Berikan hari dan jam posting tiap versi dalam 10 hari agar tidak menumpuk, serta command yang dipakai."),
        ("batch", "Susun jadwal produksi batch untuk {jumlah} konten minggu depan dengan tim {1 / 2} orang dan waktu {jam per minggu}. Output: jadwal per hari (topik, teks, gambar, video, editing, penjadwalan) dan prioritas jika waktu kurang."),
        ("evaluasi", "Ini data Insights {4 minggu terakhir}: {tempel tabel: tanggal, jam, format, jangkauan, simpan, bagikan, komentar, klik link, pesan masuk}. Analisis: (1) jam dan hari terbaik untuk tiap format, (2) pilar dan format yang paling menghasilkan simpan/bagikan/pesan, (3) yang sebaiknya dikurangi, (4) revisi jadwal minggu berikutnya. Beri alasan berbasis data saya dan tandai bila sampel terlalu kecil untuk disimpulkan."),
        ("momen", "Daftar momen dan hari penting dalam {bulan tahun} yang relevan untuk audiens saya di Indonesia, beserta ide konten untuk tiap momen. Tandai tanggal yang perlu saya verifikasi sendiri."),
    ]
    for name, text in cmds:
        w(f"### {pre}j-{name}")
        w("```\n" + f"{pre}j-{name} {text}" + "\n```\n")
    w("---\n")
    first = weeks[0]["rows"][0]
    w("## 8. Daur Ulang: Satu Topik Menjadi 10 Konten\n")
    w(f"Contoh topik: **{first['topik']}**\n")
    w("| Hari | Konten | Platform |\n|---|---|---|\n| Hari 1, 09:00 | Carousel 7 slide | Instagram |\n| Hari 1, 19:30 | 3 story berisi cuplikan + polling | IG Story, WA |\n| Hari 2, 08:30 | Versi profesional (data, poin) | LinkedIn |\n| Hari 3, 12:00 | Reel 15 detik dengan hook dari topik | Reels, TikTok, Shorts |\n| Hari 4, 12:00 | Kartu tips (satu poin) | Instagram, X |\n| Hari 5 | Pin checklist | Pinterest |\n| Hari 6 | Thread (poin-poin topik) | X |\n| Hari 7 | Reel karakter/hiburan | Reels, TikTok |\n| Hari 8 | Outline artikel blog | Website |\n| Hari 10 | Story \"pertanyaan dari kalian\" | IG Story |\n")
    w("---\n")
    w("## 9. Evaluasi (setiap minggu 15 menit, setiap 4 minggu 1 jam)\n")
    w("### 9.1 Yang dicatat (satu baris per konten)\n")
    w("```\nTanggal | Jam | Platform | Format | Pilar | Topik | Jangkauan | Simpan | Bagikan | Komentar | Klik link | Pesan masuk | Catatan\n```\n")
    w("### 9.2 Ukuran yang diprioritaskan\n")
    w("| Ukuran | Alasan |\n|---|---|\n| Pesan masuk / konsultasi | paling dekat dengan bisnis |\n| Simpan dan bagikan | tanda konten bermanfaat |\n| Klik link ke website | minat lanjut |\n| Jangkauan | hanya pelengkap, mudah naik tapi tidak selalu bernilai |\n")
    w("### 9.3 Cara menguji jam posting\n1. Jalankan jadwal di Bagian 3 selama 4 minggu tanpa mengubah jam.\n2. Lihat Insights Instagram/TikTok: jam dan hari ketika **pengikut Anda sendiri** paling aktif.\n3. Geser satu atau dua slot ke jam itu, lalu bandingkan 4 minggu berikutnya.\n4. Ubah satu hal pada satu waktu agar hasilnya bisa dibaca.\n")
    w("### 9.4 Aturan keputusan sederhana\n- Format yang selalu di bawah rata-rata selama 4 kali berturut-turut: ubah atau kurangi.\n- Pilar yang paling banyak menghasilkan pesan masuk: tambah porsinya 5-10%.\n- Jika tim kelelahan: turun ke paket Ringan, jangan berhenti total.\n")
    w("---\n")
    w("## 10. Template Kalender (salin ke Google Sheets / Notion)\n")
    w("```\nMinggu | Tema minggu | Tanggal | Hari | Jam (WIB) | Platform | Format | Pilar | Topik | Hook | CTA | Command gambar | Command video | Command teks | Status (ide/draf/jadi/terjadwal/terbit) | Link hasil | Catatan\n```\n")
    w("Daftar periksa mingguan:\n- [ ] Topik minggu depan sudah dipilih\n- [ ] Teks, gambar, video selesai\n- [ ] Semua konten dijadwalkan di jam yang benar\n- [ ] Data dan testimoni sudah diverifikasi\n- [ ] Balas komentar dan DM hari ini\n- [ ] Insights minggu lalu dicatat")
    return "\n".join(o) + "\n"


def check(md, prefix=None):
    p = []
    if md.count("```") % 2:
        p.append("Jumlah code fence ``` ganjil.")
    for h in ["## 1. Dua Paket", "## 2. Pilar", "## 3. Ritme", "## 4. Kalender", "## 5. Gudang", "## 6. Alur", "## 7. Command", "## 8. Daur", "## 9. Evaluasi", "## 10. Template"]:
        if h not in md:
            p.append(f"Bagian hilang: {h}")
    weeks = re.split(r"^### Minggu \d+:", md, flags=re.M)[1:]
    if not weeks:
        p.append("Tidak ada tabel minggu.")
    for i, wk in enumerate(weeks, 1):
        rows = re.findall(r"^\| (?:Sen|Sel|Rab|Kam|Jum|Sab|Min) \d+ \w+ \|", wk, re.M)
        if len(rows) < 3:
            p.append(f"Minggu {i}: hanya {len(rows)} baris tanggal.")
    for n in ["kalender", "mingguan", "topik", "daur", "batch", "evaluasi", "momen"]:
        if not re.search(rf"### /[\w-]+-j-{n}\n```\n/[\w-]+-j-{n} ", md):
            p.append(f"Command j-{n} hilang atau tidak di code block.")
    if prefix and f"/{prefix.strip('/-')}-j-" not in md:
        p.append("Prefix command tidak cocok.")
    return p


def main(a):
    if len(a) >= 2 and a[1] == "--example":
        print(json.dumps(example(), indent=2, ensure_ascii=False))
        return 0
    if len(a) >= 3 and a[1] == "--check":
        p = check(Path(a[2]).read_text(encoding="utf-8"), a[3] if len(a) > 3 else None)
        print("OK" if not p else "\n".join("- " + x for x in p))
        return 1 if p else 0
    if len(a) != 3:
        print(__doc__)
        return 2
    b = json.loads(Path(a[1]).read_text(encoding="utf-8"))
    if "content" in b and isinstance(b["content"], dict):
        for k, v in b["content"].items():
            b.setdefault(k, v)
    md = render(b)
    p = check(md, b["prefix"])
    warn = lint(b)
    Path(a[2]).parent.mkdir(parents=True, exist_ok=True)
    Path(a[2]).write_text(md, encoding="utf-8")
    print(f"Ditulis: {a[2]}")
    print("Validasi struktur: " + ("OK" if not p else "\n" + "\n".join("- " + x for x in p)))
    print("Lint kalender: " + ("OK" if not warn else "\n" + "\n".join("- " + x for x in warn)))
    return 1 if p else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
