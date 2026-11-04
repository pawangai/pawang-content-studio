#!/usr/bin/env python3
"""Periksa gambar hasil AI: rasio/ukuran, kepatuhan palet, teks (OCR), zona aman, ukuran dan kontras teks.

Pemakaian:
  python qa_image.py gambar.png --format story --colors "Biru Malam=#14213D,Api Dupa=#FF8A3D,Krem=#FFF6E9" \
      [--expect "Data bisnismu sudah liar?|Cek 4 tandanya"] [--json hasil.json]
  python qa_image.py gambar.png --format feed --profile profile.json
  python qa_image.py --formats        # daftar format dan zona aman

OCR hanya pelengkap (tesseract bahasa Inggris, font dekoratif sering salah baca). Selalu konfirmasi teks dengan mata.
"""
import argparse
import difflib
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

try:
    import pytesseract
    HAVE_OCR = True
except Exception:  # pragma: no cover
    HAVE_OCR = False

# ratio = w/h target; zona = fraksi (atas, bawah, kiri, kanan) yang sebaiknya bebas teks penting
FORMATS = {
    "story": dict(ratio=9 / 16, px="1080x1920", zone=(0.13, 0.177, 0.055, 0.055), note="IG Story / WA Status"),
    "reels": dict(ratio=9 / 16, px="1080x1920", zone=(0.13, 0.234, 0.055, 0.13), note="Reels/TikTok/Shorts"),
    "feed": dict(ratio=4 / 5, px="1080x1350", zone=(0.067, 0.067, 0.083, 0.083), note="IG post/carousel"),
    "square": dict(ratio=1.0, px="1080x1080", zone=(0.06, 0.06, 0.06, 0.06), note="Kartu 1:1"),
    "og": dict(ratio=1200 / 630, px="1200x630", zone=(0.095, 0.095, 0.067, 0.067), note="OG image"),
    "wide": dict(ratio=16 / 9, px="1600x900", zone=(0.06, 0.06, 0.05, 0.05), note="X/YouTube/feature 16:9"),
    "facebook": dict(ratio=1200 / 630, px="1200x630", zone=(0.095, 0.095, 0.05, 0.05), note="Facebook post"),
    "threads": dict(ratio=4 / 5, px="1080x1350", zone=(0.067, 0.067, 0.083, 0.083), note="Threads post (4:5)"),
    "pinterest": dict(ratio=2 / 3, px="1000x1500", zone=(0.05, 0.05, 0.06, 0.06), note="Pinterest pin"),
}


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def parse_colors(s):
    out = []
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        if "=" in part:
            n, h = part.split("=", 1)
        else:
            n, h = part, part
        out.append((n.strip(), h.strip().upper()))
    return out


def rgb2lab(arr):
    a = arr.astype(np.float64) / 255.0
    a = np.where(a > 0.04045, ((a + 0.055) / 1.055) ** 2.4, a / 12.92)
    m = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]])
    xyz = a @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], axis=-1)


