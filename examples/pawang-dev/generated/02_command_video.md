# Command Video Pawang.dev untuk Google Flow

Alur: **gambar dari ChatGPT** (command `/pw-...`) -> **animasikan di Google Flow** (command `/pw-v-...` di file ini).
Semua prompt ada di code block. Ganti isi `{...}` dengan kebutuhan Anda.

---

## Latihan Pertama (5 menit)

1. Di ChatGPT: upload brand board, tempel Brand Lock, lalu buat satu gambar dengan `/pw-mascot` (rasio 9:16, tanpa teks).
2. Unduh gambar sebagai PNG.
3. Di Flow: pilih **Video**, mode **Frames**, seret gambar ke **Add start frame**, lalu tempel prompt `/pw-v-hello` dari file ini.
4. Periksa konsistensi desain dan kewajaran gerakan, lalu lanjut ke command lain.

---

## 0. Setup Sekali per Proyek

### 0.1 Memilih mode di Flow

| Kebutuhan | Mode | Gambar yang diunggah |
|---|---|---|
| Menganimasikan satu gambar | Frames (start frame saja) | 1 gambar sebagai frame awal |
| Gambar A berubah jadi gambar B | Frames (start + end) | 2 gambar |
| Karakter/objek sama di banyak klip | Ingredients | Gambar karakter atau objek kunci (bisa beberapa sudut) |
| Adegan baru tanpa gambar acuan | Text to Video | Tidak ada |

Nama menu bisa berbeda di akun Anda (mis. First Frame / Last Frame). Fiturnya sama.

### 0.2 Character Lock Video (tempel di prompt Ingredients, atau di awal proyek)

```
CHARACTER LOCK - Si Liar
Pertahankan desain Si Liar persis seperti gambar acuan: makhluk berbulu biru malam, syal oranye, tongkat kayu, daun hijau sage; ekspresif, imut, tidak menyeramkan. Jangan ubah warna, proporsi, atau jumlah anggota tubuh.
Gaya visual: flat modern hangat, ilustrasi bersih, sudut membulat, banyak ruang kosong, sedikit tekstur lembut; warna hanya palet brand (Biru Malam #14213D, Api Dupa #FF8A3D, Krem #FFF6E9, Hijau Sage #A7C4A0, Putih Tulang #FAFAF7).
Gerakan: halus, natural, tidak terlalu cepat. Satu aksi utama per klip.
Tanpa teks tambahan di dalam video, tanpa logo yang berubah bentuk, tanpa orang nyata.
```

### 0.3 Rumus Prompt Video

```
[Subjek] + [aksi tunggal] + [kamera] + [lingkungan] + [cahaya] + [gaya] + [audio]
```

### 0.4 Kamus Kamera (pilih satu per klip)

| Istilah | Efek |
|---|---|
| static shot | kamera diam, cocok untuk teks/logo |
| slow push-in | mendekat pelan, fokus emosi |
| slow pull-out | menjauh, mengungkap suasana |
| pan kiri / kanan | menyapu pemandangan |
| orbit pelan | memutar mengelilingi subjek |
| tilt up | menengadah, kesan megah |
| handheld ringan | terasa hidup dan natural |
| over-the-shoulder | melihat dari belakang karakter |

### 0.5 Aturan Emas

- **Satu klip, satu aksi.** Klip pendek (sekitar 4-8 detik) gagal jika terlalu banyak aksi.
- **Prompt melengkapi gambar, bukan menentangnya.** Jangan minta warna atau pose yang berbeda dari gambar acuan.
- **Jangan animasikan teks.** Teks pada video sering berubah bentuk; tambahkan teks dan logo di CapCut/Canva setelah video jadi.
- **Samakan rasio** gambar dan video (9:16 untuk story/Reels, 16:9 untuk YouTube).
- **Sambung adegan** dengan memakai frame terakhir klip sebelumnya sebagai frame awal klip berikutnya.
- Hasil buruk? Ulangi dengan perubahan kecil satu hal saja (kamera, atau aksi), jangan ubah semuanya.

---

