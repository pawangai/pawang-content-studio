#!/usr/bin/env python3
"""Ekstrak isian {...} dari command, lalu terapkan nilai dan validasi.

Pemakaian:
  python fill.py extract <file.md|file.txt> templates.json   # daftar command + isiannya
  python fill.py apply templates.json values.json out.md     # terapkan nilai + validasi
  python fill.py --example-values templates.json             # kerangka values.json

values.json:
  {"brief": {"topik": "...", "audiens": "...", "pesan_kunci": "...", "headline": "...", "cta": "..."},
   "values": {"c001": ["nilai isian 1", "nilai isian 2", ...], ...},
   "only": ["c001", "c004"]}          # opsional: hanya id ini yang dikeluarkan
Nilai untuk data yang harus berasal dari user (kutipan, nama, harga, tanggal, dll.) yang belum diberikan
ditulis [ISI SENDIRI: keterangan] (kurung siku, bukan kurawal).
"""
import json
import re
import sys
from pathlib import Path

DATA_WORDS = ["kutipan", "jabatan", "nomor", "email", "usaha", "klien", "harga", "angka", "metrik",
              "tanggal", "periode", "benefit", "syarat", "nama file", "testimoni", "persen", "diskon"]
CONTEXT_DATA = ["metrik", "angka", "testimoni", "harga", "nomor", "periode", "diskon"]


def spans(text):
    """Posisi placeholder tingkat terluar {...} dengan dukungan kurung bersarang."""
    out, depth, start = [], 0, None
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth == 0:
                raise ValueError(f"Kurung tutup tanpa pembuka di posisi {i}: ...{text[max(0, i - 20):i + 1]}")
            depth -= 1
            if depth == 0:
                out.append((start, i + 1))
    if depth:
        raise ValueError("Ada kurung { yang tidak tertutup.")
    return out


def top_level_split(s):
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        if ch == "/" and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    parts.append(cur.strip())
    return [p for p in parts if p]


def classify(inner, context):
    info = {"hint": inner}
    m = re.search(r"(maks(?:imal)?\.?\s*)?(\d+)(?:\s*-\s*(\d+))?\s*kata", inner, re.I)
    if m:
        if m.group(3):
            info["min_words"], info["max_words"] = int(m.group(2)), int(m.group(3))
        else:
            info["max_words"] = int(m.group(2))
    opts = top_level_split(inner)
    if len(opts) > 1:
        info["options"] = opts
    low = inner.lower()
    ctx = context.lower()
    if "options" not in info and (low.strip() == "nama" or any(re.search(rf"\b{re.escape(w)}\b", low) for w in DATA_WORDS) \
            or any(w in ctx[-45:] for w in CONTEXT_DATA)):
        info["needs_user_data"] = True
    return info


def parse_commands(path):
    raw = Path(path).read_text(encoding="utf-8")
    found = [(m.group(1), raw[max(0, m.start() - 40):m.start()]) for m in re.finditer(r"```[^\n]*\n(.*?)\n```", raw, re.S)]
    blocks = [b for b, _ in found]
    labels = []
    for _, pre in found:
        m = re.search(r"\*\*([^*\n]+?):\*\*\s*$", pre)
        labels.append(m.group(1) if m else "")
    if not blocks:
        blocks, cur = [], []
        for line in raw.splitlines():
            if line.strip() == "":
                if cur:
                    blocks.append("\n".join(cur))
                    cur = []
            elif line.lstrip().startswith("/") or cur:
                cur.append(line)
        if cur:
            blocks.append("\n".join(cur))
    cmds = []
    labels = labels if len(labels) == len(blocks) else [""] * len(blocks)
    for b, lab in zip(blocks, labels):
        b = b.strip()
        if not b.startswith("/"):
            continue
        first = b.split()[0]
        if "{" in first:
            continue
        try:
            sp = spans(b)
        except ValueError as e:
            print(f"Lewati {first}: {e}")
            continue
        if not sp:
            continue
        cmds.append((first, b, sp, lab))
    return cmds


def cmd_extract(src, dst):
    items = []
    for n, (name, text, sp, lab) in enumerate(parse_commands(src), 1):
        phs = []
        for a, z in sp:
            inner = text[a + 1:z - 1]
            d = classify(inner, text[:a])
            d["raw"] = text[a:z]
            phs.append(d)
        items.append({"id": f"c{n:03d}", "command": name, "variant": lab, "text": text, "placeholders": phs})
    Path(dst).write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(items)} command berisi isian ditulis ke {dst}\n")
    for it in items:
        print(f"[{it['id']}] {it['command']} {('(' + it['variant'] + ') ') if it['variant'] else ''}- {len(it['placeholders'])} isian")
        for i, p in enumerate(it["placeholders"], 1):
            tags = []
            if "max_words" in p:
                tags.append(f"maks {p['max_words']} kata")
            if "options" in p:
                tags.append("pilih: " + " | ".join(p["options"]))
            if p.get("needs_user_data"):
                tags.append("DATA DARI USER")
            print(f"   {i}. {p['raw']}" + (f"   -> {'; '.join(tags)}" if tags else ""))
    return 0


