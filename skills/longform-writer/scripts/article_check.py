#!/usr/bin/env python3
"""Periksa artikel panjang (blog, Medium, artikel LinkedIn, newsletter) dalam Markdown dengan front matter.

Pemakaian:
  python article_check.py artikel.md [--keyword "kata kunci"] [--target-words 1200] [--site pawang.dev] [--disclosure]
Front matter (di awal berkas):
  ---
  title: ...
  meta_description: ...
  slug: ...
  keyword: ...
  target_words: 1200
  ---
Aturan angka (judul <= 60 karakter, deskripsi 120-160 karakter, paragraf <= 120 kata, kalimat rata-rata <= 22 kata) adalah patokan keterbacaan, bukan aturan mutlak.
"""
import argparse
import re
import sys
from pathlib import Path

URL_MD = re.compile(r"(?<!\!)\[([^\]]*)\]\(([^)]+)\)")
IMG = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
GENERIC = {"klik di sini", "di sini", "baca selengkapnya", "selengkapnya", "link", "tautan", "klik"}


def front(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    fm = {}
    if m:
        for ln in m.group(1).splitlines():
            if ":" in ln:
                k, v = ln.split(":", 1)
                fm[k.strip()] = v.strip().strip('"')
        return fm, text[m.end():]
    return fm, text


def words(s):
    return len(re.findall(r"\S+", s))


def strip_code(body):
    return re.sub(r"```.*?```", "", body, flags=re.S)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--keyword")
    ap.add_argument("--target-words", type=int)
    ap.add_argument("--site", default="")
    ap.add_argument("--disclosure", action="store_true")
    a = ap.parse_args()
    raw = Path(a.file).read_text(encoding="utf-8")
    fm, body = front(raw)
    body = strip_code(body)
    errs, warns, info = [], [], []
    title = fm.get("title", "")
    if not title:
        errs.append("title kosong di front matter.")
    if re.search(r"\{[^{}]+\}", body + title):
        errs.append("Masih ada isian kurung kurawal {...}.")
    todo = re.findall(r"\[ISI SENDIRI[^\]]*\]", raw)
    kw = (a.keyword or fm.get("keyword", "")).strip()
    plain = re.sub(r"[#>*_`|\-]", " ", re.sub(r"!\[[^\]]*\]\([^)]*\)|\[([^\]]*)\]\([^)]*\)", r"\1", body))
    wc = words(plain)
    tgt = a.target_words or (int(fm["target_words"]) if fm.get("target_words", "").isdigit() else None)
    if wc < 50:
        errs.append("Isi artikel hampir kosong.")
    info.append(f"{wc} kata, waktu baca sekitar {max(1, round(wc / 200))} menit (200 kata/menit).")
    if tgt and abs(wc - tgt) / tgt > 0.15:
        warns.append(f"Panjang {wc} kata menyimpang >15% dari target {tgt}.")
    if len(title) > 60:
        warns.append(f"Judul {len(title)} karakter; di hasil pencarian sering terpotong sekitar 60 (patokan).")
    md = fm.get("meta_description", "")
    if not md:
        warns.append("meta_description kosong.")
    elif not 120 <= len(md) <= 160:
        warns.append(f"meta_description {len(md)} karakter; patokan 120-160.")
    slug = fm.get("slug", "")
    if slug and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        warns.append("slug sebaiknya huruf kecil, angka, dan tanda hubung.")
    heads = [(len(m.group(1)), m.group(2).strip()) for m in re.finditer(r"^(#{1,6})\s+(.+)$", body, re.M)]
    h1 = [h for h in heads if h[0] == 1]
    h2 = [h for h in heads if h[0] == 2]
    if len(h1) > 1:
        warns.append(f"{len(h1)} judul H1; cukup satu (atau nol bila platform memakai judul dari front matter).")
    if wc >= 600 and len(h2) < 3:
        warns.append(f"Hanya {len(h2)} subjudul H2 untuk {wc} kata; pecah menjadi bagian yang mudah dipindai.")
    prev = 1
    for lvl, t in heads:
        if lvl - prev > 1:
            warns.append(f"Lompatan tingkat judul sebelum '{t[:40]}' (H{prev} ke H{lvl}).")
            break
        prev = lvl
    paras = [p for p in re.split(r"\n\s*\n", body) if p.strip() and not p.lstrip().startswith(("#", "|", "-", "*", "1.", ">", "!["))]
    longp = [p for p in paras if words(p) > 120]
    if longp:
        warns.append(f"{len(longp)} paragraf lebih dari 120 kata; pecah agar nyaman dibaca di ponsel.")
    sents = [s for s in re.split(r"(?<=[.!?])\s+", plain) if words(s) > 2]
    if sents:
        avg = sum(words(s) for s in sents) / len(sents)
        info.append(f"Rata-rata {avg:.1f} kata per kalimat.")
        if avg > 22:
            warns.append(f"Kalimat rata-rata {avg:.1f} kata (> 22); sederhanakan.")
    if kw:
        k = kw.lower()
        low = plain.lower()
        n = low.count(k)
        dens = 100 * n * len(k.split()) / max(wc, 1)
        info.append(f"Kata kunci '{kw}': {n} kali ({dens:.1f}%).")
        if k not in title.lower():
            warns.append("Kata kunci tidak ada di judul.")
        if k not in " ".join(low.split()[:100]):
            warns.append("Kata kunci tidak muncul di 100 kata pertama.")
        if h2 and not any(k.split()[0] in h[1].lower() for h in h2):
            warns.append("Tidak ada subjudul H2 yang memuat kata kunci (boleh bila tidak natural).")
        if dens > 2.5:
            warns.append(f"Kepadatan kata kunci {dens:.1f}% terlalu tinggi; tulis natural.")
    imgs = IMG.findall(body)
    noalt = [u for alt, u in imgs if not alt.strip()]
    if noalt:
        warns.append(f"{len(noalt)} gambar tanpa alt text.")
    site = (a.site or fm.get("site", "")).strip()
    links = URL_MD.findall(body)
    ext = [l for l in links if l[1].startswith("http") and (not site or site not in l[1])]
    internal = [l for l in links if l not in ext]
    info.append(f"Tautan: {len(internal)} internal, {len(ext)} eksternal.")
    if wc >= 800 and not internal and (site or not links):
        warns.append("Belum ada tautan internal; hubungkan ke artikel atau halaman layanan yang relevan.")
    for t, u in links:
        if t.strip().lower() in GENERIC:
            warns.append(f"Teks tautan generik '{t}'; gunakan teks yang menjelaskan tujuan.")
            break
    for para in re.split(r"\n\s*\n", body):
        if re.search(r"\d+\s?%|\d+\s?kali lipat", para) and not URL_MD.search(para):
            warns.append(f"Angka/persentase tanpa tautan sumber: '{para.strip()[:70]}...'")
            break
    if re.search(r"\b(terbaik|nomor ?1|dijamin|pasti (?:berhasil|naik)|100 ?%)\b", plain, re.I):
        errs.append("Ada klaim berlebihan (terbaik/nomor 1/dijamin/pasti berhasil/100%).")
    faq = [h for h in heads if re.search(r"faq|pertanyaan", h[1], re.I)]
    if faq:
        info.append("Ada bagian FAQ.")
    if a.disclosure:
        first_last = "\n".join(raw.strip().splitlines()[:12] + raw.strip().splitlines()[-6:])
        if not re.search(r"\bAI\b|kecerdasan buatan", first_last, re.I):
            warns.append("Pengungkapan bantuan AI diminta, tetapi tidak ada catatan di awal/akhir artikel.")
    print(f"Artikel: {title or '(tanpa judul)'}")
    for i in info:
        print("  info:", i)
    print("Galat: " + ("tidak ada" if not errs else "\n" + "\n".join("- " + e for e in errs)))
    print("Peringatan: " + ("tidak ada" if not warns else "\n" + "\n".join("- " + w for w in warns)))
    print(f"Belum diisi (ISI SENDIRI): {len(todo)}" + "".join("\n  - " + t for t in todo))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
