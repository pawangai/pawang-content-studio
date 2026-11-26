#!/usr/bin/env python3
"""Susun paket balasan komentar, DM, dan WhatsApp (Markdown) dari profil brand, lalu validasi.

Pemakaian:
  python build_replies.py reply.json out.md      # render + validasi
  python build_replies.py --check out.md         # validasi file
  python build_replies.py --example              # contoh reply.json (ekspor profil: profile.py export --for reply)
"""
import json
import re
import sys
from pathlib import Path

LIMIT = {"komentar": 220, "dm": 700, "wa": 900}
SENSITIVE = re.compile(r"\b(password|kata sandi|otp|pin|cvv|ktp|nomor kartu|kode verifikasi)\b", re.I)
ALLOWED_BRACE = {"nama", "usaha", "kebutuhan", "tanggal", "jam", "topik", "layanan", "tautan", "paket", "hari", "masalah", "target"}
DEFAULT_AVOID = ["dijamin", "pasti ", "100%", "terbaik", "nomor 1", "garansi", "instan"]

EXAMPLE = {
    "brand": "Pawang.dev", "prefix": "pw", "address": "Kak", "tone": "tenang, paham, jinak; hangat, ramah",
    "cta": "Konsultasi Gratis -> pawang.dev", "url": "pawang.dev",
    "avoid": ["dijamin", "pasti ", "100%"],
    "services": [{"name": "Pawang Web", "benefit": "website yang jinak: cepat, rapi, mudah diurus"},
                 {"name": "Pawang Sheet", "benefit": "angka berantakan jadi dashboard rapi"},
                 {"name": "Pawang Otomasi", "benefit": "kerja berulang dikerjakan sendiri"},
                 {"name": "Pawang Rawat", "benefit": "setelah proyek selesai, tetap ada yang jaga"}],
    "packages": [{"name": "Jinak", "desc": "paket dasar", "price": ""}, {"name": "Piawai", "desc": "fitur lebih lengkap", "price": ""},
                 {"name": "Sakti", "desc": "custom penuh", "price": ""}],
    "channels": {"platforms": ["instagram", "whatsapp"], "whatsapp": "", "email": "", "booking_url": ""},
    "hours": {"layanan": "Senin-Jumat 09:00-17:00 WIB", "respons_target": "dalam jam kerja secepatnya"},
    "faq": [{"q": "Berapa lama pengerjaan?", "a": ""}],
}


def isi(x, label):
    return x if x else f"[ISI SENDIRI: {label}]"


def tokens(b):
    ch, hr = b.get("channels", {}), b.get("hours", {})
    sv = [s["name"] for s in b.get("services", [])]
    t = {"BRAND": b["brand"], "SAPA": b.get("address", "Kak"), "CTA": b["cta"].replace("->", "\u2192"),
         "URL": b["url"], "WA": isi(ch.get("whatsapp"), "nomor WhatsApp"),
         "BOOKING": isi(ch.get("booking_url"), "tautan booking konsultasi"),
         "HOURS": isi(hr.get("layanan"), "jam layanan"), "RESP": hr.get("respons_target") or "secepatnya di jam kerja",
         "SERVICES": ", ".join(sv) if sv else isi("", "daftar layanan"),
         "EMAIL": isi(ch.get("email"), "email")}
    return t