## 1. Intro, Outro, dan Identitas

### /pw-v-logoreveal
Logo muncul dengan percikan; cocok untuk intro. Mode: Frames (start: latar kosong Krem, end: gambar logo bersih).

**Prompt:**
```
/pw-v-logoreveal Static shot. Latar Krem bersih, percikan kecil berwarna Api Dupa muncul dari tengah lalu menyatu membentuk logo yang ada di end frame. Gerakan halus dan elegan, cahaya lembut hangat. Tidak ada teks tambahan. Audio: bunyi chime lembut, tanpa musik keras.
```

### /pw-v-outro
Penutup dengan ruang kosong untuk CTA. Mode: Frames (start: gambar penutup).

**Prompt:**
```
/pw-v-outro Si Liar duduk tenang dan melambai ramah ke kamera, latar hutan sage lembut dengan cahaya senja hangat. Slow push-in. Satu gerakan saja: lambaian tangan. Audio: musik akustik pelan dan suara ambient ringan. Sisakan ruang kosong di sepertiga atas untuk teks CTA yang ditambahkan nanti.
```

### /pw-v-hello
Sapaan singkat maskot; cocok untuk test pertama. Mode: Frames (start: gambar maskot menghadap kamera).

**Prompt:**
```
/pw-v-hello Si Liar menyapa kamera: tersenyum, mengangkat satu tangan melambai dua kali, matanya berkedip. Static shot, latar Krem polos, cahaya lembut. Gerakan halus, desain karakter tidak berubah. Audio: suara sapaan ceria singkat atau efek bunyi lucu pelan.
```

---

## 2. Short Video (Reels, TikTok, WA Story)

### /pw-v-reels-hook
Pembuka 3 detik yang menahan penonton. Mode: Frames atau Ingredients, rasio 9:16.

**Prompt:**
```
/pw-v-reels-hook Rasio 9:16. Si Liar tiba-tiba menghadapi spreadsheet kusut, kabel liar, dan notifikasi bertubi-tubi dan menatap kamera dengan ekspresi panik lucu. Slow push-in cepat ke wajahnya. Latar hutan sage lembut dengan cahaya senja hangat dengan palet brand. Cahaya hangat. Audio: efek bunyi singkat yang lucu.
```

### /pw-v-story
Video promo vertikal. Mode: Frames atau Ingredients, rasio 9:16.

**Prompt:**
```
/pw-v-story Rasio 9:16. Si Liar berjalan ke arah kamera di jalan setapak lembut, lalu berhenti dan menunjuk ke atas tempat teks akan ditambahkan nanti. Slow pull-out. Latar hutan sage lembut dengan cahaya senja hangat. Sisakan sepertiga atas kosong untuk judul dan sepertiga bawah kosong untuk tombol CTA. Audio: musik ceria pelan.
```

### /pw-v-loop
Latar animasi berulang tanpa karakter. Mode: Text to Video atau Frames.

**Prompt:**
```
/pw-v-loop Latar animasi berulang tanpa karakter: elemen dekoratif khas Pawang.dev melayang pelan di atas Krem #FFF6E9, bergerak halus. Static shot, gerakan sangat lembut dan merata sehingga awal dan akhir terlihat sama. Tanpa teks. Audio: tanpa suara.
```

### /pw-v-dialog
Maskot berbicara (audio dihasilkan model; periksa hasilnya). Mode: Frames atau Ingredients.

**Prompt:**
```
/pw-v-dialog Close-up Si Liar menghadap kamera, mulut bergerak natural saat berbicara, ekspresi hangat. Ia berkata dengan suara ramah dan tenang: "{kalimat maks 12 kata}". Static shot, latar Krem polos, cahaya lembut. Audio: suara karakter jelas, tanpa musik.
```

---

## 3. Cerita dan Penjelasan

### /pw-v-cerita
Cerita pendek 4 adegan; buat gambar tiap adegan lebih dulu. Mode: Ingredients (agar karakter/objek konsisten).

