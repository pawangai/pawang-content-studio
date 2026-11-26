---
name: quora-answer-writer
description: Tulis jawaban Quora (dan forum tanya-jawab serupa) yang benar-benar bermanfaat dan jujur untuk membangun kredibilitas brand tanpa spam, mulai dari memilih pertanyaan yang layak dijawab, memeriksa kebijakan terbaru platform, menyusun jawaban langsung ke inti dengan contoh dan langkah, pengungkapan hubungan dengan brand, sampai pemeriksaan otomatis (panjang, jumlah dan posisi tautan, nada promosi, klaim berlebihan, klaim pengalaman, kemiripan dengan jawaban lama). Gunakan setiap kali user menyebut Quora, ingin menjawab pertanyaan publik demi kredibilitas atau trafik, mencari pertanyaan yang cocok dengan keahliannya, atau meminta draf jawaban tanya-jawab, bahkan jika user tidak menyebut kata "skill".
---

# Quora Answer Writer

Jawaban Q&A bekerja karena **membantu**, bukan karena promosi. Skill ini menulis jawaban yang berdiri sendiri sebagai jawaban bagus, lalu memeriksa hal-hal yang biasa membuat jawaban dianggap spam atau tidak jujur.

## Prinsip yang tidak boleh dilanggar

- **Pengalaman dan kredensial hanya yang benar-benar dimiliki user.** Jangan menulis "selama 10 tahun", "500 klien", atau hasil bisnis jika user tidak memberikannya. Tanyakan, atau pakai `[ISI SENDIRI: pengalaman nyata]`.
- **Ungkapkan hubungan dengan brand** bila brand disebut ("Saya bekerja di/mendirikan ..."). Menyamar sebagai pihak ketiga yang tidak terkait adalah menyesatkan.
- **Bantuan AI**: jika kebijakan platform atau komunitas meminta pengungkapan, ikuti. Draf dari skill ini harus dibaca, diverifikasi, dan disunting user sebelum diposting; jangan menempel mentah massal.
- **Tidak ada klaim hasil** ("pasti naik", "dijamin") dan angka tanpa sumber.
- **Satu jawaban, satu pertanyaan.** Jangan menempel jawaban yang sama di banyak pertanyaan.

## Alur kerja

1. **Ambil konteks**: pertanyaan persis (atau topik/keahlian untuk mencari pertanyaan), siapa user dan keahliannya yang nyata (ambil dari `profile.json` bagian `author` bila ada), tujuan (kredibilitas, bukan jualan), bahasa pertanyaan.
2. **Cek kebijakan terbaru** dengan pencarian web sebelum menulis: aturan Quora tentang promosi, tautan, dan konten buatan AI. Ringkas 2-3 poin beserta sumbernya. Jika tidak menemukan sumber resmi, katakan terus terang bahwa tidak dapat memverifikasi dan minta user membaca kebijakan Quora sendiri. Jangan mengandalkan ingatan.
3. **Pilih pertanyaan** (bila user belum punya): relevan dengan keahlian nyata, ditanyakan orang sungguhan, belum punya jawaban lengkap, dan Anda bisa menambah nilai. Lihat `references/quora-guide.md`. Jangan menjawab hal di luar keahlian user.
4. **Susun jawaban** dengan struktur: jawaban inti di kalimat pertama, alasan, contoh atau langkah, batasan atau kapan jawaban tidak berlaku, lalu (hanya bila relevan) satu catatan pengungkapan dan satu tautan yang melengkapi. Beri dua versi: **ringkas** (100-200 kata) dan **lengkap** (250-450 kata).
5. **Periksa**: `python scripts/answer_check.py jawaban.md --question "..." --brand "Nama" [--prior jawaban_lama.md] [--ai-disclosure]`. Perbaiki semua **Galat**; pertimbangkan tiap **Peringatan** (tautan, promosi, pengungkapan, klaim).
6. **Verifikasi klaim**: tandai setiap klaim pengalaman, angka, atau fakta yang harus dikonfirmasi user atau dibuktikan dengan sumber. Gunakan pencarian web untuk fakta yang bisa berubah dan sertakan sumbernya.
7. **Serahkan**: jawaban (code block agar mudah disalin), daftar `[ISI SENDIRI]`, ringkasan kebijakan yang dicek, dan baris untuk **Content Log** (Platform = Quora, Format = Jawaban, Topik = pertanyaan, Hook = kalimat pertama, Link post setelah terbit). Gunakan cek duplikat dari `content-pipeline` agar pertanyaan yang sama tidak dijawab dua kali.

## Format keluaran

```
Pertanyaan: ...
Kebijakan yang dicek: (2-3 poin + sumber, atau "tidak dapat diverifikasi")
Versi ringkas: (code block)
Versi lengkap: (code block)
Yang harus Anda verifikasi/isi: ...
Baris Content Log: ...
```

## File

- `scripts/answer_check.py` - pemeriksa draf jawaban
- `references/quora-guide.md` - cara memilih pertanyaan, struktur jawaban, etika promosi, daftar periksa
