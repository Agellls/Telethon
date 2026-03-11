# Telethon Forwarder - Northflank Deployment

Aplikasi untuk forward pesan dan media dari satu Telegram chat ke chat lain.

## Prerequisites

- Telegram API credentials (api_id dan api_hash dari https://my.telegram.org)
- Chat ID untuk source dan target

## Setup Lokal

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Environment Variables

Copy `.env.example` ke `.env`:

```bash
cp .env.example .env
```

Edit `.env` dengan credentials Anda:

```env
API_ID=your_api_id
API_HASH=your_api_hash
DOWNLOAD_DIR=downloads
```

### 3. Jalankan Aplikasi

```bash
python main.py
```

Aplikasi akan prompt input:

```
Enter source chat ID: -1001857184829
Enter target group ID: -5192815181
```

## Deployment ke Northflank

### Option 1: Deploy via Git (Recommended)

1. **Push ke GitHub/GitLab**

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Di Northflank Dashboard:**
   - Create new Service
   - Pilih "Source Code" > GitHub/GitLab
   - Select repository
   - Build Type: Docker
   - Dockerfile: Gunakan default (Dockerfile di root)

3. **Set Environment Variables:**
   - Di Service settings, tambahkan:
     - `API_ID` = your_id
     - `API_HASH` = your_hash
     - `DOWNLOAD_DIR` = downloads
4. **Run and Input Chat IDs:**
   - Deploy service
   - Buka Shell di Northflank dashboard
   - Aplikasi akan prompt untuk input:
     ```
     Enter source chat ID: [input your source chat ID]
     Enter target group ID: [input your target group ID]
     ```

### Option 2: Deploy via Docker Image

1. **Build Docker image lokal:**

   ```bash
   docker build -t telethon-forwarder .
   ```

2. **Test lokal dengan docker-compose:**

   ```bash
   docker-compose up
   ```

3. **Push ke Docker registry (Docker Hub/GitHub Container Registry):**

   ```bash
   docker tag telethon-forwarder yourusername/telethon-forwarder
   docker push yourusername/telethon-forwarder
   ```

4. **Di Northflank, gunakan image URL**

## Struktur File

```
.
├── main.py              # Main application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── .dockerignore        # Files to exclude from Docker build
├── .env.example         # Environment variables template
├── northflank.json      # Northflank configuration (optional)
└── downloads/           # Directory untuk downloaded media
```

## Environment Variables

| Variable     | Description                    | Required                   |
| ------------ | ------------------------------ | -------------------------- |
| API_ID       | Telegram API ID                | ✅ Yes                     |
| API_HASH     | Telegram API Hash              | ✅ Yes                     |
| DOWNLOAD_DIR | Directory untuk download media | ❌ No (default: downloads) |

**Note:** Source dan Target chat IDs di-input secara manual saat aplikasi dijalankan.

## Important Notes

⚠️ **Session Management**

- Aplikasi akan membuat file `session` saat pertama kali login via Telegram
- Di Northflank, jalankan via Shell untuk melakukan login interaktif:
  1. Buka Shell di service
  2. Jalankan `python main.py`
  3. Input chat IDs sesuai prompt
  4. Scan QR code atau input phone number untuk login Telegram
  5. Setelah login sekali, app bisa restart tanpa perlu login lagi (session tersimpan)
- Mount `/app/session` sebagai persistent volume agar session tetap ada

⚠️ **Storage**

- Download directory harus persistent jika menggunakan Northflank
- Gunakan Cloud Storage (S3, GCS, dll) untuk file jangka panjang
- Update code untuk upload ke cloud storage sebelum delete lokal

⚠️ **Rate Limiting**

- Bot sudah handle FloodWaitError
- Jangan spam messages terlalu cepat

## Troubleshooting

### "Session" file missing

- Jalankan lokal dulu dengan akun Telegram untuk generate session
- Atau set Northflank untuk prompt login

### Media download fails

- Pastikan disk space cukup
- Check network connectivity
- Verify akses ke source chat

### Heap out of memory

- Reduce media file size limit
- Implement streaming upload ke cloud storage
- Increase Northflank memory allocation

## Support

Untuk lebih info tentang Northflank: https://northflank.com/docs
Untuk Telethon: https://docs.telethon.dev/