def words(s):
    return len(re.findall(r"\S+", s))


def cmd_apply(tpl, vals, out):
    items = json.loads(Path(tpl).read_text(encoding="utf-8"))
    data = json.loads(Path(vals).read_text(encoding="utf-8"))
    values = data.get("values", {})
    only = data.get("only")
    errors, warns, user_items, todo = [], [], [], []
    blocks = []
    for it in items:
        if only and it["id"] not in only:
            continue
        v = values.get(it["id"])
        if v is None:
            errors.append(f"{it['id']} {it['command']}: tidak ada nilai.")
            continue
        phs = it["placeholders"]
        if len(v) != len(phs):
            errors.append(f"{it['id']} {it['command']}: butuh {len(phs)} nilai, diberi {len(v)}.")
            continue
        text = it["text"]
        sp = spans(text)
        res = text
        loc_todo, loc_user = [], []
        for (a, z), p, val in reversed(list(zip(sp, phs, v))):
            val = str(val).strip()
            tag = f"{it['id']} {it['command']} {p['raw'][:40]}"
            if not val:
                errors.append(f"{tag}: nilai kosong.")
            if "{" in val or "}" in val:
                errors.append(f"{tag}: nilai masih mengandung kurung kurawal.")
            if val.startswith("[ISI SENDIRI"):
                loc_todo.append(f"{it['command']}: {val}")
            else:
                if "max_words" in p and words(val) > p["max_words"]:
                    errors.append(f"{tag}: {words(val)} kata, maksimal {p['max_words']}: '{val}'")
                if "min_words" in p and words(val) < p["min_words"]:
                    warns.append(f"{tag}: {words(val)} kata, disarankan minimal {p['min_words']}.")
                if "options" in p and val.lower() not in [o.lower() for o in p["options"]]:
                    warns.append(f"{tag}: nilai di luar opsi {p['options']} (boleh jika opsi hanya contoh kategori).")
                if p.get("needs_user_data"):
                    loc_user.append(f"{it['command']}: {p['raw'][:45]} -> {val}")
            if '"' in val and a > 0 and text[a - 1] == '"':
                warns.append(f"{tag}: nilai mengandung tanda kutip ganda di dalam placeholder bertanda kutip.")
            res = res[:a] + val + res[z:]
        if "{" in res.replace("[ISI SENDIRI", "["):
            if re.search(r"\{[^}]*\}", res):
                errors.append(f"{it['id']} {it['command']}: masih ada kurung kurawal di hasil.")
        todo.extend(reversed(loc_todo))
        user_items.extend(reversed(loc_user))
        blocks.append((it, res))
    lines = ["# Command Siap Tempel", ""]
    br = data.get("brief")
    if br:
        lines.append("## Brief Konten")
        lines.append("```")
        for k, x in br.items():
            lines.append(f"{k}: {x}")
        lines.append("```\n")
    lines.append("Tempel Brand Lock dan upload brand board dulu (sekali per chat), lalu salin command di bawah satu per satu.\n")
    for it, res in blocks:
        lines.append(f"### {it['command']}" + (f" ({it['variant']})" if it.get("variant") else ""))
        lines.append("```\n" + res + "\n```\n")
    if todo:
        lines.append("## Yang Masih Perlu Anda Isi")
        lines += [f"- {t}" for t in todo]
        lines.append("")
    if user_items:
        lines.append("## Data dari Anda (periksa kebenarannya)")
        lines += [f"- {t}" for t in user_items]
        lines.append("")
    Path(out).write_text("\n".join(lines), encoding="utf-8")
    print(f"Ditulis: {out} ({len(blocks)} command)")
    print("Galat: " + ("tidak ada" if not errors else "\n" + "\n".join("- " + e for e in errors)))
    print("Peringatan: " + ("tidak ada" if not warns else "\n" + "\n".join("- " + w for w in warns)))
    print(f"Belum diisi (ISI SENDIRI): {len(todo)}")
    return 1 if errors else 0


def cmd_example(tpl):
    items = json.loads(Path(tpl).read_text(encoding="utf-8"))
    print(json.dumps({"brief": {"topik": "", "audiens": "", "pesan_kunci": "", "headline": "", "cta": ""},
                      "values": {it["id"]: [""] * len(it["placeholders"]) for it in items}}, indent=2, ensure_ascii=False))
    return 0


def main(a):
    if len(a) == 4 and a[1] == "extract":
        return cmd_extract(a[2], a[3])
    if len(a) == 5 and a[1] == "apply":
        return cmd_apply(a[2], a[3], a[4])
    if len(a) == 3 and a[1] == "--example-values":
        return cmd_example(a[2])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
