#!/usr/bin/env python3
"""Bandingkan logo/karakter acuan dengan hasil AI (perkiraan kasar, bukan pengganti mata).

Pemakaian: python logo_compare.py acuan.png hasil.png [--crop x0,y0,x1,y1]
Memakai pencocokan fitur ORB (OpenCV) + kemiripan warna dominan. Logo datar kecil sering memberi sedikit fitur;
hasil rendah belum tentu berarti berbeda. Selalu bandingkan visual side-by-side.
"""
import argparse
import sys

import numpy as np
from PIL import Image

try:
    import cv2
except Exception:
    cv2 = None


def dominant(img, k=4):
    s = img.convert("RGB")
    s.thumbnail((120, 120))
    q = s.quantize(colors=k, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:k * 3]
    return [(c, tuple(pal[i * 3:i * 3 + 3])) for c, i in sorted(q.getcolors(), reverse=True)]


def color_sim(a, b):
    ha = np.histogram(np.asarray(a.convert("HSV").resize((100, 100)))[..., 0], bins=12, range=(0, 256))[0].astype(float)
    hb = np.histogram(np.asarray(b.convert("HSV").resize((100, 100)))[..., 0], bins=12, range=(0, 256))[0].astype(float)
    ha, hb = ha / ha.sum(), hb / hb.sum()
    return float(np.minimum(ha, hb).sum())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ref")
    ap.add_argument("cand")
    ap.add_argument("--crop")
    a = ap.parse_args()
    ref, cand = Image.open(a.ref).convert("RGB"), Image.open(a.cand).convert("RGB")
    if a.crop:
        x0, y0, x1, y1 = map(int, a.crop.split(","))
        cand = cand.crop((x0, y0, x1, y1))
    print(f"Kemiripan komposisi warna (0-1): {color_sim(ref, cand):.2f}")
    print("Warna dominan acuan :", " ".join("#%02X%02X%02X(%d)" % (*c, n) for n, c in dominant(ref)))
    print("Warna dominan hasil :", " ".join("#%02X%02X%02X(%d)" % (*c, n) for n, c in dominant(cand)))
    if cv2 is None:
        print("OpenCV tidak tersedia; hanya perbandingan warna.")
        return 0
    g1 = cv2.cvtColor(np.asarray(ref), cv2.COLOR_RGB2GRAY)
    g2 = cv2.cvtColor(np.asarray(cand), cv2.COLOR_RGB2GRAY)
    orb = cv2.ORB_create(1500)
    k1, d1 = orb.detectAndCompute(g1, None)
    k2, d2 = orb.detectAndCompute(g2, None)
    if d1 is None or d2 is None or len(k1) < 8 or len(k2) < 8:
        print("Fitur terlalu sedikit untuk pencocokan; bandingkan dengan mata.")
        return 0
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    good = [m for m, n in (p for p in bf.knnMatch(d1, d2, k=2) if len(p) == 2) if m.distance < 0.75 * n.distance]
    inl = 0
    if len(good) >= 4:
        src = np.float32([k1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst = np.float32([k2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        H, mask = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
        inl = int(mask.sum()) if mask is not None else 0
    verdict = "kemungkinan sama" if inl >= 15 else "mirip sebagian, periksa visual" if inl >= 8 else "tidak ditemukan/berbeda (atau logo terlalu sederhana)"
    print(f"Fitur acuan {len(k1)}, hasil {len(k2)}, cocok {len(good)}, inlier {inl} -> {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
