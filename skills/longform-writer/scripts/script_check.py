#!/usr/bin/env python3
"""Periksa skrip video panjang (YouTube) dan buat daftar bab untuk deskripsi.

Pemakaian:
  python script_check.py skrip.md [--wpm 150] [--duration 8:00] [--chapters]
Format skrip:
  ---
  title: ...
  duration: 8:00
  ---
  ## [00:00] Hook
  Narasi yang diucapkan...
  > (visual: B-roll, grafik)        <- baris yang diawali '>' atau '(' tidak dihitung sebagai narasi
  ## [00:25] Bagian 1
Aturan bab YouTube: bab pertama di 00:00, minimal tiga bab, tiap bab minimal 10 detik.
Kecepatan bicara patokan 150 kata/menit (rentang wajar 120-180); sesuaikan dengan pembicara.
"""
import argparse
import re
import sys
from pathlib import Path


def sec(ts):
    p = [int(x) for x in ts.split(":")]
    return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2]


def fmt(s):
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60:02d}:{s % 60:02d}"


def words(s):
    return len(re.findall(r"\S+", s))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--wpm", type=int, default=150)
    ap.add_argument("--duration")
    ap.add_argument("--chapters", action="store_true")
    a = ap.parse_args()
    raw = Path(a.file).read_text(encoding="utf-8")
    m = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", raw, re.S)
    fm, body = {}, raw
    if m:
        for ln in m.group(1).splitlines():
            if ":" in ln:
                k, v = ln.split(":", 1)
                fm[k.strip()] = v.strip()
        body = raw[m.end():]
    dur = a.duration or fm.get("duration")
    total = sec(dur) if dur else None
    errs, warns, info, todo = [], [], [], re.findall(r"\[ISI SENDIRI[^\]]*\]", raw)
    if total is None:
        warns.append("Durasi total belum ditentukan (isi duration: di front matter atau --duration); durasi dan kecepatan bicara bab terakhir tidak dapat diperiksa.")
    parts = re.split(r"^##\s*\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s*(.*)$", body, flags=re.M)
    secs = []
    for i in range(1, len(parts), 3):
        secs.append(dict(t=sec(parts[i]), title=parts[i + 1].strip(), text=parts[i + 2]))
    if not secs:
        print("Galat: tidak ada bagian berformat '## [mm:ss] Judul'.")
        return 1
    if re.search(r"\{[^{}]+\}", raw):
        errs.append("Masih ada isian kurung kurawal {...}.")
    for i, s in enumerate(secs):
        end = secs[i + 1]["t"] if i + 1 < len(secs) else total
        s["dur"] = (end - s["t"]) if end is not None else None
        narr = "\n".join(l for l in s["text"].splitlines() if l.strip() and not l.lstrip().startswith((">", "(", "[")))
        s["words"] = words(narr)
    if secs[0]["t"] != 0:
        errs.append("Bagian pertama harus di 00:00 (syarat bab YouTube).")
    if len(secs) < 3:
        warns.append("Kurang dari 3 bagian; YouTube mensyaratkan minimal tiga bab agar bab tampil.")
    for i in range(1, len(secs)):
        if secs[i]["t"] <= secs[i - 1]["t"]:
            errs.append(f"Waktu tidak berurutan di '{secs[i]['title']}'.")
    for s in secs:
        if s["dur"] is not None and s["dur"] < 10:
            warns.append(f"Bab '{s['title']}' hanya {s['dur']} detik (minimal 10 untuk bab YouTube).")
        if s["dur"]:
            wpm = s["words"] / (s["dur"] / 60)
            if wpm > a.wpm * 1.2:
                warns.append(f"'{s['title']}': {wpm:.0f} kata/menit, terlalu padat; kurangi narasi atau perpanjang bagian.")
            elif wpm < a.wpm * 0.55 and s["words"] > 0:
                warns.append(f"'{s['title']}': {wpm:.0f} kata/menit, sangat longgar; tambah isi atau percepat bagian.")
            elif s["words"] == 0:
                info.append(f"'{s['title']}': tanpa narasi (visual/musik saja).")
    first = secs[0]
    if first["dur"] and first["dur"] > 45:
        warns.append(f"Hook/pembuka {first['dur']} detik; ringkas jadi sekitar 30 detik atau kurang.")
    if not re.search(r"(langganan|subscribe|komentar|tonton|kunjungi|konsultasi|simpan|bagikan)", secs[-1]["text"], re.I):
        warns.append("Bagian terakhir tidak memuat ajakan (CTA).")
    tw = sum(s["words"] for s in secs)
    if total:
        info.append(f"Total {tw} kata untuk {fmt(total)} ({tw / (total / 60):.0f} kata/menit).")
    print("Skrip:", fm.get("title", "(tanpa judul)"))
    for i in info:
        print("  info:", i)
    print("Galat: " + ("tidak ada" if not errs else "\n" + "\n".join("- " + e for e in errs)))
    print("Peringatan: " + ("tidak ada" if not warns else "\n" + "\n".join("- " + w for w in warns)))
    print(f"Belum diisi (ISI SENDIRI): {len(todo)}" + "".join("\n  - " + t for t in todo))
    if a.chapters:
        print("\nBab untuk deskripsi YouTube:")
        for s in secs:
            print(f"{fmt(s['t'])} {s['title']}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
