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
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
SOURCE_CHAT_ID=-1001857184829
TARGET_GROUP_ID=-5192815181
DOWNLOAD_DIR=downloads
```

### 3. Jalankan Aplikasi

```bash
python main.py
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
     - `TELEGRAM_API_ID` = your_id
     - `TELEGRAM_API_HASH` = your_hash
     - `SOURCE_CHAT_ID` = chat_id
     - `TARGET_GROUP_ID` = group_id
     - `DOWNLOAD_DIR` = downloads

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

| Variable          | Description                       | Required                   |
| ----------------- | --------------------------------- | -------------------------- |
| TELEGRAM_API_ID   | Telegram API ID                   | ✅ Yes                     |
| TELEGRAM_API_HASH | Telegram API Hash                 | ✅ Yes                     |
| SOURCE_CHAT_ID    | Source chat ID (negative number)  | ✅ Yes                     |
| TARGET_GROUP_ID   | Target group ID (negative number) | ✅ Yes                     |
| DOWNLOAD_DIR      | Directory untuk download media    | ❌ No (default: downloads) |

## Important Notes

⚠️ **Session Management**

- Aplikasi akan membuat file `session` saat pertama kali run
- Di Northflank, gunakan persistent volumes untuk folder session:
  - Mount path: `/app/session`
  - Atau copy session file secara manual

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
