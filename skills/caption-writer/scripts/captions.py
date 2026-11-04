#!/usr/bin/env python3
"""Render dan periksa caption multi-platform dari captions.json.

Pemakaian:
  python captions.py render captions.json out.md   # render + validasi
  python captions.py check captions.json            # validasi saja
  python captions.py --example                      # contoh captions.json
  python captions.py --limits                       # tabel batas platform

Batas karakter di bawah adalah batas aman yang konservatif; sumber publik berbeda-beda
dan platform bisa mengubahnya (mis. TikTok dilaporkan 2.200 atau 4.000). Cek ulang bila perlu.
"""
import difflib
import json
import re
import sys
from pathlib import Path

# max = batas karakter aman; visible = perkiraan karakter yang terlihat sebelum "selengkapnya"
# tags = (min, max) hashtag yang disarankan; hard_tags = batas keras
LIMITS = {
    "instagram": dict(name="Instagram", max=2200, visible=125, tags=(3, 5), hard_tags=30, link_clickable=False),
    "tiktok": dict(name="TikTok", max=2200, visible=None, tags=(3, 5), hard_tags=None, link_clickable=False),
    "x": dict(name="X (Twitter)", max=280, visible=None, tags=(0, 2), hard_tags=None, link_clickable=True, url_len=23),
    "threads": dict(name="Threads", max=500, visible=None, tags=(0, 1), hard_tags=None, link_clickable=True),
    "linkedin": dict(name="LinkedIn", max=3000, visible=140, tags=(3, 5), hard_tags=None, link_clickable=True),
    "facebook": dict(name="Facebook", max=5000, visible=125, tags=(0, 2), hard_tags=None, link_clickable=True),
    "pinterest": dict(name="Pinterest", max=500, visible=None, tags=(0, 3), hard_tags=None, link_clickable=True, title_max=100),
    "youtube": dict(name="YouTube Shorts", max=5000, visible=None, tags=(3, 5), hard_tags=15, link_clickable=True, title_max=100),
    "whatsapp": dict(name="WhatsApp Status", max=700, visible=None, tags=(0, 0), hard_tags=None, link_clickable=True, approx=True),
}
DEFAULT_AVOID = ["dijamin", "pasti ", "100%", "terbaik", "nomor 1", "no. 1", "garansi", "viral", "tanpa risiko", "instan"]
URL_RE = re.compile(r"https?://\S+|\b[\w-]+\.(?:com|id|dev|co\.id|io|app|net)\b\S*", re.I)
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\U0001F000-\U0001F2FF]")

EXAMPLE = {
    "brand": "Pawang.dev",
    "cta": "Konsultasi Gratis -> pawang.dev",
    "avoid": ["dijamin", "pasti ", "100%"],
    "brief": {"topik": "4 tanda data bisnis sudah liar", "tujuan": "edukasi lalu ajakan konsultasi", "konten": "carousel 7 slide + reel 24 detik"},
    "items": [
        {"platform": "instagram", "format": "carousel",
         "caption": "Cari satu angka, buka lima file? Itu tanda data bisnismu mulai liar.\n\nKabar baiknya, bisa dijinakkan tanpa istilah teknis yang bikin pusing. Geser untuk 4 tandanya, lalu cek mana yang kamu alami.\n\nSimpan postingan ini untuk dicek ulang bulan depan.\n\nMau dibantu? Konsultasi Gratis \u2192 link di bio.",
         "hashtags": ["#digitalbisnis", "#otomasiusaha", "#dashboardbisnis", "#umkmdigital"],
         "alt_text": "Carousel tujuh slide berjudul 4 tanda data bisnis sudah liar, dengan maskot Si Liar terlilit kabel dan kertas.",
         "hook_alternatives": ["Satu angka, lima file. Familiar?", "Datamu liar? Cek 4 tandanya."]},
        {"platform": "tiktok", "format": "reel",
         "caption": "Satu angka, lima file. Familiar? Geser ke video untuk 4 tanda data bisnismu mulai liar. Konsultasi Gratis di link bio.",
         "hashtags": ["#umkmdigital", "#datalaporan", "#tipsbisnis"]},
        {"platform": "linkedin", "format": "carousel",
         "caption": "Berapa file yang Anda buka untuk menjawab satu pertanyaan tentang penjualan bulan lalu?\n\nJika jawabannya lebih dari satu, data bisnis Anda mungkin sudah mulai liar. Empat tandanya ada di carousel ini:\n1. Satu angka punya banyak versi\n2. Laporan dibuat manual setiap minggu\n3. Pesan pelanggan tercecer di banyak tempat\n4. Hanya satu orang yang paham filenya\n\nPawang membantu merapikan data tanpa istilah teknis yang membingungkan.\nKonsultasi Gratis: pawang.dev",
         "hashtags": ["#UMKM", "#TransformasiDigital", "#Otomasi"],
         "first_comment": "Mana dari 4 tanda ini yang paling sering Anda temui?"},
        {"platform": "x", "format": "kartu",
         "caption": "Cari satu angka, buka lima file. Itu tanda data bisnismu mulai liar. Cek 4 tandanya. Konsultasi Gratis: pawang.dev",
         "hashtags": ["#UMKM"]},
    ],
}


