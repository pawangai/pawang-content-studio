#!/usr/bin/env python3
"""Hasilkan plugin marketplace dari skills/ untuk Claude Code, Codex, Antigravity (agy), dan claude.ai.

Sumber kebenaran tetap `skills/` dan `skills.json`. Skrip ini menyalin skill (tanpa evals/) ke
`plugins/pawang-content-studio/skills/` dan menulis semua manifest dari konstanta di bawah.

Pemakaian (dari akar repo):
  python scripts/build_plugins.py           # tulis ulang semua berkas turunan
  python scripts/build_plugins.py --check   # gagal (exit 1) bila ada berkas turunan yang tidak sinkron
  python scripts/build_plugins.py --zip     # juga kemas dist-plugin/<nama>-<versi>.zip untuk unggah admin claude.ai
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path

from build_all import SKIP_DIRS, SKIP_FILES, frontmatter

LOGGER = logging.getLogger("build_plugins")

ROOT = Path(__file__).resolve().parent.parent
KEBAB_CASE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_SKILL_DESCRIPTION = 1024  # batas Antigravity; Claude.ai/Codex lebih longgar
ZIP_EPOCH = (1980, 1, 1, 0, 0, 0)

MARKETPLACE_NAME = "pawang-studio"
PLUGIN_NAME = "pawang-content-studio"
PLUGIN_TITLE = "Pawang Content Studio"
PLUGIN_VERSION = "1.0.0"
PLUGIN_CATEGORY = "Productivity"
AUTHOR_NAME = "Pawang.dev"
DESCRIPTION = (
    "14 skill alur konten end-to-end: brand board, command gambar/video, jadwal, "
    "caption, artikel, QA, balasan DM, dan evaluasi performa."
)
LONG_DESCRIPTION = (
    "Rangkaian 14 skill yang tersambung lewat satu profile.json: identitas brand, command gambar "
    "dan video, panduan teks dan layout, jadwal bertanggal, caption, artikel dan skrip YouTube, "
    "jawaban Quora, QA aset, balasan DM, dan evaluasi performa."
)
KEYWORDS = ["content", "konten", "brand", "social-media", "caption", "calendar", "umkm"]
SUGGESTED_PROMPTS = [
    "Buatkan brand board standar untuk brand saya",
    "Buatkan jadwal konten 4 minggu mulai Senin depan, paket Ringan",
    "Cek duplikat topik konten ini sebelum saya produksi",
]

PLUGIN_REL = Path("plugins") / PLUGIN_NAME
AGY_MANIFEST_REL = Path(".antigravity-plugin") / "plugin.json"


class BuildError(Exception):
    """Sumber skill atau skills.json tidak valid sehingga plugin tidak bisa dibangun."""


@dataclass(frozen=True)
class Artifact:
    """Isi satu berkas turunan beserta status bit eksekusinya."""

    content: bytes
    executable: bool = False


def dump_json(data: dict[str, object]) -> bytes:
    """Serialisasi JSON stabil (indent 2, UTF-8, newline akhir) agar diff dan --check deterministik."""
    return (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def load_registry() -> list[dict[str, object]]:
    """Baca daftar skill dari skills.json.

    Raises:
        BuildError: berkas tidak ada atau bukan JSON yang valid.
    """
    path = ROOT / "skills.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))["skills"]
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        raise BuildError(f"skills.json tidak bisa dibaca: {exc}") from exc


def validate_skills(registry: list[dict[str, object]]) -> list[Path]:
    """Pastikan tiap skill terdaftar, bernama kebab-case, dan lolos batas deskripsi Antigravity.

    Returns:
        Folder skill yang valid, terurut menurut nama.

    Raises:
        BuildError: ada skill yang melanggar aturan.
    """
    problems: list[str] = []
    registered = {str(entry["name"]) for entry in registry}
    skills_dir = ROOT / "skills"
    dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir())
    for sdir in dirs:
        if sdir.name not in registered:
            problems.append(f"{sdir.name}: tidak terdaftar di skills.json")
        if not KEBAB_CASE.match(sdir.name):
            problems.append(f"{sdir.name}: nama folder bukan kebab-case")
        skill_md = sdir / "SKILL.md"
        if not skill_md.exists():
            problems.append(f"{sdir.name}: SKILL.md tidak ada")
            continue
        fm, err = frontmatter(skill_md.read_text(encoding="utf-8"))
        if err or fm is None:
            problems.append(f"{sdir.name}: {err}")
            continue
        if fm["name"] != sdir.name:
            problems.append(f"{sdir.name}: name di frontmatter ('{fm['name']}') berbeda dari nama folder")
        description = fm["description"] or ""
        if not description or len(description) > MAX_SKILL_DESCRIPTION:
            problems.append(f"{sdir.name}: description kosong atau > {MAX_SKILL_DESCRIPTION} karakter")
    for name in sorted(registered - {d.name for d in dirs}):
        problems.append(f"{name}: terdaftar di skills.json tetapi foldernya tidak ada")
    if problems:
        raise BuildError("\n".join(problems))
    return dirs


def skill_artifacts(skill_dirs: list[Path]) -> dict[Path, Artifact]:
    """Salin berkas runtime tiap skill (tanpa evals/, cache, dan .pyc) ke tata letak plugin."""
    artifacts: dict[Path, Artifact] = {}
    for sdir in skill_dirs:
        for src in sorted(sdir.rglob("*")):
            rel = src.relative_to(sdir)
            if src.is_dir() or set(rel.parts) & SKIP_DIRS or src.name in SKIP_FILES or src.suffix == ".pyc":
                continue
            target = PLUGIN_REL / "skills" / sdir.name / rel
            executable = bool(src.stat().st_mode & 0o111)
            artifacts[target] = Artifact(src.read_bytes(), executable)
    return artifacts


def plugin_readme(registry: list[dict[str, object]]) -> str:
    """README di akar plugin; Antigravity menampilkannya sebelum instalasi."""
    rows = "\n".join(
        f"| `{entry['name']}` | {entry['short_description']} |"
        for entry in sorted(registry, key=lambda e: (int(e["stage"]), str(e["name"])))  # type: ignore[arg-type]
    )
    return (
        f"# {PLUGIN_TITLE}\n\n"
        f"{LONG_DESCRIPTION}\n\n"
        "Skill aktif otomatis saat permintaan cocok dengan deskripsinya. Bila tidak terpicu, sebut nama skill "
        "secara eksplisit, misalnya: *\"Gunakan skill asset-qa untuk memeriksa gambar ini.\"*\n\n"
        "## Skill\n\n"
        "| Skill | Fungsi |\n|---|---|\n"
        f"{rows}\n\n"
        "## Prasyarat\n\n"
        "- `asset-qa` memakai Pillow dan numpy (opsional OpenCV, Tesseract, ffmpeg). "
        "Pasang dengan `pip install Pillow numpy opencv-python-headless pytesseract`.\n"
        "- Skill lain hanya memakai pustaka standar Python 3.9+.\n"
    )


def manifest_artifacts(registry: list[dict[str, object]]) -> dict[Path, Artifact]:
    """Tulis seluruh manifest plugin dan katalog marketplace dari konstanta modul."""
    author = {"name": AUTHOR_NAME}
    claude_plugin: dict[str, object] = {
        "name": PLUGIN_NAME,
        "version": PLUGIN_VERSION,
        "description": DESCRIPTION,
        "author": author,
        "keywords": KEYWORDS,
    }
    codex_plugin: dict[str, object] = {
        **claude_plugin,
        "skills": "./skills/",
        "interface": {
            "displayName": PLUGIN_TITLE,
            "shortDescription": DESCRIPTION,
            "longDescription": LONG_DESCRIPTION,
            "developerName": AUTHOR_NAME,
            "category": PLUGIN_CATEGORY,
            "capabilities": ["Read", "Write"],
            "defaultPrompt": SUGGESTED_PROMPTS,
        },
    }
    agy_plugin: dict[str, object] = {
        "$schema": "https://antigravity.google/schemas/v1/plugin.json",
        "name": PLUGIN_NAME,
        "displayName": PLUGIN_TITLE,
        "version": PLUGIN_VERSION,
        "description": DESCRIPTION,
        "suggestedPrompts": SUGGESTED_PROMPTS,
        "author": author,
        "keywords": KEYWORDS,
    }
    source = f"./{PLUGIN_REL.as_posix()}"
    claude_marketplace: dict[str, object] = {
        "name": MARKETPLACE_NAME,
        "owner": author,
        "metadata": {"description": LONG_DESCRIPTION, "version": PLUGIN_VERSION},
        "plugins": [
            {
                "name": PLUGIN_NAME,
                "source": source,
                "description": DESCRIPTION,
                "version": PLUGIN_VERSION,
                "author": author,
                "category": PLUGIN_CATEGORY,
                "keywords": KEYWORDS,
            }
        ],
    }
    codex_marketplace: dict[str, object] = {
        "name": MARKETPLACE_NAME,
        "interface": {"displayName": PLUGIN_TITLE},
        "plugins": [
            {
                "name": PLUGIN_NAME,
                "source": {"source": "local", "path": source},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": PLUGIN_CATEGORY,
            }
        ],
    }
    return {
        Path(".claude-plugin/marketplace.json"): Artifact(dump_json(claude_marketplace)),
        Path(".agents/plugins/marketplace.json"): Artifact(dump_json(codex_marketplace)),
        AGY_MANIFEST_REL: Artifact(dump_json(agy_plugin)),  # instal agy dari URL GitHub memakai akar repo
        PLUGIN_REL / ".claude-plugin/plugin.json": Artifact(dump_json(claude_plugin)),
        PLUGIN_REL / ".codex-plugin/plugin.json": Artifact(dump_json(codex_plugin)),
        PLUGIN_REL / AGY_MANIFEST_REL: Artifact(dump_json(agy_plugin)),
        PLUGIN_REL / "README.md": Artifact(plugin_readme(registry).encode("utf-8")),
    }


def build_artifacts() -> dict[Path, Artifact]:
    """Kumpulkan semua berkas turunan (path relatif terhadap akar repo)."""
    registry = load_registry()
    skill_dirs = validate_skills(registry)
    return {**skill_artifacts(skill_dirs), **manifest_artifacts(registry)}


def stale_files(expected: dict[Path, Artifact]) -> list[Path]:
    """Berkas di plugins/<nama>/ yang tidak lagi dihasilkan oleh sumber."""
    plugin_dir = ROOT / PLUGIN_REL
    if not plugin_dir.is_dir():
        return []
    return sorted(
        p.relative_to(ROOT)
        for p in plugin_dir.rglob("*")
        if p.is_file() and p.relative_to(ROOT) not in expected
    )


def write_artifacts(expected: dict[Path, Artifact]) -> int:
    """Tulis berkas yang berubah, hapus berkas basi, dan kembalikan jumlah perubahan."""
    changed = 0
    for rel, artifact in sorted(expected.items()):
        target = ROOT / rel
        if target.exists() and target.read_bytes() == artifact.content:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(artifact.content)
        target.chmod(0o755 if artifact.executable else 0o644)
        changed += 1
        LOGGER.info("tulis   %s", rel.as_posix())
    for rel in stale_files(expected):
        (ROOT / rel).unlink()
        changed += 1
        LOGGER.info("hapus   %s", rel.as_posix())
    plugin_dir = ROOT / PLUGIN_REL
    for directory in sorted((p for p in plugin_dir.rglob("*") if p.is_dir()), reverse=True):
        if not any(directory.iterdir()):
            directory.rmdir()
    return changed


def check_artifacts(expected: dict[Path, Artifact]) -> int:
    """Bandingkan berkas turunan dengan sumber; kembalikan jumlah ketidaksesuaian."""
    drift = 0
    for rel, artifact in sorted(expected.items()):
        target = ROOT / rel
        if not target.exists():
            LOGGER.error("hilang  %s", rel.as_posix())
            drift += 1
        elif target.read_bytes() != artifact.content:
            LOGGER.error("beda    %s", rel.as_posix())
            drift += 1
    for rel in stale_files(expected):
        LOGGER.error("basi    %s", rel.as_posix())
        drift += 1
    return drift


def write_zip(expected: dict[Path, Artifact]) -> Path:
    """Kemas isi plugin (manifest di akar ZIP) untuk unggah manual lewat admin claude.ai.

    Stempel waktu dan urutan berkas tetap agar ZIP identik di setiap build.
    """
    out_dir = ROOT / "dist-plugin"
    out_dir.mkdir(exist_ok=True)
    target = out_dir / f"{PLUGIN_NAME}-{PLUGIN_VERSION}.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for rel, artifact in sorted(expected.items()):
            if PLUGIN_REL not in rel.parents:
                continue
            info = zipfile.ZipInfo(rel.relative_to(PLUGIN_REL).as_posix(), ZIP_EPOCH)
            info.external_attr = (0o755 if artifact.executable else 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, artifact.content)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="hanya periksa sinkronisasi, jangan menulis")
    parser.add_argument("--zip", action="store_true", help="kemas juga ZIP plugin ke dist-plugin/")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    try:
        expected = build_artifacts()
    except BuildError as exc:
        LOGGER.error("GALAT:\n%s", exc)
        return 1

    if args.check:
        drift = check_artifacts(expected)
        if drift:
            LOGGER.error("%d berkas tidak sinkron. Jalankan: python scripts/build_plugins.py", drift)
            return 1
        LOGGER.info("Plugin sinkron dengan skills/ (%d berkas).", len(expected))
        return 0

    changed = write_artifacts(expected)
    LOGGER.info("Selesai: %d berkas diperbarui, %d berkas dikelola.", changed, len(expected))
    if args.zip:
        LOGGER.info("ZIP: %s", write_zip(expected).relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