def scenarios(b, t):
    S = []
    add = lambda *a: S.append(a)
    # (id, kanal, judul, pemicu, [(label, teks)], catatan)
    add("k1", "komentar", "Komentar positif / terima kasih", "Pujian, emoji, terima kasih",
        [("Balasan", "Terima kasih, [[SAPA]]! Senang kalau bermanfaat. Kalau ada pertanyaan, kami di sini.")], "Balas dalam 24 jam; variasikan kata agar tidak terkesan otomatis.")
    add("k2", "komentar", "Pertanyaan di komentar -> pindah ke DM", "Calon klien bertanya hal yang butuh detail",
        [("Balasan", "Pertanyaan bagus, [[SAPA]]. Biar jawabannya pas dengan kondisi usahamu, kami kirim detailnya lewat DM ya.")], "Setelah membalas, kirim DM pembuka (lihat d2).")
    add("k3", "komentar", "Komentar 'INFO' / minta detail", "Komentar berisi kata kunci INFO atau 'mau tau'",
        [("Balasan", "Siap, [[SAPA]]! Detailnya kami kirim ke DM sekarang ya.")], "Kirim DM d3 maksimal beberapa menit setelah balasan.")
    add("k4", "komentar", "Tanya harga di komentar", "'Harganya berapa?'",
        [("Balasan", "Harganya menyesuaikan kebutuhan, [[SAPA]]. Kami kirim gambaran lewat DM ya, supaya tidak salah perkiraan.")], "Jangan sebut angka di publik kecuali kebijakan brand menetapkannya.")
    add("k5", "komentar", "Keluhan / kritik di publik", "Pelanggan atau calon pelanggan kecewa",
        [("Balasan", "Mohon maaf atas ketidaknyamanannya, [[SAPA]]. Kami ingin membantu; boleh kami hubungi lewat DM untuk menelusuri masalahnya?")], "Empati dulu, jangan membela diri atau berdebat; selesaikan di DM lalu perbarui bila perlu.")
    add("k6", "komentar", "Komentar nyinyir / hater", "Sindiran tanpa pertanyaan nyata",
        [("Balasan (jika perlu)", "Terima kasih masukannya, [[SAPA]]. Kalau ada hal spesifik yang bisa kami perbaiki, kami terbuka mendengarnya.")], "Sering paling baik tidak dibalas. Jangan terpancing; sembunyikan hanya bila melanggar aturan komunitas (SARA, spam, ujaran kasar).")
    add("k7", "komentar", "Spam / jualan pihak lain", "Tautan judi, promosi akun lain",
        [("Tindakan", "Tidak dibalas. Sembunyikan atau hapus komentar, laporkan akun bila perlu.")], "Tidak perlu template balasan.")
    # DM / WA
    add("d1", "dm", "Balasan otomatis di luar jam layanan", "Pesan masuk saat tutup",
        [("DM / WA", "Halo, [[SAPA]]! Terima kasih sudah menghubungi [[BRAND]]. Saat ini kami di luar jam layanan ([[HOURS]]). Pesanmu sudah kami terima dan akan kami balas [[RESP]]. Kalau mau, ceritakan singkat kebutuhanmu di sini ya.")],
        "Atur sebagai balasan otomatis/away message. Sebut jam dengan jujur.")
    add("d2", "dm", "Sapaan pertama + pertanyaan kualifikasi", "Pesan pertama di jam layanan",
        [("DM", "Halo {nama}, terima kasih sudah menghubungi [[BRAND]]. Supaya kami bisa bantu dengan tepat, boleh ceritakan: 1) usahanya bergerak di bidang apa, 2) bagian mana yang paling merepotkan sekarang, 3) kapan idealnya mulai berubah?")],
        "Tiga pertanyaan saja, jangan interogasi. Jika sudah jelas dari pesan awal, lewati pertanyaan yang sudah terjawab.")
    add("d3", "dm", "Keyword INFO: ringkasan layanan", "Dari komentar atau story 'INFO'",
        [("DM", "Halo {nama}! Ini ringkasan [[BRAND]]: [[SERVICES]]. Biar rekomendasinya pas, ceritakan dulu kebutuhan atau kendala utamamu. Atau langsung jadwalkan [[CTA]].")],
        "Kirim cepat, lalu tunggu jawaban; jangan mengirim tiga pesan beruntun.")
    for s in b.get("services", []):
        add("l_" + re.sub(r"\W+", "", s["name"].lower()), "dm", f"Tanya tentang {s['name']}", f"Calon klien menanyakan {s['name']}",
            [("DM", f"{s['name']}: {s['benefit']}. Biasanya dipakai ketika {{masalah}}. Kalau mau, kami bantu cek kondisimu dulu lewat konsultasi gratis; cukup balas 'mau' dan kami kirim jadwalnya.")],
            "Ganti {masalah} dengan situasi umum layanan itu; jangan menambah klaim hasil.")
    pk = b.get("packages", [])
    if pk:
        lines = "; ".join(f"{p['name']} ({p.get('desc', '')}): " + isi(p.get("price"), f"harga paket {p['name']}") for p in pk)
        add("d4", "dm", "Tanya paket", "'Paketnya apa saja?'",
            [("DM", f"Ada {len(pk)} paket: {lines}. Biasanya dipilih sesuai kebutuhan dan skala usaha. Mau kami bantu pilihkan setelah tahu kondisinya?")], "Harga hanya dari profil; kosong berarti belum ditetapkan.")
    add("d5", "dm", "Tanya harga", "'Berapa biayanya?'",
        [("DM", "Biayanya tergantung ruang lingkup, {nama}, jadi kami tidak ingin asal menyebut angka. Ceritakan singkat kebutuhanmu, nanti kami kirim gambaran biaya setelah konsultasi gratis. Cocok kalau kita jadwalkan?")],
        "Beri jalan, bukan penolakan. Jika harga paket sudah ditetapkan di profil, sebutkan kisarannya dari d4.")
    add("d6", "dm", "Tanya portofolio / contoh", "'Ada contoh hasilnya?'",
        [("DM", "Ada, {nama}. Contoh kami bisa dilihat di [ISI SENDIRI: tautan portofolio/studi kasus]. Kalau mau, kami carikan contoh yang paling mirip dengan usahamu.")], "Hanya tautkan karya yang boleh ditampilkan.")
    add("d7", "dm", "Tanya durasi pengerjaan", "'Berapa lama jadinya?'",
        [("DM", "Lama pengerjaan tergantung ruang lingkupnya, {nama}. [ISI SENDIRI: kisaran waktu sesuai kebijakan]. Setelah kami paham kebutuhanmu, kami beri perkiraan yang lebih tepat.")], "Jangan menjanjikan tanggal sebelum ruang lingkup jelas.")
    add("d8", "dm", "Minta diskon / nego", "'Bisa kurang?'",
        [("DM", "Terima kasih sudah mempertimbangkan [[BRAND]], {nama}. Untuk saat ini harga mengikuti ruang lingkup. [ISI SENDIRI: kebijakan diskon, jika ada]. Kalau anggaran terbatas, kami bisa bantu menyesuaikan lingkup supaya tetap pas.")],
        "Jangan mengarang promo. Tawarkan penyesuaian lingkup, bukan potongan sembarangan.")
    add("d9", "dm", "Tawarkan konsultasi gratis", "Calon klien tertarik",
        [("DM", "Kalau begitu, yuk jadwalkan [[CTA]], {nama}. Pilih waktu di sini: [[BOOKING]]. Atau balas dengan dua pilihan hari dan jam yang cocok.")], "Satu ajakan, satu tautan.")
    add("d10", "dm", "Konfirmasi jadwal konsultasi", "Jadwal sudah disepakati",
        [("DM", "Beres, {nama}. Konsultasi kita pada {hari}, {tanggal} pukul {jam}. Mohon siapkan gambaran kendala dan, jika ada, contoh file atau tampilan yang dipakai sekarang (tanpa password atau data pribadi). Sampai jumpa!")],
        "Jangan meminta kredensial atau data sensitif sebelum ada kesepakatan dan jalur aman.")
    add("d11", "dm", "Pengingat jadwal", "H-1 atau 1 jam sebelum",
        [("Pengingat H-1", "Halo {nama}, pengingat: besok {jam} kita konsultasi. Kalau perlu ganti waktu, kabari kami ya."),
         ("Pengingat 1 jam", "Halo {nama}, sebentar lagi kita mulai konsultasi pukul {jam}. Tautan/lokasi: [ISI SENDIRI: tautan pertemuan atau lokasi].")],
        "Dua pengingat cukup.")
    add("d12", "dm", "Setelah konsultasi: ringkasan", "Segera setelah konsultasi",
        [("DM", "Terima kasih waktunya, {nama}. Ringkasan: masalah {masalah}, target {target}. Langkah berikutnya dari kami: [ISI SENDIRI: langkah dan tenggat]. Kalau ada yang kurang tepat, kabari saja.")], "Kirim di hari yang sama.")
    add("d13", "dm", "Follow-up bertahap", "Belum ada balasan",
        [("D+1", "Halo {nama}, kami ingin memastikan pesan kemarin sudah terbaca. Kalau masih bingung memulai dari mana, kami siap bantu menjelaskan."),
         ("D+3", "Halo {nama}, kami tambah satu hal yang mungkin berguna: {topik}. Kalau mau dibahas, balas saja ya."),
         ("D+7", "Halo {nama}, ini pesan terakhir dari kami agar tidak mengganggu. Pintu tetap terbuka kapan pun kamu siap: [[CTA]].")],
        "Maksimal tiga kali. Berhenti bila ada penolakan jelas.")
    add("d14", "dm", "Calon klien belum siap / menolak", "'Nanti dulu' atau 'tidak jadi'",
        [("DM", "Tidak masalah sama sekali, {nama}. Terima kasih sudah mampir. Kalau suatu saat butuh, kabari kami; kami siap membantu.")], "Tutup dengan hangat. Catat alasan di daftar lead.")
    add("d15", "dm", "Di luar layanan", "Permintaan yang bukan bidang kami",
        [("DM", "Terima kasih sudah bertanya, {nama}. Untuk hal itu sepertinya di luar bidang kami, jadi kami tidak ingin asal menjawab. Kalau ada kebutuhan di [[SERVICES]], kami senang membantu.")], "Jujur lebih baik daripada menjanjikan yang tidak bisa.")
    add("d16", "dm", "Klien mengirim password / data sensitif", "Pesan berisi kata sandi, OTP, atau data pribadi",
        [("DM", "Terima kasih, {nama}, tapi demi keamanan jangan kirim kata sandi, kode OTP, atau data pribadi lewat chat. Kami tidak memerlukannya sekarang. Kalau nanti butuh akses, kami atur lewat cara yang aman dan resmi.")],
        "Hapus pesan bila memungkinkan dan jangan menyalin ke catatan. Akses akun ditangani lewat prosedur aman yang disepakati.")
    add("d17", "dm", "Komplain / revisi", "Klien tidak puas atau minta perubahan",
        [("DM", "Terima kasih sudah menyampaikan, {nama}, dan mohon maaf atas ketidaknyamanannya. Kami ingin memahami dulu: bagian mana yang belum sesuai? Setelah itu kami kabari langkah perbaikannya [[RESP]].")],
        "Dengar dulu, jangan membela diri, jangan menjanjikan sebelum paham. Eskalasi bila serius (lihat bagian eskalasi).")
    add("d18", "dm", "Terima kasih dan minta ulasan", "Proyek selesai dan klien puas",
        [("DM", "Terima kasih sudah mempercayakan ke [[BRAND]], {nama}. Kalau berkenan, boleh kami minta satu-dua kalimat pengalamanmu untuk testimoni? Kami hanya menampilkannya dengan izinmu.")],
        "Testimoni hanya dari klien nyata dan dengan izin.")
    add("d19", "dm", "Jawab pertanyaan umum (FAQ)", "Pertanyaan yang sering muncul",
        [("DM", f"{{layanan}}: " + "{jawaban singkat dari FAQ}. Kalau mau lebih rinci, kami bisa bantu lewat konsultasi gratis.")],
        "Isi dari daftar FAQ resmi. Untuk jawaban yang belum ada, gunakan [ISI SENDIRI].")
    for f in b.get("faq", []):
        ans = isi(f.get("a"), f"jawaban untuk '{f.get('q')}'")
        add("f_" + re.sub(r"\W+", "", f.get("q", "")[:12].lower()), "dm", f"FAQ: {f.get('q')}", "Pertanyaan umum",
            [("DM", f"{ans}")], "Sumber: FAQ di profil brand.")
    return S