def luminance(rgb):
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    c = np.where(c > 0.03928, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def palette_report(img, colors, de_ok=20.0, de_off=25.0):
    small = img.copy()
    small.thumbnail((200, 200))
    arr = np.asarray(small.convert("RGB"))
    lab = rgb2lab(arr.reshape(-1, 3))
    pal_lab = rgb2lab(np.array([hex2rgb(h) for _, h in colors], dtype=np.float64))
    d = np.linalg.norm(lab[:, None, :] - pal_lab[None, :, :], axis=2)
    nearest, dmin = d.argmin(axis=1), d.min(axis=1)
    chroma = np.hypot(lab[:, 1], lab[:, 2])
    on = dmin <= de_ok
    neutral = (~on) & (chroma < 12)
    off = ~(on | neutral)
    n = len(dmin)
    # klaster dominan
    q = small.convert("RGB").quantize(colors=8, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:24]
    counts = sorted(q.getcolors(), reverse=True)
    clusters = []
    for cnt, idx in counts:
        rgb = tuple(pal[idx * 3:idx * 3 + 3])
        l = rgb2lab(np.array([rgb], dtype=np.float64))[0]
        dd = np.linalg.norm(pal_lab - l, axis=1)
        j = int(dd.argmin())
        pct = 100 * cnt / n
        if pct < 3:
            continue
        clusters.append(dict(hex="#%02X%02X%02X" % rgb, pct=round(pct, 1), nearest=colors[j][0], delta_e=round(float(dd[j]), 1),
                             chroma=round(float(np.hypot(l[1], l[2])), 1)))
    per_color = {colors[i][0]: round(100 * float(((nearest == i) & on).sum()) / n, 1) for i in range(len(colors))}
    flagged = [c for c in clusters if c["delta_e"] > de_off and c["chroma"] >= 12]
    return dict(on_palette_pct=round(100 * on.mean(), 1), neutral_pct=round(100 * neutral.mean(), 1),
                off_palette_pct=round(100 * off.mean(), 1), per_color_pct=per_color, dominant_clusters=clusters,
                off_palette_clusters=flagged)


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


def ocr_words(img):
    if not HAVE_OCR:
        return None
    try:
        langs = pytesseract.get_languages(config="")
        lang = "ind+eng" if "ind" in langs else "eng"
        d = pytesseract.image_to_data(img.convert("RGB"), lang=lang, output_type=pytesseract.Output.DICT, config="--psm 11")
    except Exception:
        return None
    out = []
    for i, t in enumerate(d["text"]):
        t = t.strip()
        try:
            conf = float(d["conf"][i])
        except Exception:
            conf = -1
        if (len(t) >= 2 or t.isdigit()) and conf >= 50:
            out.append(dict(text=t, conf=conf, x=d["left"][i], y=d["top"][i], w=d["width"][i], h=d["height"][i]))
    return out


def text_report(img, words, fmt):
    W, H = img.size
    gray = np.asarray(img.convert("RGB"))
    res = dict(words=len(words), unsafe=[], small=[], low_contrast=[])
    zt, zb, zl, zr = fmt["zone"] if fmt else (0, 0, 0, 0)
    for w in words:
        x0, y0, x1, y1 = w["x"], w["y"], w["x"] + w["w"], w["y"] + w["h"]
        where = []
        if fmt:
            if y0 < zt * H:
                where.append("atas")
            if y1 > H * (1 - zb):
                where.append("bawah")
            if x0 < zl * W:
                where.append("kiri")
            if x1 > W * (1 - zr):
                where.append("kanan")
        if where:
            res["unsafe"].append(dict(text=w["text"], zona="/".join(where)))
        if w["h"] < 0.025 * W and len(w["text"]) >= 3:
            res["small"].append(dict(text=w["text"], tinggi_px=w["h"]))
        crop = gray[max(0, y0):y1, max(0, x0):x1]
        if crop.size:
            lum = luminance(crop.reshape(-1, 3))
            lo, hi = np.percentile(lum, 5), np.percentile(lum, 95)
            ratio = (max(lo, hi) + 0.05) / (min(lo, hi) + 0.05)
            if ratio < 3.0:
                res["low_contrast"].append(dict(text=w["text"], kontras=round(float(ratio), 2)))
    return res


def expect_report(words, expected):
    full = norm(" ".join(w["text"] for w in words))
    toks = full.split()
    out = []
    for e in expected:
        en = norm(e)
        if not en:
            continue
        if en in full:
            out.append(dict(expected=e, status="ditemukan", ocr=e))
            continue
        k = max(1, len(en.split()))
        best, bs = "", 0.0
        for i in range(0, max(1, len(toks) - k + 1)):
            cand = " ".join(toks[i:i + k])
            r = difflib.SequenceMatcher(None, en, cand).ratio()
            if r > bs:
                best, bs = cand, r
        status = "MIRIP-CEK EJAAN" if bs >= 0.8 else "TIDAK DITEMUKAN"
        out.append(dict(expected=e, status=status, ocr=best, mirip=round(bs, 2)))
    return out


def edge_density(img, fmt):
    g = np.asarray(img.convert("L").resize((200, int(200 * img.size[1] / img.size[0]))), dtype=np.float64)
    gx, gy = np.abs(np.diff(g, axis=1))[:-1, :], np.abs(np.diff(g, axis=0))[:, :-1]
    mag = gx + gy
    H, W = mag.shape
    zt, zb, zl, zr = fmt["zone"]
    center = mag[int(zt * H):int(H * (1 - zb)), int(zl * W):int(W * (1 - zr))].mean()
    zones = dict(atas=mag[:int(zt * H)].mean() if zt else 0, bawah=mag[int(H * (1 - zb)):].mean() if zb else 0)
    return {k: round(float(v / (center + 1e-6)), 2) for k, v in zones.items()}, round(float(center), 2)


def run(path, fmt_name=None, colors=None, expect=None):
    img = Image.open(path)
    img.load()
    W, H = img.size
    rep = dict(file=str(path), size=f"{W}x{H}", findings=[])
    f = rep["findings"]
    fmt = FORMATS.get(fmt_name) if fmt_name else None
    if fmt_name and not fmt:
        raise SystemExit(f"Format tidak dikenal: {fmt_name} (pilih: {', '.join(FORMATS)})")
    if fmt:
        r = W / H
        if abs(r - fmt["ratio"]) / fmt["ratio"] > 0.02:
            f.append(("RASIO", f"Rasio {W}x{H} ({r:.3f}) berbeda dari target {fmt['px']} ({fmt['ratio']:.3f}); crop/resize di Canva atau minta rasio yang benar."))
        elif W < int(fmt["px"].split("x")[0]) * 0.9:
            f.append(("RESOLUSI", f"Lebar {W}px lebih kecil dari target {fmt['px']}; hasil bisa buram setelah diunggah."))
    if colors:
        pr = palette_report(img, colors)
        rep["palette"] = pr
        if pr["off_palette_pct"] > 25:
            f.append(("PALET", f"{pr['off_palette_pct']}% piksel berwarna di luar palet brand (netral {pr['neutral_pct']}%)."))
        for c in pr["off_palette_clusters"]:
            f.append(("PALET", f"Warna dominan {c['hex']} ({c['pct']}%) tidak cocok dengan palet; terdekat {c['nearest']} (selisih {c['delta_e']})."))
    words = ocr_words(img)
    if words is None:
        rep["ocr"] = "tidak tersedia"
        if fmt:
            ed, c = edge_density(img, fmt)
            rep["edge_density_vs_center"] = ed
            for k, v in ed.items():
                if v > 0.6:
                    f.append(("ZONA-AMAN", f"Area {k} cukup padat detail ({v}x pusat); periksa apakah ada teks/elemen penting di sana."))
    else:
        rep["ocr_text"] = " ".join(w["text"] for w in words)
        tr = text_report(img, words, fmt)
        rep["text"] = tr
        for u in tr["unsafe"]:
            f.append(("ZONA-AMAN", f"Teks '{u['text']}' berada di zona {u['zona']} yang tertutup UI aplikasi."))
        for s in tr["small"][:5]:
            f.append(("UKURAN-TEKS", f"Teks '{s['text']}' kecil ({s['tinggi_px']}px); target tinggi huruf >= 2,5% lebar gambar."))
        for c in tr["low_contrast"][:5]:
            f.append(("KONTRAS", f"Teks '{c['text']}' kontras rendah ({c['kontras']}:1; minimal 3:1)."))
        if expected_present(expect):
            er = expect_report(words, expect)
            rep["expected"] = er
            for e in er:
                if e["status"] != "ditemukan":
                    f.append(("EJAAN", f"'{e['expected']}' -> OCR membaca '{e['ocr']}' ({e['status']}); periksa dengan mata."))
    return rep


def expected_present(e):
    return bool(e)


def summarize(rep):
    lines = [f"File: {rep['file']}  ({rep['size']})"]
    if "palette" in rep:
        p = rep["palette"]
        lines.append(f"Palet: sesuai {p['on_palette_pct']}% | netral {p['neutral_pct']}% | di luar palet {p['off_palette_pct']}%")
    if "ocr_text" in rep:
        lines.append(f"OCR membaca: {rep['ocr_text'][:200]}")
    if not rep["findings"]:
        lines.append("Temuan otomatis: tidak ada (tetap periksa dengan mata: ejaan, logo, karakter).")
    for k, m in rep["findings"]:
        lines.append(f"[{k}] {m}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image", nargs="?")
    ap.add_argument("--format")
    ap.add_argument("--colors")
    ap.add_argument("--profile")
    ap.add_argument("--expect")
    ap.add_argument("--json")
    ap.add_argument("--formats", action="store_true")
    a = ap.parse_args()
    if a.formats:
        for k, v in FORMATS.items():
            print(f"{k:<10} {v['px']:<10} zona (atas,bawah,kiri,kanan)={v['zone']}  {v['note']}")
        return 0
    if not a.image:
        ap.print_help()
        return 2
    colors = parse_colors(a.colors) if a.colors else None
    if a.profile:
        pj = json.loads(Path(a.profile).read_text(encoding="utf-8"))
        colors = [(c["name"], c["hex"]) for c in pj["colors"]]
    exp = [x for x in (a.expect or "").split("|") if x.strip()]
    rep = run(a.image, a.format, colors, exp)
    print(summarize(rep))
    if a.json:
        Path(a.json).write_text(json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")
    return 1 if rep["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
