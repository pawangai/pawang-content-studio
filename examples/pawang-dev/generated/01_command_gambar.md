# Command Konten Pawang.dev untuk ChatGPT

Cara pakai: upload brand board -> tempel **Brand Lock** (Bagian 0) -> jalankan command dari Bagian 1 dst. Ganti isi `{...}` dengan topik Anda.

---

## 0. Setup Sekali di Awal

### 0.1 Brand Lock (tempel di awal chat, atau simpan di Custom Instructions / Project ChatGPT)

```
BRAND LOCK - Pawang.dev
Selalu ikuti brand board yang saya upload. Jangan mengubah logo, maskot, warna, atau font.

Brand: Pawang.dev
Tagline: "Digitalmu liar? Serahkan ke Pawang."
Karakter brand: tenang, paham, jinak; hangat, ramah, tidak menakut-nakuti dengan istilah teknis.
Maskot: "Si Liar" - makhluk berbulu biru malam, syal oranye, tongkat kayu, daun hijau sage; ekspresif, imut, tidak menyeramkan.

Warna (hanya ini):
- Biru Malam #14213D (utama, tenang, tepercaya)
- Api Dupa #FF8A3D (aksen, CTA, energi)
- Krem #FFF6E9 (latar, ramah)
- Hijau Sage #A7C4A0 (pendukung, segar)
- Putih Tulang #FAFAF7 (teks di latar gelap, bersih)

Tipografi: Plus Jakarta Sans (judul, tebal), Inter (isi).
Logo: huruf P dengan lingkaran oranye dan percikan bintang, wordmark "Pawang" dengan ".dev" lebih kecil di bawah kanan.
Gaya visual: flat modern hangat, ilustrasi bersih, sudut membulat, banyak ruang kosong, sedikit tekstur lembut.
Layanan: Pawang Web, Pawang Sheet, Pawang Otomasi, Pawang Rawat.
Paket: Jinak (hijau), Piawai (oranye), Sakti (ungu).
CTA standar: "Konsultasi Gratis → pawang.dev"
Bahasa: Indonesia santai-profesional, kalimat pendek.

Aturan teks pada gambar:
- Tulis teks seminimal mungkin, besar, dan terbaca.
- Eja persis seperti yang saya berikan. Jangan menambah/mengubah kata.
- Jaga margin aman 6% dari tepi.
- Jangan pakai warna di luar palet.
```

### 0.2 Aturan Ukuran

| Platform / Kebutuhan | Rasio | Piksel |
|---|---|---|
| IG Post / Carousel | 4:5 | 1080x1350 |
| IG Story / WA Status / Reels cover | 9:16 | 1080x1920 |
| X / Twitter post | 16:9 | 1600x900 |
| X header | 3:1 | 1500x500 |
| Pinterest Pin | 2:3 | 1000x1500 |
| LinkedIn post | 1.91:1 | 1200x627 |
| Facebook post | 1.91:1 | 1200x630 |
| Threads post | 4:5 | 1080x1350 |
| LinkedIn banner | 4:1 | 1584x396 |
| OG Image / Link preview | 1.91:1 | 1200x630 |
| Feature image artikel | 16:9 | 1600x900 |
| YouTube thumbnail | 16:9 | 1280x720 |
| Logo / foto profil / favicon | 1:1 | 1024x1024 |

Catatan: ChatGPT membuat gambar dalam rasio terdekat. Jika piksel tidak persis, resize/crop di Canva atau Figma.

### 0.3 Tips Konsistensi

- Selalu upload brand board di chat yang sama sebelum command.
- Carousel: minta **satu slide per permintaan**, lalu ketik "lanjut slide berikutnya, gaya identik".
- Jika teks salah eja: ketik `Perbaiki teks saja menjadi: "{teks benar}". Jangan ubah elemen lain.`
- Hasil bagus: ketik `Pertahankan gaya ini sebagai referensi untuk semua gambar berikutnya.`
- Logo resmi sebaiknya tetap diambil dari file aslinya; AI bisa sedikit mengubah bentuk logo.

---

## 1. Identitas & Aset Brand

### /pw-logo
Logo baru atau variasi logo dari brand board. Ukuran: 1:1 (1024x1024).