FLOW = [
    ("1. Pesan masuk / komentar", "Tangkap perhatian", "Balas cepat; pindahkan pertanyaan butuh detail ke DM", "Jam layanan: [[RESP]]"),
    ("2. Sapa dan pahami", "Tahu kebutuhan", "Sapaan hangat + 3 pertanyaan kualifikasi (d2)", "Hari yang sama"),
    ("3. Beri gambaran", "Relevan, tidak membanjiri", "Ringkasan layanan yang cocok (d3 / layanan / paket)", "Hari yang sama"),
    ("4. Tawarkan konsultasi", "Satu langkah berikutnya", "Ajak jadwalkan konsultasi gratis (d9)", "Setelah tahap 3"),
    ("5. Jadwalkan dan konfirmasi", "Mengunci waktu", "Konfirmasi (d10) + pengingat H-1 dan 1 jam (d11)", "Tepat waktu"),
    ("6. Konsultasi", "Memahami dan merekomendasikan", "Ringkasan setelah sesi (d12)", "Hari yang sama"),
    ("7. Penawaran dan keputusan", "Kejelasan lingkup", "Kirim penawaran tertulis; follow-up D+1/D+3/D+7 (d13)", "Sesuai kesepakatan"),
    ("8. Setelah proyek", "Hubungan jangka panjang", "Terima kasih dan ulasan (d18); tawarkan perawatan", "Setelah serah terima"),
]

