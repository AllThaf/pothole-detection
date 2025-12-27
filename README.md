# Pothole Detection System

Sistem deteksi dan pemetaan lubang jalan menggunakan YOLOv8 untuk survei kondisi jalan di Kota Bandung.

**Pengolahan Citra Digital - Politeknik Negeri Bandung | Semester 5 | 2025**

---

## Deskripsi

Proyek ini menggunakan deep learning (YOLOv8) untuk mendeteksi lubang jalan dari video rekaman. Hasil deteksi ditampilkan dalam bentuk website interaktif dengan peta dan statistik.

### Fitur Utama
- Deteksi lubang jalan otomatis dari video
- Klasifikasi tingkat keparahan (kecil, sedang, besar)
- Deduplication (menghindari hitung ganda)
- Export data ke JSON
- Website interaktif dengan peta
- Statistik dan analisis data

---

## Quick Start

### 1. Instalasi Dependencies

```bash
pip install -r requirements.txt
```

### 2. Proses Video

```bash
python process_video.py
```

Masukkan informasi yang diminta:
- Path video (contoh: `sample/vid/pothole1.mp4`)
- Nama jalan (contoh: `Jl. Ir. H. Juanda`)
- Arah perekaman (contoh: `Dago Utara - Dago Selatan`)
- Kota (default: `Bandung`)

### 3. Lihat Hasil di Website

Buka file `web/index.html` di browser atau deploy ke GitHub Pages.

---

## Struktur Proyek

```
pothole-detection/
├── best.pt                    # Model YOLOv8 yang sudah dilatih
├── process_video.py           # Script utama untuk memproses video
├── train.py                   # Script untuk melatih model (opsional)
├── main.py                    # Script lama (sudah tidak digunakan)
├── test.py                    # Script testing (opsional)
├── requirements.txt           # Dependencies Python
├── README.md                  # Dokumentasi ini
│
├── data/                      # Data hasil deteksi (lokal)
│   └── detections.json
│
├── web/                       # Website untuk menampilkan hasil
│   ├── index.html            # Halaman utama website
│   └── data/
│       └── detections.json   # Data untuk website
│
└── sample/                    # Contoh video/gambar untuk testing
    ├── vid/
    └── pict/
```

---

## Cara Penggunaan Detail

### Mode 1: Interactive (Rekomendasi)

Proses satu video secara interaktif:

```bash
python process_video.py
```

Pilih opsi `1` untuk interactive mode, lalu ikuti instruksi.

**Output:**
- Data disimpan ke `data/detections.json`
- Data juga disimpan ke `web/data/detections.json` (jika folder web ada)
- Summary ditampilkan di terminal

### Mode 2: Batch Processing

Untuk memproses banyak video sekaligus, edit file `process_video.py`:

```python
videos_to_process = [
    {
        'video_path': 'sample/vid/pothole1.mp4',
        'street_name': 'Jl. Ir. H. Juanda',
        'direction': 'Dago Utara - Dago Selatan',
        'city': 'Bandung'
    },
    {
        'video_path': 'sample/vid/pothole2.mp4',
        'street_name': 'Jl. Soekarno-Hatta',
        'direction': 'Timur - Barat',
        'city': 'Bandung'
    },
    # Tambahkan video lain...
]
```

Lalu jalankan:

```bash
python process_video.py
```

Pilih opsi `2` untuk batch mode.

---

## Deploy Website

### Opsi 1: Lokal (Testing)

Buka langsung file HTML di browser:

```bash
# Windows
start web/index.html

# Mac/Linux
open web/index.html
```

### Opsi 2: GitHub Pages (Gratis & Online)

1. **Push ke GitHub:**

```bash
git init
git add .
git commit -m "Initial commit - Pothole Detection System"
git branch -M main
git remote add origin https://github.com/USERNAME/pothole-bandung.git
git push -u origin main
```

2. **Aktifkan GitHub Pages:**
   - Buka repository di GitHub
   - Settings -> Pages
   - Source: Deploy from a branch
   - Branch: `main`
   - Folder: `/web`
   - Save

3. **Akses website:**
   - URL: `https://USERNAME.github.io/pothole-bandung/`
   - Website akan update otomatis setiap kali push data baru

### Update Data Setelah Deploy

Setelah memproses video baru:

```bash
git add web/data/detections.json
git commit -m "Update data - Jl. [nama jalan]"
git push
```

Website akan update dalam 1-2 menit!

---

## Format Data

File `detections.json` berisi array of objects dengan struktur:

```json
[
  {
    "jalan": "Jl. Ir. H. Juanda",
    "arah": "Dago Utara - Dago Selatan",
    "kota": "Bandung",
    "tanggal": "2025-01-15",
    "waktu": "14:30:00",
    "total_lubang": 47,
    "durasi_video": 120.5,
    "lubang_per_menit": 23.4,
    "statistik": {
      "kecil": 20,
      "sedang": 18,
      "besar": 9
    },
    "detail_lubang": [
      {
        "id": 1,
        "timestamp": 2.5,
        "frame": 75,
        "confidence": 0.89,
        "area": 3500,
        "severity": "kecil"
      }
      // ... lubang lainnya
    ]
  }
  // ... ruas jalan lainnya
]
```