**Singkat:**
```
/pw-logo Versi {horizontal / stacked / ikon saja / satu warna / gelap} di latar bersih.
```

**Detail:**
```
/pw-logo Buat ulang logo Pawang.dev sesuai brand board: huruf P dengan lingkaran oranye dan percikan bintang, wordmark "Pawang" dengan ".dev" lebih kecil di bawah kanan. Versi {horizontal}. Latar {Krem #FFF6E9 / Biru Malam #14213D / putih}. Vektor bersih, tepi tajam, proporsi sama persis dengan board, tanpa efek bayangan, ruang bersih di sekeliling logo. Tampilkan juga versi kecil 64px untuk uji keterbacaan.
```

### /pw-favicon
Ikon aplikasi dan favicon. Ukuran: 1:1 (512x512).

**Singkat:**
```
/pw-favicon Ikon aplikasi dan favicon Pawang.dev.
```

**Detail:**
```
/pw-favicon Ikon Pawang.dev di kotak membulat Biru Malam #14213D, elemen utama logo tetap terbaca di ukuran 32px. Tampilkan 3 versi: ikon aplikasi, favicon sederhana, dan versi latar Krem #FFF6E9. Rasio 1:1.
```

### /pw-profil
Foto profil sosmed. Ukuran: 1:1 (1024x1024).

**Singkat:**
```
/pw-profil Foto profil bulat untuk {Instagram / X / LinkedIn / WhatsApp Business}.
```

**Detail:**
```
/pw-profil Foto profil {platform}: logo Pawang.dev di tengah area aman lingkaran, latar {Biru Malam #14213D / Krem #FFF6E9}, tanpa teks tambahan, kontras tinggi, tetap jelas pada ukuran 110px. Rasio 1:1.
```

### /pw-mascot
Maskot dalam pose atau ekspresi baru. Ukuran: 1:1 atau bebas.

**Singkat:**
```
/pw-mascot Si Liar {pose / aksi}.
```

**Detail:**
```
/pw-mascot Si Liar maskot Pawang.dev sedang {memegang laptop / membawa palu perbaikan / mengirim notifikasi}. Pertahankan desain karakter persis seperti board: makhluk berbulu biru malam, syal oranye, tongkat kayu, daun hijau sage; ekspresif, imut, tidak menyeramkan. Ekspresi {senang / bingung / bangga}. Latar {bersih / Krem #FFF6E9 / lanskap lembut}. Gaya flat modern hangat, ilustrasi bersih, sudut membulat, banyak ruang kosong, sedikit tekstur lembut.
```

### /pw-stickerpack
Set stiker WhatsApp/Telegram dari maskot. Ukuran: 1:1 per lembar.

**Singkat:**
```
/pw-stickerpack Set stiker Si Liar untuk balas chat klien.
```

**Detail:**
```
/pw-stickerpack Satu lembar 12 stiker Si Liar dengan ekspresi dan teks pendek: "Siap!", "Tenang", "Sebentar ya", "Beres!", "Mohon maaf", "Halo!", "Mantap", "Revisi?", "Oke", "Cek dulu", "Makasih", "Otw". Setiap stiker terpisah jelas, outline putih tebal, latar bersih, gaya konsisten, teks Plus Jakarta Sans tebal.
```

### /pw-pattern
Pola latar berulang. Ukuran: 1:1 seamless.

**Singkat:**
```
/pw-pattern Pola latar brand.
```

**Detail:**
```
/pw-pattern Pola berulang halus untuk latar memakai elemen khas Pawang.dev (percikan bintang oranye kecil, daun sage, dan siluet P) di atas Krem #FFF6E9, kontras rendah agar teks tetap terbaca. Seamless, rasio 1:1.
```

### /pw-brandboard
Papan identitas brand untuk proyek atau klien lain. Ukuran: 3:2.

**Singkat:**
```
/pw-brandboard Papan identitas brand untuk {proyek / klien}.
```

**Detail:**
```
/pw-brandboard Brand identity board seperti gambar terlampir, tetapi untuk {nama brand}: logo, palet 5 warna dengan kode hex, tipografi, maskot jika ada, nilai brand, mockup ponsel, dan profil Instagram. Tata letak bersih dan rapi.
```

---

## 2. Instagram

