# Katalog Skill

Empat belas skill, urut sesuai tahap alur. Kolom "Skrip" menunjukkan bagian yang dikerjakan skrip (deterministik dan bisa diuji); sisanya adalah penilaian Claude.

| # | Skill | Tahap | Fungsi singkat |
|---|---|---|---|
| 0 | `content-pipeline` | pengarah | memilih skill per tahap, anti duplikat, Content Log, Calendar |
| 1 | `brandboard-standard` | identitas | brand board dan Brand Spec standar (16 section) |
| 2 | `brand-profile-builder` | identitas | `profile.json` tunggal, kontras warna, Brand/Voice Lock, ekspor |
| 3 | `brand-command-pack` | perangkat | command gambar untuk ChatGPT |
| 4 | `flow-video-command-pack` | perangkat | command video untuk Google Flow |
| 5 | `content-text-layout-pack` | perangkat | teks, layout, dan waktu untuk Canva/CapCut |
| 6 | `content-calendar-pack` | rencana | jadwal bertanggal, gudang topik |
| 7 | `command-filler` | produksi | mengisi `{...}` pada command |
| 8 | `caption-writer` | produksi | caption per platform |
| 9 | `asset-qa` | kendali mutu | memeriksa gambar dan video, prompt perbaikan |
| 10 | `inbound-reply-pack` | percakapan | balasan komentar, DM, WhatsApp |
| 11 | `performance-analyzer` | belajar | analisis Insights, revisi jadwal |
| 12 | `quora-answer-writer` | produksi | jawaban Quora yang bermanfaat dan jujur |
| 13 | `longform-writer` | produksi | artikel, newsletter, skrip YouTube |

---

## content-pipeline
- **Dipicu oleh**: "mulai dari mana", "langkah selanjutnya", "cek apakah sudah pernah dibuat", menyebut Drive/Sheets/Calendar/Gmail/Notion.
- **Input**: konteks proyek; Content Log; kalender.
- **Output**: rencana per tahap, hasil cek duplikat, baris Content Log, `.ics`.
- **Skrip**: `dedupe_check.py` (kemiripan topik dan hook), `calendar_export.py` (kalender `.md` -> CSV + ICS).
- **Templat**: `content-log.csv`, `insights.csv`, `lead-tracker.csv`, `folder-structure.md`.

## brandboard-standard
- **Dipicu oleh**: "buatkan brand board", "brand guideline", "audit brand board", "samakan formatnya".
- **Input**: nama, tagline, bidang usaha, audiens, tone, preferensi warna.
- **Output**: Brand Spec Markdown (16 section dalam dua cakupan: bertingkat atau lengkap), prompt gambar, checklist QA.
- **Skrip**: tidak ada (menggunakan templat `assets/brand-spec-template.md` dan referensi `references/section-spec.md`).

## brand-profile-builder
- **Dipicu oleh**: "ini brand saya", mengunggah brand board atau logo, mengganti data brand.
- **Input**: Brand Spec, gambar board, atau deskripsi.
- **Output**: `profile.json`, tabel kontras WCAG, Brand Lock, Voice Lock, ekspor ke 8 target (`command-pack`, `flow-video`, `text-layout`, `calendar`, `caption`, `reply`, `quora`, `longform`).
- **Skrip**: `profile.py` (`--example`, `from-spec`, `validate`, `export`, `lock`, `colors`).

## brand-command-pack
- **Dipicu oleh**: "buatkan command untuk ChatGPT", kumpulan prompt gambar.
- **Output**: file `.md` ±40 command `/xx-...` (logo, favicon, maskot, stiker, carousel, story, OG, feature image, X, LinkedIn, Pinterest, iklan, testimoni, mockup), semua di code block.
- **Skrip**: `build_pack.py` + `catalog.py`. Command yang butuh maskot/layanan/paket dilewati otomatis bila tidak ada.

## flow-video-command-pack
- **Dipicu oleh**: "command video", "prompt Google Flow", animasi maskot.
- **Output**: ±16 command `/xx-v-...`, Character/Visual Lock, kamus kamera, paket cerita 4 klip berpasangan dengan prompt gambar.
- **Skrip**: `build_pack.py` + `catalog.py`.

