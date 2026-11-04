# Panduan Workspace dan Konektor

Konektor (MCP) berbeda tiap akun dan nama alatnya bisa berubah. **Periksa daftar alat yang tersedia di percakapan**, jangan menebak nama alat. Semua langkah di bawah punya jalur manual jika konektor tidak ada.

## Google Drive (disarankan)
| Kebutuhan | Dengan konektor | Tanpa konektor |
|---|---|---|
| Simpan `profile.json`, aset, laporan | Simpan ke folder proyek sesuai `templates/folder-structure.md` | User mengunggah/mengunduh file |
| Cari konten yang sudah ada | Cari folder/berkas dengan kata kunci topik di `02-Aset` dan Content Log | User menempel CSV Content Log atau daftar judul |
| Satu sumber kebenaran | `profile.json` di `00-Brand` dibaca di awal tiap sesi | User mengunggah `profile.json` di awal sesi |

## Google Sheets
- **Content Log** (wajib): tabel semua konten; dibaca untuk cek duplikat dan ditulis saat status berubah.
- **Kalender**: salinan tabel kalender; kolom Status dipakai tim.
- **Insights** dan **Lead Tracker**: tempat data untuk `performance-analyzer` dan `inbound-reply-pack`.
- Jika hanya bisa membaca: ekspor sebagai CSV lalu jalankan skrip.

## Google Calendar
- Event posting (jam sesuai kalender), event produksi batch (blok 2-3 jam), pengingat evaluasi (tiap 4 minggu), dan jadwal konsultasi klien.
- Dari `calendar_export.py` didapat `.ics` yang bisa diimpor tanpa konektor.
- Selalu tampilkan daftar event sebelum membuat dan minta persetujuan; jangan mengundang pihak luar tanpa izin.

## Gmail
- Untuk **draf**: konfirmasi jadwal konsultasi, follow-up, ringkasan setelah konsultasi, laporan mingguan. Jangan mengirim otomatis.
- Gunakan template dari `inbound-reply-pack` dan isi `{...}` lewat `command-filler`.
- Jangan menaruh data sensitif atau kata sandi dalam email.

## Notion
- Cocok untuk papan Kanban konten (status), SOP produksi, dan basis pengetahuan FAQ.
- Properti usulan: Judul, Status, Tanggal terbit, Platform, Format, Pilar, Link aset, Link post, Owner.
- Sinkron dengan Content Log: satu sumber saja yang dianggap utama (disarankan Sheet), yang lain sebagai tampilan.

## Slack (opsional)
- Notifikasi internal: konten siap QA, jadwal besok, pesan lead baru. Kirim hanya ke kanal yang disepakati.

## Urutan prioritas pemasangan
1. Google Drive + Sheets (anti duplikat, penyimpanan)
2. Google Calendar (jadwal)
3. Gmail (draf)
4. Notion / Slack (kolaborasi tim)

## Urutan membaca di awal sesi
1. `profile.json` -> 2. Content Log (30-60 hari terakhir) -> 3. jadwal minggu ini -> 4. lead yang menunggu.
