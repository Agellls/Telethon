import os
import asyncio
import sys
import logging
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError

# ===== LOGGING SETUP =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Disable stdout buffering for Northflank
sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None

# ===== ENV VALIDATION =====
logger.info("🔍 Validating environment variables...")
required_env = ["API_ID", "API_HASH", "SOURCE_CHAT", "TARGET_GROUP"]
missing_env = [var for var in required_env if not os.getenv(var)]

if missing_env:
    logger.error("❌ Missing environment variables!")
    logger.error(f"❌ Missing: {', '.join(missing_env)}")
    logger.error("📝 Please set all required environment variables")
    sys.exit(1)

logger.info("✅ All environment variables valid!")

# ===== CHECK SESSION =====
logger.info("🔐 Checking Telegram session...")
if not os.path.exists("session.session"):
    logger.error("❌ Session file not found!")
    logger.error("❌ Run 'python login.py' first to authenticate")
    sys.exit(1)

logger.info("✅ Session file found!")

# ===== CONFIG =====
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

source_chat = int(os.getenv("SOURCE_CHAT"))
target_group = int(os.getenv("TARGET_GROUP"))

DOWNLOAD_DIR = "downloads"
logger.info(f"📁 Download directory: {DOWNLOAD_DIR}")
logger.info(f"📌 Source chat: {source_chat}")
logger.info(f"📌 Target group: {target_group}")

# ===== CLIENT =====
logger.info("🔐 Initializing Telegram client...")
client = TelegramClient("session", api_id, api_hash)

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
logger.info("✅ Client initialized successfully")


@client.on(events.NewMessage(chats=source_chat))
async def handler(event):
    msg = event.text or ""
    
    try:
        if event.media:
            logger.info("⬇️ Downloading media...")
            
            file_path = await event.download_media(
                file=f"{DOWNLOAD_DIR}/"
            )
            
            if not file_path:
                logger.error("❌ Failed to download media")
                return
            
            logger.info(f"⬆️ Uploading {file_path}")
            
            await client.send_file(
                target_group,
                file_path,
                caption=msg
            )
            
            logger.info("✅ Media resent")
            
            # delete local file
            os.remove(file_path)
        
        else:
            logger.info(f"💬 Resending text message: {msg[:50]}...")
            await client.send_message(
                target_group,
                msg
            )
            
            logger.info("✅ Text resent")
    
    except FloodWaitError as e:
        logger.warning(f"🚫 FloodWait {e.seconds}s - waiting...")
        await asyncio.sleep(e.seconds)
    
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)


# ===== START =====
if __name__ == "__main__":
    try:
        logger.info("🚀 Starting Telegram client...")
        logger.info("📱 Connecting to Telegram...")
        
        client.start()
        
        logger.info("✅ Connected to Telegram!")
        logger.info("👂 Listening for new messages...")
        logger.info(f"📨 Forwarding messages from chat {source_chat} to {target_group}")
        
        # Keep the client running
        client.run_until_disconnected()
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("🛑 Shutting down...")
        client.disconnect()