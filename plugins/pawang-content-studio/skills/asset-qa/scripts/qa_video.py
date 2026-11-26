#!/usr/bin/env python3
"""Periksa video hasil Flow/AI: info teknis, ambil frame, palet per frame, zona aman, lonjakan perubahan, drift warna.

Pemakaian:
  python qa_video.py klip.mp4 --format reels --colors "Biru Malam=#14213D,Api Dupa=#FF8A3D" \
      [--every 1.0] [--out /tmp/qa_klip] [--ocr-frames 6] [--expect-duration 24]
Hasil: folder frame, contact.jpg (lembar kontak untuk dilihat dengan mata), ringkasan di layar.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from qa_image import FORMATS, parse_colors, palette_report, ocr_words, text_report  # noqa: E402


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)],
                       capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("ffprobe gagal: " + r.stderr[:200])
    j = json.loads(r.stdout)
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    if not v:
        raise SystemExit("Tidak ada stream video.")
    num, den = (v.get("avg_frame_rate") or "0/1").split("/")
    fps = float(num) / float(den) if float(den) else 0
    dur = float(j["format"].get("duration") or v.get("duration") or 0)
    return dict(width=v["width"], height=v["height"], fps=round(fps, 2), duration=round(dur, 2), has_audio=bool(a),
                codec=v.get("codec_name"))


def extract(path, out, every, dur, maxn=40):
    out.mkdir(parents=True, exist_ok=True)
    times = []
    t = 0.0
    while t < dur and len(times) < maxn:
        times.append(round(t, 2))
        t += every
    if dur and (not times or times[-1] < dur - 0.3):
        times.append(round(max(dur - 0.2, 0), 2))
    files = []
    for t in times:
        fp = out / f"frame_{t:06.2f}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(path), "-frames:v", "1", str(fp)], check=False)
        if fp.exists():
            files.append((t, fp))
    return files


def hue_hist(img):
    s = img.copy()
    s.thumbnail((120, 120))
    hsv = np.asarray(s.convert("HSV"), dtype=np.float64)
    mask = (hsv[..., 1] > 40) & (hsv[..., 2] > 40)
    h = np.histogram(hsv[..., 0][mask], bins=12, range=(0, 256))[0].astype(np.float64)
    return h / (h.sum() + 1e-9)


def contact(files, out, cols=6, tw=180):
    th = int(tw * Image.open(files[0][1]).size[1] / Image.open(files[0][1]).size[0])
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 16)), "white")
    d = ImageDraw.Draw(sheet)
    for i, (t, fp) in enumerate(files):
        im = Image.open(fp).convert("RGB")
        im.thumbnail((tw, th))
        x, y = (i % cols) * tw, (i // cols) * (th + 16)
        sheet.paste(im, (x, y + 16))
        d.text((x + 3, y + 2), f"{t:.1f}s", fill="black")
    sheet.save(out, quality=85)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", nargs="?")
    ap.add_argument("--format", default="reels")
    ap.add_argument("--colors")
    ap.add_argument("--profile")
    ap.add_argument("--every", type=float, default=1.0)
    ap.add_argument("--out")
    ap.add_argument("--ocr-frames", type=int, default=6)
    ap.add_argument("--expect-duration", type=float)
    ap.add_argument("--formats", action="store_true")
    a = ap.parse_args()
    if a.formats:
        for k, v in FORMATS.items():
            print(f"{k:<10} {v['px']:<10} zona (atas,bawah,kiri,kanan)={v['zone']}  {v['note']}")
        return 0
    if not a.video:
        ap.print_help()
        return 2
    fmt = FORMATS.get(a.format)
    if not fmt:
        raise SystemExit(f"Format tidak dikenal: {a.format} (pilih: {', '.join(FORMATS)})")
    info = probe(a.video)
    out = Path(a.out or f"/tmp/qa_{Path(a.video).stem}")
    findings = []
    print(f"Video: {info['width']}x{info['height']} @ {info['fps']}fps, {info['duration']}s, audio={'ya' if info['has_audio'] else 'TIDAK'}, codec={info['codec']}")
    r = info["width"] / info["height"]
    if abs(r - fmt["ratio"]) / fmt["ratio"] > 0.02:
        findings.append(("RASIO", f"Rasio {info['width']}x{info['height']} berbeda dari target {fmt['px']}."))
    if not info["has_audio"]:
        findings.append(("AUDIO", "Tidak ada audio; pastikan memang disengaja atau tambahkan musik/efek di editor."))
    if a.expect_duration and abs(info["duration"] - a.expect_duration) > 1.5:
        findings.append(("DURASI", f"Durasi {info['duration']}s, target {a.expect_duration}s."))
    files = extract(a.video, out, a.every, info["duration"])
    if not files:
        raise SystemExit("Gagal mengambil frame.")
    contact(files, out / "contact.jpg")
    colors = parse_colors(a.colors) if a.colors else None
    if a.profile:
        pj = json.loads(Path(a.profile).read_text(encoding="utf-8"))
        colors = [(c["name"], c["hex"]) for c in pj["colors"]]
    prev, diffs, base_h = None, [], None
    low_pal = []
    for t, fp in files:
        im = Image.open(fp).convert("RGB")
        g = np.asarray(im.resize((64, 64)).convert("L"), dtype=np.float64)
        if prev is not None:
            diffs.append((t, float(np.abs(g - prev).mean())))
        prev = g
        hh = hue_hist(im)
        if base_h is None:
            base_h = hh
        sim = float(np.minimum(base_h, hh).sum())
        if sim < 0.5 and hh.sum() > 0:
            findings.append(("DRIFT-WARNA", f"Frame {t:.1f}s: komposisi warna berbeda jauh dari frame awal (kemiripan {sim:.2f}); cek apakah karakter/latar berubah."))
        if colors:
            pr = palette_report(im, colors)
            if pr["off_palette_pct"] > 30:
                low_pal.append((t, pr["off_palette_pct"]))
    if low_pal:
        findings.append(("PALET", "Frame dengan warna di luar palet >30%: " + ", ".join(f"{t:.1f}s ({p}%)" for t, p in low_pal[:6])))
    if diffs:
        med = float(np.median([d for _, d in diffs])) or 1e-6
        for t, d in diffs:
            if d > max(3 * med, 25):
                findings.append(("LONJAKAN", f"Perubahan mendadak di {t:.1f}s (selisih {d:.1f} vs median {med:.1f}); mungkin cut, glitch, atau perubahan karakter."))
    # OCR pada sebagian frame (digabung agar tidak berulang)
    step = max(1, len(files) // max(1, a.ocr_frames))
    seen_txt, seen_zone = {}, {}
    for t, fp in files[::step][:a.ocr_frames]:
        im = Image.open(fp).convert("RGB")
        words = ocr_words(im)
        if words:
            tr = text_report(im, words, fmt)
            txt = " ".join(w["text"] for w in words)[:80]
            seen_txt.setdefault(txt, []).append(t)
            for u in tr["unsafe"]:
                seen_zone.setdefault((u["text"], u["zona"]), []).append(t)
    for txt, ts in seen_txt.items():
        findings.append(("TEKS-DI-VIDEO", f"Teks terbaca di {len(ts)} frame ({', '.join(f'{x:.1f}s' for x in ts)}): '{txt}'. Teks di dalam video AI sering berubah bentuk; sebaiknya ditambah di CapCut."))
    for (txt, zona), ts in seen_zone.items():
        findings.append(("ZONA-AMAN", f"'{txt}' di zona {zona} pada {len(ts)} frame ({ts[0]:.1f}s dst.)."))
    print(f"Frame: {len(files)} tersimpan di {out}; lembar kontak: {out / 'contact.jpg'} (lihat dengan mata)")
    if not findings:
        print("Temuan otomatis: tidak ada (tetap periksa visual: karakter, logo, anggota tubuh, gerakan).")
    for k, m in findings:
        print(f"[{k}] {m}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
