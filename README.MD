Ini panduan pengembangan website untuk analisa data broker summary sebagai penentu arah selanjutnya dalam menganalisa saham. Kombinasi ini cocok ditambahkan dengan analisa teknikal dan fundamental.
---
### 1. Business Process (Alur Logika)
Tujuan: Mengetahui posisi harga rata-rata Broker X di berbagai saham.

**Input:**
*   Kode Broker (misal: `CC`, `AK`, `BK`).
*   Rentang Tanggal (Start Date - End Date).

**Proses di Backend:**
1.  **Filtering:** Ambil semua transaksi yang dilakukan oleh Broker tersebut dalam rentang tanggal yang dipilih.
2.  **Grouping:** Kelompokkan data berdasarkan Kode Saham (misal: BBRI, BBCA, GOTO).
3.  **Calculation (Bandarmology Logic):**
    *   Hitung **Net Volume** = Volume Beli - Volume Jual.
    *   (Jika Net Volume > 0, berarti Akumulasi).
    *   Hitung **Average Price (AVG):** Total Value Pembelian / Total Volume Pembelian.
4.  **Fetching Current Price:** Ambil harga saham saat ini (Closing Price / Live Price).
5.  **Classification:** Bandingkan `Avg Price Broker` vs `Current Price`.
    *   **Floating Profit (Hijau):** Current Price > Avg Price (Broker untung).
    *   **BEP (Kuning):** Current Price == Avg Price.
    *   **Floating Loss (Merah):** Current Price < Avg Price (Broker nyangkut).

**Output:**
*   Tabel daftar saham yang diakumulasi broker tersebut, diurutkan dari value transaksi terbesar atau status profitabilitas.

---

### 2. Tech Stack
#### Opsi Terbaik: Python + Streamlit
*   **Bahasa:** Python.
*   **Library Data:** Pandas.
*   **Frontend & Server:** **Streamlit**.
*   **Data Fetching:** `yfinance` + Custom API/CSV.
*   **Database:** PostgreSQL atau MySQL.

---

### 3. Ringkasan Fitur untuk User
Agar informasinya "daging" semua, tampilkan kolom ini di website:
1.  **Kode Saham**
2.  **Broker Avg Price** (Harga rata-rata bandar)
3.  **Current Price** (Harga pasar sekarang)
4.  **Selisih (%)** -> (Current - Avg) / Avg.
    *   Jika positif (+): Beri warna Hijau (Indikasi Broker sudah cuan/Floating Profit).
    *   Jika negatif (-): Beri warna Merah (Indikasi Broker nyangkut/Floating Loss -> Potensi *Average Down* atau *Rebound*).
5.  **Total Value Akumulasi** (Seberapa banyak uang yang mereka masukkan).

---

### 4. Alur Pembuatan (Step-by-Step)
#### Fase 1: Persiapan Lingkungan Kerja (Environment Setup)
1.  **Instalasi Python:** Pastikan Python versi terbaru sudah terinstal di komputer.
2.  **Siapkan Virtual Environment:** Buat ruang kerja isolasi agar library tidak bentrok dengan proyek lain.
3.  **Instalasi Library Utama:**
    *   Library untuk membuat tampilan web (Dashboard).
    *   Library untuk pengolahan data tabel/matematika.
    *   Library untuk mengambil harga saham pasar saat ini (Market Data).
    *   Library untuk membaca format JSON.

#### Fase 2: Membangun Antarmuka Input (Frontend Basic)
1.  **Buat Judul & Deskripsi:** Berikan judul halaman yang jelas.
2.  **Buat Area Input JSON:**
    *   Sediakan kolom teks area yang besar (Text Area) di mana user bisa menempelkan (paste) *raw JSON* yang didapat dari network tab.
    *   Opsi alternatif: Tambahkan fitur upload file `.json` atau `.txt` jika teksnya terlalu panjang.
3.  **Tombol Eksekusi:** Buat tombol "Analisa" untuk memicu pemrosesan data setelah JSON dimasukkan.

#### Fase 3: Logika Pemrosesan Data JSON (Backend Logic)
1.  **Validasi Input:**
    *   Buat logika pengecekan: Apakah teks yang dimasukkan user adalah format JSON yang valid? Jika bukan, tampilkan pesan error.
2.  **Navigasi Struktur JSON:**
    *   Identifikasi lokasi data target. Berdasarkan contohmu, target ada di dalam objek `data` -> `broker_summary` -> `brokers_buy`.
3.  **Ekstraksi Data (Parsing):**
    *   Ambil hanya kolom yang diperlukan: `netbs_stock_code` (Kode Saham), `netbs_buy_avg_price` (Harga Rata-rata), dan `bval` (Total Value Pembelian).
    *   Konversi tipe data: Ubah data harga dan value dari *string* (teks) menjadi *float* atau *integer* (angka) agar bisa dihitung.

#### Fase 4: Integrasi Data Harga Pasar (External Data)
*Meskipun data broker manual, harga pembanding (Current Price) harus otomatis agar relevan.*

1.  **Koleksi Daftar Saham:** Kumpulkan semua kode saham unik yang ditemukan dari hasil ekstraksi JSON di Fase 3.
2.  **Request Harga Saham:**
    *   Gunakan library data saham (seperti Yahoo Finance) untuk meminta harga penutupan terakhir (*Last Close*) dari daftar saham tersebut.
    *   Tambahkan penanganan error: Jika ada kode saham yang tidak ditemukan (misal warrant atau kode lama), pastikan program tidak *crash*.
3.  **Penggabungan Data:** Masukkan data "Harga Saat Ini" ke dalam tabel data broker yang sudah dibuat sebelumnya.

#### Fase 5: Analisa & Klasifikasi (The "Bandarmology" Logic)
1.  **Hitung Selisih (Floating P/L):**
    *   Rumus: `(Harga Saat Ini - Harga Rata-rata Broker) / Harga Rata-rata Broker`.
    *   Ubah hasil desimal menjadi format Persentase (%).
2.  **Logika Pengelompokan (Status):**
    *   Tentukan syarat **Profit**: Jika persentase positif (di atas 0%).
    *   Tentukan syarat **Loss/Nyangkut**: Jika persentase negatif (di bawah 0%).
    *   Tentukan syarat **BEP**: Jika persentase 0%.

#### Fase 6: Visualisasi Hasil (Frontend Final)
1.  **Desain Tabel:**
    *   Tampilkan kolom utama: Kode Saham, Avg Price Broker, Current Price, Total Value (Miliar/Juta), dan Status Gain/Loss (%).
2.  **Sorting (Pengurutan):**
    *   Secara default, urutkan tabel berdasarkan **Total Value** (bval) dari terbesar ke terkecil. Ini penting untuk melihat di mana uang besar (Big Money) ditaruh.
3.  **Conditional Formatting (Pewarnaan):**
    *   Berikan warna latar belakang hijau muda pada baris saham yang statusnya Profit.
    *   Berikan warna latar belakang merah muda pada baris saham yang statusnya Loss.
4.  **Metrik Tambahan (Opsional):**
    *   Tampilkan ringkasan di atas tabel, misal: "Total Saham Diakumulasi: 10", "Posisi Profit: 6", "Posisi Loss: 4".

#### Fase 7: Testing (Uji Coba)
1.  Buka website Stockbit, buka tab Network, ambil JSON broker summary.
2.  Copy JSON tersebut.
3.  Jalankan aplikasimu, Paste JSON.
4.  Cek apakah tabel muncul, apakah angkanya masuk akal, dan apakah warna indikator Profit/Loss sesuai dengan perhitungan.

---