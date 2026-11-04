#!/usr/bin/env python3
"""Periksa draf jawaban Quora (atau forum tanya-jawab serupa) sebelum diposting.

Pemakaian:
  python answer_check.py jawaban.md --question "Pertanyaan persis" --brand "Pawang" [--prior jawaban1.md jawaban2.md] [--ai-disclosure]
Pemeriksaan: panjang, kelangsungan jawaban, tautan (jumlah dan posisi), promosi, pengungkapan hubungan dengan brand,
klaim berlebihan, klaim pengalaman yang harus diverifikasi, angka tanpa sumber, format, kemiripan dengan jawaban lama.
Skrip ini membantu; kebijakan Quora yang berlaku saat ini harus dicek terpisah.
"""
import argparse
import difflib
import re
import sys
from pathlib import Path

STOP = set("yang dan di ke dari untuk dengan atau pada ini itu apa bagaimana kenapa mengapa apakah cara bisa dapat ada tidak saya anda kamu kita kami adalah dalam akan sudah juga".split())
URL = re.compile(r"https?://\S+|www\.\S+|\b[\w-]+\.(?:com|id|dev|co\.id|io|app|net|org)/\S+", re.I)
BARE = re.compile(r"\b[\w-]+\.(?:com|id|dev|co\.id|io|app|net|org)\b(?!/)", re.I)
PROMO = re.compile(r"\b(diskon|promo|beli sekarang|hubungi kami|klik (?:link|tautan)|daftar sekarang|penawaran terbatas|gratis konsultasi|konsultasi gratis|order sekarang)\b", re.I)
CLAIM = re.compile(r"\b(terbaik|nomor ?1|no\. ?1|dijamin|pasti (?:berhasil|naik|untung)|100 ?%|tanpa risiko|instan|garansi)\b", re.I)
EXPERIENCE = re.compile(r"(selama \d+ tahun|\d+ (?:klien|pelanggan|proyek|usaha)|kami (?:sudah|telah|pernah)|saya (?:sudah|telah|pernah)|pengalaman (?:saya|kami))", re.I)
DISCLOSE = re.compile(r"(saya|kami)\s+(?:adalah\s+)?(?:pendiri|founder|bekerja|mengelola|membuat|membangun|bagian dari|memiliki)|afiliasi|disclosure|pengungkapan|(?:full )?disclaimer", re.I)
GREET = re.compile(r"^(halo|hai|hi|terima kasih atas pertanyaan|pertanyaan bagus|wah)", re.I)
SHORT = ("bit.ly", "tinyurl", "t.co", "s.id", "cutt.ly", "rebrand.ly")


def words(s):
    return len(re.findall(r"\S+", s))


