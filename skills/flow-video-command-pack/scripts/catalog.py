"""Katalog command video Google Flow. Token [[X]] diisi dari brand.json; {x} adalah isian user.

Entry: dict(name, desc, mode, requires, blocks, alt)
 - blocks: list[(label, prompt)] dipakai bila brand punya maskot (atau tidak butuh maskot)
 - alt: blocks pengganti bila brand TIDAK punya maskot (None = pakai blocks yang sama)
 - requires: ["mascot"] -> command dilewati bila tidak ada maskot
"""

def E(name, desc, mode, blocks, requires=None, alt=None):
    return dict(name=name, desc=desc, mode=mode, blocks=blocks, requires=requires or [], alt=alt)

SECTIONS = [
("Intro, Outro, dan Identitas", [
 E("logoreveal", "Logo muncul dengan percikan; cocok untuk intro.", "Frames (start: latar kosong [[LIGHT_NAME]], end: gambar logo bersih)",
   [("Prompt", "Static shot. Latar [[LIGHT_NAME]] bersih, percikan kecil berwarna [[ACCENT_NAME]] muncul dari tengah lalu menyatu membentuk logo yang ada di end frame. Gerakan halus dan elegan, cahaya lembut hangat. Tidak ada teks tambahan. Audio: bunyi chime lembut, tanpa musik keras.")]),
 E("outro", "Penutup dengan ruang kosong untuk CTA.", "Frames (start: gambar penutup)",
   [("Prompt", "[[SUBJ]] duduk tenang dan melambai ramah ke kamera, latar [[WORLD]]. Slow push-in. Satu gerakan saja: lambaian tangan. Audio: musik akustik pelan dan suara ambient ringan. Sisakan ruang kosong di sepertiga atas untuk teks CTA yang ditambahkan nanti.")],
   alt=[("Prompt", "Kamera slow pull-out dari {objek utama} ke pemandangan penuh, latar [[WORLD]], cahaya hangat. Satu gerakan kamera saja. Audio: musik akustik pelan. Sisakan ruang kosong di sepertiga atas untuk teks CTA yang ditambahkan nanti.")]),
 E("hello", "Sapaan singkat maskot; cocok untuk test pertama.", "Frames (start: gambar maskot menghadap kamera)",
   [("Prompt", "[[SUBJ]] menyapa kamera: tersenyum, mengangkat satu tangan melambai dua kali, matanya berkedip. Static shot, latar [[LIGHT_NAME]] polos, cahaya lembut. Gerakan halus, desain karakter tidak berubah. Audio: suara sapaan ceria singkat atau efek bunyi lucu pelan.")],
   requires=["mascot"]),
]),
("Short Video (Reels, TikTok, WA Story)", [
 E("reels-hook", "Pembuka 3 detik yang menahan penonton.", "Frames atau Ingredients, rasio 9:16",
   [("Prompt", "Rasio 9:16. [[SUBJ]] tiba-tiba menghadapi [[PROBLEM]] dan menatap kamera dengan ekspresi panik lucu. Slow push-in cepat ke wajahnya. Latar [[WORLD]] dengan palet brand. Cahaya hangat. Audio: efek bunyi singkat yang lucu.")],
   alt=[("Prompt", "Rasio 9:16. Close-up {objek utama} di tengah [[PROBLEM]], kamera slow push-in cepat. Latar [[WORLD]] dengan palet brand. Cahaya hangat. Audio: efek bunyi singkat yang menarik perhatian.")]),
 E("story", "Video promo vertikal.", "Frames atau Ingredients, rasio 9:16",
   [("Prompt", "Rasio 9:16. [[SUBJ]] berjalan ke arah kamera di jalan setapak lembut, lalu berhenti dan menunjuk ke atas tempat teks akan ditambahkan nanti. Slow pull-out. Latar [[WORLD]]. Sisakan sepertiga atas kosong untuk judul dan sepertiga bawah kosong untuk tombol CTA. Audio: musik ceria pelan.")],
   alt=[("Prompt", "Rasio 9:16. {objek utama} di tengah komposisi, kamera slow orbit setengah lingkaran. Latar [[WORLD]]. Sisakan sepertiga atas kosong untuk judul dan sepertiga bawah kosong untuk tombol CTA. Audio: musik ceria pelan.")]),
 E("loop", "Latar animasi berulang tanpa karakter.", "Text to Video atau Frames",
   [("Prompt", "Latar animasi berulang tanpa karakter: elemen dekoratif khas [[BRAND]] melayang pelan di atas [[LIGHT]], bergerak halus. Static shot, gerakan sangat lembut dan merata sehingga awal dan akhir terlihat sama. Tanpa teks. Audio: tanpa suara.")]),
 E("dialog", "Maskot berbicara (audio dihasilkan model; periksa hasilnya).", "Frames atau Ingredients",
   [("Prompt", "Close-up [[SUBJ]] menghadap kamera, mulut bergerak natural saat berbicara, ekspresi hangat. Ia berkata dengan suara ramah dan tenang: \"{kalimat maks 12 kata}\". Static shot, latar [[LIGHT_NAME]] polos, cahaya lembut. Audio: suara karakter jelas, tanpa musik.")],
   requires=["mascot"]),
]),
("Cerita dan Penjelasan", [
 E("cerita", "Cerita pendek 4 adegan; buat gambar tiap adegan lebih dulu.", "Ingredients (agar karakter/objek konsisten)",
   [("Perencanaan adegan (tempel di ChatGPT atau catatan Anda)",
     "Rencanakan cerita 4 adegan, masing-masing 1 klip, tema: \"{tema, mis. [[STORY_THEME]]}\".\nAdegan 1 - Masalah: {kekacauan terlihat}\nAdegan 2 - Menemukan solusi: {tokoh menemukan solusi}\nAdegan 3 - Penyelesaian: {proses menyelesaikan}\nAdegan 4 - Hasil: {rapi dan tenang}\nUntuk tiap adegan berikan: (a) prompt gambar untuk ChatGPT, (b) prompt gerakan untuk Flow, (c) satu kalimat narasi opsional. Gunakan Brand Lock dan Visual Lock."),
    ("Prompt Flow per adegan",
     "Adegan {nomor}. [[SUBJ]] {aksi tunggal}. Kamera {static / slow push-in / pan kanan}. Latar {tempat}. Cahaya {pagi hangat / senja lembut}. Pertahankan desain persis seperti gambar acuan. Audio: {efek bunyi / musik pelan / narasi: \"...\"}.")],
   alt=[("Perencanaan adegan (tempel di ChatGPT atau catatan Anda)",
     "Rencanakan cerita 4 adegan, masing-masing 1 klip, tema: \"{tema, mis. [[STORY_THEME]]}\".\nAdegan 1 - Masalah: {kekacauan terlihat}\nAdegan 2 - Menemukan solusi: {momen penemuan}\nAdegan 3 - Penyelesaian: {proses menyelesaikan}\nAdegan 4 - Hasil: {rapi dan tenang}\nUntuk tiap adegan berikan: (a) prompt gambar untuk ChatGPT, (b) prompt gerakan untuk Flow, (c) satu kalimat narasi opsional. Gunakan Brand Lock dan Visual Lock."),
    ("Prompt Flow per adegan",
     "Adegan {nomor}. {objek utama} {aksi tunggal}. Kamera {static / slow push-in / pan kanan}. Latar {tempat}. Cahaya {pagi hangat / senja lembut}. Pertahankan desain persis seperti gambar acuan. Audio: {efek bunyi / musik pelan / narasi: \"...\"}.")]),
 E("penjelasan", "Penjelasan layanan: dari kekacauan ke rapi.", "Frames atau Ingredients",
   [("Prompt", "[[SUBJ]] berdiri di depan layar besar berisi [[PROBLEM]]. Ia mengetuk layar, dan kekacauan berubah menjadi [[SOLUTION]]. Slow push-in, satu gerakan utama. Cahaya hangat, gaya [[STYLE]]. Audio: bunyi \"ting\" lembut saat berubah.")],
   alt=[("Prompt", "Layar besar berisi [[PROBLEM]] berubah menjadi [[SOLUTION]] dalam satu gerakan halus. Slow push-in, satu gerakan utama. Cahaya hangat, gaya [[STYLE]]. Audio: bunyi \"ting\" lembut saat berubah.")]),
 E("beforeafter", "Transisi dari kondisi kacau ke rapi.", "Frames (start: kondisi kacau, end: kondisi rapi)",
   [("Prompt", "Transisi mulus dari frame awal ke frame akhir: elemen yang kacau tersusun rapi satu per satu, warna berubah dari abu-krem ke [[DARK_NAME]] dan [[ACCENT_NAME]] cerah. Static shot, gerakan halus dan berurutan, tanpa teks. Audio: bunyi klik lembut berulang lalu chime pelan di akhir.")]),
]),
("Layanan dan Bukti", [
 E("layanan", "Tampilkan satu layanan atau produk.", "Frames atau Ingredients",
   [("Prompt", "[[SUBJ]] menunjukkan layar laptop berisi tampilan terkait {[[SERVICES_LIST]]}. Tangannya menunjuk bagian penting, layar menyala hangat. Slow push-in ke layar. Latar meja kerja sederhana palet brand. Tanpa teks terbaca di layar (pakai bentuk abstrak). Audio: bunyi klik lembut.")],
   alt=[("Prompt", "Close-up {[[SERVICES_LIST]]} dalam penggunaan nyata, tangan menyentuh bagian penting. Slow push-in. Latar sederhana palet brand. Tanpa teks terbaca di layar atau kemasan. Audio: bunyi lembut sesuai aksi.")]),
 E("testimoni", "Gerakan halus pada kartu testimoni.", "Frames (start: gambar kartu dari testimoni)",
   [("Prompt", "Gerakan sangat halus: bintang [[ACCENT_NAME]] berkilau satu per satu, tanda kutip bergerak naik sedikit, [[SUBJ]] kecil di pojok mengangguk bangga. Static shot, teks pada kartu tetap diam dan tidak berubah. Audio: chime lembut.")],
   alt=[("Prompt", "Gerakan sangat halus: bintang [[ACCENT_NAME]] berkilau satu per satu, tanda kutip bergerak naik sedikit. Static shot, teks pada kartu tetap diam dan tidak berubah. Audio: chime lembut.")]),
 E("produk", "Merchandise atau mockup produk.", "Frames (start: gambar mockup)",
   [("Prompt", "Orbit pelan mengelilingi {topi / tote bag / ponsel / kemasan} berlogo [[BRAND]] di atas meja kayu hangat. Cahaya studio lembut, bokeh latar. Logo tetap tajam dan tidak berubah bentuk. Audio: musik ambient pelan.")]),
]),
("Perpanjangan dan Penyambungan", [
 E("extend", "Melanjutkan klip yang sudah bagus.", "Extend dari klip sebelumnya",
   [("Prompt", "Lanjutkan klip sebelumnya: {aksi berikutnya yang wajar}, kamera tetap {gaya yang sama}, latar dan cahaya sama persis, desain tidak berubah.")]),
 E("transisi", "Menyambung dua adegan berbeda.", "Frames (start: frame akhir adegan A, end: frame awal adegan B)",
   [("Prompt", "Transisi halus dari adegan A ke adegan B: {kamera bergerak menembus daun / layar memudar hangat / percikan menutup layar lalu terbuka}. Satu gerakan kamera saja, tanpa perubahan desain.")]),
 E("ganti-sudut", "Variasi sudut pandang karakter yang sama.", "Ingredients",
   [("Prompt", "[[SUBJ]] yang sama dari sudut {samping / belakang / atas}, aksi dan pose tetap, latar dan palet sama. Static shot.")],
   requires=["mascot"]),
]),
]