### /pw-carousel
Carousel edukasi 7 slide. Jalankan per slide. Ukuran: 4:5 (1080x1350).

**Singkat:**
```
/pw-carousel {topik}. 7 slide, slide 1 dulu.
```

**Detail:**
```
/pw-carousel Topik: "{topik}". Format IG 4:5 (1080x1350). Struktur 7 slide:
1. Hook (judul besar, Si Liar mengintip)
2. Masalah yang dirasakan audiens
3-6. Satu poin per slide, angka besar, judul 5-7 kata, penjelasan maksimal 2 kalimat
7. CTA "Konsultasi Gratis → pawang.dev" dengan Si Liar dan tombol Api Dupa
Latar bergantian Krem dan Biru Malam, aksen Api Dupa, nomor slide kecil di pojok, logo kecil di footer, panah geser di slide 1-6. Buat **slide 1 saja** dulu, lalu tunggu perintah "lanjut slide berikutnya, gaya identik".
```

### /pw-igpost
Post Instagram tunggal. Ukuran: 4:5 (1080x1350).

**Singkat:**
```
/pw-igpost {pesan singkat}.
```

**Detail:**
```
/pw-igpost Post Instagram 4:5. Headline "{headline maks 8 kata}", subteks "{subteks maks 15 kata}". Visual {Si Liar / ilustrasi layanan Pawang}. Latar {Krem / Biru Malam}, aksen Api Dupa, logo kecil di pojok bawah, CTA "pawang.dev".
```

### /pw-igstory
Story Instagram 9:16. Ukuran: 9:16 (1080x1920).

**Singkat:**
```
/pw-igstory {tujuan: promo / tips / testimoni / poll}.
```

**Detail:**
```
/pw-igstory Story Instagram 9:16 (1080x1920) tentang "{pesan}". Judul besar di sepertiga atas, Si Liar di tengah, tombol CTA Api Dupa "{teks CTA}" di sepertiga bawah. Sisakan 250px kosong di atas dan bawah untuk UI Instagram. Latar {Krem / Biru Malam}.
```

### /pw-reelcover
Cover Reels. Ukuran: 9:16 (1080x1920).

**Singkat:**
```
/pw-reelcover {judul reel}.
```

**Detail:**
```
/pw-reelcover Cover Reels 9:16 dengan judul "{judul maks 6 kata}", Si Liar, latar Biru Malam #14213D, teks Putih Tulang dengan satu kata di-highlight Api Dupa. Area aman tengah 1:1 agar tetap terbaca di grid profil.
```

### /pw-highlight
Set ikon highlight story. Ukuran: 1:1 per ikon.

**Singkat:**
```
/pw-highlight Set ikon highlight story.
```

**Detail:**
```
/pw-highlight 6 ikon highlight bulat 1:1: Pawang Web, Pawang Sheet, Pawang Otomasi, Pawang Rawat, Testimoni dan Paket. Ikon minimalis Api Dupa di latar Krem, outline Biru Malam, gaya seragam, tanpa teks panjang.
```

---

## 3. WhatsApp

### /pw-wastory
Status WhatsApp. Ukuran: 9:16 (1080x1920).

**Singkat:**
```
/pw-wastory {promo / info / testimoni}.
```

**Detail:**
```
/pw-wastory Status WhatsApp 9:16 (1080x1920). Pesan: "{pesan maks 12 kata}". Nada hangat dan ramah. Si Liar di bawah, teks besar di atas, tombol "Chat Kami" Api Dupa. Latar Krem, aksen Hijau Sage. Teks sangat besar agar terbaca di layar kecil.
```

### /pw-wacatalog
Gambar katalog WhatsApp Business per layanan. Ukuran: 1:1.

**Singkat:**
```
/pw-wacatalog Gambar produk untuk {Pawang Web, Pawang Sheet, Pawang Otomasi, Pawang Rawat}.
```

**Detail:**
```
/pw-wacatalog Gambar katalog WhatsApp Business 1:1 untuk layanan "{nama layanan}": ikon layanan besar, nama layanan, satu kalimat manfaat "{manfaat}", label paket "{Jinak/Piawai/Sakti}" dengan warna paket (hijau/oranye/ungu). Latar Krem, kartu Putih Tulang membulat.
```

### /pw-wabroadcast
Banner broadcast WhatsApp. Ukuran: 1:1.

