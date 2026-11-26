#!/usr/bin/env python3
"""Analisis data Insights: jam, hari, format, pilar, platform. Jujur soal sampel kecil dan faktor yang tercampur.

Pemakaian:
  python analyze.py data.csv --out laporan.md [--json saran.json] [--min-n 4] [--lift 1.25]
  python analyze.py --template        # cetak templat CSV

Kolom (alias Indonesia/Inggris diterima): Tanggal, Jam, Platform, Format, Pilar, Topik, Jangkauan, Simpan, Bagikan,
Komentar, Klik link, Pesan masuk. Angka boleh berformat 1.234 / 1,2rb / 3jt.
Hanya memakai pustaka standar Python.
"""
import argparse
import csv
import datetime as dt
import io
import json
import re
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "mei": 5, "jun": 6, "jul": 7, "agu": 8, "agt": 8, "sep": 9, "okt": 10, "nov": 11, "des": 12,
         "may": 5, "aug": 8, "oct": 10, "dec": 12}
ALIASES = {
    "tanggal": ["tanggal", "date", "tgl"], "jam": ["jam", "hour", "time", "waktu"], "platform": ["platform", "kanal", "channel"],
    "format": ["format", "jenis"], "pilar": ["pilar", "pillar"], "topik": ["topik", "topic", "judul"],
    "jangkauan": ["jangkauan", "reach", "accounts reached", "views", "tayangan"], "simpan": ["simpan", "saves", "save"],
    "bagikan": ["bagikan", "shares", "share"], "komentar": ["komentar", "comments", "comment"],
    "klik": ["klik link", "klik", "link clicks", "clicks", "klik_link"], "pesan": ["pesan masuk", "pesan", "dm", "dms", "messages", "leads"],
}
TEMPLATE = "Tanggal,Jam,Platform,Format,Pilar,Topik,Jangkauan,Simpan,Bagikan,Komentar,Klik link,Pesan masuk\n2026-10-26,09:00,Instagram,Carousel,Paham,4 tanda data liar,1200,35,18,6,9,2\n"


def num(x):
    if x is None:
        return None
    s = str(x).strip().lower().replace(" ", "")
    if s in ("", "-", "na", "n/a", "null"):
        return None
    m = re.fullmatch(r"([\d.,]+)(rb|k|jt|m)?", s)
    if not m:
        return None
    body, suf = m.groups()
    if suf:
        v = float(body.replace(",", "."))
        return v * {"rb": 1e3, "k": 1e3, "jt": 1e6, "m": 1e6}[suf]
    if re.fullmatch(r"\d{1,3}(\.\d{3})+", body):
        return float(body.replace(".", ""))
    if re.fullmatch(r"\d{1,3}(,\d{3})+", body):
        return float(body.replace(",", ""))
    return float(body.replace(",", "."))


def pdate(s):
    s = str(s).strip()
    for f in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return dt.datetime.strptime(s, f).date()
        except ValueError:
            pass
    m = re.search(r"(\d{1,2})\s+([A-Za-z]{3,})\w*\s*(\d{4})?", s)
    if m and m.group(2)[:3].lower() in BULAN:
        y = int(m.group(3)) if m.group(3) else dt.date.today().year
        return dt.date(y, BULAN[m.group(2)[:3].lower()], int(m.group(1)))
    return None


def phour(s):
    m = re.search(r"(\d{1,2})(?::|\.)?(\d{2})?", str(s))
    return int(m.group(1)) if m and 0 <= int(m.group(1)) <= 23 else None


def bucket(h):
    return "pagi 06-10" if 6 <= h < 11 else "siang 11-14" if 11 <= h < 15 else "sore 15-18" if 15 <= h < 19 else "malam 19-23" if 19 <= h < 24 else "lainnya"