**Perencanaan adegan (tempel di ChatGPT atau catatan Anda):**
```
/pw-v-cerita Rencanakan cerita 4 adegan, masing-masing 1 klip, tema: "{tema, mis. Si Liar menjinakkan data bisnis yang kacau}".
Adegan 1 - Masalah: {kekacauan terlihat}
Adegan 2 - Menemukan solusi: {tokoh menemukan solusi}
Adegan 3 - Penyelesaian: {proses menyelesaikan}
Adegan 4 - Hasil: {rapi dan tenang}
Untuk tiap adegan berikan: (a) prompt gambar untuk ChatGPT, (b) prompt gerakan untuk Flow, (c) satu kalimat narasi opsional. Gunakan Brand Lock dan Visual Lock.
```

**Prompt Flow per adegan:**
```
/pw-v-cerita Adegan {nomor}. Si Liar {aksi tunggal}. Kamera {static / slow push-in / pan kanan}. Latar {tempat}. Cahaya {pagi hangat / senja lembut}. Pertahankan desain persis seperti gambar acuan. Audio: {efek bunyi / musik pelan / narasi: "..."}.
```

### /pw-v-penjelasan
Penjelasan layanan: dari kekacauan ke rapi. Mode: Frames atau Ingredients.

**Prompt:**
```
/pw-v-penjelasan Si Liar berdiri di depan layar besar berisi spreadsheet kusut, kabel liar, dan notifikasi bertubi-tubi. Ia mengetuk layar, dan kekacauan berubah menjadi tampilan rapi dan tenang dengan warna Biru Malam dan Api Dupa. Slow push-in, satu gerakan utama. Cahaya hangat, gaya flat modern hangat, ilustrasi bersih, sudut membulat, banyak ruang kosong, sedikit tekstur lembut. Audio: bunyi "ting" lembut saat berubah.
```

### /pw-v-beforeafter
Transisi dari kondisi kacau ke rapi. Mode: Frames (start: kondisi kacau, end: kondisi rapi).

**Prompt:**
```
/pw-v-beforeafter Transisi mulus dari frame awal ke frame akhir: elemen yang kacau tersusun rapi satu per satu, warna berubah dari abu-krem ke Biru Malam dan Api Dupa cerah. Static shot, gerakan halus dan berurutan, tanpa teks. Audio: bunyi klik lembut berulang lalu chime pelan di akhir.
```

---

## 4. Layanan dan Bukti

### /pw-v-layanan
Tampilkan satu layanan atau produk. Mode: Frames atau Ingredients.

**Prompt:**
```
/pw-v-layanan Si Liar menunjukkan layar laptop berisi tampilan terkait {Pawang Web / Pawang Sheet / Pawang Otomasi / Pawang Rawat}. Tangannya menunjuk bagian penting, layar menyala hangat. Slow push-in ke layar. Latar meja kerja sederhana palet brand. Tanpa teks terbaca di layar (pakai bentuk abstrak). Audio: bunyi klik lembut.
```

### /pw-v-testimoni
Gerakan halus pada kartu testimoni. Mode: Frames (start: gambar kartu dari testimoni).

**Prompt:**
```
/pw-v-testimoni Gerakan sangat halus: bintang Api Dupa berkilau satu per satu, tanda kutip bergerak naik sedikit, Si Liar kecil di pojok mengangguk bangga. Static shot, teks pada kartu tetap diam dan tidak berubah. Audio: chime lembut.
```

### /pw-v-produk
Merchandise atau mockup produk. Mode: Frames (start: gambar mockup).

**Prompt:**
```
/pw-v-produk Orbit pelan mengelilingi {topi / tote bag / ponsel / kemasan} berlogo Pawang.dev di atas meja kayu hangat. Cahaya studio lembut, bokeh latar. Logo tetap tajam dan tidak berubah bentuk. Audio: musik ambient pelan.
```

---

## 5. Perpanjangan dan Penyambungan

### /pw-v-extend
Melanjutkan klip yang sudah bagus. Mode: Extend dari klip sebelumnya.

**Prompt:**
```
/pw-v-extend Lanjutkan klip sebelumnya: {aksi berikutnya yang wajar}, kamera tetap {gaya yang sama}, latar dan cahaya sama persis, desain tidak berubah.
```

