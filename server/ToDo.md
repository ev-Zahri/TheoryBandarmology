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

Untuk menjalankan kode di server, pastikan sudah aktif virtual environment

```bash
uvicorn api.main:app --reload --port 8000
```