ESCALATE = [
    "Keluhan serius (uang, kehilangan data, ancaman hukum, media): hentikan balasan otomatis, kabari pemilik/penanggung jawab dalam satu jam kerja.",
    "Permintaan harga final, kontrak, atau potongan harga: hanya penanggung jawab yang memutuskan.",
    "Permintaan di luar layanan atau meminta jaminan hasil: jawab jujur, jangan menjanjikan.",
    "Data sensitif (kata sandi, OTP, KTP, kartu): jangan diminta dan jangan disimpan di chat; arahkan ke jalur aman.",
    "Ujaran kasar, SARA, ancaman: jangan dilayani; simpan bukti, sembunyikan/laporkan, kabari penanggung jawab.",
    "Pertanyaan media/jurnalis atau pihak resmi: teruskan ke penanggung jawab.",
]


def fill(text, t):
    return re.sub(r"\[\[([A-Z_]+)\]\]", lambda m: t[m.group(1)], text)


def render(b):
    for k in ("brand", "prefix", "cta", "url"):
        if not b.get(k):
            raise SystemExit(f"reply.json: field wajib '{k}' kosong")
    t = tokens(b)
    pre = "/" + b["prefix"].strip("/-") + "-b-"
    S = scenarios(b, t)
    o, w = [], None
    w = o.append
    w(f"# Paket Balasan {b['brand']}: Komentar, DM, dan WhatsApp\n")
    w("Template siap salin untuk membalas calon klien dari pesan pertama sampai konsultasi. Isi `{...}` dengan data pesan yang sedang dibalas; `[ISI SENDIRI: ...]` adalah data yang harus Anda tentukan lebih dulu.\n")
    w("---\n")
    w("## 1. Prinsip Membalas\n")
    for x in ["**Cepat dan jujur.** Balas di jam layanan; di luar jam, pakai balasan otomatis yang menyebut jam sebenarnya.",
              f"**Hangat, bukan menekan.** Nada brand: {b.get('tone', 'ramah dan profesional')}. Satu ajakan per pesan.",
              "**Pahami dulu, tawarkan kemudian.** Tanyakan kebutuhan sebelum menyebut solusi.",
              "**Tidak mengarang.** Harga, durasi, dan klaim hasil hanya dari kebijakan Anda.",
              "**Pindahkan hal detail dari komentar ke DM**; keluhan selesaikan di DM, bukan berdebat di publik.",
              "**Keamanan data.** Jangan meminta atau menyimpan kata sandi, OTP, KTP, atau nomor kartu lewat chat."]:
        w("- " + x)
    w(f"\nTarget respons (hipotesis awal, sesuaikan kemampuan tim): {t['RESP']}. Jam layanan: {t['HOURS']}.\n")
    w("---\n")
    w("## 2. Alur dari Pesan Pertama sampai Konsultasi\n")
    w("| Tahap | Tujuan | Tindakan | Waktu |\n|---|---|---|---|")
    for r in FLOW:
        w("| " + " | ".join(fill(x, t) for x in r) + " |")
    w("\n---\n")
    n = 2
    for kanal, title in [("komentar", "Template Balasan Komentar Publik (maks. 220 karakter)"), ("dm", "Template DM / WhatsApp")]:
        n += 1
        w(f"## {n}. {title}\n")
        for sid, k, judul, pemicu, variants, catatan in [s for s in S if s[1] == kanal]:
            w(f"### {sid.upper()} - {judul}")
            w(f"Pemicu: {pemicu}.\n")
            for lab, text in variants:
                w(f"**{lab}:**")
                w("```\n" + fill(text, t) + "\n```")
            w(f"Catatan: {catatan}\n")
        w("---\n")
    n += 1
    w(f"## {n}. Eskalasi: Kapan Manusia Harus Turun Tangan\n")
    for x in ESCALATE:
        w("- " + x)
    w("\n---\n")
    n += 1
    w(f"## {n}. Pencatatan Lead\n")
    w("```\nTanggal | Sumber (komentar/DM/WA/story) | Nama | Usaha | Kebutuhan | Layanan diminati | Tahap (1-8) | Jadwal konsultasi | Follow-up berikutnya | Status (baru/proses/menunggu/menang/tidak jadi) | Alasan jika tidak jadi | Catatan\n```\n")
    w("Tinjau tiap minggu: berapa pesan masuk, berapa yang dijadwalkan konsultasi, berapa yang jadi, alasan tidak jadi paling sering. Tanpa data pribadi sensitif di catatan.\n")
    w("---\n")
    n += 1
    w(f"## {n}. Command Pembuat Balasan (jalankan di ChatGPT atau Claude)\n")
    w("Tempel Voice Lock dulu. Command ini membuat balasan khusus untuk pesan yang sedang Anda hadapi.\n")
    cmds = [
        ("balas", "Pesan masuk dari calon klien: \"{tempel pesan}\". Saluran: {komentar / DM Instagram / WhatsApp}. Konteks: {tahap 1-8 dan info yang sudah diketahui}. Tulis 2 pilihan balasan (singkat dan lebih lengkap) sesuai Voice Lock, satu ajakan, tanpa menjanjikan harga/hasil, dan tanpa meminta data sensitif. Tandai [ISI SENDIRI] untuk hal yang harus saya tentukan."),
        ("followup", "Calon klien {nama} terakhir membalas {tanggal} tentang {topik}. Tulis rangkaian follow-up D+1, D+3, D+7 yang hangat, tidak mendesak, dan menambah nilai di tiap pesan. Maksimal 3 pesan."),
        ("komplain", "Pelanggan menulis: \"{tempel keluhan}\". Tulis balasan yang empatik, tidak membela diri, tidak mengaku salah sebelum fakta jelas, dan mengarahkan ke penyelesaian di DM. Beri juga catatan apakah perlu eskalasi."),
        ("ringkas", "Berikut percakapan dengan calon klien: {tempel percakapan}. Ringkas menjadi: kebutuhan, kendala, target, tahap alur (1-8), langkah berikutnya, dan baris catatan lead siap salin ke tabel."),
        ("faq", "Dari daftar pertanyaan yang sering diterima: {tempel pertanyaan}. Tulis jawaban singkat (maksimal 3 kalimat) untuk tiap pertanyaan dengan nada Voice Lock. Jika jawabannya butuh data yang tidak saya berikan, tulis [ISI SENDIRI] dan jangan menebak."),
    ]
    for name, text in cmds:
        w(f"### {pre}{name}")
        w("```\n" + f"{pre}{name} {text}" + "\n```\n")
    w("---\n")
    n += 1
    w(f"## {n}. Daftar Periksa Mingguan\n")
    for x in ["Semua pesan dan komentar sudah dibalas atau dicatat", "Lead yang menunggu sudah di-follow-up sesuai jadwal", "Keluhan sudah selesai atau dieskalasi",
              "Pesan otomatis sesuai jam layanan", "Tidak ada data sensitif tersimpan di catatan", "Alasan 'tidak jadi' dicatat dan dibaca"]:
        w(f"- [ ] {x}")
    return "\n".join(o) + "\n", S, t


