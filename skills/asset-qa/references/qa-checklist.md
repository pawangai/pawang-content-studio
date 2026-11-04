# Daftar Periksa QA dan Strategi Perbaikan

## Urutan prioritas
1. **Ejaan dan isi teks** - satu huruf salah pada tagline atau CTA merusak kepercayaan.
2. **Logo dan karakter** - bentuk, warna, jumlah elemen sama dengan acuan.
3. **Anatomi dan objek aneh** - jari, tangan, mata, objek melayang, teks acak.
4. **Zona aman** - tidak ada teks/tombol penting di area tertutup UI aplikasi.
5. **Warna palet** - warna dominan hanya dari palet brand.
6. **Ukuran dan kontras teks** - terbaca di ponsel (tinggi huruf >= 2,5% lebar gambar; kontras >= 3:1 untuk teks besar, 4,5:1 untuk teks kecil).
7. **Rasio dan resolusi** - sesuai tujuan unggah.
8. **Video**: lonjakan mendadak, perubahan karakter, teks berubah bentuk, audio, durasi.

## Cara memeriksa ejaan
Bandingkan kata demi kata dengan teks yang seharusnya. Perhatikan: huruf hilang (Konsultsi), huruf tertukar, tanda baca (->), angka yang dibaca huruf (4 vs A), kapitalisasi, dan kata yang ditambahkan model.

## Strategi perbaikan
| Masalah | Strategi |
|---|---|
| Salah eja pada satu kata | Prompt "Perbaiki teks saja"; jika gagal dua kali, buat gambar tanpa teks dan tambahkan teks di Canva |
| Teks panjang rusak | Pangkas teks; atau buat visual tanpa teks |
| Logo berubah | Unggah logo asli sebagai acuan; atau tempel logo asli di Canva setelah gambar jadi |
| Karakter berubah | Unggah gambar acuan karakter di setiap permintaan; di Flow pakai Ingredients |
| Warna salah | Sebut nama warna dan hex; batasi palet |
| Teks di zona tidak aman | Minta ruang kosong 250 px atas dan 340-450 px bawah, lalu tambahkan teks sendiri |
| Video penuh glitch | Satu aksi, kamera static, klip lebih pendek, gambar awal lebih bersih |
| Teks di video berubah | Buat ulang tanpa teks; tambahkan di CapCut |

## Kapan menyerah dan membuat ulang
- Dua kali perbaikan tidak membuahkan hasil.
- Lebih dari tiga masalah berbeda pada satu gambar.
- Komposisi berubah setiap kali diedit.

## Format laporan
```
Keputusan: layak unggah | perbaiki dulu | buat ulang
Ringkasan: satu kalimat
Tabel temuan: Pemeriksaan | Hasil | Temuan | Perbaikan
Prompt perbaikan: code block per masalah
Tidak diperiksa: (jika ada)
```