**Singkat:**
```
/pw-wabroadcast Banner broadcast untuk {promo}.
```

**Detail:**
```
/pw-wabroadcast Banner broadcast WhatsApp 1:1 dengan judul "{judul}", periode "{tanggal}", satu CTA Api Dupa "Balas Chat Ini", Si Liar. Maksimal 3 baris teks.
```

---

## 4. X (Twitter), LinkedIn, Facebook, Threads

### /pw-xpost
Gambar post X. Ukuran: 16:9 (1600x900).

**Singkat:**
```
/pw-xpost {pesan}.
```

**Detail:**
```
/pw-xpost Gambar post X 16:9 (1600x900). Satu pernyataan kuat: "{kalimat maks 12 kata}". Tipografi besar Plus Jakarta Sans, latar Biru Malam #14213D, kata kunci Api Dupa, Si Liar kecil di pojok kanan bawah, handle "pawang.dev" kecil di kiri bawah.
```

### /pw-xheader
Header profil X. Ukuran: 3:1 (1500x500).

**Singkat:**
```
/pw-xheader Header profil X.
```

**Detail:**
```
/pw-xheader Header X 3:1 (1500x500). Tagline "Digitalmu liar? Serahkan ke Pawang." di kiri-tengah, Si Liar di kanan, latar lembut kombinasi Krem dan Hijau Sage. Jauhkan elemen penting dari area bawah kiri tempat foto profil menimpa.
```

### /pw-xthread
Gambar pembuka thread X. Ukuran: 16:9.

**Singkat:**
```
/pw-xthread {topik}. Gambar pembuka thread.
```

**Detail:**
```
/pw-xthread Gambar pembuka thread X 16:9 berjudul "{judul thread}" dengan label "Thread" dan angka "{jumlah} tips". Si Liar kecil menunjuk judul. Latar Krem #FFF6E9, judul Biru Malam, aksen Api Dupa.
```

### /pw-linkedin
Gambar post LinkedIn. Ukuran: 1.91:1 (1200x627).

**Singkat:**
```
/pw-linkedin {topik profesional}.
```

**Detail:**
```
/pw-linkedin Gambar post LinkedIn 1.91:1 (1200x627). Nada lebih profesional: judul "{judul}", satu data atau angka besar "{angka}", ikon sederhana, logo kecil saja tanpa elemen dekoratif besar. Latar Putih Tulang #FAFAF7, Biru Malam dan aksen Api Dupa.
```

### /pw-linkedinbanner
Banner profil LinkedIn. Ukuran: 4:1 (1584x396).

**Singkat:**
```
/pw-linkedinbanner Banner profil LinkedIn.
```

**Detail:**
```
/pw-linkedinbanner Banner 4:1 (1584x396) dengan layanan atau produk utama (Pawang Web, Pawang Sheet, Pawang Otomasi, Pawang Rawat) sebagai ikon kecil berurutan, tagline di kiri, "pawang.dev" di kanan. Latar Biru Malam #14213D, teks Putih Tulang, aksen Api Dupa. Area kiri bawah dikosongkan untuk foto profil.
```

### /pw-fbpost
Gambar post Facebook. Ukuran: 1.91:1 (1200x630).

**Singkat:**
```
/pw-fbpost {pesan}.
```

**Detail:**
```
/pw-fbpost Gambar post Facebook 1.91:1 (1200x630) dengan satu pesan "{kalimat maks 12 kata}". Si Liar di kanan, teks besar di kiri dengan Plus Jakarta Sans, latar Krem, aksen Api Dupa, logo kecil dan "pawang.dev" di bawah. Margin aman 60px, tidak ada teks penting di tepi.
```

### /pw-threads
Gambar post Threads. Ukuran: 4:5 (1080x1350).

**Singkat:**
```
/pw-threads {pernyataan}.
```

**Detail:**
```
/pw-threads Gambar post Threads 4:5 (1080x1350) dengan satu pernyataan singkat "{kalimat maks 10 kata}" di tengah, tipografi Plus Jakarta Sans besar, latar {Krem / Biru Malam}, satu kata Api Dupa, Si Liar kecil di pojok. Gaya sederhana dan percakapan, bukan iklan.
```

