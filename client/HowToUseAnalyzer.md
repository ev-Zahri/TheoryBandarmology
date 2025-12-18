### Bagaimana Menggunakan Kode Quant

#### A. Z-SCORE (Standard Score) -> Deteksi Anomali
Ini adalah senjata utama Quant untuk menentukan Overbought/Oversold secara ilmiah.
*   **Rumus Matematika:**
    $$Z = \frac{(HargaSekarang - RataRata)}{StandarDeviasi}$$

*   **Cara Membacanya:**
    *   **Z-Score 0:** Harga pas di rata-rata. Normal.
    *   **Z-Score +2:** Harga sudah menyimpang jauh ke atas (Langka, hanya terjadi 5% waktu). **Potensi Reversal Turun**.
    *   **Z-Score -2:** Harga menyimpang jauh ke bawah (Diskon besar). **Potensi Reversal Naik**.
    *   **Z-Score +3:** Sangat Ekstrim (Outlier).

*   **Kenapa ini lebih baik dari RSI?**
    *   RSI punya batas 0-100. Z-Score tidak punya batas, dia mengukur *penyimpangan* berdasarkan volatilitas saat itu.

#### B. ATR (Average True Range) -> Pengukur Energi
*   **Konsep:**
    Berapa rata-rata pergerakan harga saham ini dalam sehari (dalam Rupiah)?

*   **Rumus:**
    Diambil rata-rata 14 hari dari nilai terbesar antara:
    1.  High hari ini - Low hari ini.
    2.  |High hari ini - Close kemarin|.
    3.  |Low hari ini - Close kemarin|.

*   **Cara Pakai:**
    *   Misal harga saham 1000.
    *   ATR-nya 50 perak.
    *   Artinya: Wajar jika saham ini naik/turun 50 perak sehari.
    *   **Keputusan Quant:** Jangan pasang Stop Loss cuma 20 perak! Itu cuma "noise". Pasang Stop Loss minimal 1x ATR (50 perak) atau 2x ATR (100 perak) agar tidak kena kocek bandar.

#### C. PIVOT POINTS (Algorithmic S/R) -> Peta Jalan Objektif
*   **Konsep:**
    Titik keseimbangan harga berdasarkan pertarungan High, Low, dan Close hari kemarin.

*   **Rumus (Classic):**
    *   $Pivot (P) = (High + Low + Close) / 3$
    *   $Resistance 1 (R1) = (2 \times P) - Low$
    *   $Support 1 (S1) = (2 \times P) - High$

*   **Cara Pakai:**
    Komputer akan otomatis bilang: "Buy di dekat S1, Jual di dekat R1". Tidak ada subjektivitas garis miring-miring.

#### D. Beta ($\beta$) - Sensitivitas Pasar
*   **Pertanyaan:** "Kalau IHSG naik 1%, saham ini biasanya naik berapa persen?"
*   **Fungsi:** Mengukur keagresifan saham dibanding pasar (Benchmark).
*   **Interpretasi:**
    *   $\beta = 1$: Geraknya sama persis dengan IHSG.
    *   $\beta > 1$ (misal 2.5): Saham Agresif. IHSG naik 1%, dia naik 2.5%. Tapi kalau IHSG turun 1%, dia longsor 2.5%.
    *   $\beta < 1$ (misal 0.5): Saham Defensif.

#### E. Value at Risk (VaR) - Simulasi Kebangkrutan
*   **Pertanyaan:** "Dalam kondisi pasar normal (95% confidence), berapa kerugian maksimal saya besok?"
*   **Fungsi:** Manajemen risiko profesional.
*   **Interpretasi:**
    *   Jika VaR (95%) = -3.5%.
    *   Artinya: Ada peluang 95% kerugian Anda besok tidak akan lebih dari 3.5%. Hanya ada 5% peluang (Black Swan) kerugiannya lebih besar dari itu.

#### F. Kaufman Efficiency Ratio (KER) - Kualitas Tren
*   **Pertanyaan:** "Tren naiknya mulus (clean) atau bergerigi (choppy/banyak noise)?"
*   **Fungsi:** Membedakan tren yang *sustainable* vs tren yang "kocokan bandar".
*   **Rumus:** `(Perubahan Harga Bersih) / (Total Jalan yang Ditempuh)`.
*   **Interpretasi:**
    *   Nilai mendekati 1: Tren sangat mulus (seperti jalan tol). Kuat.
    *   Nilai mendekati 0: Pasar *sideways* penuh noise (banyak jarum naik turun).

---