SHOT_FORMULA = "[Subjek] + [aksi tunggal] + [kamera] + [lingkungan] + [cahaya] + [gaya] + [audio]"

CAMERA = [
("static shot", "kamera diam, cocok untuk teks/logo"),
("slow push-in", "mendekat pelan, fokus emosi"),
("slow pull-out", "menjauh, mengungkap suasana"),
("pan kiri / kanan", "menyapu pemandangan"),
("orbit pelan", "memutar mengelilingi subjek"),
("tilt up", "menengadah, kesan megah"),
("handheld ringan", "terasa hidup dan natural"),
("over-the-shoulder", "melihat dari belakang karakter"),
]

MODES = [
("Menganimasikan satu gambar", "Frames (start frame saja)", "1 gambar sebagai frame awal"),
("Gambar A berubah jadi gambar B", "Frames (start + end)", "2 gambar"),
("Karakter/objek sama di banyak klip", "Ingredients", "Gambar karakter atau objek kunci (bisa beberapa sudut)"),
("Adegan baru tanpa gambar acuan", "Text to Video", "Tidak ada"),
]

RULES = [
"**Satu klip, satu aksi.** Klip pendek (sekitar 4-8 detik) gagal jika terlalu banyak aksi.",
"**Prompt melengkapi gambar, bukan menentangnya.** Jangan minta warna atau pose yang berbeda dari gambar acuan.",
"**Jangan animasikan teks.** Teks pada video sering berubah bentuk; tambahkan teks dan logo di CapCut/Canva setelah video jadi.",
"**Samakan rasio** gambar dan video (9:16 untuk story/Reels, 16:9 untuk YouTube).",
"**Sambung adegan** dengan memakai frame terakhir klip sebelumnya sebagai frame awal klip berikutnya.",
"Hasil buruk? Ulangi dengan perubahan kecil satu hal saja (kamera, atau aksi), jangan ubah semuanya.",
]
