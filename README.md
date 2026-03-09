# Telethon Resend - Docker Setup

Telegram message forwarding bot dengan Docker support.

## ✅ Requirements

- Docker & Docker Compose installed (untuk local)
- Northflank / Cloud hosting dengan SSH access
- `.env` file dengan credentials yang valid

## 🚀 Quick Start

### 1. Setup Environment Variables

```bash
cp .env.example .env
```

Edit `.env` dan isi dengan:

- `API_ID` - Telegram API ID
- `API_HASH` - Telegram API Hash
- `SOURCE_CHAT` - ID chat sumber (harus follow bot)
- `TARGET_GROUP` - ID grup target untuk forward

### 2. Local Setup (Docker)

**Linux/Mac:**

```bash
chmod +x start.sh
./start.sh
```

**Windows:**

```bash
start.bat
```

Atau langsung:

```bash
docker-compose up --build
```

### 3. Northflank Setup (Cloud SSH)

#### Step 1: Set Environment Variables di Northflank Dashboard

- API_ID
- API_HASH
- SOURCE_CHAT
- TARGET_GROUP

#### Step 2: Login via SSH

```bash
# Connect ke Northflank SSH shell
```

#### Step 3: Run Login Script (FIRST TIME ONLY)

```bash
python login.py
```

- Pilih method login: QR Code atau Phone Number
- Complete authentication
- Session akan tersimpan otomatis

#### Step 4: Restart Container atau Run Bot

```bash
python main.py
```

Bot akan start listening untuk pesan baru.

---

## 📁 File Structure

```
.
├── main.py             # Main bot application
├── login.py            # Interactive login script (RUN FIRST)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker container config
├── docker-compose.yml  # Compose orchestration
├── .dockerignore       # Files to exclude from build
├── .env.example        # Environment template
├── start.sh            # Linux/Mac startup script
├── start.bat           # Windows startup script
├── downloads/          # Downloaded media folder
└── session.session     # Telethon session (created by login.py)
```

---

## 🔧 Troubleshooting

### Container tidak start:

- Pastikan semua environment variables sudah diset
- Check Docker & Docker Compose terinstall

### Environment variables error:

- Pastikan semua 4 variables di `.env`: `API_ID`, `API_HASH`, `SOURCE_CHAT`, `TARGET_GROUP`
- Tidak boleh ada spasi extra di `.env`

### Bot tidak listening (Northflank):

1. Check session file ada: `ls -la session*`
2. Jika tidak ada → run `python login.py` dulu
3. Kemudian `python main.py`

### FloodWait Error:

- Bot akan auto pause sesuai durasi yang diminta Telegram
- Normal behavior, tunggu selesai

### "Session file not found" error:

- Meaning: Belum login ke Telegram
- Solution: Run `python login.py` terlebih dahulu via SSH

---

## 📝 Manual Docker Commands

Build image:

```bash
docker build -t telethon-resend .
```

Run container dengan env:

```bash
docker run -it --env-file .env \
  -v $(pwd)/downloads:/app/downloads \
  telethon-resend
```

---

## 💾 Notes

- Session Telethon disimpan di file `session.session` (persistent across restarts)
- Downloads disimpan di `downloads` folder
- Container akan auto-restart jika crash (unless-stopped policy)
- Login hanya perlu 1x saja, session tersimpan permanent