### /pw-fbcover
Cover halaman Facebook. Ukuran: 2.63:1 (820x312).

**Singkat:**
```
/pw-fbcover Cover halaman Facebook.
```

**Detail:**
```
/pw-fbcover Cover Facebook 820x312. Si Liar di kanan, tagline dan CTA "Konsultasi Gratis → pawang.dev" di kiri, latar hangat Krem dan Hijau Sage. Teks di area tengah aman untuk tampilan mobile.
```

---

## 5. Pinterest

### /pw-pin
Pin Pinterest. Ukuran: 2:3 (1000x1500).

**Singkat:**
```
/pw-pin {judul pin}.
```

**Detail:**
```
/pw-pin Pin Pinterest 2:3 (1000x1500). Judul "{judul 6-9 kata}" besar di sepertiga atas, ilustrasi {tema} di tengah, URL "pawang.dev" di bawah. Latar Krem atau Hijau Sage, tipografi tebal, tampak seperti infografis ringan yang ingin disimpan.
```

### /pw-pinchecklist
Pin checklist. Ukuran: 2:3.

**Singkat:**
```
/pw-pinchecklist {topik}. 5 poin.
```

**Detail:**
```
/pw-pinchecklist Pin checklist 2:3 berjudul "{judul}" dengan 5 butir centang Api Dupa: "{poin 1}", "{poin 2}", "{poin 3}", "{poin 4}", "{poin 5}". Kartu Putih Tulang membulat di atas latar Krem, Si Liar kecil mengintip dari pojok.
```

---

## 6. Web, Blog, SEO

### /pw-og
Open Graph image untuk link preview. Ukuran: 1.91:1 (1200x630).

**Singkat:**
```
/pw-og {judul halaman}.
```

**Detail:**
```
/pw-og OG image 1.91:1 (1200x630) untuk halaman "{judul halaman}". Judul maks 8 kata di kiri dengan Plus Jakarta Sans tebal, logo Pawang.dev kecil di kiri atas, Si Liar di kanan bawah, "pawang.dev" di kiri bawah. Latar Biru Malam #14213D dengan teks Putih Tulang dan satu kata Api Dupa. Margin aman 80px karena platform sering memotong tepi.
```

### /pw-feature
Feature image artikel blog. Ukuran: 16:9 (1600x900).

**Singkat:**
```
/pw-feature {judul artikel}.
```

**Detail:**
```
/pw-feature Feature image artikel blog 16:9 (1600x900) berjudul "{judul artikel}". Ilustrasi konseptual {tema artikel} dengan Si Liar sebagai pemandu. Judul besar di sisi kiri maksimal 2 baris, latar {Krem / Biru Malam / Hijau Sage}, aksen Api Dupa. Tanpa teks selain judul dan "pawang.dev". Area tengah aman untuk crop 1:1 dan 4:3.
```

### /pw-feature-notext
Feature image tanpa teks (judul ditambah di CMS). Ukuran: 16:9.

**Singkat:**
```
/pw-feature-notext {tema}.
```

**Detail:**
```
/pw-feature-notext Ilustrasi 16:9 bertema "{tema}" tanpa teks sama sekali. Si Liar dan elemen {laptop / spreadsheet / notifikasi / palu} di sisi kanan, sisi kiri dibiarkan kosong lapang untuk judul. Palet brand, gaya flat modern hangat, ilustrasi bersih, sudut membulat, banyak ruang kosong, sedikit tekstur lembut.
```

### /pw-hero
Ilustrasi hero landing page. Ukuran: 16:9.

**Singkat:**
```
/pw-hero Hero landing page.
```

**Detail:**
```
/pw-hero Ilustrasi hero website 16:9. Si Liar sebagai tokoh utama dalam lanskap lembut bernuansa brand, ruang kosong luas di kiri untuk headline "Digitalmu liar? Serahkan ke Pawang." dan tombol "Konsultasi Gratis". Pencahayaan hangat, kedalaman berlapis, palet brand.
```

### /pw-ads
Banner iklan 3 ukuran. Ukuran: 1:1, 4:5, 9:16.

**Singkat:**
```
/pw-ads Iklan {Meta / Google Display} untuk {layanan}.
```

