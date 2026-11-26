# Plugin Marketplace

Repo ini sekaligus menjadi **marketplace plugin** untuk Claude Code, Codex, Antigravity (`agy`), dan claude.ai/Cowork. Isinya satu plugin, `pawang-content-studio`, yang membungkus ke-14 skill.

| Platform | Berkas katalog / manifest | Identitas |
|---|---|---|
| Claude Code | `.claude-plugin/marketplace.json`, `plugins/pawang-content-studio/.claude-plugin/plugin.json` | `pawang-content-studio@pawang-studio` |
| Codex | `.agents/plugins/marketplace.json`, `plugins/pawang-content-studio/.codex-plugin/plugin.json` | `pawang-content-studio@pawang-studio` |
| Antigravity (`agy`) | `.antigravity-plugin/plugin.json` (akar repo) dan `plugins/pawang-content-studio/.antigravity-plugin/plugin.json` | `pawang-content-studio` |
| claude.ai / Cowork | katalog Claude yang sama (sinkron GitHub) atau ZIP dari `--zip` | `pawang-content-studio` |

## Claude Code

```text
/plugin marketplace add pawangai/pawang-content-studio
/plugin install pawang-content-studio@pawang-studio
```

Uji lokal tanpa memasang: `claude --plugin-dir plugins/pawang-content-studio`. Validasi: `claude plugin validate .`. Skill muncul dengan awalan plugin, misalnya `pawang-content-studio:caption-writer`.

## Codex

```bash
codex plugin marketplace add pawangai/pawang-content-studio
codex plugin add pawang-content-studio@pawang-studio
# perbarui setelah ada rilis baru
codex plugin marketplace upgrade pawang-studio
```

Alternatif lewat antarmuka: buka `/plugins`, pilih marketplace **Pawang Content Studio**, lalu pasang. Checkout sebagian: tambahkan `--sparse .agents/plugins --sparse plugins`. Untuk uji lokal, arahkan ke folder hasil clone: `codex plugin marketplace add ./pawang-content-studio`.

## Antigravity (`agy`)

```bash
# dari GitHub
agy plugin install https://github.com/pawangai/pawang-content-studio

# dari clone lokal
agy plugin validate ./plugins/pawang-content-studio
agy plugin install ./plugins/pawang-content-studio
agy plugin list
```

Skill muncul sebagai `/<nama-skill>`. Tanpa plugin, salin isi `skills/` ke `~/.gemini/config/skills/` (global) atau `<proyek>/.agents/skills/` (per proyek).

## claude.ai

- **Akun pribadi**: unggah per skill dari `dist/*.skill` (lihat README bagian 4).
- **Team/Enterprise (pemilik organisasi)**: buka *Organization settings > Plugins & skills > Marketplaces*, tambahkan repo ini lewat **Sync from GitHub** (`pawangai/pawang-content-studio`), lalu atur ketersediaan plugin per grup. Cowork dan Skills harus aktif, dan Claude GitHub App harus terpasang pada repo. Sinkron membaca `.claude-plugin/marketplace.json`; sumber relatif `./plugins/...` didukung penuh.
- **Tanpa GitHub**: jalankan `python scripts/build_plugins.py --zip`, lalu unggah `dist-plugin/pawang-content-studio-<versi>.zip` lewat unggahan plugin manual di halaman admin yang sama. ZIP ini tidak di-commit (`*.zip` ada di `.gitignore`).

## Memperbarui dan merilis

`plugins/` adalah **hasil generasi**. Jangan edit berkas di dalamnya; ubah `skills/` atau konstanta di `scripts/build_plugins.py` (versi, deskripsi, prompt awal, nama pembuat).

```bash
python scripts/build_all.py            # validasi dan kemas dist/
python scripts/build_plugins.py        # sinkronkan plugins/ dan semua manifest
python scripts/build_plugins.py --check   # exit 1 bila ada berkas yang tidak sinkron (untuk CI)
```

Naikkan `PLUGIN_VERSION` pada setiap rilis agar klien mendeteksi pembaruan, lalu beri tag git yang sama (`v1.1.0`). Catat perubahan memakai Conventional Commits (`feat:` naik minor, `fix:` naik patch).

## Catatan

- Manifest disusun dari dokumentasi resmi masing-masing platform. Validasi dengan CLI-nya sebelum rilis publik: `claude plugin validate .` dan `agy plugin validate --strict ./plugins/pawang-content-studio`.
- `asset-qa` memerlukan paket Python dari `requirements.txt`; skill lain hanya memakai pustaka standar.
- Belum ada berkas `LICENSE`; tentukan lisensi, lalu tambahkan field `license` di `scripts/build_plugins.py` sebelum publikasi terbuka.