## content-text-layout-pack
- **Dipicu oleh**: "teks apa yang diisi", "layout", "di detik berapa".
- **Output**: aturan teks, layout carousel 7 slide, story, reel detik demi detik, thumbnail, caption dasar, command `/xx-t-...`, langkah Canva dan CapCut.
- **Skrip**: render + lint isi (hook <= 8 kata, teks video <= 6 kata per baris, durasi tampil 1 detik + 0,3 detik per kata).

## content-calendar-pack
- **Dipicu oleh**: "jadwal konten", "posting apa hari ini", "jam posting".
- **Output**: paket ritme (Ringan/Standar), pilar, ritme mingguan, kalender bertanggal, gudang topik, alur batch, command `/xx-j-...`, evaluasi.
- **Skrip**: lint kalender (awal Senin, topik ganda, prefix, jam, porsi pilar).

## command-filler
- **Dipicu oleh**: command dengan `{...}`, "isikan", "lengkapi placeholder".
- **Output**: command siap tempel; daftar `[ISI SENDIRI]`.
- **Skrip**: `fill.py extract` (mengurai isian, batas kata, opsi, data dari user, dukungan kurung bersarang) dan `apply` (menerapkan nilai, memastikan teks di luar kurung tidak berubah).

## caption-writer
- **Dipicu oleh**: "tulis caption", hashtag, alt text.
- **Output**: caption per platform + hashtag + alt text + komentar pertama + alternatif hook.
- **Skrip**: `captions.py` (batas karakter, hook terlihat, jumlah hashtag, link tidak bisa diklik, klaim berlebihan, kemiripan antar-platform).

## asset-qa
- **Dipicu oleh**: mengunggah gambar/video hasil AI dan bertanya "sudah benar belum".
- **Output**: keputusan (layak unggah / perbaiki dulu / buat ulang), tabel temuan, prompt perbaikan.
- **Skrip**: `qa_image.py` (rasio, palet, OCR, zona aman, ukuran dan kontras teks, ejaan), `qa_video.py` (frame, lembar kontak, lonjakan, drift warna, audio, durasi), `logo_compare.py`, `fixprompts.py`.
- **Batas**: OCR hanya bahasa Inggris dan sering salah pada font dekoratif; mata Claude yang menentukan.

## inbound-reply-pack
- **Dipicu oleh**: "balas komentar/DM", "calon klien tanya harga", "follow-up", "ada komplain".
- **Output**: alur 8 tahap, 30+ template, eskalasi, Lead Tracker, command `/xx-b-...`; atau balasan untuk pesan nyata.
- **Skrip**: `build_replies.py` (batas panjang, klaim berlebihan, larangan meminta kata sandi/data pribadi).

## performance-analyzer
- **Dipicu oleh**: data statistik posting, "jam terbaik", "evaluasi 4 minggu".
- **Output**: laporan, saran revisi kalender (JSON), batasan analisis.
- **Skrip**: `analyze.py` (median, sampel kecil, faktor tercampur, pemenang hanya bila selisih >= 1,25x).

## quora-answer-writer
- **Dipicu oleh**: menyebut Quora, menjawab pertanyaan publik demi kredibilitas, mencari pertanyaan yang cocok.
- **Output**: jawaban versi ringkas dan lengkap, ringkasan kebijakan yang dicek (dengan sumber atau pernyataan tidak dapat diverifikasi), daftar yang harus diverifikasi, baris Content Log.
- **Skrip**: `answer_check.py` (panjang, kelangsungan jawaban, jumlah dan posisi tautan, tautan pendek/UTM, nada promosi, klaim berlebihan, pengungkapan hubungan dengan brand, klaim pengalaman, angka tanpa sumber, kemiripan dengan jawaban lama).
- **Prinsip**: tidak ada pengalaman atau kredensial karangan; brand yang disebut harus diungkapkan; satu tautan paling banyak.

## longform-writer
- **Dipicu oleh**: "buatkan artikel", blog, Medium, LinkedIn Article, newsletter, skrip YouTube, riset topik.
- **Output**: berkas `.md` berfront matter (artikel, newsletter) atau skrip bertanda waktu (video), sumber, paket penerbitan (judul, meta, slug, alt text, prompt gambar fitur), rencana daur ulang, baris Content Log.
- **Skrip**: `article_check.py` (judul, meta, slug, H2, keterbacaan, kata kunci, alt text, tautan, angka tanpa sumber, FAQ, pengungkapan AI), `script_check.py` (bab YouTube, kecepatan bicara per bab, hook, CTA, daftar bab untuk deskripsi).
- **Templat**: artikel, newsletter, skrip YouTube.