**Detail:**
```
/pw-ads Buat 3 variasi banner iklan untuk "{layanan}": 1:1, 4:5, dan 9:16. Setiap variasi: satu headline 6 kata, satu manfaat, satu tombol Api Dupa "Konsultasi Gratis". Variasi A fokus masalah, B fokus hasil, C fokus harga/paket. Hanya palet brand, logo kecil, teks minimal agar lolos aturan iklan.
```

---

## 7. Konten Penjualan & Kepercayaan

### /pw-paket
Perbandingan paket. Ukuran: 4:5.

**Singkat:**
```
/pw-paket Perbandingan paket Jinak, Piawai dan Sakti.
```

**Detail:**
```
/pw-paket Infografis 4:5 kolom paket: Jinak (hijau, paket dasar), Piawai (oranye, fitur lebih lengkap) dan Sakti (ungu, custom penuh). Tiap kolom: nama, satu kalimat, 4 poin fitur "{poin}", harga "{harga}". Tandai paket tengah "Paling Dipilih". Kartu membulat, ikon sederhana.
```

### /pw-testimoni
Kartu testimoni. Ukuran: 1:1.

**Singkat:**
```
/pw-testimoni "{kutipan}" - {nama}, {usaha}.
```

**Detail:**
```
/pw-testimoni Kartu testimoni 1:1 dengan kutipan "{kutipan maks 20 kata}", nama "{nama}", usaha "{usaha}", lima bintang Api Dupa. Latar Krem, tanda kutip besar Hijau Sage, Si Liar kecil dengan ekspresi bangga. Foto klien opsional: {pakai / tanpa}.
```

### /pw-beforeafter
Visual sebelum-sesudah. Ukuran: 4:5.

**Singkat:**
```
/pw-beforeafter {kasus}.
```

**Detail:**
```
/pw-beforeafter Visual dua panel 4:5. Kiri "Sebelum": {kondisi kacau, nuansa abu-krem}. Kanan "Sesudah": {kondisi rapi, nuansa Biru Malam dan Api Dupa cerah}. Garis pemisah tengah, label jelas, satu metrik hasil "{mis. hemat 10 jam/minggu}".
```

### /pw-casestudy
Carousel studi kasus 5 slide. Ukuran: 4:5.

**Singkat:**
```
/pw-casestudy {klien/proyek}.
```

**Detail:**
```
/pw-casestudy Carousel 5 slide 4:5 studi kasus "{klien}": (1) judul hasil, (2) masalah, (3) solusi Pawang.dev, (4) hasil dengan angka besar, (5) CTA "Konsultasi Gratis → pawang.dev". Buat slide satu per satu, gaya identik, palet brand.
```

### /pw-promo
Poster promo. Ukuran: 1:1 / 9:16.

**Singkat:**
```
/pw-promo {nama promo, periode}.
```

**Detail:**
```
/pw-promo Poster promo {1:1 / 9:16} "{nama promo}": benefit "{benefit}", periode "{tanggal}", syarat singkat "{syarat}", tombol Api Dupa "Klaim di pawang.dev". Si Liar kecil di pojok. Warna dominan Api Dupa dan Biru Malam, tetap rapi dan tidak ramai.
```

### /pw-faq
Carousel FAQ. Ukuran: 4:5.

**Singkat:**
```
/pw-faq 5 pertanyaan umum klien.
```

**Detail:**
```
/pw-faq Carousel FAQ 4:5. Slide 1 judul "Sering Ditanyakan". Slide 2-6: satu pertanyaan per slide dan jawaban maksimal 25 kata. Pertanyaan: "{Q1}", "{Q2}", "{Q3}", "{Q4}", "{Q5}". Slide terakhir CTA "Konsultasi Gratis → pawang.dev". Gaya identik.
```

### /pw-tips
Kartu tips seri. Ukuran: 1:1.

**Singkat:**
```
/pw-tips {topik}. Tips cepat.
```

**Detail:**
```
/pw-tips Kartu tips 1:1: judul "Tips Pawang #{nomor}", satu tips "{tips maks 18 kata}", ikon sederhana, Si Liar mengacungkan jempol. Seri visual konsisten agar bisa dijadikan template.
```

### /pw-quote
Kartu kutipan. Ukuran: 1:1.

**Singkat:**
```
/pw-quote "{kalimat}".
```

