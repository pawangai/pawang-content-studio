#!/usr/bin/env python3
"""Uji asap (smoke test): menjalankan seluruh alur dengan brand contoh Pawang.dev dan memeriksa tiap skill saling terhubung.

Pemakaian (dari akar repo):  python scripts/smoke_test.py
Keluaran contoh disimpan di examples/pawang-dev/generated/. Kebutuhan: Python 3.9+; Pillow dan numpy untuk uji asset-qa (dilewati bila tidak ada).
"""
import csv
import datetime as dt
import json
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = ROOT / "skills"
OUT = ROOT / "examples" / "pawang-dev" / "generated"
OUT.mkdir(parents=True, exist_ok=True)
PY = sys.executable
results = []


def run(args, **kw):
    return subprocess.run([PY, *map(str, args)], capture_output=True, text=True, cwd=ROOT, **kw)


def step(name, fn):
    try:
        ok, note = fn()
    except Exception as e:  # noqa: BLE001
        ok, note = False, f"{type(e).__name__}: {e}"
    results.append((name, "LULUS" if ok is True else "LEWAT" if ok is None else "GAGAL", note))


def load_example(skill, script="build_pack.py"):
    r = run([S / skill / "scripts" / script, "--example"])
    return json.loads(r.stdout)


def main():
    prof = {}

    def s1():
        global prof
        base = json.loads(run([S / "brand-profile-builder/scripts/profile.py", "--example"]).stdout)
        if "--update-examples" in sys.argv:
            (ROOT / "examples/pawang-dev/profile.json").write_text(json.dumps(base, indent=2, ensure_ascii=False), encoding="utf-8")
        prof = base
        return (ROOT / "examples/pawang-dev/profile.json").exists() and bool(base.get("examples")) and bool(base.get("content", {}).get("weeks_plan")), "profile.json contoh mandiri dan lengkap"
    step("1. profil contoh dibuat", s1)

    def s2():
        r = run([S / "brand-profile-builder/scripts/profile.py", "from-spec", ROOT / "examples/pawang-dev/brand-spec.md", OUT / "profile_from_spec.json"])
        rv = run([S / "brand-profile-builder/scripts/profile.py", "validate", OUT / "profile_from_spec.json"])
        p = json.loads((OUT / "profile_from_spec.json").read_text(encoding="utf-8"))
        roles = {c["role"] for c in p["colors"]}
        return r.returncode == 0 and rv.returncode == 0 and {"dark", "accent", "light"} <= roles and p.get("prefix") == "pw", f"validasi OK, role warna: {sorted(roles)}"
    step("2. Brand Spec -> draf profil", s2)

    def s3():
        r = run([S / "brand-profile-builder/scripts/profile.py", "validate", ROOT / "examples/pawang-dev/profile.json"])
        return r.returncode == 0, "kontras dan field diperiksa"
    step("3. validasi profil + kontras", s3)

    exports = {}

    def s4():
        bad = []
        for t in ("command-pack", "flow-video", "text-layout", "calendar", "caption", "reply"):
            f = OUT / f"export_{t}.json"
            r = run([S / "brand-profile-builder/scripts/profile.py", "export", ROOT / "examples/pawang-dev/profile.json", "--for", t, f])
            exports[t] = f
            if r.returncode != 0:
                bad.append(t)
        return not bad, "semua target lengkap" if not bad else "belum lengkap: " + ", ".join(bad)
    step("4. ekspor profil ke 6 target", s4)

    def build(skill, script, key, out, ok_text):
        def f():
            r = run([S / skill / "scripts" / script, exports[key], OUT / out])
            return (r.returncode == 0 and ok_text in r.stdout), r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-120:]
        return f
    step("5. brand-command-pack render", build("brand-command-pack", "build_pack.py", "command-pack", "01_command_gambar.md", "Validasi: OK"))
    step("6. flow-video-command-pack render", build("flow-video-command-pack", "build_pack.py", "flow-video", "02_command_video.md", "Validasi: OK"))
    step("7. content-text-layout-pack render", build("content-text-layout-pack", "build_pack.py", "text-layout", "03_panduan_teks_layout.md", "Lint isi contoh: OK"))
    step("8. content-calendar-pack render", build("content-calendar-pack", "build_pack.py", "calendar", "04_jadwal_konten.md", "Lint kalender: OK"))
    step("9. inbound-reply-pack render", build("inbound-reply-pack", "build_replies.py", "reply", "07_paket_balasan.md", "Galat: tidak ada"))

    def s10():
        d = load_example("caption-writer", "captions.py")
        (OUT / "captions.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        r = run([S / "caption-writer/scripts/captions.py", "render", OUT / "captions.json", OUT / "05_caption.md"])
        return r.returncode == 0 and "Galat: tidak ada" in r.stdout, "caption contoh lolos batas platform"
    step("10. caption-writer render", s10)

    def s11():
        try:
            from PIL import Image, ImageDraw, ImageFont  # noqa: F401
            import numpy  # noqa: F401
        except Exception:
            return None, "Pillow/numpy tidak ada"
        im = Image.new("RGB", (1080, 1920), "#14213D")
        d = ImageDraw.Draw(im)
        d.rectangle((300, 1000, 780, 1300), fill="#22AA55")
        im.save(OUT / "uji_story.png")
        r = run([S / "asset-qa/scripts/qa_image.py", OUT / "uji_story.png", "--format", "story", "--profile", ROOT / "examples/pawang-dev/profile.json"])
        rl = run([S / "asset-qa/scripts/logo_compare.py", OUT / "uji_story.png", OUT / "uji_story.png"])
        issues_f = OUT / "issues_uji.json"
        issues_f.write_text(json.dumps({"tool": "chatgpt", "brand": "Pawang.dev", "issues": [{"type": "palette", "where": "kotak tengah", "color": "Biru Malam", "hex": "#14213D"}]}, ensure_ascii=False), encoding="utf-8")
        rf = run([S / "asset-qa/scripts/fixprompts.py", issues_f, OUT / "fixprompts_uji.md"])
        issues_f.unlink(missing_ok=True)
        (OUT / "fixprompts_uji.md").unlink(missing_ok=True)
        return ("[PALET]" in r.stdout and rl.returncode == 0 and rf.returncode == 0), "qa_image, logo_compare, dan fixprompts teruji"
    step("11. asset-qa mendeteksi warna salah", s11)

    def s12():
        random.seed(7)
        sched = [("Senin", "09:00", "Instagram", "Carousel", "Paham"), ("Selasa", "12:00", "Reels", "Reel", "Paham"), ("Rabu", "19:30", "Instagram", "Story", "Paham"),
                 ("Kamis", "09:30", "Instagram", "Carousel", "Jinak"), ("Jumat", "12:00", "Instagram", "Kartu tips", "Paham"),
                 ("Sabtu", "19:00", "Reels", "Reel", "Si Liar"), ("Minggu", "19:30", "Instagram", "Testimoni", "Tenang")]
        rows = []
        d0 = dt.date(2026, 10, 26)
        for w in range(4):
            for i, (h, j, p, f, pl) in enumerate(sched):
                base = {"Carousel": 900, "Reel": 1800, "Story": 500, "Kartu tips": 700, "Testimoni": 600}[f]
                reach = int(base * random.uniform(0.7, 1.4))
                rows.append([(d0 + dt.timedelta(days=w * 7 + i)).isoformat(), j, p, f, pl, f"topik {w}-{i}", reach, int(reach * 0.03), int(reach * 0.01), 3, int(reach * 0.01), random.choice([0, 1, 2])])
        with open(OUT / "insights_SINTETIS.csv", "w", newline="", encoding="utf-8") as fh:
            wr = csv.writer(fh)
            wr.writerow("Tanggal,Jam,Platform,Format,Pilar,Topik,Jangkauan,Simpan,Bagikan,Komentar,Klik link,Pesan masuk".split(","))
            wr.writerows(rows)
        r = run([S / "performance-analyzer/scripts/analyze.py", OUT / "insights_SINTETIS.csv", "--out", OUT / "08_laporan_performa_SINTETIS.md"])
        return r.returncode == 0, "analisis data sintetis (bukan data nyata)"
    step("12. performance-analyzer", s12)

    def s13():
        r = run([S / "command-filler/scripts/fill.py", "extract", OUT / "01_command_gambar.md", OUT / "templates.json"])
        items = json.loads((OUT / "templates.json").read_text(encoding="utf-8"))
        vals = {}
        for it in items[:6]:
            v = []
            for p in it["placeholders"]:
                opt = p.get("options")
                v.append(opt[0] if opt else "contoh")
            vals[it["id"]] = v
        (OUT / "values.json").write_text(json.dumps({"values": vals, "only": list(vals)}, ensure_ascii=False), encoding="utf-8")
        r2 = run([S / "command-filler/scripts/fill.py", "apply", OUT / "templates.json", OUT / "values.json", OUT / "06_command_terisi_contoh.md"])
        return r.returncode == 0 and r2.returncode == 0 and "Galat: tidak ada" in r2.stdout, f"{len(items)} command berisi isian ditemukan"
    step("13. command-filler extract + apply", s13)

    def s14():
        r = run([S / "content-pipeline/scripts/calendar_export.py", OUT / "04_jadwal_konten.md", "--csv", OUT / "content-log.csv", "--ics", OUT / "jadwal.ics", "--prefix", "pw"])
        r2 = run([S / "content-pipeline/scripts/dedupe_check.py", OUT / "content-log.csv", "--topic", "Empat tanda data bisnismu sudah liar"])
        r3 = run([S / "content-pipeline/scripts/dedupe_check.py", OUT / "content-log.csv", "--topic", "Resep nasi goreng spesial"])
        ok = r.returncode == 0 and "[DUPLIKAT]" in r2.stdout and "[BARU]" in r3.stdout
        return ok, "kalender -> CSV + ICS; duplikat terdeteksi, topik baru lolos"
    step("14. content-pipeline: ekspor + anti duplikat", s14)

    def s15():
        bad = []
        for t in ("quora", "longform"):
            r = run([S / "brand-profile-builder/scripts/profile.py", "export", ROOT / "examples/pawang-dev/profile.json", "--for", t, OUT / f"export_{t}.json"])
            if r.returncode != 0:
                bad.append(t)
        return not bad, "ekspor quora dan longform lengkap" if not bad else "belum lengkap: " + ", ".join(bad)
    step("15. profil -> ekspor quora + longform", s15)

    def s16():
        r = run([S / "quora-answer-writer/scripts/answer_check.py", ROOT / "examples/pawang-dev/jawaban-quora-contoh.md", "--question", "Bagaimana cara merapikan data penjualan yang tersebar di banyak file?", "--brand", "Pawang"])
        bad = OUT / "jawaban_buruk.md"
        bad.write_text("Halo! Pawang adalah TERBAIK nomor 1, dijamin 100%. Klik https://bit.ly/x?utm_source=q dan https://pawang.dev diskon.", encoding="utf-8")
        r2 = run([S / "quora-answer-writer/scripts/answer_check.py", bad, "--question", "x", "--brand", "Pawang"])
        return r.returncode == 0 and "Galat: tidak ada" in r.stdout and r2.returncode == 1 and "Klaim berlebihan" in r2.stdout, "jawaban baik lolos; jawaban promosi ditolak"
    step("16. quora-answer-writer pemeriksa", s16)

    def s17():
        r = run([S / "longform-writer/scripts/article_check.py", ROOT / "examples/pawang-dev/artikel-contoh.md", "--site", "pawang.dev"])
        r2 = run([S / "longform-writer/scripts/script_check.py", ROOT / "examples/pawang-dev/skrip-youtube-contoh.md", "--chapters"])
        return r.returncode == 0 and r2.returncode == 0 and "00:00 Hook" in r2.stdout, "artikel dan skrip contoh tanpa galat; daftar bab dibuat"
    step("17. longform-writer artikel + skrip", s17)

    def s18():
        t = (OUT / "01_command_gambar.md").read_text(encoding="utf-8")
        return "### /pw-fbpost" in t and "### /pw-threads" in t, "command Facebook dan Threads ada"
    step("18. cakupan Facebook + Threads", s18)

    w = max(len(r[0]) for r in results)
    for n, st, note in results:
        print(f"{n:<{w}}  {st:<6} {note}")
    fails = [r for r in results if r[1] == "GAGAL"]
    print(f"\n{len(results) - len(fails)}/{len(results)} langkah lulus atau dilewati." if not fails else f"\n{len(fails)} langkah GAGAL.")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