### /pw-v-transisi
Menyambung dua adegan berbeda. Mode: Frames (start: frame akhir adegan A, end: frame awal adegan B).

**Prompt:**
```
/pw-v-transisi Transisi halus dari adegan A ke adegan B: {kamera bergerak menembus daun / layar memudar hangat / percikan menutup layar lalu terbuka}. Satu gerakan kamera saja, tanpa perubahan desain.
```

### /pw-v-ganti-sudut
Variasi sudut pandang karakter yang sama. Mode: Ingredients.

**Prompt:**
```
/pw-v-ganti-sudut Si Liar yang sama dari sudut {samping / belakang / atas}, aksi dan pose tetap, latar dan palet sama. Static shot.
```

---

## 6. Paket Kerja Siap Pakai: "Si Liar menjinakkan data bisnis yang kacau" (4 klip)

Pasangan prompt: gambar untuk **ChatGPT**, gerakan untuk **Flow**. Rasio 9:16.

### Adegan 1 - Masalah
ChatGPT:
```
/pw-mascot Si Liar menghadapi spreadsheet kusut, kabel liar, dan notifikasi bertubi-tubi, ekspresi panik lucu, latar Krem polos, tanpa teks, rasio 9:16.
```
Flow:
```
/pw-v-reels-hook Adegan 1. Si Liar menggeleng panik lalu menghela napas, elemen kekacauan bergerak pelan. Slow push-in. Pertahankan desain persis seperti gambar acuan. Audio: efek bunyi sesuai kekacauan.
```

### Adegan 2 - Menemukan solusi
ChatGPT:
```
/pw-mascot Si Liar berdiri di depan cahaya Api Dupa lembut yang menyala sebagai tanda solusi, ekspresi penuh harap, latar hutan sage lembut dengan cahaya senja hangat, rasio 9:16, tanpa teks.
```
Flow:
```
/pw-v-cerita Adegan 2. Cahaya Api Dupa menyala pelan di depan Si Liar, ia mendongak penuh harap. Static shot dengan sedikit push-in. Audio: chime lembut.
```

### Adegan 3 - Penyelesaian
ChatGPT:
```
/pw-mascot Si Liar menyentuh layar besar berisi spreadsheet kusut, kabel liar, dan notifikasi bertubi-tubi yang mulai tertata, rasio 9:16, tanpa teks terbaca.
```
Flow:
```
/pw-v-penjelasan Adegan 3. Si Liar menyentuh layar, kekacauan tersusun menjadi tampilan rapi dan tenang dengan warna Biru Malam dan Api Dupa. Slow push-in. Audio: bunyi klik berurutan lalu "ting".
```

### Adegan 4 - Hasil
ChatGPT:
```
/pw-mascot Si Liar tenang dan tersenyum di samping tampilan rapi dan tenang dengan warna Biru Malam dan Api Dupa, latar hutan sage lembut dengan cahaya senja hangat, rasio 9:16, ruang kosong atas dan bawah untuk teks.
```
Flow:
```
/pw-v-outro Adegan 4. Si Liar tersenyum dan melambai pelan ke kamera, cahaya hangat. Slow pull-out. Audio: musik akustik pelan.
```

Setelah semua klip selesai: gabungkan di CapCut, tambahkan judul "Digitalmu liar? Serahkan ke Pawang." dan CTA "Konsultasi Gratis → pawang.dev" sebagai teks pada editor, bukan di dalam video AI.

---

## 7. Template Isi Cepat

```
/pw-v-{command}
Gambar acuan: {nama file dari ChatGPT}
Mode: {Frames / Ingredients / Text to Video}
Rasio: {9:16 / 16:9}
Subjek: {Si Liar / objek}
Aksi tunggal: 
Kamera: {static / slow push-in / pan / orbit}
Latar & cahaya: 
Audio: {efek / musik / dialog "..." / tanpa suara}
Ruang kosong untuk teks: {atas / bawah / tidak perlu}
```