def load(path):
    raw = Path(path).read_text(encoding="utf-8-sig")
    try:
        dialect = csv.Sniffer().sniff(raw.split("\n")[0], delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    rd = csv.DictReader(io.StringIO(raw), dialect=dialect)
    cols = {}
    for h in rd.fieldnames:
        key = h.strip().lower()
        for k, al in ALIASES.items():
            if key in al and k not in cols:
                cols[k] = h
    rows, problems = [], []
    for n, r in enumerate(rd, 2):
        g = lambda k: r.get(cols.get(k, ""), "") if cols.get(k) else ""
        d = pdate(g("tanggal"))
        h = phour(g("jam"))
        reach = num(g("jangkauan"))
        if d is None or reach is None or reach <= 0:
            problems.append(f"Baris {n}: tanggal/jangkauan tidak terbaca, dilewati.")
            continue
        row = dict(tanggal=d, hari=HARI[d.weekday()], jam=h, bucket=bucket(h) if h is not None else "tidak diketahui",
                   platform=g("platform").strip() or "?", format=g("format").strip() or "?", pilar=g("pilar").strip() or "?",
                   topik=g("topik").strip(), jangkauan=reach)
        for k in ("simpan", "bagikan", "komentar", "klik", "pesan"):
            v = num(g(k))
            row[k] = v if v is not None else 0.0
            if cols.get(k) is None:
                row[k + "_ada"] = False
        row["save_rate"] = 100 * row["simpan"] / reach
        row["share_rate"] = 100 * row["bagikan"] / reach
        row["komen_rate"] = 100 * row["komentar"] / reach
        row["klik_rate"] = 100 * row["klik"] / reach
        rows.append(row)
    missing = [k for k in ("tanggal", "jangkauan") if k not in cols]
    return rows, cols, problems, missing


def stats(rows, key):
    g = defaultdict(list)
    for r in rows:
        g[r[key]].append(r)
    out = []
    for k, rs in g.items():
        out.append(dict(grup=k, n=len(rs), reach=st.median(x["jangkauan"] for x in rs), save=st.median(x["save_rate"] for x in rs),
                        share=st.median(x["share_rate"] for x in rs), klik=st.median(x["klik_rate"] for x in rs),
                        pesan=sum(x["pesan"] for x in rs) / len(rs), pesan_total=sum(x["pesan"] for x in rs)))
    return sorted(out, key=lambda x: -x["pesan"] * 1000 - x["save"])


def table(title, data, min_n):
    lines = [f"### {title}", "", "| Grup | n | Jangkauan (median) | Simpan % (median) | Bagikan % (median) | Klik % (median) | Pesan/posting | Catatan |", "|---|---|---|---|---|---|---|---|"]
    for d in data:
        note = "sampel kecil" if d["n"] < min_n else ""
        lines.append(f"| {d['grup']} | {d['n']} | {d['reach']:.0f} | {d['save']:.2f} | {d['share']:.2f} | {d['klik']:.2f} | {d['pesan']:.2f} | {note} |")
    return "\n".join(lines) + "\n"


def leader(data, metric, min_n, lift):
    ok = [d for d in data if d["n"] >= min_n]
    if len(ok) < 2:
        return None, "butuh minimal dua grup dengan sampel cukup"
    s = sorted(ok, key=lambda d: -d[metric])
    top, second = s[0], s[1]
    if second[metric] <= 0:
        return (top, "satu-satunya yang menghasilkan") if top[metric] > 0 else (None, "tidak ada hasil")
    if top[metric] / second[metric] >= lift:
        return top, f"{top[metric] / second[metric]:.2f}x grup kedua ({second['grup']})"
    return None, f"selisih kecil ({top['grup']} vs {second['grup']}: {top[metric] / second[metric]:.2f}x < {lift}x)"


def main(a):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv_file", nargs="?")
    ap.add_argument("--out", default="laporan_performa.md")
    ap.add_argument("--json", dest="json_out")
    ap.add_argument("--min-n", type=int, default=4)
    ap.add_argument("--lift", type=float, default=1.25)
    ap.add_argument("--template", action="store_true")
    args = ap.parse_args(a[1:])
    if args.template:
        print(TEMPLATE, end="")
        return 0
    if not args.csv_file:
        print(__doc__)
        return 2
    path = args.csv_file
    opt = lambda f, d=None: {"--out": args.out, "--json": args.json_out}.get(f, d)
    min_n, lift = args.min_n, args.lift
    rows, cols, problems, missing = load(path)
    if missing or len(rows) < 8:
        print("Data belum cukup untuk analisis: " + (f"kolom hilang {missing}; " if missing else "") + f"{len(rows)} baris terbaca (minimal 8; ideal 20+ dari 4 minggu).")
        for p in problems[:5]:
            print(" - " + p)
        return 1
    rows.sort(key=lambda r: r["tanggal"])
    span = (rows[-1]["tanggal"] - rows[0]["tanggal"]).days + 1
    L = [f"# Laporan Performa Konten ({rows[0]['tanggal']} s/d {rows[-1]['tanggal']})", ""]
    L.append(f"Data: {len(rows)} posting selama {span} hari. Median dipakai untuk jangkauan dan rasio agar tidak terpengaruh satu posting viral. Grup dengan n < {min_n} diberi tanda sampel kecil dan tidak dijadikan dasar keputusan.\n")
    L.append("Kolom tersedia: " + ", ".join(sorted(cols)) + (". **Kolom tidak ada:** " + ", ".join(k for k in ("simpan", "bagikan", "komentar", "klik", "pesan") if k not in cols) if any(k not in cols for k in ("simpan", "bagikan", "komentar", "klik", "pesan")) else "") + "\n")
    dims = [("format", "Per format"), ("pilar", "Per pilar"), ("platform", "Per platform"), ("hari", "Per hari"), ("bucket", "Per waktu posting")]
    S = {}
    for k, t in dims:
        S[k] = stats(rows, k)
        L.append(table(t, S[k], min_n))
    # faktor tercampur
    fm = defaultdict(set)
    for r in rows:
        fm[r["bucket"]].add(r["format"])
    confounded = all(len(v) == 1 for v in fm.values()) and len(fm) > 1
    L.append("## Temuan\n")
    findings, sug = [], dict(rhythm_changes=[], pillar_shift=[], reduce=[], insufficient=[], notes=[])
    if confounded:
        n = "Setiap slot waktu hanya dipakai satu format, sehingga **jam dan format tercampur**: perbedaan antar-jam belum bisa dipisahkan dari perbedaan format. Uji jam dengan format yang sama di dua jam berbeda."
        findings.append("- " + n)
        sug["notes"].append(n)
    for k, metric, label in [("format", "pesan", "pesan masuk per posting"), ("format", "save", "tingkat simpan"), ("pilar", "pesan", "pesan masuk per posting"),
                             ("pilar", "save", "tingkat simpan"), ("platform", "reach", "jangkauan"), ("bucket", "reach", "jangkauan")]:
        top, why = leader(S[k], metric, min_n, lift)
        if top:
            findings.append(f"- **{k.capitalize()} terbaik untuk {label}:** {top['grup']} ({why}, n={top['n']}).")
        else:
            findings.append(f"- {k.capitalize()} untuk {label}: belum ada pemenang jelas ({why}).")
    small = [f"{k}:{d['grup']}" for k, _ in dims for d in S[k] if d["n"] < min_n]
    if small:
        sug["insufficient"] = small
        findings.append(f"- Sampel kecil (n < {min_n}), jangan disimpulkan: {', '.join(small[:10])}{'...' if len(small) > 10 else ''}.")
    # tren
    half = len(rows) // 2
    a1, a2 = st.median(r["jangkauan"] for r in rows[:half]), st.median(r["jangkauan"] for r in rows[half:])
    chg = 100 * (a2 - a1) / a1 if a1 else 0
    findings.append(f"- Tren jangkauan (median paruh pertama vs kedua): {a1:.0f} -> {a2:.0f} ({chg:+.0f}%).")
    med = st.median(r["jangkauan"] for r in rows)
    outl = [r for r in rows if r["jangkauan"] > 3 * med]
    if outl:
        findings.append("- Posting jauh di atas normal (> 3x median): " + "; ".join(f"{r['tanggal']} {r['format']} '{r['topik'][:40]}' ({r['jangkauan']:.0f})" for r in outl[:3]) + ". Pelajari penyebabnya, jangan jadikan patokan.")
    top5 = sorted(rows, key=lambda r: (-r["pesan"], -r["save_rate"]))[:3]
    findings.append("- Posting paling menghasilkan pesan/simpan: " + "; ".join(f"{r['tanggal']} {r['format']} '{r['topik'][:40]}' (pesan {r['pesan']:.0f}, simpan {r['save_rate']:.2f}%)" for r in top5) + ".")
    L += findings + [""]
    # saran jadwal
    L.append("## Saran Revisi Kalender\n")
    reco = []
    lt, _ = leader(S["bucket"], "reach", min_n, lift)
    if lt and not confounded:
        reco.append(f"Pindahkan konten utama ke waktu **{lt['grup']}** (jangkauan median tertinggi, n={lt['n']}); uji 4 minggu sebelum mengunci.")
        sug["rhythm_changes"].append({"waktu": lt["grup"], "alasan": "jangkauan median tertinggi dan selisih memenuhi ambang", "kepercayaan": "sedang"})
    lp, _ = leader(S["pilar"], "pesan", min_n, lift)
    if lp:
        reco.append(f"Tambah porsi pilar **{lp['grup']}** 5-10 poin (pesan masuk per posting tertinggi), kurangi dari pilar dengan hasil terendah dan n cukup.")
        sug["pillar_shift"].append({"pilar": lp["grup"], "perubahan": "+5 sampai +10", "alasan": "pesan masuk per posting tertinggi"})
    ok = [d for d in S["format"] if d["n"] >= min_n]
    if len(ok) >= 3:
        worst = sorted(ok, key=lambda d: (d["pesan"], d["save"]))[0]
        top_reach = max(ok, key=lambda d: d["reach"])
        extra = (f" Namun {worst['grup']} memiliki jangkauan median tertinggi ({worst['reach']:.0f}); mungkin berperan sebagai pintu masuk, bukan pendorong pesan, jadi perbaiki CTA-nya sebelum mengurangi."
                 if top_reach is worst else " Ubah pendekatan atau kurangi frekuensi, jangan hapus sebelum diuji ulang dua kali.")
        reco.append(f"Format **{worst['grup']}** paling lemah untuk pesan dan simpan (pesan {worst['pesan']:.2f}/posting, simpan {worst['save']:.2f}%).{extra}")
        sug["reduce"].append({"format": worst["grup"], "alasan": "terendah pada pesan dan simpan di antara grup dengan sampel cukup"})
    if not reco:
        reco.append("Belum ada perubahan yang cukup didukung data. Pertahankan jadwal dan kumpulkan 4 minggu lagi; ubah hanya satu hal pada satu waktu.")
    L += [f"{i}. {r}" for i, r in enumerate(reco, 1)] + [""]
    L.append("## Batasan\n")
    L += ["- Data mencerminkan akun Anda dalam periode ini; korelasi bukan bukti sebab-akibat.",
          "- Topik, momen (11.11, gajian, libur), dan kualitas visual ikut memengaruhi hasil dan tidak dipisahkan di sini.",
          "- Insights 'jam aktif pengikut' di aplikasi adalah pelengkap yang berguna untuk memilih jam uji.",
          "- Ubah satu variabel pada satu waktu agar 4 minggu berikutnya bisa dibaca."]
    if problems:
        L += ["", f"Baris yang dilewati: {len(problems)}"] + [f"- {p}" for p in problems[:5]]
    Path(opt("--out", "laporan_performa.md")).write_text("\n".join(L) + "\n", encoding="utf-8")
    if opt("--json"):
        Path(opt("--json")).write_text(json.dumps(sug, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Ditulis: {opt('--out', 'laporan_performa.md')} ({len(rows)} posting)")
    print("\n".join(findings[:6]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
