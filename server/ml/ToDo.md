Sebelum run dan install library, pastikan sudah aktif virtual environment
```bash
cmd: venv\Scripts\activate

output: (venv) PS D:\Code Programs\Tech Stack\TheoryBandarmologi\ml>
```

Setelah aktif virtual environment, install library yang diperlukan

Untuk deactive virtual environment

```bash
Kondisi: (venv) PS D:\Code Programs\Tech Stack\TheoryBandarmologi\ml>

cmd deactivate
```


Tentu, ini adalah ide yang bagus. Menggunakan gaya desain (**Design System**) yang konsisten akan membuat aplikasi Anda terlihat profesional seperti *Bloomberg Terminal* atau aplikasi *Fintech* modern.

Saya akan merekomendasikan tema **"Modern Dark Fintech"**. Alasan memilih Dark Mode adalah karena trader/investor terbiasa melihat layar chart berlatar gelap agar mata tidak cepat lelah, dan warna indikator (Hijau/Merah) akan terlihat lebih kontras (pop-out).

Berikut adalah detail desain per halaman beserta **Prompt** yang bisa Anda gunakan (misalnya di *v0.dev*, *Midjourney*, atau tools AI design lainnya).

---

### 🎨 Design System (Panduan Gaya Utama)
Sebelum masuk ke halaman, ini adalah "Aturan Dasar" agar semua halaman terlihat satu gaya:
*   **Background:** Deep Charcoal / Hampir Hitam (`#0f172a` atau `Slate-900`).
*   **Card/Container:** Sedikit lebih terang dari background (`#1e293b` atau `Slate-800`) dengan border tipis (`Slate-700`).
*   **Accent Color:** Electric Blue (`#3b82f6`) untuk tombol utama.
*   **Semantic Colors:**
    *   Profit/Win: Neon Green (`#22c55e`).
    *   Loss/Nyangkut: Soft Red (`#ef4444`).
    *   Text: Putih bersih untuk heading, abu-abu (`Slate-400`) untuk label.
*   **Typography:** Kombinasi *Inter* (UI Text) dan *JetBrains Mono* (Angka/Data).

---

### 1. Halaman Utama: Dashboard Analyzer (Penting/Major)
Ini adalah halaman inti. User masuk, paste JSON, dan melihat hasil.

**Komponen:**
*   **Major:**
    *   **Navbar Sederhana:** Logo di kiri ("BandarDetector"), Menu simpel di kanan.
    *   **Input Section (Hero):** 2 Kolom input (Kode Broker & Tanggal) + 1 Area besar (Textarea) untuk Paste JSON + Tombol "Analyze".
    *   **Result Table:** Tabel data saham dengan kolom: Stock, Broker Avg, Current Price, Value, dan Status (Badge).
*   **Minor:**
    *   **Summary Cards:** 3 Kartu kecil di atas tabel (Total Value, Total Saham Profit, Total Saham Loss).
    *   **Loading State:** Skeleton loader saat data sedang diproses.

