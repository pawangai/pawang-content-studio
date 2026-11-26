#!/usr/bin/env python3
"""Render kumpulan command gambar (Markdown) dari brand.json/profile.json, atau validasi berkas yang ada.

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
from catalog import SECTIONS, FUSIONS, FUSIONS_MASCOT, SIZE_TABLE  # noqa: E402

EXAMPLE = {
    "brand": "Pawang.dev",
    "brand_short": "Pawang",
    "prefix": "pw",
    "tagline": "Digitalmu liar? Serahkan ke Pawang.",
    "cta": "Konsultasi Gratis -> pawang.dev",
    "cta_short": "Konsultasi Gratis",
    "url": "pawang.dev",
    "handle": "pawang.dev",
    "quote": "Karena digital yang jinak adalah digital yang berguna.",
    "tone": "tenang, paham, jinak; hangat, ramah, tidak menakut-nakuti dengan istilah teknis",
    "style": "flat modern hangat, ilustrasi bersih, sudut membulat, banyak ruang kosong, sedikit tekstur lembut",
    "logo_desc": "huruf P dengan lingkaran oranye dan percikan bintang, wordmark \"Pawang\" dengan \".dev\" lebih kecil di bawah kanan",
    "colors": [
        {"role": "dark", "name": "Biru Malam", "hex": "#14213D", "use": "utama, tenang, tepercaya"},
        {"role": "accent", "name": "Api Dupa", "hex": "#FF8A3D", "use": "aksen, CTA, energi"},
        {"role": "light", "name": "Krem", "hex": "#FFF6E9", "use": "latar, ramah"},
        {"role": "support", "name": "Hijau Sage", "hex": "#A7C4A0", "use": "pendukung, segar"},
        {"role": "offwhite", "name": "Putih Tulang", "hex": "#FAFAF7", "use": "teks di latar gelap, bersih"},
    ],
    "fonts": {"heading": "Plus Jakarta Sans", "body": "Inter"},
    "mascot": {
        "name": "Si Liar",
        "desc": "makhluk berbulu biru malam, syal oranye, tongkat kayu, daun hijau sage; ekspresif, imut, tidak menyeramkan",
    },
    "services": [
        {"name": "Pawang Web"}, {"name": "Pawang Sheet"},
        {"name": "Pawang Otomasi"}, {"name": "Pawang Rawat"},
    ],
    "packages": [
        {"name": "Jinak", "color": "hijau", "desc": "paket dasar"},
        {"name": "Piawai", "color": "oranye", "desc": "fitur lebih lengkap"},
        {"name": "Sakti", "color": "ungu", "desc": "custom penuh"},
    ],
    "pattern_elements": "percikan bintang oranye kecil, daun sage, dan siluet P",
}

REQUIRED = ["brand", "prefix", "tagline", "cta", "url", "colors", "fonts", "logo_desc"]


def join_id(items):
    items = list(items)
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " dan " + items[-1]


def color(brand, role, fallbacks=()):
    by_role = {c["role"]: c for c in brand["colors"]}
    for r in (role, *fallbacks):
        if r in by_role:
            return by_role[r]
    raise SystemExit(f"brand.json: warna dengan role '{role}' tidak ada (role wajib: dark, accent, light)")


def build_tokens(b):
    for k in REQUIRED:
        if not b.get(k):
            raise SystemExit(f"brand.json: field wajib '{k}' kosong atau tidak ada")
    t = {}
    t["BRAND"] = b["brand"]
    t["BRAND_SHORT"] = b.get("brand_short") or b["brand"].split(".")[0]
    t["P"] = "/" + b["prefix"].strip("/-") + "-"
    t["TAGLINE"] = b["tagline"]
    t["CTA"] = b["cta"].replace("->", "\u2192")
    t["CTA_SHORT"] = b.get("cta_short") or t["CTA"].split("\u2192")[0].strip()
    t["URL"] = b["url"]
    t["HANDLE"] = b.get("handle") or b["url"]
    t["LOGO_DESC"] = b["logo_desc"]
    t["STYLE"] = b.get("style", "flat modern, bersih, sudut membulat")
    t["TONE"] = b.get("tone", "ramah dan profesional")
    t["FONT_H"] = b["fonts"]["heading"]
    t["FONT_B"] = b["fonts"]["body"]
    t["BRAND_QUOTE"] = b.get("quote") or b["tagline"]
    t["PATTERN_ELEMENTS"] = b.get("pattern_elements", "logo kecil dan elemen dekoratif khas brand")

    dark = color(b, "dark")
    accent = color(b, "accent")
    light = color(b, "light")
    support = color(b, "support", ("accent",))
    offwhite = color(b, "offwhite", ("light",))
    for key, c in [("DARK", dark), ("ACCENT", accent), ("LIGHT", light), ("SUPPORT", support), ("OFFWHITE", offwhite)]:
        t[key] = f"{c['name']} {c['hex']}"
        t[key + "_NAME"] = c["name"]

    services = [s["name"] for s in b.get("services", [])]
    t["SERVICES_LIST"] = ", ".join(services) if services else "layanan utama"
    pk = b.get("packages", [])
    t["PACKAGES_NAMES"] = join_id(p["name"] for p in pk)
    t["PACKAGES_DETAIL"] = join_id(
        f"{p['name']} ({p.get('color', 'warna khas')}, {p.get('desc', 'deskripsi singkat')})" for p in pk
    )
    t["PACKAGE_LABEL_HINT"] = (
        ", label paket \"{" + "/".join(p["name"] for p in pk) + "}\" dengan warna paket ("
        + "/".join(p.get("color", "warna") for p in pk) + ")"
        if pk else ""
    )
    labels = services[:4] + ["Testimoni"] + (["Paket"] if pk else [])
    t["HIGHLIGHT_LABELS"] = join_id(labels[:6]) if services else "Layanan, Testimoni, Tips, Promo, Tentang, Kontak"

    m = b.get("mascot")
    if m:
        n = m["name"]
        t["MASCOT"], t["MASCOT_DESC"] = n, m["desc"]
        t["M_MAIN"] = n
        t["M_MAIN_RIGHT"] = f"{n} berekspresi kuat di kanan"
        t["M_SMALL"] = f"{n} kecil"
        t["M_SLIDE1"] = f", {n} mengintip"
        t["M_CTA"] = f" dengan {n}"
        t["M_GUIDE"] = f" dengan {n} sebagai pemandu"
        t["M_HERO"] = f"{n} sebagai tokoh utama dalam lanskap lembut bernuansa brand"
        t["M_PROUD"] = f"{n} kecil dengan ekspresi bangga"
        t["M_THUMBS"] = f"{n} mengacungkan jempol"
        t["M_SLIDE_NOTE"] = f", {n} hanya di slide judul dan penutup"
        t["VISUAL_CHOICES"] = f"{n} / ilustrasi layanan {t['BRAND_SHORT']}"
    else:
        t["MASCOT"] = t["MASCOT_DESC"] = ""
        t["M_MAIN"] = "ilustrasi konseptual utama"
        t["M_MAIN_RIGHT"] = "satu objek utama besar di kanan"
        t["M_SMALL"] = "ikon logo kecil"
        t["M_SLIDE1"] = t["M_CTA"] = t["M_GUIDE"] = t["M_SLIDE_NOTE"] = ""
        t["M_HERO"] = f"Ilustrasi suasana khas {t['BRAND']} sebagai fokus utama"
        t["M_PROUD"] = "ikon centang kecil " + accent["name"]
        t["M_THUMBS"] = "ikon jempol sederhana"
        t["VISUAL_CHOICES"] = "ilustrasi produk / ikon / data"
    return t


def fill(text, tokens):
    def rep(m):
        key = m.group(1)
        if key not in tokens:
            raise SystemExit(f"Token tidak dikenal di katalog: [[{key}]]")
        return tokens[key]
    return re.sub(r"\[\[([A-Z0-9_]+)\]\]", rep, text)


def brand_lock(b, t):
    colors = "\n".join(f"- {c['name']} {c['hex']} ({c.get('use', c['role'])})" for c in b["colors"])
    lines = [
        f"BRAND LOCK - {b['brand']}",
        "Selalu ikuti brand board yang saya upload. Jangan mengubah logo, maskot, warna, atau font.",
        "",
        f"Brand: {b['brand']}",
        f"Tagline: \"{b['tagline']}\"",
        f"Karakter brand: {t['TONE']}.",
    ]
    if b.get("mascot"):
        lines.append(f"Maskot: \"{b['mascot']['name']}\" - {b['mascot']['desc']}.")
    lines += [
        "",
        "Warna (hanya ini):",
        colors,
        "",
        f"Tipografi: {t['FONT_H']} (judul, tebal), {t['FONT_B']} (isi).",
        f"Logo: {b['logo_desc']}.",
        f"Gaya visual: {t['STYLE']}.",
    ]
    if b.get("services"):
        lines.append("Layanan: " + ", ".join(s["name"] for s in b["services"]) + ".")
    if b.get("packages"):
        lines.append("Paket: " + ", ".join(f"{p['name']} ({p.get('color', '')})" for p in b["packages"]) + ".")
    lines += [
        f"CTA standar: \"{t['CTA']}\"",
        "Bahasa: Indonesia santai-profesional, kalimat pendek.",
        "",
        "Aturan teks pada gambar:",
        "- Tulis teks seminimal mungkin, besar, dan terbaca.",
        "- Eja persis seperti yang saya berikan. Jangan menambah/mengubah kata.",
        "- Jaga margin aman 6% dari tepi.",
        "- Jangan pakai warna di luar palet.",
    ]
    return "\n".join(lines)


def render(b):
    t = build_tokens(b)
    P = t["P"]
    has_m = bool(b.get("mascot"))
    out = []
    w = out.append
    w(f"# Command Konten {b['brand']} untuk ChatGPT\n")
    w("Cara pakai: upload brand board -> tempel **Brand Lock** (Bagian 0) -> jalankan command dari Bagian 1 dst. Ganti isi `{...}` dengan topik Anda.\n")
    w("---\n")
    w("## 0. Setup Sekali di Awal\n")
    w("### 0.1 Brand Lock (tempel di awal chat, atau simpan di Custom Instructions / Project ChatGPT)\n")
    w("```\n" + brand_lock(b, t) + "\n```\n")
    w("### 0.2 Aturan Ukuran\n")
    w("| Platform / Kebutuhan | Rasio | Piksel |\n|---|---|---|")
    for a, r, p in SIZE_TABLE:
        w(f"| {a} | {r} | {p} |")
    w("\nCatatan: ChatGPT membuat gambar dalam rasio terdekat. Jika piksel tidak persis, resize/crop di Canva atau Figma.\n")
    w("### 0.3 Tips Konsistensi\n")
    w("- Selalu upload brand board di chat yang sama sebelum command.")
    w("- Carousel: minta **satu slide per permintaan**, lalu ketik \"lanjut slide berikutnya, gaya identik\".")
    w("- Jika teks salah eja: ketik `Perbaiki teks saja menjadi: \"{teks benar}\". Jangan ubah elemen lain.`")
    w("- Hasil bagus: ketik `Pertahankan gaya ini sebagai referensi untuk semua gambar berikutnya.`")
    w("- Logo resmi sebaiknya tetap diambil dari file aslinya; AI bisa sedikit mengubah bentuk logo.\n")
    w("---\n")

    sec_no = 0
    for title, cmds in SECTIONS:
        rendered = []
        for name, desc, size, req, singkat, detail in cmds:
            if any(not b.get(r) for r in req):
                continue
            rendered.append((name, desc, size, singkat, detail))
        if not rendered:
            continue
        sec_no += 1
        w(f"## {sec_no}. {title}\n")
        for name, desc, size, singkat, detail in rendered:
            w(f"### {P}{name}")
            w(f"{fill(desc, t)} Ukuran: {size}.\n")
            w("**Singkat:**")
            w("```\n" + fill(f"{P}{name} {singkat}", t) + "\n```\n")
            w("**Detail:**")
            w("```\n" + fill(f"{P}{name} {detail}", t) + "\n```\n")
        w("---\n")

    sec_no += 1
    w(f"## {sec_no}. Command Gabungan (Fusion)\n")
    for cmd, desc in FUSIONS + (FUSIONS_MASCOT if has_m else []):
        w(f"**{desc}:**")
        w("```\n" + fill(cmd, t) + "\n```\n")
    w("Cara pakai fusion: ChatGPT membuat ukuran pertama, lalu balas `lanjut ukuran berikutnya, gaya identik`.\n")
    w("---\n")
    sec_no += 1
    w(f"## {sec_no}. Template Isi Cepat (Salin, Isi, Kirim)\n")
    w("```\n" + P + "{command}\nTopik: \nJudul/headline (maks 8 kata): \nSubteks (maks 15 kata): \n"
      "Visual: {" + t["VISUAL_CHOICES"] + "}\nLatar: {" + t["LIGHT_NAME"] + " / " + t["DARK_NAME"] + " / " + t["SUPPORT_NAME"] + "}\n"
      "CTA: " + t["CTA"] + "\nPlatform & rasio: \n```\n")
    return "\n".join(out), b


def check(md, prefix=None):
    """Kembalikan daftar masalah yang ditemukan pada berkas hasil render."""
    problems = []
    if md.count("```") % 2:
        problems.append("Jumlah code fence ``` ganjil (ada yang tidak tertutup).")
    if "[[" in md:
        problems.append("Masih ada token [[...]] yang belum terisi.")
    heads = list(re.finditer(r"^### (/[\w-]+)\s*$", md, re.M))
    if not heads:
        problems.append("Tidak ada heading command '### /prefix-nama'.")
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(md)
        block = md[h.end():end]
        cmd = h.group(1)
        for label in ("Singkat", "Detail"):
            m = re.search(rf"\*\*{label}:\*\*\n```\n(.*?)\n```", block, re.S)
            if not m:
                problems.append(f"{cmd}: bagian {label} tidak berada di dalam code block.")
            elif not m.group(1).lstrip().startswith(cmd):
                problems.append(f"{cmd}: prompt {label} tidak diawali nama command.")
    if prefix:
        bad = [h.group(1) for h in heads if not h.group(1).startswith("/" + prefix.strip("/-") + "-")]
        if bad:
            problems.append("Prefix tidak konsisten: " + ", ".join(bad))
    return problems


def main(argv):
    if len(argv) >= 2 and argv[1] == "--example":
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False))
        return 0
    if len(argv) >= 3 and argv[1] == "--check":
        probs = check(Path(argv[2]).read_text(encoding="utf-8"), argv[3] if len(argv) > 3 else None)
        print("OK" if not probs else "\n".join("- " + p for p in probs))
        return 1 if probs else 0
    if len(argv) != 3:
        print(__doc__)
        return 2
    brand = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    md, b = render(brand)
    probs = check(md, b["prefix"])
    Path(argv[2]).parent.mkdir(parents=True, exist_ok=True)
    Path(argv[2]).write_text(md, encoding="utf-8")
    n = len(re.findall(r"^### /", md, re.M))
    print(f"Ditulis: {argv[2]} ({n} command)")
    if probs:
        print("Masalah:\n" + "\n".join("- " + p for p in probs))
        return 1
    print("Validasi: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