def check(md, b=None):
    errs, warns, todo = [], [], []
    if md.count("```") % 2:
        errs.append("Jumlah code fence ganjil.")
    if "[[" in md:
        errs.append("Masih ada token [[...]].")
    avoid = [x.lower() for x in ((b or {}).get("avoid") or DEFAULT_AVOID)]
    # analisis per bagian template
    for sec in re.split(r"^### ", md, flags=re.M)[1:]:
        title = sec.split("\n", 1)[0]
        kanal = "komentar" if re.match(r"K\d", title) else "dm" if re.match(r"(D|L_|F_)", title) else None
        blocks = re.findall(r"```\n(.*?)\n```", sec, re.S)
        if re.match(r"/", title):
            for bl in blocks:
                if not bl.startswith(title.strip()):
                    errs.append(f"{title}: prompt tidak diawali nama command.")
            continue
        if kanal is None:
            continue
        for bl in blocks:
            lim = LIMIT["komentar"] if kanal == "komentar" else LIMIT["dm"]
            clean = re.sub(r"\[ISI SENDIRI[^\]]*\]", "", bl)
            if len(clean) > lim and not bl.startswith("Tidak dibalas"):
                errs.append(f"{title}: {len(clean)} karakter, melebihi {lim}.")
            for m in re.findall(r"\[ISI SENDIRI[^\]]*\]", bl):
                todo.append(f"{title.split(' - ')[0]}: {m}")
            for br in re.findall(r"\{([^{}]+)\}", bl):
                if br.split()[0].lower().strip(",") not in ALLOWED_BRACE and not br.lower().startswith("jawaban"):
                    warns.append(f"{title}: isian {{{br}}} tidak umum; pastikan akan diisi.")
            if SENSITIVE.search(bl) and not re.search(r"jangan|tanpa|tidak (?:perlu|memerlukan)|demi keamanan", bl, re.I):
                errs.append(f"{title}: menyebut data sensitif tanpa larangan; template tidak boleh meminta kredensial/data pribadi.")
            hit = [a.strip() for a in avoid if a in bl.lower() + " "]
            if hit:
                errs.append(f"{title}: kata klaim berlebihan {hit}.")
            if bl.count("!") > 2:
                warns.append(f"{title}: lebih dari 2 tanda seru.")
    return errs, warns, sorted(set(todo))


def main(a):
    if len(a) >= 2 and a[1] == "--example":
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False))
        return 0
    if len(a) == 3 and a[1] == "--check":
        e, w, t = check(Path(a[2]).read_text(encoding="utf-8"))
        print("Galat: " + ("tidak ada" if not e else "\n" + "\n".join("- " + x for x in e)))
        print("Peringatan: " + ("tidak ada" if not w else "\n" + "\n".join("- " + x for x in w)))
        return 1 if e else 0
    if len(a) != 3:
        print(__doc__)
        return 2
    b = json.loads(Path(a[1]).read_text(encoding="utf-8"))
    md, S, t = render(b)
    e, w, todo = check(md, b)
    Path(a[2]).parent.mkdir(parents=True, exist_ok=True)
    Path(a[2]).write_text(md, encoding="utf-8")
    print(f"Ditulis: {a[2]} ({len(S)} skenario)")
    print("Galat: " + ("tidak ada" if not e else "\n" + "\n".join("- " + x for x in e)))
    print("Peringatan: " + ("tidak ada" if not w else "\n" + "\n".join("- " + x for x in w)))
    print(f"Belum diisi (ISI SENDIRI): {len(todo)}")
    for x in todo[:20]:
        print("  - " + x)
    return 1 if e else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