**📝 Prompt untuk AI Generator:**
> Create a high-fidelity UI design for a stock analysis web application dashboard in dark mode.
>
> **Style:** Modern fintech, professional, clean lines, dark slate background (#0f172a).
>
> **Top Section (Input):** A prominent card containing a form. Fields for 'Broker Code' (small input), 'Date' (date picker), and a large 'Paste JSON Here' textarea area. A bright blue 'Analyze Broker' button on the right.
>
> **Bottom Section (Results):** A data table displaying stock analysis.
> *   Columns: Stock Ticker (bold), Broker Avg Price, Current Market Price, Total Value, and Status.
> *   The 'Status' column uses pill-shaped badges: Green for 'Profit', Red for 'Loss', Gray for 'BEP'.
> *   Rows should have subtle hover effects.
> *   Numbers should use a monospaced font.
>
> **Header:** Above the table, place 3 summary cards displaying: "Total Transacted Value", "Winning Stocks", "Losing Stocks". Use neon green and red accents for the numbers.

---

### 2. Halaman Visualisasi / Chart (Opsional/Major)
Halaman ini muncul jika user ingin melihat representasi visual dari data tabel (misal: tombol "View Chart" diklik).

**Komponen:**
*   **Major:**
    *   **Bar Chart Besar:** Menunjukkan "Buying Power" per saham (Top 5 Saham dengan Value terbesar).
    *   **Pie Chart:** Proporsi Win vs Loss.
*   **Minor:**
    *   **Back Button:** Tombol kembali ke tabel.
    *   **Filter:** Dropdown kecil untuk filter (Top 10, All, Only Profit).

**📝 Prompt untuk AI Generator:**
> UI design for a stock data visualization page, dark mode fintech theme.
>
> **Layout:** Two main sections.
> 1.  **Left/Top:** A large horizontal Bar Chart titled "Top Accumulation by Value". The bars should be gradient blue.
> 2.  **Right/Bottom:** A Donut Chart titled "Portfolio Win/Loss Ratio". Segments colored in Green (Profit) and Red (Loss).
>
> **Style:** Minimalist, using dark gray card backgrounds with rounded corners. The charts should look modern (like Recharts or Chart.js style) against the dark background. Include a small 'Back to Dashboard' button at the top left.

---

### 3. Halaman Panduan / How-to (Opsional/Minor)
Karena cara mengambil JSON dari Stockbit itu agak "tricky" (via Network Tab), user butuh panduan.

**Komponen:**
*   **Major:**
    *   **Step-by-step List:** Teks instruksi.
    *   **Screenshot Placeholders:** Tempat menaruh gambar contoh Network Tab.
*   **Minor:**
    *   **Code Snippet Box:** Menampilkan contoh bentuk JSON yang benar agar user tidak bingung.
    *   **FAQ Accordion:** Pertanyaan umum (Misal: "Kenapa error?", "Token expired?").

**📝 Prompt untuk AI Generator:**
> UI design for a 'Documentation' or 'Help' page within a dark mode trading app.
>
> **Content:** A centered layout focused on readability.
> 1.  **Title:** "How to Get Broker Data".
> 2.  **Steps:** A vertical timeline or numbered list. Each step has a title (e.g., "Open Network Tab") and a placeholder rectangle for a screenshot.
> 3.  **Code Block:** A dark container showing a sample JSON structure with syntax highlighting (colors for keys and values).
>
> **Typography:** Clean sans-serif font, high contrast text for easy reading on dark background.

---

### 4. Halaman Error / Empty State (Minor tapi Penting)
Tampilan ketika user belum memasukkan data atau data JSON salah.

**Komponen:**
*   **Major:**
    *   **Illustration:** Ikon atau ilustrasi sederhana (misal: kaca pembesar atau robot bingung).
    *   **Message:** "Belum ada data dianalisa" atau "Format JSON Salah".
*   **Minor:**
    *   **Action Button:** Tombol "Coba Lagi" atau "Lihat Panduan".

**📝 Prompt untuk AI Generator:**
> UI design for an 'Empty State' or 'No Data' component in a dark theme web app.
>
> **Visual:** Centered on the screen.
> *   **Icon:** A subtle, modern linear icon (gray color) representing a search or a chart.
> *   **Text:** "Waiting for Data" in bold white, followed by a smaller gray subtitle "Paste your Stockbit JSON to start analyzing."
> *   **Button:** A subtle outline button saying "See Instructions".
>
> **Atmosphere:** Clean, spacious, not cluttered.

---

### Tips Implementasi di React + Tailwind

Untuk mencapai desain ini dengan cepat di kode nanti:

1.  **Install Library Icon:** Gunakan `lucide-react` (ikonnya sangat modern dan cocok untuk dashboard).
2.  **Warna Status:** Buat *helper function* di React untuk badge tabel.
    ```javascript
    // Contoh logic class Tailwind
    const getBadgeColor = (status) => {
      if (status.includes("PROFIT")) return "bg-green-900 text-green-300 border-green-700";
      if (status.includes("LOSS")) return "bg-red-900 text-red-300 border-red-700";
      return "bg-slate-700 text-slate-300";
    }
    ```
3.  **Font:** Gunakan Google Font `Inter` untuk body dan `Roboto Mono` untuk angka harga/persentase agar terlihat seperti terminal saham asli.

Apakah deskripsi visual ini sudah sesuai dengan bayangan Anda?