---

## Tips Perekaman Video

Untuk hasil deteksi terbaik:

1. **Kualitas Video:**
   - Resolusi minimal 720p (1080p lebih baik)
   - Frame rate minimal 30 fps
   - Lighting yang baik (hindari malam hari)

2. **Posisi Kamera:**
   - Dashcam atau pegang di depan kendaraan
   - Arahkan ke jalan (jangan terlalu miring)
   - Tinggi ideal: 1-1.5 meter dari tanah

3. **Kecepatan Kendaraan:**
   - Kecepatan rendah-sedang (20-40 km/jam)
   - Kecepatan terlalu tinggi = lubang bisa terlewat
   - Kecepatan terlalu rendah = file video besar

4. **Durasi:**
   - Rekam per segmen jalan (tidak perlu satu video panjang)
   - Lebih mudah diproses per segmen
   - Bisa parallel processing oleh tim

---

## Troubleshooting

### Error: "Cannot open video"

**Solusi:**
- Pastikan path video benar
- Cek apakah file video corrupt
- Format yang didukung: MP4, AVI, MOV

### Error: "Model file not found"

**Solusi:**
- Pastikan file `best.pt` ada di root directory
- Jika tidak ada, copy dari folder training: `runs/detect/train/weights/best.pt`

### Video proses lambat

**Solusi:**
- Default: proses setiap 10 frame (sudah optimal)
- Untuk lebih cepat, ubah `process_every = 10` menjadi `15` atau `20` di `process_video.py`
- Trade-off: deteksi bisa kurang akurat

### Website tidak menampilkan data

**Solusi:**
- Pastikan file `web/data/detections.json` ada dan valid
- Cek console browser (F12) untuk error
- Pastikan struktur JSON benar

### Duplicate detections (lubang sama terdeteksi berkali-kali)

**Solusi:**
- Sudah ada deduplication otomatis (jarak < 100 pixel)
- Jika masih banyak duplikat, ubah threshold di line:
  ```python
  if dist < 100:  # Ubah nilai ini (misal: 150)
  ```

---

## Workflow untuk Tim

### Pembagian Tugas

**Tim 1: Perekaman Video**
- Rekam video jalan yang ditugaskan
- Format nama file: `{nama_jalan}_{arah}_{tanggal}.mp4`
- Upload ke shared folder

**Tim 2: Processing**
- Proses video menggunakan `process_video.py`
- Cek hasil deteksi (apakah masuk akal)
- Commit data ke GitHub

**Tim 3: Website & Dokumentasi**
- Monitor website setelah update
- Buat laporan/presentasi
- Screenshot dan dokumentasi

### Checklist Jalan yang Disarankan di Bandung

- [ ] Jl. Ir. H. Juanda (2 arah)
- [ ] Jl. Soekarno-Hatta (2 arah)
- [ ] Jl. Dago (2 arah)
- [ ] Jl. Dipatiukur (2 arah)
- [ ] Jl. Pasteur (2 arah)
- [ ] Jl. Cihampelas (2 arah)
- [ ] Jl. Setiabudi (2 arah)
- [ ] Jl. Buah Batu (2 arah)

**Estimasi waktu:**
- Perekaman: 1-2 hari (parallel)
- Processing: 2-3 hari (bisa parallel)
- Deploy & polish: 1 hari

---

## Interpretasi Hasil

### Klasifikasi Severity

- **Kecil** (area < 5000 px²): Lubang kecil, masih bisa dilewati
- **Sedang** (5000-15000 px²): Lubang menengah, perlu hati-hati
- **Besar** (> 15000 px²): Lubang besar, berbahaya

### Metric Penting

- **Total Lubang**: Jumlah total lubang terdeteksi
- **Lubang per Menit**: Density lubang (semakin tinggi = jalan semakin rusak)
- **Rata-rata per Jalan**: Untuk membandingkan kondisi antar jalan

### Contoh Interpretasi

```
Jl. Ir. H. Juanda
- Total: 47 lubang
- Lubang/menit: 23.4
- Interpretasi: Jalan dengan kerusakan tinggi, perlu perbaikan segera

Jl. Dago
- Total: 12 lubang
- Lubang/menit: 6.5
- Interpretasi: Kondisi jalan relatif baik
```

---

## Future Improvements

Fitur yang bisa ditambahkan di masa depan:

- GPS integration untuk koordinat akurat
- Upload video langsung di website
- Estimasi biaya perbaikan
- Export PDF report
- Perbandingan antar waktu (trend analysis)
- Mobile app untuk perekaman
- API untuk integrasi dengan sistem lain

---

## License

MIT License - Copyright (c) 2025

---

## Tim Pengembang

Proyek ini dikembangkan oleh mahasiswa Politeknik Negeri Bandung untuk mata kuliah Pengolahan Citra Digital.

---

## Kontak & Support

Jika ada pertanyaan atau masalah, silakan buat issue di GitHub atau hubungi tim pengembang.

---

**Semoga bermanfaat!**