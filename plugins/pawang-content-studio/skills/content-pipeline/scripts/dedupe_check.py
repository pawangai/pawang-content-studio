#!/usr/bin/env python3
"""Cek apakah topik/hook baru sudah pernah dipakai (anti konten ganda) terhadap log konten.

Pemakaian:
  python dedupe_check.py content-log.csv --topic "4 tanda data bisnis sudah liar" [--hook "..."] [--platform instagram] [--days 120]
  python dedupe_check.py content-log.csv --batch rencana.csv       # periksa banyak (kolom: Topik[,Hook,Platform,Format])
  python dedupe_check.py --template                                  # templat content-log.csv

Log (CSV dari Google Sheets): minimal kolom Topik; dipakai juga Hook, Platform, Format, Status, Tanggal terbit, Link post.
Hasil: BARU / MIRIP / DUPLIKAT beserta baris yang cocok. Ambang: DUPLIKAT >= 0.80, MIRIP >= 0.55 (bisa diubah).
Kemiripan = maksimum dari Jaccard token dan rasio urutan karakter, setelah normalisasi (huruf kecil, tanpa tanda baca dan kata sambung).
"""
import argparse
import csv
import datetime as dt
import difflib
import io
import re
import sys
from pathlib import Path

STOP = set("yang dan di ke dari untuk dengan atau pada ini itu kamu anda kak kita kami mu nya sudah belum akan lebih agar supaya jadi adalah dalam oleh juga cara tips apa kenapa mengapa bagaimana".split())
TEMPLATE = ("ID,Tanggal rencana,Tanggal terbit,Platform,Format,Pilar,Topik,Hook,Slug,Status,Link aset (Drive),Link post,Command,Catatan\n"
            "C-001,2026-10-26,,Instagram,Carousel,Paham,4 tanda data bisnis sudah liar,Data bisnismu sudah liar? Cek 4 tandanya,4-tanda-data-liar,rencana,,,/pw-carousel,\n")
ALIAS = {"topik": ["topik", "topic", "judul"], "hook": ["hook"], "slug": ["slug"], "platform": ["platform", "kanal"], "format": ["format"],
         "status": ["status"], "terbit": ["tanggal terbit", "terbit", "published"], "rencana": ["tanggal rencana", "tanggal"],
         "link": ["link post", "link"]}


def stem(w):
    if len(w) <= 4 or w.isdigit():
        return w
    s = re.sub(r"(?:kan|an|nya)$", "", w)
    if len(s) >= 4:
        w = s
    s = re.sub(r"^(?:me(?:ng|ny|m|n)?|ber|di|pe(?:ng|ny|m|n)?|ter|ke|se)", "", w)
    return s if len(s) >= 4 else w


def norm(s):
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return [stem(w) for w in s.split() if w not in STOP and (len(w) > 1 or w.isdigit())]


def sim(a, b):
    ta, tb = norm(a), norm(b)
    if not ta or not tb:
        return 0.0
    sa, sb = set(ta), set(tb)
    jac = len(sa & sb) / len(sa | sb)
    seq = difflib.SequenceMatcher(None, " ".join(sorted(ta)), " ".join(sorted(tb))).ratio()
    return max(jac, seq)


def cols(headers):
    out = {}
    for h in headers:
        for k, al in ALIAS.items():
            if h.strip().lower() in al and k not in out:
                out[k] = h
    return out


def pdate(s):
    for f in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return dt.datetime.strptime((s or "").strip(), f).date()
        except ValueError:
            pass
    return None


def load(path):
    raw = Path(path).read_text(encoding="utf-8-sig")
    rd = csv.DictReader(io.StringIO(raw))
    c = cols(rd.fieldnames or [])
    if "topik" not in c:
        raise SystemExit("Log harus punya kolom Topik.")
    rows = []
    for r in rd:
        g = lambda k: (r.get(c[k], "") if k in c else "").strip()
        if not g("topik") and not g("hook"):
            continue
        rows.append(dict(topik=g("topik"), hook=g("hook"), slug=g("slug"), platform=g("platform").lower(), format=g("format"), status=g("status"),
                         terbit=pdate(g("terbit")) or pdate(g("rencana")), link=g("link")))
    return rows


def check(rows, topic, hook="", platform="", days=None, dup=0.80, sim_th=0.55):
    today = dt.date.today()
    hits = []
    for r in rows:
        if days and r["terbit"] and (today - r["terbit"]).days > days and r["terbit"] <= today:
            continue
        s_t = sim(topic, r["topik"]) if r["topik"] else 0
        s_slug = sim(topic, r.get("slug", "").replace("-", " ")) if r.get("slug") else 0
        s_t = max(s_t, s_slug)
        s_h = sim(hook, r["hook"]) if hook and r["hook"] else 0
        s = max(s_t, s_h)
        if s >= sim_th:
            same_platform = (not platform) or (not r["platform"]) or platform.lower() == r["platform"]
            hits.append((s, same_platform, r, "hook" if s_h > s_t else "topik"))
    hits.sort(key=lambda x: -x[0])
    if not hits:
        return "BARU", []
    best = hits[0]
    verdict = "DUPLIKAT" if best[0] >= dup else "MIRIP"
    if best[0] >= dup and not best[1]:
        verdict = "MIRIP (platform berbeda: boleh sebagai daur ulang, ubah sudut)"
    return verdict, hits[:3]


def show(verdict, hits, topic):
    print(f"[{verdict}] {topic}")
    for s, sp, r, by in hits:
        t = r["terbit"].isoformat() if r["terbit"] else "tanpa tanggal"
        print(f"    {s:.2f} ({by}) -> '{r['topik'] or r['hook']}' | {r['platform'] or '-'} {r['format'] or ''} | {r['status'] or '-'} | {t}" + (f" | {r['link']}" if r["link"] else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("log", nargs="?")
    ap.add_argument("--topic")
    ap.add_argument("--hook", default="")
    ap.add_argument("--platform", default="")
    ap.add_argument("--days", type=int)
    ap.add_argument("--batch")
    ap.add_argument("--template", action="store_true")
    a = ap.parse_args()
    if a.template:
        print(TEMPLATE, end="")
        return 0
    if not a.log:
        ap.print_help()
        return 2
    rows = load(a.log)
    bad = 0
    if a.batch:
        for r in load(a.batch):
            v, h = check(rows, r["topik"], r["hook"], r["platform"], a.days)
            show(v, h, r["topik"] or r["hook"])
            bad += v.startswith("DUPLIKAT")
    elif a.topic:
        v, h = check(rows, a.topic, a.hook, a.platform, a.days)
        show(v, h, a.topic)
        bad = v.startswith("DUPLIKAT")
    else:
        ap.print_help()
        return 2
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
