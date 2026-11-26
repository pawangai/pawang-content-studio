#!/usr/bin/env python3
"""Ekspor kalender konten (Markdown dari content-calendar-pack) ke CSV log (Google Sheets) dan ICS (Google Calendar).

Pemakaian:
  python calendar_export.py jadwal_konten.md --csv content-log.csv --ics jadwal.ics [--year 2026] [--prefix pw] [--duration 30]
Tahun diambil dari kalimat "mulai Senin, 26 Oktober 2026" di berkas bila ada, atau dari --year.
ICS memakai zona waktu Asia/Jakarta (WIB). Impor ICS bisa dilakukan lewat Google Calendar tanpa konektor apa pun.
"""
import argparse
import csv
import datetime as dt
import re
import sys
from pathlib import Path

BULAN = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "Mei": 5, "Jun": 6, "Jul": 7, "Agu": 8, "Sep": 9, "Okt": 10, "Nov": 11, "Des": 12}
BULAN_PENUH = {"januari": 1, "februari": 2, "maret": 3, "april": 4, "mei": 5, "juni": 6, "juli": 7, "agustus": 8, "september": 9, "oktober": 10, "november": 11, "desember": 12}
ROW = re.compile(r"^\|\s*(Sen|Sel|Rab|Kam|Jum|Sab|Min)\s+(\d{1,2})\s+(\w{3})\s*\|\s*(\d{2}:\d{2})\s*\|(.*)\|\s*(★)?\s*\|\s*$")


def parse(md, year=None):
    m = re.search(r"mulai\s+\*\*\w+,\s*(\d{1,2})\s+(\w+)\s+(\d{4})", md)
    start_year = int(m.group(3)) if m else year
    if not start_year:
        raise SystemExit("Tahun tidak ditemukan; berikan --year.")
    start_month = BULAN_PENUH.get(m.group(2).lower()) if m else None
    week = ""
    out = []
    prev = None
    y = start_year
    for ln in md.splitlines():
        h = re.match(r"^### Minggu \d+:\s*(.*?)\s*\(", ln)
        if h:
            week = h.group(1)
        r = ROW.match(ln)
        if not r:
            continue
        hari, d, mon, jam, rest, star = r.groups()
        cells = [c.strip() for c in rest.split("|")]
        # setelah tanggal dan jam: platform | format | pilar | topik | command
        if len(cells) < 5:
            continue
        platform, fmt, pilar, topik, cmd = cells[0], cells[1], cells[2], cells[3], cells[4]
        mm = BULAN[mon]
        if prev and mm < prev:
            y += 1
        prev = mm
        date = dt.date(y, mm, int(d))
        out.append(dict(date=date, jam=jam, platform=platform, format=fmt, pilar=pilar, topik=topik,
                        command=cmd.replace("`", ""), minimal=bool(star), minggu=week))
    return out


def write_csv(rows, path, prefix):
    hdr = ["ID", "Tanggal rencana", "Tanggal terbit", "Platform", "Format", "Pilar", "Topik", "Hook", "Slug", "Status", "Link aset (Drive)", "Link post", "Command", "Catatan"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(hdr)
        for i, r in enumerate(rows, 1):
            slug = re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", r["topik"].lower())).strip("-")[:60]
            w.writerow([f"{(prefix or 'C').upper()}-{i:03d}", r["date"].isoformat(), "", r["platform"], r["format"], r["pilar"], r["topik"], "", slug,
                        "rencana", "", "", r["command"], ("minimal; " if r["minimal"] else "") + f"minggu: {r['minggu']}"])


def esc(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def write_ics(rows, path, minutes):
    L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//pawang-content-studio//ID", "CALSCALE:GREGORIAN", "X-WR-TIMEZONE:Asia/Jakarta",
         "BEGIN:VTIMEZONE", "TZID:Asia/Jakarta", "BEGIN:STANDARD", "DTSTART:19700101T000000", "TZOFFSETFROM:+0700", "TZOFFSETTO:+0700", "TZNAME:WIB", "END:STANDARD", "END:VTIMEZONE"]
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for i, r in enumerate(rows, 1):
        h, m = map(int, r["jam"].split(":"))
        s = dt.datetime.combine(r["date"], dt.time(h, m))
        e = s + dt.timedelta(minutes=minutes)
        L += ["BEGIN:VEVENT", f"UID:content-{r['date']:%Y%m%d}-{h:02d}{m:02d}-{i}@pawang-content-studio", f"DTSTAMP:{stamp}",
              f"DTSTART;TZID=Asia/Jakarta:{s:%Y%m%dT%H%M%S}", f"DTEND;TZID=Asia/Jakarta:{e:%Y%m%dT%H%M%S}",
              "SUMMARY:" + esc(f"Posting: {r['topik']} ({r['format']})"),
              "DESCRIPTION:" + esc(f"Platform: {r['platform']}\nPilar: {r['pilar']}\nCommand: {r['command']}\nMinggu: {r['minggu']}"),
              "BEGIN:VALARM", "TRIGGER:-PT30M", "ACTION:DISPLAY", "DESCRIPTION:Siap-siap posting", "END:VALARM", "END:VEVENT"]
    L.append("END:VCALENDAR")
    Path(path).write_text("\r\n".join(L) + "\r\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("md")
    ap.add_argument("--csv")
    ap.add_argument("--ics")
    ap.add_argument("--year", type=int)
    ap.add_argument("--prefix", default="")
    ap.add_argument("--duration", type=int, default=30)
    a = ap.parse_args()
    rows = parse(Path(a.md).read_text(encoding="utf-8"), a.year)
    if not rows:
        print("Tidak ada baris kalender terbaca (pastikan berkas dari content-calendar-pack).")
        return 1
    if a.csv:
        write_csv(rows, a.csv, a.prefix)
    if a.ics:
        write_ics(rows, a.ics, a.duration)
    print(f"{len(rows)} jadwal dibaca ({rows[0]['date']} s/d {rows[-1]['date']})" + (f"; CSV: {a.csv}" if a.csv else "") + (f"; ICS: {a.ics}" if a.ics else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
