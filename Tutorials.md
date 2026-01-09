Website ini menyediakan berbagai fitur analisis, seperti kemampuan untuk menganalisis *broker summary* untuk satu atau beberapa broker sekaligus dengan dukungan rentang tanggal tertentu.

### 1. Fitur Broker Summary
Fitur ini memungkinkan Anda untuk menganalisis data broker yang diunggah dalam format JSON. File JSON tersebut bisa didapatkan dengan menjalankan skrip *interceptor* berikut di konsol browser Anda:

```javascript
(function() {
    // Tempat penyimpanan data sementara di memori browser
    window.stockbitDataLog = [];
    
    console.log('%c[System] Interceptor Aktif!', 'background: #222; color: #bada55; padding: 5px;');
    console.log('Script ini akan menangkap data Broker Summary otomatis saat Anda klik "Filter" di website.');
    console.log('Ketik %cdownloadHasil()%c untuk mengambil file JSON gabungan.', 'color: orange; font-weight: bold', '');

    // --- 1. INTERCEPT FETCH (Untuk Browser Modern) ---
    const originalFetch = window.fetch;
    window.fetch = async (...args) => {
        const response = await originalFetch(...args);
        const url = typeof args[0] === 'string' ? args[0] : args[0].url;

        // Filter: Hanya ambil URL yang mengandung endpoint activity broker
        if (url.includes('findata-view/marketdetectors/activity')) {
            const clone = response.clone();
            clone.json().then(data => {
                saveData(data, url, 'FETCH');
            }).catch(err => console.error("Gagal parse JSON Fetch:", err));
        }
        return response;
    };

    // --- 2. INTERCEPT XHR (Untuk Request Tradisional) ---
    const rawOpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function(method, url) {
        this._url = url;
        return rawOpen.apply(this, arguments);
    };

    const rawSend = XMLHttpRequest.prototype.send;
    XMLHttpRequest.prototype.send = function() {
        this.addEventListener('load', function() {
            if (this._url && this._url.includes('findata-view/marketdetectors/activity')) {
                try {
                    const data = JSON.parse(this.responseText);
                    saveData(data, this._url, 'XHR');
                } catch (e) {
                    // Bukan JSON atau error parse
                }
            }
        });
        return rawSend.apply(this, arguments);
    };

    // --- FUNGSI PENGOLAH DATA ---
    function saveData(jsonResponse, url, source) {
        // Ekstrak Kode Broker dari URL (Misal: BK, AD, YP)
        const brokerMatch = url.match(/\/activity\/([^\/?]+)/);
        const brokerCode = brokerMatch ? brokerMatch[1] : 'UNKNOWN';
        
        // Ambil info tanggal dari URL agar kita tahu data periode mana ini
        const urlObj = new URL(url);
        const fromDate = urlObj.searchParams.get('from') || 'n/a';
        const toDate = urlObj.searchParams.get('to') || 'n/a';

        const entry = {
            timestamp: new Date().toISOString(),
            broker: brokerCode,
            periode: { from: fromDate, to: toDate },
            source: source,
            url: url,
            response: jsonResponse
        };

        window.stockbitDataLog.push(entry);
        console.log(`%c[CAPTURED] ${brokerCode} (%c${fromDate} s/d ${toDate}%c) - Total: ${window.stockbitDataLog.length}`, 
            'color: #00ff00', 'color: #3498db', 'color: #00ff00');
    }

    // --- FUNGSI UNTUK DOWNLOAD ---
    window.downloadHasil = function() {
        if (window.stockbitDataLog.length === 0) {
            console.warn("Belum ada data yang tertangkap.");
            return;
        }

        const blob = new Blob([JSON.stringify(window.stockbitDataLog, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `stockbit_broker_summary_log_${new Date().getTime()}.json`;
        a.click();
        console.log("File JSON berhasil diunduh.");
    };
})();
```

### Panduan Penggunaan:
1. **Jalankan Skrip**: Salin kode di atas, tempel (*paste*) ke dalam konsol browser (*Inspect Element* > *Console*) pada halaman Stockbit, lalu tekan **Enter**.
2. **Tangkap Data**: Buka fitur **Bandar Detector** di Stockbit, pilih tab **Broker Activity**, lalu lakukan filter sesuai kebutuhan (pilih broker dan rentang tanggal). Skrip akan otomatis menyimpan data setiap kali Anda menekan tombol filter.
3. **Unduh JSON**: Setelah selesai mengumpulkan data, ketik `downloadHasil()` di konsol dan tekan **Enter**. File JSON akan otomatis terunduh dan siap digunakan di website ini.