def count_len(text, lim):
    if lim.get("url_len"):
        text = URL_RE.sub("x" * lim["url_len"], text)
    return len(text)


def final_text(it):
    cap = it["caption"].rstrip()
    tags = " ".join(it.get("hashtags", []))
    return cap + ("\n\n" + tags if tags else "")


def check(data):
    errors, warns, todo = [], [], []
    avoid = [a.lower() for a in (data.get("avoid") or DEFAULT_AVOID)]
    cta_key = (data.get("cta") or "").replace("->", "\u2192").split("\u2192")[0].strip().lower()
    items = data.get("items", [])
    if not items:
        errors.append("items kosong.")
    for it in items:
        p = it.get("platform", "").lower()
        if p not in LIMITS:
            errors.append(f"Platform tidak dikenal: '{p}' (pilih: {', '.join(LIMITS)})")
            continue
        lim = LIMITS[p]
        tag = f"{lim['name']}"
        txt = final_text(it)
        n = count_len(txt, lim)
        if not it.get("caption", "").strip():
            errors.append(f"{tag}: caption kosong.")
        if "{" in txt or "}" in txt:
            errors.append(f"{tag}: masih ada kurung kurawal.")
        for m in re.findall(r"\[ISI SENDIRI[^\]]*\]", txt):
            todo.append(f"{tag}: {m}")
        if n > lim["max"]:
            errors.append(f"{tag}: {n} karakter, melebihi batas {lim['max']}.")
        title = it.get("title")
        if title and lim.get("title_max") and len(title) > lim["title_max"]:
            errors.append(f"{tag}: judul {len(title)} karakter, melebihi {lim['title_max']}.")
        tags = it.get("hashtags", [])
        bad = [t for t in tags if not re.fullmatch(r"#[\w\u00C0-\u024F]+", t)]
        if bad:
            errors.append(f"{tag}: format hashtag salah: {bad}")
        if lim["hard_tags"] and len(tags) > lim["hard_tags"]:
            errors.append(f"{tag}: {len(tags)} hashtag, melebihi batas {lim['hard_tags']}.")
        lo, hi = lim["tags"]
        if not (lo <= len(tags) <= hi):
            warns.append(f"{tag}: {len(tags)} hashtag; disarankan {lo}-{hi}.")
        first = it["caption"].strip().split("\n")[0]
        if lim["visible"] and len(first) > lim["visible"]:
            warns.append(f"{tag}: baris pertama {len(first)} karakter; hook sebaiknya muat dalam ±{lim['visible']} karakter sebelum 'selengkapnya'.")
        if len(EMOJI_RE.findall(txt)) > 3:
            warns.append(f"{tag}: lebih dari 3 emoji.")
        if txt.count("!") > 2:
            warns.append(f"{tag}: lebih dari 2 tanda seru.")
        if len([w for w in re.findall(r"\b[A-Z]{4,}\b", txt)]) > 2:
            warns.append(f"{tag}: terlalu banyak kata kapital.")
        low = txt.lower() + " "
        hit = [a.strip() for a in avoid if a in low]
        if hit:
            errors.append(f"{tag}: kata klaim berlebihan: {hit}")
        if cta_key and cta_key not in low:
            warns.append(f"{tag}: tidak memuat CTA '{cta_key}'.")
        if not lim["link_clickable"] and URL_RE.search(it["caption"]):
            warns.append(f"{tag}: link di caption tidak bisa diklik; arahkan ke 'link di bio'.")
        if lim.get("approx"):
            warns.append(f"{tag}: batas karakter perkiraan; cek di aplikasi.")
        if it.get("alt_text") and len(it["alt_text"]) > 150:
            warns.append(f"{tag}: alt text {len(it['alt_text'])} karakter; ringkas (<150).")
    caps = [(i, it["caption"]) for i, it in enumerate(items) if it.get("caption")]
    for a in range(len(caps)):
        for b in range(a + 1, len(caps)):
            r = difflib.SequenceMatcher(None, caps[a][1], caps[b][1]).ratio()
            if r > 0.85:
                warns.append(f"Caption {items[caps[a][0]]['platform']} dan {items[caps[b][0]]['platform']} terlalu mirip ({r:.0%}); sesuaikan per platform.")
    return errors, warns, todo