def toks(s):
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP and len(w) > 2}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("answer")
    ap.add_argument("--question", default="")
    ap.add_argument("--brand", default="")
    ap.add_argument("--prior", nargs="*", default=[])
    ap.add_argument("--ai-disclosure", action="store_true", help="platform/kebijakan meminta pengungkapan bantuan AI")
    a = ap.parse_args()
    text = Path(a.answer).read_text(encoding="utf-8").strip()
    errs, warns, info, todo = [], [], [], []
    if not text:
        print("Galat: jawaban kosong")
        return 1
    if re.search(r"\{[^{}]+\}", text):
        errs.append("Masih ada isian kurung kurawal {...}.")
    todo = re.findall(r"\[ISI SENDIRI[^\]]*\]", text)
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    wc = words(text)
    if wc < 80:
        warns.append(f"Terlalu singkat ({wc} kata); jawaban bermanfaat biasanya memberi alasan atau contoh.")
    elif wc > 700:
        warns.append(f"Panjang ({wc} kata); pangkas atau bagi dengan subjudul ringkas.")
    else:
        info.append(f"Panjang {wc} kata (patokan nyaman 150-450 kata).")
    first = re.split(r"(?<=[.!?])\s", paras[0])[0]
    if GREET.search(first):
        warns.append("Pembuka berupa sapaan/pujian; langsung jawab pertanyaannya di kalimat pertama.")
    if words(first) > 35:
        warns.append(f"Kalimat pertama {words(first)} kata; jawaban inti sebaiknya singkat dan jelas.")
    if a.question:
        q = toks(a.question)
        if q and not (q & toks(" ".join(paras[:1]))):
            warns.append("Paragraf pertama tidak memuat kata kunci pertanyaan; pastikan langsung menjawab.")
    urls = URL.findall(text)
    if len(urls) > 1:
        errs.append(f"{len(urls)} tautan; gunakan paling banyak satu dan hanya bila benar-benar melengkapi jawaban.")
    for i, p in enumerate(paras[:2]):
        if URL.search(p):
            warns.append("Tautan muncul di dua paragraf pertama; beri nilai dulu, tautan belakangan.")
            break
    if any(s in u.lower() for u in urls for s in SHORT):
        errs.append("Ada tautan pendek (bit.ly dsb.); gunakan tautan asli yang transparan.")
    if any("utm_" in u.lower() for u in urls):
        warns.append("Tautan memuat parameter pelacakan (utm); sebaiknya dihapus.")
    bare = sorted(set(m.lower() for m in BARE.findall(text) if m.lower() not in "".join(urls).lower()))
    if bare:
        info.append(f"Domain tertulis sebagai teks ({', '.join(bare)}); aplikasi bisa mengubahnya jadi tautan, hitung sebagai tautan.")
    brand_hits = len(re.findall(re.escape(a.brand), text, re.I)) if a.brand else 0
    if brand_hits > 1:
        warns.append(f"Brand '{a.brand}' disebut {brand_hits} kali; cukup sekali dan hanya bila relevan.")
    if brand_hits and not DISCLOSE.search(text):
        errs.append("Brand disebut tanpa pengungkapan hubungan Anda dengan brand (mis. 'Saya bekerja di/mendirikan ...'). Wajib jujur soal afiliasi.")
    pm = PROMO.findall(text)
    if pm:
        warns.append(f"Kata bernada promosi: {sorted(set(x.lower() for x in pm))}; batasi satu ajakan halus di akhir dan hanya bila relevan.")
    cl = CLAIM.findall(text)
    if cl:
        errs.append(f"Klaim berlebihan: {sorted(set(x.lower() for x in cl))}.")
    ex = EXPERIENCE.findall(text)
    if ex:
        info.append("Klaim pengalaman yang HARUS benar dan bisa Anda pertanggungjawabkan: " + "; ".join(sorted(set(e if isinstance(e, str) else e[0] for e in ex))))
    for s in re.split(r"(?<=[.!?])\s", text):
        if re.search(r"\d+\s?%|kali lipat", s) and not URL.search(s):
            warns.append(f"Angka tanpa sumber: '{s[:70]}...'; beri sumber atau hapus.")
            break
    heads = [p for p in paras if p.startswith("#")]
    if len(heads) > 2:
        warns.append(f"{len(heads)} judul bagian; jawaban Q&A lebih nyaman dengan paling banyak satu-dua subjudul.")
    if len(re.findall(r"[\U0001F300-\U0001FAFF]", text)) > 2:
        warns.append("Emoji lebih dari 2; gaya jawaban sebaiknya tenang.")
    if a.ai_disclosure and not re.search(r"\bAI\b|kecerdasan buatan|dibantu (?:oleh )?(?:alat|AI)", text, re.I):
        warns.append("Kebijakan meminta pengungkapan bantuan AI, tetapi tidak ada catatan pengungkapan di jawaban.")
    for pf in a.prior:
        pt = Path(pf).read_text(encoding="utf-8")
        r = difflib.SequenceMatcher(None, text.lower()[:3000], pt.lower()[:3000]).ratio()
        if r > 0.7:
            warns.append(f"Mirip {r:.0%} dengan jawaban lama ({Path(pf).name}); hindari menempel jawaban yang sama.")
    print(f"Jawaban: {wc} kata, {len(urls)} tautan, {len(paras)} paragraf")
    for i in info:
        print("  info:", i)
    print("Galat: " + ("tidak ada" if not errs else "\n" + "\n".join("- " + e for e in errs)))
    print("Peringatan: " + ("tidak ada" if not warns else "\n" + "\n".join("- " + w for w in warns)))
    print(f"Belum diisi (ISI SENDIRI): {len(todo)}" + ("".join("\n  - " + t for t in todo)))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
