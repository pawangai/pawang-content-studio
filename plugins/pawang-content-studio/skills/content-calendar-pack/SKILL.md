---
name: content-calendar-pack
description: Buat file Markdown jadwal konten sosial media yang menjawab "posting apa, hari apa, jam berapa, topik apa" — berisi paket ritme (Ringan/Standar), pilar konten, ritme mingguan dengan jam posting WIB, kalender 4+ minggu bertanggal lengkap dengan topik dan command yang dipakai, gudang topik, alur produksi batch, command pembuat jadwal (/prefix-j-...), rencana daur ulang satu topik jadi banyak konten, dan cara evaluasi jam posting. Gunakan skill ini setiap kali user bingung jadwal konten, ingin content calendar/kalender editorial, rencana posting mingguan atau bulanan, ide topik berkelanjutan, jam posting terbaik, atau melanjutkan dari command gambar, video, dan teks (brand-command-pack, flow-video-command-pack, content-text-layout-pack), bahkan jika user tidak menyebut kata "skill" atau "kalender".
---

# Content Calendar Pack

Menghasilkan satu file `.md` yang menyelesaikan masalah "tidak tahu mau posting apa dan kapan": ritme mingguan, kalender bertanggal, topik per hari, dan command yang dipakai di tiap konten. Sambung dengan tiga skill sebelumnya: kolom Command di kalender menunjuk ke `/prefix-...` (gambar), `/prefix-v-...` (video), dan `/prefix-t-...` (teks).

Skrip menghitung tanggal, menyusun tabel, dan melakukan lint. Pekerjaan Anda: memahami brand dan audiens, menentukan pilar, menulis topik yang spesifik, dan menandai yang butuh data nyata.

## Alur kerja

1. **Ambil brand dan konteks**: nama, awalan command, CTA, URL, audiens, platform aktif, dan seberapa banyak waktu tim (menentukan paket Ringan atau Standar). Pakai ulang `brand.json` dari skill sebelumnya bila ada. Jika platform user terbatas (mis. hanya Instagram dan TikTok), **ganti `rhythm` dan `extras`** supaya tidak memuat LinkedIn, X, Pinterest, atau blog yang tidak mereka kelola. Skema: `references/brand-json.md`.
2. **Tentukan tanggal mulai**: Senin terdekat setelah hari ini (cek tanggal hari ini dari konteks percakapan; lint akan menolak awal minggu yang bukan Senin).
3. **Rancang pilar**: lima pilar yang dinamai khas brand (contoh Pawang: Paham, Jinak, Tenang, Si Liar, Ajakan) dengan porsi total 100% (bawaan 35/25/20/15/5). Sesuaikan jika bisnis lebih banyak jualan atau lebih banyak edukasi.
4. **Tulis `weeks_plan`**: tiap minggu satu tema dan baris per hari (`hari`, `topik`, `command`; opsional `pilar`, `format`, `jam`, `platform`, `minimal`). Topik harus spesifik dan bisa dibuat (judul carousel, bukan "konten edukasi"). Sebarkan format, jangan lima carousel berturut-turut. Gunakan momen nyata (musim belanja, awal/akhir bulan) hanya jika relevan.
5. **Verifikasi tanggal penting**: bila memakai hari besar atau tanggal acara, cek dengan pencarian web, atau tandai "verifikasi sendiri" di `momen`. Jangan mengandalkan ingatan untuk tanggal yang bergeser tiap tahun.
6. **Render**: `python scripts/build_pack.py brand.json /mnt/user-data/outputs/<brand>_jadwal_konten.md`. Skrip memvalidasi struktur dan melint kalender: awal bukan Senin, topik duplikat, command tanpa awalan brand, pilar tidak dikenal, jam di luar 06:00-22:30, porsi pilar melenceng lebih dari 15 poin, minggu dengan kurang dari 3 konten minimal. Perbaiki sampai bersih.
7. **Tinjau** kalender seperti editor: apakah beban produksi masuk akal, apakah ada hari tanpa konten yang seharusnya ada, apakah topik testimoni/klaim ditandai butuh data nyata.
8. **Serahkan** dengan `present_files` dan balasan singkat: tanggal mulai, paket, ringkasan tema tiap minggu, asumsi, dan catatan bahwa jam posting adalah hipotesis yang diuji 4 minggu lewat Insights.

## Prinsip

- **Konsisten mengalahkan banyak**: Ringan = 3 konten utama (tanda ★) per minggu; Standar = 5-7. Jangan jadwalkan lebih dari yang bisa diproduksi tim.
- **Jam posting adalah hipotesis.** Sumber publik tentang jam terbaik beragam dan sebagian besar blog, bukan data platform; kesimpulan yang berulang: konten bisnis di hari kerja pagi dan jam istirahat, video pendek siang dan malam. Selalu sertakan cara menguji lewat Insights akun sendiri. Jika user menanyakan jam terbaik terbaru, cari sumber saat ini.
- **Tidak mengarang**: tidak ada angka hasil, testimoni, atau klaim "slot terbatas/diskon" kecuali dari user.
- **Satu topik, banyak konten**: Bagian 8 memuat rencana daur ulang 10 konten agar topik tidak cepat habis.

## File

- `scripts/build_pack.py` - render, validasi, lint (`--example`, `--check`)
- `references/brand-json.md` - skema `brand.json`, aturan menulis `weeks_plan`
