#!/usr/bin/env python3
"""Validasi semua skill di skills/ lalu kemas menjadi satu .skill per skill (satu ZIP per skill, sesuai syarat unggah Claude.ai).

Pemakaian (dari akar repo):
  python scripts/build_all.py                 # validasi + kemas ke dist/
  python scripts/build_all.py --short         # kemas juga ke dist-short/ dengan deskripsi <= 200 karakter (cadangan bila unggahan menolak deskripsi panjang)
  python scripts/build_all.py --check         # validasi saja
  python scripts/build_all.py --only asset-qa caption-writer
"""
import argparse
import json
import py_compile
import re
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"evals", "__pycache__", ".git"}
SKIP_FILES = {".DS_Store"}


def frontmatter(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not m:
        return None, "frontmatter tidak ditemukan"
    fm = m.group(1)
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    desc = re.search(r"^description:\s*(.+)$", fm, re.M)
    return {"name": name.group(1).strip() if name else None, "description": desc.group(1).strip() if desc else None, "raw": fm}, None


def validate(sdir, short=None):
    errs, warns = [], []
    sm = sdir / "SKILL.md"
    if not sm.exists():
        return ["SKILL.md tidak ada"], warns, {}
    fm, err = frontmatter(sm.read_text(encoding="utf-8"))
    if err:
        return [err], warns, {}
    if fm["name"] != sdir.name:
        errs.append(f"name '{fm['name']}' tidak sama dengan nama folder '{sdir.name}'")
    d = fm["description"] or ""
    if not d:
        errs.append("description kosong")
    if len(d) > 1024:
        errs.append(f"description {len(d)} karakter (> 1024)")
    elif len(d) > 200:
        warns.append(f"description {len(d)} karakter (> 200; gunakan dist-short bila unggahan menolak)")
    if not d.startswith(('"', "'")) and ": " in d:
        errs.append("description mengandung ': ' tanpa tanda kutip (YAML tidak valid)")
    if short is not None and len(short) > 200:
        errs.append(f"short_description {len(short)} karakter (> 200)")
    if short is not None and ": " in short:
        errs.append("short_description mengandung ': ' (YAML tidak valid); pakai tanda kurung")
    body = sm.read_text(encoding="utf-8")
    for ref in set(re.findall(r"`((?:scripts|references|templates|assets)/[\w./-]+)`", body)):
        if not (sdir / ref).exists():
            errs.append(f"berkas yang dirujuk tidak ada: {ref}")
    ev_dir = sdir / "evals"
    if not ev_dir.is_dir() or len([p for p in ev_dir.iterdir() if p.is_dir()]) < 2:
        warns.append("folder evals/ belum memiliki minimal 2 kasus uji")
    with tempfile.TemporaryDirectory() as tmpd:
        for py in sdir.rglob("*.py"):
            if "__pycache__" in py.parts:
                continue
            try:
                py_compile.compile(str(py), doraise=True, cfile=str(Path(tmpd) / (py.stem + ".pyc")))
            except py_compile.PyCompileError as e:
                errs.append(f"{py.relative_to(sdir)} tidak bisa dikompilasi: {e.msg.strip()[:80]}")
    return errs, warns, fm


def pack(sdir, out_dir, short_desc=None):
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"{sdir.name}.skill"
    n = 0
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(sdir.rglob("*")):
            rel = f.relative_to(sdir)
            if f.is_dir() or set(rel.parts) & SKIP_DIRS or f.name in SKIP_FILES or f.suffix == ".pyc":
                continue
            data = f.read_bytes()
            if short_desc and rel.as_posix() == "SKILL.md":
                t = data.decode("utf-8")
                t = re.sub(r"^description:\s*.+$", lambda m: "description: " + short_desc, t, count=1, flags=re.M)
                data = t.encode("utf-8")
            z.writestr(f"{sdir.name}/{rel.as_posix()}", data)
            n += 1
    return target, n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--short", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    reg = {s["name"]: s for s in json.loads((ROOT / "skills.json").read_text(encoding="utf-8"))["skills"]}
    stray = [p.name for p in (ROOT / "skills").iterdir() if not p.is_dir() and p.name not in SKIP_FILES]
    for s in stray:
        print(f"GALAT: berkas liar di skills/: {s}")
    tpl_root = ROOT / "templates"
    tpl_skill = ROOT / "skills" / "content-pipeline" / "templates"
    if tpl_root.is_dir() and tpl_skill.is_dir():
        for tf in tpl_root.iterdir():
            if tf.is_file() and (not (tpl_skill / tf.name).exists() or (tpl_skill / tf.name).read_bytes() != tf.read_bytes()):
                if not a.check:
                    (tpl_skill / tf.name).write_bytes(tf.read_bytes())
                else:
                    stray.append(f"templates/{tf.name} tidak sinkron")
    dirs = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    if a.only:
        dirs = [d for d in dirs if d.name in a.only]
    bad = len(stray)
    long_desc = []
    print(f"{'skill':<26}{'deskripsi':>10}{'berkas':>8}{'ukuran':>10}  status")
    for d in dirs:
        short = reg.get(d.name, {}).get("short_description")
        if d.name not in reg:
            print(f"{d.name:<26} TIDAK TERDAFTAR di skills.json")
            bad += 1
            continue
        errs, warns, fm = validate(d, short)
        info = ""
        if not errs and not a.check:
            t, n = pack(d, ROOT / "dist")
            info = f"{n:>8}{t.stat().st_size / 1024:>8.0f}KB"
            if a.short:
                pack(d, ROOT / "dist-short", short)
        else:
            info = f"{'':>8}{'':>10}"
        status = "OK" if not errs else "GALAT"
        print(f"{d.name:<26}{len((fm or {}).get('description') or ''):>10}{info}  {status}")
        for e in errs:
            print("    GALAT:", e)
            bad += 1
        for w in warns:
            if "gunakan dist-short" in w:
                long_desc.append(d.name)
            else:
                print("    catatan:", w)
    missing = [n for n in reg if not (ROOT / "skills" / n).exists()]
    for n in missing:
        print(f"{n}: terdaftar tetapi folder tidak ada")
        bad += 1
    if long_desc:
        print(f"\nCatatan: {len(long_desc)} skill punya deskripsi > 200 karakter (batas spesifikasi 1024). Bila Claude.ai menolak unggahan karena deskripsi, pakai dist-short/ (jalankan dengan --short).")
    print("\nSemua skill valid." if not bad else f"\n{bad} masalah ditemukan.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