def render(data, out):
    errors, warns, todo = check(data)
    cta = (data.get("cta") or "").replace("->", "\u2192")
    o = []
    w = o.append
    w(f"# Caption {data.get('brand', '')}: {data.get('brief', {}).get('topik', '')}\n")
    br = data.get("brief")
    if br:
        w("```")
        for k, v in br.items():
            w(f"{k}: {v}")
        w("```\n")
    w("Salin caption ke aplikasi, lalu unggah gambar/video. Tambahkan CTA dan link sesuai catatan tiap platform.\n")
    rows = []
    for it in data["items"]:
        p = it["platform"].lower()
        if p not in LIMITS:
            continue
        lim = LIMITS[p]
        txt = final_text(it)
        n = count_len(txt, lim)
        w(f"## {lim['name']}" + (f" ({it['format']})" if it.get("format") else ""))
        if it.get("title"):
            w("**Judul:**\n```\n" + it["title"] + "\n```")
        w("**Caption:**\n```\n" + txt + "\n```")
        if it.get("first_comment"):
            w("**Komentar pertama:**\n```\n" + it["first_comment"] + "\n```")
        if it.get("alt_text"):
            w("**Alt text (aksesibilitas):**\n```\n" + it["alt_text"] + "\n```")
        if it.get("hook_alternatives"):
            w("**Alternatif hook:**\n```\n" + "\n".join(it["hook_alternatives"]) + "\n```")
        note = "link di bio" if not lim["link_clickable"] else "link bisa diklik"
        w(f"_{n}/{lim['max']} karakter, {len(it.get('hashtags', []))} hashtag, {note}._\n")
        rows.append((lim["name"], n, lim["max"], len(it.get("hashtags", [])), "OK" if n <= lim["max"] else "MELEBIHI"))
    w("## Ringkasan\n")
    w("| Platform | Karakter | Batas | Hashtag | Status |\n|---|---|---|---|---|")
    for r in rows:
        w(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |")
    if todo:
        w("\n## Yang Masih Perlu Anda Isi\n")
        for t in todo:
            w(f"- {t}")
    w("\nBatas karakter adalah batas aman yang konservatif; cek ulang di aplikasi karena platform dapat mengubahnya.")
    Path(out).write_text("\n".join(o) + "\n", encoding="utf-8")
    return errors, warns, todo


def report(errors, warns, todo):
    print("Galat: " + ("tidak ada" if not errors else "\n" + "\n".join("- " + e for e in errors)))
    print("Peringatan: " + ("tidak ada" if not warns else "\n" + "\n".join("- " + w for w in warns)))
    print(f"Belum diisi (ISI SENDIRI): {len(todo)}")


def main(a):
    if len(a) >= 2 and a[1] == "--example":
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False))
        return 0
    if len(a) >= 2 and a[1] == "--limits":
        for k, v in LIMITS.items():
            print(f"{v['name']:<16} maks {v['max']:<5} terlihat {str(v['visible']):<5} hashtag {v['tags']}  link {'klik' if v['link_clickable'] else 'bio'}")
        return 0
    if len(a) == 3 and a[1] == "check":
        e, w, t = check(json.loads(Path(a[2]).read_text(encoding="utf-8")))
        report(e, w, t)
        return 1 if e else 0
    if len(a) == 4 and a[1] == "render":
        e, w, t = render(json.loads(Path(a[2]).read_text(encoding="utf-8")), a[3])
        print(f"Ditulis: {a[3]}")
        report(e, w, t)
        return 1 if e else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
