#!/usr/bin/env python3
"""Buat prompt perbaikan siap tempel dari daftar temuan.

Pemakaian: python fixprompts.py temuan.json out.md
temuan.json: {"tool": "chatgpt|flow", "brand": "Pawang.dev", "issues": [
  {"type": "spelling", "found": "Konsultsi", "expected": "Konsultasi Gratis"},
  {"type": "palette", "where": "latar bawah", "color": "Biru Malam", "hex": "#14213D"},
  {"type": "logo", "detail": "lingkaran oranye hilang"},
  {"type": "character", "name": "Si Liar", "detail": "syal berubah jadi hijau"},
  {"type": "safe_zone", "element": "tombol CTA", "zone": "bawah", "move_to": "sepertiga bawah di atas 340 px"},
  {"type": "small_text", "element": "subteks", "min": "40 px"},
  {"type": "contrast", "element": "judul", "fix": "teks Putih Tulang #FAFAF7 di atas Biru Malam"},
  {"type": "extra_text", "detail": "tulisan acak di pojok kanan atas"},
  {"type": "ratio", "target": "9:16 (1080x1920)"},
  {"type": "anatomy", "detail": "tangan kiri punya enam jari"},
  {"type": "video_text", "detail": "teks pada layar berubah bentuk"},
  {"type": "video_glitch", "at": "3.0s", "detail": "karakter berubah warna"}]}
"""
import json
import sys
from pathlib import Path

KEEP = "Jangan ubah elemen lain: tata letak, warna, logo, karakter, dan gaya harus tetap sama."


def make(i, ctx):
    t = i["type"]
    brand = ctx.get("brand", "brand")
    if t == "spelling":
        return ("Teks salah eja", f"Perbaiki teks saja: ganti \"{i['found']}\" menjadi \"{i['expected']}\". Eja persis seperti ini, huruf besar-kecil sama. {KEEP}")
    if t == "palette":
        return ("Warna di luar palet", f"Ubah warna {i.get('where', 'area yang salah')} menjadi {i['color']} {i['hex']}. Hanya pakai warna palet {brand}. {KEEP}")
    if t == "logo":
        return ("Logo berubah", f"Kembalikan logo {brand} persis seperti gambar acuan yang saya unggah ({i['detail']}). Jangan menggambar ulang atau menambah elemen pada logo. {KEEP}")
    if t == "character":
        return ("Karakter berubah", f"Kembalikan desain {i['name']} persis seperti gambar acuan ({i['detail']}). Pertahankan warna, proporsi, dan jumlah anggota tubuh. {KEEP}")
    if t == "safe_zone":
        return ("Elemen di zona tidak aman", f"Pindahkan {i['element']} dari zona {i['zone']} ke {i.get('move_to', 'area aman')}. Sisakan area kosong sekitar 250 px di atas dan 340 px di bawah (story) atau 450 px (video). {KEEP}")
    if t == "small_text":
        return ("Teks terlalu kecil", f"Perbesar {i['element']} menjadi minimal {i.get('min', '40 px')} agar terbaca di ponsel, tanpa mengubah isi teks. {KEEP}")
    if t == "contrast":
        return ("Kontras rendah", f"Perbaiki kontras {i['element']}: {i['fix']}. Isi teks tidak berubah. {KEEP}")
    if t == "extra_text":
        return ("Teks asing", f"Hapus teks yang tidak diminta ({i['detail']}). Hanya teks yang saya tentukan yang boleh ada. {KEEP}")
    if t == "ratio":
        return ("Rasio salah", f"Buat ulang komposisi yang sama dengan rasio {i['target']}. Pertahankan semua elemen dan sisakan ruang kosong untuk teks.")
    if t == "anatomy":
        return ("Anatomi/anggota tubuh janggal", f"Perbaiki anatomi: {i['detail']}. Karakter harus memiliki jumlah anggota tubuh normal sesuai desain acuan. {KEEP}")
    if t == "video_text":
        return ("Teks pada video berubah bentuk", "Buat ulang klip TANPA teks apa pun di dalam video (tanpa huruf, logo bertulisan, atau papan tanda terbaca). Teks akan ditambahkan di CapCut/Canva. Pertahankan adegan, karakter, dan gerakan yang sama.")
    if t == "video_glitch":
        return ("Glitch pada video", f"Buat ulang klip dengan satu aksi sederhana dan kamera static. Pertahankan desain karakter persis seperti gambar acuan; masalah sebelumnya: {i['detail']} di {i.get('at', 'beberapa detik')}. Gunakan mode Ingredients dengan gambar karakter yang sama.")
    return ("Lainnya", i.get("detail", ""))


def main(a):
    if len(a) != 3:
        print(__doc__)
        return 2
    d = json.loads(Path(a[1]).read_text(encoding="utf-8"))
    tool = d.get("tool", "chatgpt")
    lines = ["# Prompt Perbaikan", "",
             ("Di ChatGPT: unggah gambar yang bermasalah (dan gambar acuan bila ada), lalu tempel prompt di bawah. Satu perbaikan per permintaan memberi hasil paling stabil." if tool == "chatgpt"
              else "Di Flow: unggah ulang gambar acuan sebagai frame awal atau ingredient, lalu tempel prompt di bawah. Ubah satu hal per percobaan."), ""]
    for n, i in enumerate(d["issues"], 1):
        title, prompt = make(i, d)
        lines += [f"## {n}. {title}", "```", prompt, "```", ""]
    if len(d["issues"]) > 1:
        lines += ["## Semua sekaligus (jika perbaikan di atas ringan)", "```",
                  " ".join(make(i, d)[1].replace(KEEP, "").strip() for i in d["issues"] if i["type"] in ("spelling", "palette", "small_text", "contrast", "extra_text")) + " " + KEEP, "```", ""]
    Path(a[2]).write_text("\n".join(lines), encoding="utf-8")
    print(f"Ditulis: {a[2]} ({len(d['issues'])} perbaikan)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
