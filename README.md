# VidozaCLI – Alat CLI Python Pengunduh Video Aman Tanpa Iklan

![VidozaCLI - Logo](https://github.com/user-attachments/assets/31e73233-9b37-4729-b4b6-1122434e6ce6)

> **VidozaCLI** adalah alat baris perintah (_CLI tool_) modern untuk mengunduh video dari Videq dan platform serupa tanpa iklan berbahaya, malware, atau gangguan lainnya. Dirancang untuk pengalaman pengguna yang aman, cepat, dan bebas hambatan.

## 📚 Latar Belakang

Platform streaming seperti [`videq.fitm`](https://videq.fitm) sering kali menyajikan konten bermanfaat, namun iklan agresif dan potensi malware dapat mengganggu kenyamanan serta keamanan pengguna. **VidozaCLI** hadir sebagai solusi: mengunduh video langsung tanpa membuka peramban, tanpa iklan, dan tanpa risiko.

Dengan rekayasa permintaan HTTP tingkat lanjut, VidozaCLI meniru interaksi peramban yang sah, melewati mekanisme keamanan sederhana, dan memastikan pengunduhan yang bersih serta efisien.

## ✨ Fitur Utama

- **Pengunduhan Konkuren:** Menggunakan `asyncio` & `aiohttp` untuk unduhan paralel.
- **Lintas Platform:** Kompatibel dengan Linux, Windows, dan macOS.
- **Bebas Iklan & Malware:** Tidak perlu membuka browser, langsung unduh video .mp4.
- **Multi-Tautan:** Bisa unduh banyak video sekaligus dalam satu perintah.
- **Antarmuka Profesional:** Progress bar & logging berwarna untuk setiap unduhan.
- **Penamaan Berkas Otomatis:** Nama file otomatis dari judul video, sudah disanitasi.

## ⚡ Instalasi

> **Persyaratan:** Python 3.8 atau lebih baru.

1. **Kloning Repositori**
   
   ```bash
   git clone https://github.com/RozhakDev/VidozaCLI.git
   cd VidozaCLI
   ```

2. **Instal Dependensi**
   
   ```bash
   pip install -r requirements.txt
   ```

3. **Instalasi Editable (Opsional)**
   
   ```bash
   pip install -e .
   ```

## 🚀 Penggunaan

Setelah instalasi, gunakan perintah `vidozaCLI` atau jalankan modul secara langsung.

### Sintaks Dasar

```bash
vidozaCLI <tautan_1> <tautan_2> ... [opsi]
```

### Contoh

- **Unduh satu video:**
  
  ```bash
  vidozaCLI https://videq.fit/e/z40jeu954mk5
  ```
- **Unduh beberapa video sekaligus:**
  
  ```bash
  vidozaCLI https://videq.fit/e/z40jeu954mk5,https://videq.my/d/z40jeu954mk5
  ```
- **Simpan ke direktori tertentu:**
  
  ```bash
  vidozaCLI https://videq.fit/e/z40jeu954mk5 -o "D:/Koleksi Video/Anime"
  ```
- **Mode verbose untuk debugging:**
  
  ```bash
  vidozaCLI https://videq.fit/e/z40jeu954mk5 -v
  ```

## 🗂️ Struktur Proyek

```text
VidozaCLI/
├── vidoza_downloader/
│   ├── main.py           # Titik masuk CLI & parser argumen
│   ├── downloader.py     # Logika inti pengunduhan
│   ├── network.py        # Pengelola sesi & header HTTP
│   ├── parser.py         # Parsing HTML & Regex
│   ├── logger.py         # Logging kustom
│   └── utils.py          # Utilitas (sanitasi nama file, dll)
├── tests/                # Unit tests
├── pyproject.toml        # Definisi proyek & dependensi
└── README.md             # Dokumentasi ini
```

## ⚠️ Peringatan & Penafian

**Alat ini dibuat murni untuk tujuan edukasi.** Tujuannya adalah untuk mempelajari dan mendemonstrasikan konsep rekayasa permintaan HTTP, _web scraping_, dan pengembangan aplikasi baris perintah (CLI) dengan Python.

Pengguna bertanggung jawab penuh atas penggunaan alat ini. Harap hormati hak cipta dan patuhi syarat & ketentuan dari situs web mana pun yang Anda akses. Pengembang tidak bertanggung jawab atas segala bentuk penyalahgunaan.

## 🤝 Kontribusi

Kami sangat menyambut kontribusi dari komunitas untuk membuat VidozaCLI menjadi lebih baik. Jika Anda menemukan bug, memiliki ide untuk fitur baru, atau ingin menyempurnakan kode, silakan buka _Issue_ untuk mendiskusikannya terlebih dahulu. Untuk kontribusi kode, Anda dapat melakukan _fork_ pada repositori ini, membuat branch baru untuk perubahan Anda, dan kemudian mengirimkan _Pull Request_ dengan deskripsi yang jelas. Setiap bantuan, sekecil apa pun, sangat kami hargai!

## 📄 Lisensi

Proyek ini menggunakan **MIT License**. Lihat [LICENSE](LICENSE) untuk detail.