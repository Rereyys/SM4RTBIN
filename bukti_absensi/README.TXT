SM4RTBIN ♻️
Sistem Absensi Pemilahan Sampah Berbasis Tim & Bukti Fisik

SM4RTBIN adalah platform digital pos penjagaan pemilahan sampah sekolah inovatif yang menggabungkan verifikasi ganda (dual-auth) petugas serta pencatatan inventaris tong sampah secara real-time. Mengusung estetika antarmuka Cyberpunk Terminal / Retro-Futuristic Dark Tech Mode, sistem ini dirancang untuk memastikan kedisiplinan penuh di lapangan lewat validasi berbasis hardware (RFID & QR Scanner) serta dokumentasi foto bukti fisik terintegrasi.

Tema & Karakteristik UI:

Aplikasi ini dirancang dengan pendekatan visual Cyberpunk Terminal yang unik, memberikan pengalaman layaknya mengoperasikan sistem operasi desktop klasik (.exe) langsung di dalam browser web.

Dark Tech Mode: Menggunakan basis palet warna Navy-Slate gelap (#0f172a) untuk meminimalisir kelelahan mata (eye strain) petugas saat berjaga di area outdoor/indoor dalam durasi lama.
Aksen Neon & Hierarki Visual: Menggunakan warna Emerald Neon untuk status sukses/aktif, Amber untuk langkah pemindaian, dan Rose/Crimson untuk peringatan regulasi.
Draggable Windows: Memanfaatkan JavaScript murni untuk memberikan pengalaman interaktif di mana jendela informasi bantuan dan regulasi dapat digeser (*drag-and-drop*) secara bebas di atas area kerja utama.
Tipografi Terkurasi: Kombinasi font Comfortaa untuk judul jendela, Share Tech Mono untuk visualisasi data/counter digital, dan Plus Jakarta Sans untuk keterbacaan teks utama yang optimal.

Teknologi & Spesifikasi Project

Sistem ini dibangun menggunakan arsitektur web modern yang ringan, responsif, dan mudah diintegrasikan dengan perangkat keras (seperti RFID Reader atau USB Barcode Scanner).

Bahasa Pemrograman & Framework Utama:
Backend: Python 3.x - Bahasa pemrograman utama untuk pengolahan logika data, session management, dan API endpoint.
Web Framework: Django 5.x / 6.x - Framework backend berkemampuan tinggi untuk manajemen database (ORM), keamanan data, dan penyediaan Django Admin Panel yang tangguh.

Frontend & Antarmuka:

CSS Framework: Tailwind CSS - Untuk implementasi utilitas desain utilitas-first yang responsif dan presisi tinggi. Ikonografi: Font Awesome 6.5.1 - Penyedia aset ikon modern berbasis vektor. Scripting: Vanilla JavaScript (ES6+) - Mengatur logika mesin scanner (buffer input keyboard), interaktivitas komponen draggable window, integrasi hardware kamera, dan komunikasi asinkronous (Fetch API).

Alur Kerja Sistem (Workflow)

1. [STEP 01] Registrasi Petugas (Dual-Auth): Petugas 1 memindai kartu RFID miliknya pada alat pembaca, sistem memverifikasi identitas, lalu Petugas 1 memilih peran tugas (Pencatat / Pengawas). Setelah Petugas 1 siap, slot Petugas 2 akan terbuka. Petugas 2 memindai kartu RFID-nya dan memilih peran yang tersisa.
2. Aktivasi Sesi Gabungan:
Setelah kedua petugas terverifikasi, sistem mengaktifkan sesi tim di server dan menyalakan perangkat keras kamera pemantau secara otomatis.
3. [STEP 02] Pemindaian Barcode Tong: Petugas mendata setiap tong sampah yang masuk dengan memindai QR Barcode yang tertempel pada tong. Setiap pemindaian sukses akan menaikkan angka Counter Terdata secara real-time.
4. Penguncian Bukti Fisik & Submit Sesi: Sebelum mengakhiri sesi, petugas wajib menekan tombol "Tangkap Foto Bukti"*\ untuk mengambil dokumentasi fisik area pos jaga menggunakan kamera terintegrasi.
Tombol "Submit Sesi Kerja" akan aktif setelah foto berhasil dikunci. Data dikirim ke server (/api/submit-sesi/), kamera dinonaktifkan, dan browser akan otomatis dialihkan ke halaman "Terima Kasih" sebagai bukti log sukses (SUCCESS_200).