**Detail:**
```
/pw-quote Kartu kutipan 1:1 dengan kalimat "{kalimat}" di tengah, tipografi besar. Opsi kalimat brand: "Karena digital yang jinak adalah digital yang berguna.". Latar Biru Malam #14213D, kata kunci Api Dupa, logo kecil di bawah.
```

### /pw-announce
Visual pengumuman. Ukuran: 1:1 dan 9:16.

**Singkat:**
```
/pw-announce {pengumuman}.
```

**Detail:**
```
/pw-announce Visual pengumuman 1:1 dan 9:16: label "Info" Api Dupa, judul "{judul}", detail satu kalimat, Si Liar kecil. Hangat dan sesuai karakter brand (tenang, paham, jinak; hangat, ramah, tidak menakut-nakuti dengan istilah teknis), bukan formal kaku.
```

---

## 8. Mockup & Presentasi

### /pw-mockup
Mockup produk fotografi. Ukuran: bebas.

**Singkat:**
```
/pw-mockup {topi / kaos / tote bag / kartu nama / ponsel}.
```

**Detail:**
```
/pw-mockup Mockup fotografi produk {merchandise} dengan logo Pawang.dev persis seperti board, bahan {Biru Malam / Krem}, pencahayaan studio lembut, latar kayu hangat, komposisi rapi dengan ruang kosong.
```

### /pw-cardnama
Kartu nama dua sisi. Ukuran: bebas.

**Singkat:**
```
/pw-cardnama Kartu nama untuk {nama, jabatan}.
```

**Detail:**
```
/pw-cardnama Kartu nama dua sisi. Depan: logo di tengah, latar Biru Malam #14213D. Belakang: nama "{nama}", jabatan "{jabatan}", WhatsApp "{nomor}", email "{email}", "pawang.dev", latar Krem #FFF6E9. Tipografi Plus Jakarta Sans + Inter, tata letak lega.
```

### /pw-slide
Template slide presentasi. Ukuran: 16:9.

**Singkat:**
```
/pw-slide Template slide presentasi.
```

**Detail:**
```
/pw-slide Template 16:9 untuk presentasi penawaran: slide judul, agenda, masalah, solusi, paket/harga, studi kasus, penutup. Satu gambar per permintaan, mulai dari slide judul. Latar Krem dan Biru Malam bergantian, Si Liar hanya di slide judul dan penutup.
```

### /pw-ytthumb
Thumbnail YouTube. Ukuran: 16:9 (1280x720).

**Singkat:**
```
/pw-ytthumb {judul video}.
```

**Detail:**
```
/pw-ytthumb Thumbnail YouTube 16:9 (1280x720), maksimal 4 kata besar "{judul}", Si Liar berekspresi kuat di kanan, latar Biru Malam #14213D kontras tinggi, kata utama Api Dupa dengan outline tipis, tanpa elemen kecil yang hilang saat diperkecil.
```

---

## 9. Command Gabungan (Fusion)

**Carousel 4:5 + versi story 9:16 dengan pesan sama:**
```
/pw-carousel /pw-wastory {topik}
```

**OG image dan feature image dari satu judul, gaya seragam:**
```
/pw-og /pw-feature {judul artikel}
```

**Tiga ukuran dari satu pesan untuk multi-platform:**
```
/pw-igpost /pw-xpost /pw-linkedin {pesan}
```

**Kartu testimoni dan versi status WhatsApp:**
```
/pw-testimoni /pw-wastory "{kutipan}"
```

**Poster promo, banner iklan, dan story serangkai:**
```
/pw-promo /pw-ads /pw-igstory {promo}
```

**Maskot baru lalu set stiker bertema sama:**
```
/pw-mascot /pw-stickerpack {tema}
```

Cara pakai fusion: ChatGPT membuat ukuran pertama, lalu balas `lanjut ukuran berikutnya, gaya identik`.

---

## 10. Template Isi Cepat (Salin, Isi, Kirim)

```
/pw-{command}
Topik: 
Judul/headline (maks 8 kata): 
Subteks (maks 15 kata): 
Visual: {Si Liar / ilustrasi layanan Pawang}
Latar: {Krem / Biru Malam / Hijau Sage}
CTA: Konsultasi Gratis → pawang.dev
Platform & rasio: 
```
