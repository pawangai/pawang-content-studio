#!/usr/bin/env python3
"""Render command pack video Google Flow (Markdown) dari brand.json, atau validasi file yang ada.

Pemakaian:
  python build_pack.py brand.json out.md          # render + validasi
  python build_pack.py --check out.md [prefix]    # validasi saja
  python build_pack.py --example                  # cetak contoh brand.json
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from catalog import SECTIONS, SHOT_FORMULA, CAMERA, MODES, RULES  # noqa: E402

EXAMPLE = {
    "brand": "Pawang.dev", "brand_short": "Pawang", "prefix": "pw",
    "tagline": "Digitalmu liar? Serahkan ke Pawang.",
    "cta": "Konsultasi Gratis -> pawang.dev", "url": "pawang.dev",
    "tone": "tenang, paham, jinak; hangat dan ramah",
    "style": "flat modern hangat, ilustrasi 3D-lembut bersih, sudut membulat",
    "logo_desc": "huruf P dengan lingkaran oranye dan percikan bintang",
    "colors": [
        {"role": "dark", "name": "Biru Malam", "hex": "#14213D"},
        {"role": "accent", "name": "Api Dupa", "hex": "#FF8A3D"},
        {"role": "light", "name": "Krem", "hex": "#FFF6E9"},
        {"role": "support", "name": "Hijau Sage", "hex": "#A7C4A0"},
    ],
    "fonts": {"heading": "Plus Jakarta Sans", "body": "Inter"},
    "mascot": {"name": "Si Liar", "desc": "makhluk berbulu biru malam, syal oranye, tongkat kayu, mata besar ekspresif, tubuh bulat imut"},
    "services": [{"name": "Pawang Web"}, {"name": "Pawang Sheet"}, {"name": "Pawang Otomasi"}, {"name": "Pawang Rawat"}],
    "video": {
        "world": "hutan sage lembut dengan cahaya senja hangat",
        "problem": "spreadsheet kusut, kabel liar, dan notifikasi bertubi-tubi",
        "solution": "tampilan rapi dan tenang dengan warna Biru Malam dan Api Dupa",
        "story_theme": "Si Liar menjinakkan data bisnis yang kacau",
        "scenes": [],
    },
}
REQUIRED = ["brand", "prefix", "tagline", "cta", "url", "colors", "logo_desc"]


def color(b, role, fallbacks=()):
    by = {c["role"]: c for c in b["colors"]}
    for r in (role, *fallbacks):
        if r in by:
            return by[r]
    raise SystemExit(f"brand.json: warna role '{role}' tidak ada (wajib: dark, accent, light)")


def tokens(b):
    for k in REQUIRED:
        if not b.get(k):
            raise SystemExit(f"brand.json: field wajib '{k}' kosong atau tidak ada")
    v = b.get("video", {})
    t = {}
    t["BRAND"] = b["brand"]
    t["BRAND_SHORT"] = b.get("brand_short") or b["brand"].split(".")[0]
    pre = b["prefix"].strip("/-")
    t["PI"] = f"/{pre}-"
    t["P"] = f"/{pre}-v-"
    t["TAGLINE"] = b["tagline"]
    t["CTA"] = b["cta"].replace("->", "\u2192")
    t["URL"] = b["url"]
    t["TONE"] = b.get("tone", "ramah dan profesional")
    t["STYLE"] = b.get("style", "flat modern, bersih")
    t["LOGO_DESC"] = b["logo_desc"]
    dark, acc, light = color(b, "dark"), color(b, "accent"), color(b, "light")
    sup = color(b, "support", ("accent",))
    for k, c in [("DARK", dark), ("ACCENT", acc), ("LIGHT", light), ("SUPPORT", sup)]:
        t[k] = f"{c['name']} {c['hex']}"
        t[k + "_NAME"] = c["name"]
    t["WORLD"] = v.get("world", "latar khas brand dengan palet brand")
    t["PROBLEM"] = v.get("problem", "kekacauan yang relevan dengan bisnis")
    t["SOLUTION"] = v.get("solution", f"tampilan rapi dan tenang dengan warna {dark['name']} dan {acc['name']}")
    m = b.get("mascot")
    t["SUBJ"] = m["name"] if m else "{objek utama}"
    t["STORY_THEME"] = v.get("story_theme", "{tema cerita}")
    sv = [s["name"] for s in b.get("services", [])]
    t["SERVICES_LIST"] = " / ".join(sv) if sv else "produk atau layanan utama"
    t["IMG_CMD"] = f"{t['PI']}mascot" if m else f"{t['PI']}feature-notext"
    return t


def fill(text, t):
    def rep(m):
        if m.group(1) not in t:
            raise SystemExit(f"Token tidak dikenal: [[{m.group(1)}]]")
        return t[m.group(1)]
    return re.sub(r"\[\[([A-Z0-9_]+)\]\]", rep, text)


def visual_lock(b, t):
    m = b.get("mascot")
    if m:
        return "\n".join([
            f"CHARACTER LOCK - {m['name']}",
            f"Pertahankan desain {m['name']} persis seperti gambar acuan: {m['desc']}. Jangan ubah warna, proporsi, atau jumlah anggota tubuh.",
            f"Gaya visual: {t['STYLE']}; warna hanya palet brand ({', '.join(c['name'] + ' ' + c['hex'] for c in b['colors'])}).",
            "Gerakan: halus, natural, tidak terlalu cepat. Satu aksi utama per klip.",
            "Tanpa teks tambahan di dalam video, tanpa logo yang berubah bentuk, tanpa orang nyata.",
        ])
    return "\n".join([
        f"VISUAL LOCK - {b['brand']}",
        f"Pertahankan objek utama dan logo ({b['logo_desc']}) persis seperti gambar acuan. Jangan ubah warna atau bentuk.",
        f"Gaya visual: {t['STYLE']}; warna hanya palet brand ({', '.join(c['name'] + ' ' + c['hex'] for c in b['colors'])}).",
        "Gerakan: halus, natural, tidak terlalu cepat. Satu aksi utama per klip.",
        "Tanpa teks tambahan di dalam video, tanpa logo yang berubah bentuk, tanpa orang nyata.",
    ])


def default_scenes(b, t):
    has_m = bool(b.get("mascot"))
    s = t["SUBJ"]
    if not has_m:
        return [
            ("Masalah",
             f"{t['IMG_CMD']} Suasana {t['PROBLEM']}, nuansa kusam dan penuh tekanan, latar {t['WORLD']}, tanpa teks, rasio 9:16.",
             f"Adegan 1. Kamera slow push-in ke {t['PROBLEM']}, elemen bergerak tidak beraturan. Pertahankan desain persis seperti gambar acuan. Audio: efek bunyi sesuai suasana."),
            ("Menemukan solusi",
             f"{t['IMG_CMD']} Cahaya {t['ACCENT_NAME']} lembut menyala di tengah suasana, tanda mulainya solusi, latar {t['WORLD']}, tanpa teks, rasio 9:16.",
             f"Adegan 2. Cahaya {t['ACCENT_NAME']} menyala pelan dan menyebar. Static shot dengan sedikit push-in. Audio: chime lembut."),
            ("Penyelesaian",
             f"{t['IMG_CMD']} Proses {t['PROBLEM']} mulai tertata, tangan menata elemen satu per satu, tanpa teks terbaca, rasio 9:16.",
             f"Adegan 3. Elemen tersusun menjadi {t['SOLUTION']}. Slow push-in. Audio: bunyi klik berurutan lalu \"ting\"."),
            ("Hasil",
             f"{t['IMG_CMD']} {t['SOLUTION']}, latar {t['WORLD']}, rasio 9:16, ruang kosong atas dan bawah untuk teks.",
             f"Adegan 4. Kamera slow pull-out dari {t['SOLUTION']} ke pemandangan penuh, cahaya hangat. Audio: musik akustik pelan."),
        ]
    return [
        ("Masalah",
         f"{t['IMG_CMD']} {s} menghadapi {t['PROBLEM']}, ekspresi panik lucu, latar {t['LIGHT_NAME']} polos, tanpa teks, rasio 9:16.",
         f"Adegan 1. {s} menggeleng panik lalu menghela napas, elemen kekacauan bergerak pelan. Slow push-in. Pertahankan desain persis seperti gambar acuan. Audio: efek bunyi sesuai kekacauan."),
        ("Menemukan solusi",
         f"{t['IMG_CMD']} {s} berdiri di depan cahaya {t['ACCENT_NAME']} lembut yang menyala sebagai tanda solusi, ekspresi penuh harap, latar {t['WORLD']}, rasio 9:16, tanpa teks.",
         f"Adegan 2. Cahaya {t['ACCENT_NAME']} menyala pelan di depan {s}, ia mendongak penuh harap. Static shot dengan sedikit push-in. Audio: chime lembut."),
        ("Penyelesaian",
         f"{t['IMG_CMD']} {s} menyentuh layar besar berisi {t['PROBLEM']} yang mulai tertata, rasio 9:16, tanpa teks terbaca.",
         f"Adegan 3. {s} menyentuh layar, kekacauan tersusun menjadi {t['SOLUTION']}. Slow push-in. Audio: bunyi klik berurutan lalu \"ting\"."),
        ("Hasil",
         f"{t['IMG_CMD']} {s} tenang dan tersenyum di samping {t['SOLUTION']}, latar {t['WORLD']}, rasio 9:16, ruang kosong atas dan bawah untuk teks.",
         f"Adegan 4. {s} tersenyum dan melambai pelan ke kamera, cahaya hangat. Slow pull-out. Audio: musik akustik pelan."),
    ]


def render(b):
    t = tokens(b)
    has_m = bool(b.get("mascot"))
    P = t["P"]
    o, w = [], None
    w = o.append
    w(f"# Command Video {b['brand']} untuk Google Flow\n")
    w(f"Alur: **gambar dari ChatGPT** (command `{t['PI']}...`) -> **animasikan di Google Flow** (command `{P}...` di file ini).")
    w("Semua prompt ada di code block. Ganti isi `{...}` dengan kebutuhan Anda.\n")
    w("---\n")
    w("## Latihan Pertama (5 menit)\n")
    first = f"{P}hello" if has_m else f"{P}logoreveal"
    w(f"1. Di ChatGPT: upload brand board, tempel Brand Lock, lalu buat satu gambar dengan `{t['IMG_CMD']}` (rasio 9:16, tanpa teks).")
    w("2. Unduh gambar sebagai PNG.")
    w(f"3. Di Flow: pilih **Video**, mode **Frames**, seret gambar ke **Add start frame**, lalu tempel prompt `{first}` dari file ini.")
    w("4. Periksa konsistensi desain dan kewajaran gerakan, lalu lanjut ke command lain.\n")
    w("---\n")
    w("## 0. Setup Sekali per Proyek\n")
    w("### 0.1 Memilih mode di Flow\n")
    w("| Kebutuhan | Mode | Gambar yang diunggah |\n|---|---|---|")
    for a, bb, c in MODES:
        w(f"| {a} | {bb} | {c} |")
    w("\nNama menu bisa berbeda di akun Anda (mis. First Frame / Last Frame). Fiturnya sama.\n")
    w(f"### 0.2 {'Character' if has_m else 'Visual'} Lock Video (tempel di prompt Ingredients, atau di awal proyek)\n")
    w("```\n" + visual_lock(b, t) + "\n```\n")
    w("### 0.3 Rumus Prompt Video\n")
    w("```\n" + SHOT_FORMULA + "\n```\n")
    w("### 0.4 Kamus Kamera (pilih satu per klip)\n")
    w("| Istilah | Efek |\n|---|---|")
    for a, c in CAMERA:
        w(f"| {a} | {c} |")
    w("\n### 0.5 Aturan Emas\n")
    for r in RULES:
        w("- " + r)
    w("\n---\n")

    n = 0
    for title, cmds in SECTIONS:
        items = [c for c in cmds if all(b.get(r) for r in c["requires"])]
        if not items:
            continue
        n += 1
        w(f"## {n}. {title}\n")
        for c in items:
            blocks = c["blocks"] if (has_m or c["alt"] is None) else c["alt"]
            w(f"### {P}{c['name']}")
            w(f"{c['desc']} Mode: {fill(c['mode'], t)}.\n")
            for label, text in blocks:
                w(f"**{label}:**")
                w("```\n" + fill(f"{P}{c['name']} {text}", t) + "\n```\n")
        w("---\n")

    n += 1
    theme = t["STORY_THEME"] if not t["STORY_THEME"].startswith("{") else "cerita pendek brand"
    w(f"## {n}. Paket Kerja Siap Pakai: \"{theme}\" (4 klip)\n")
    w("Pasangan prompt: gambar untuk **ChatGPT**, gerakan untuk **Flow**. Rasio 9:16.\n")
    scenes = b.get("video", {}).get("scenes") or None
    if scenes:
        sc = [(s["title"], s["image"], s["motion"]) for s in scenes]
    else:
        sc = default_scenes(b, t)
    for i, (title, img, motion) in enumerate(sc, 1):
        cmd = {1: "reels-hook", 2: "cerita", 3: "penjelasan", 4: "outro"}.get(i, "cerita")
        w(f"### Adegan {i} - {title}")
        w("ChatGPT:")
        w("```\n" + img + "\n```")
        w("Flow:")
        w("```\n" + f"{P}{cmd} {motion}" + "\n```\n")
    w(f"Setelah semua klip selesai: gabungkan di CapCut, tambahkan judul \"{t['TAGLINE']}\" dan CTA \"{t['CTA']}\" sebagai teks pada editor, bukan di dalam video AI.\n")
    w("---\n")
    n += 1
    w(f"## {n}. Template Isi Cepat\n")
    w("```\n" + f"{P}{{command}}\nGambar acuan: {{nama file dari ChatGPT}}\nMode: {{Frames / Ingredients / Text to Video}}\nRasio: {{9:16 / 16:9}}\n"
      f"Subjek: {{{t['SUBJ'].strip('{}')} / objek}}\nAksi tunggal: \nKamera: {{static / slow push-in / pan / orbit}}\nLatar & cahaya: \n"
      "Audio: {efek / musik / dialog \"...\" / tanpa suara}\nRuang kosong untuk teks: {atas / bawah / tidak perlu}\n```\n")
    return "\n".join(o)


def check(md, prefix=None):
    probs = []
    if md.count("```") % 2:
        probs.append("Jumlah code fence ``` ganjil.")
    if "[[" in md:
        probs.append("Masih ada token [[...]].")
    heads = list(re.finditer(r"^### (/[\w-]+-v-[\w-]+)\s*$", md, re.M))
    if not heads:
        probs.append("Tidak ada heading command '### /prefix-v-nama'.")
    for i, h in enumerate(heads):
        end = md.find("\n## ", h.end())
        nxt = heads[i + 1].start() if i + 1 < len(heads) else len(md)
        end = min(x for x in (end if end != -1 else len(md), nxt))
        block = md[h.end():end]
        cmd = h.group(1)
        found = re.findall(r"\*\*[^\n]+:\*\*\n```\n(.*?)\n```", block, re.S)
        if not found:
            probs.append(f"{cmd}: tidak ada prompt di dalam code block.")
        for f in found:
            if not f.lstrip().startswith(cmd):
                probs.append(f"{cmd}: ada prompt yang tidak diawali nama command.")
    if prefix:
        pre = "/" + prefix.strip("/-") + "-v-"
        bad = [h.group(1) for h in heads if not h.group(1).startswith(pre)]
        if bad:
            probs.append("Prefix tidak konsisten: " + ", ".join(bad))
    return probs


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
    Path(a[2]).parent.mkdir(parents=True, exist_ok=True)
    Path(a[2]).write_text(md, encoding="utf-8")
    print(f"Ditulis: {a[2]} ({len(re.findall(r'^### /', md, re.M))} command)")
    if p:
        print("Masalah:\n" + "\n".join("- " + x for x in p))
        return 1
    print("Validasi: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
