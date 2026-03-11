import os
import asyncio
import sys
import signal
import logging
import time
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

# ===== GLOBAL STATE =====
is_shutting_down = False

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
session_file = "session.session"
if not os.path.exists(session_file):
    logger.error("❌ Session file not found!")
    logger.error(f"❌ Expected location: {os.path.abspath(session_file)}")
    logger.error("❌ Anda belum login - Run 'python login.py' first to authenticate")
    logger.error("❌ Untuk Northflank: Upload session.session pertama kali via persistent storage")
    sys.exit(1)

logger.info(f"✅ Session file found at {os.path.abspath(session_file)}")

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
async def keep_alive():
    """Keep-alive ping untuk prevent idle di Northflank"""
    while not is_shutting_down:
        try:
            await asyncio.sleep(300)  # Ping setiap 5 menit
            if client.is_connected():
                logger.debug("💓 Keep-alive ping sent")
        except Exception as e:
            logger.warning(f"⚠️ Keep-alive error: {e}")


def signal_handler(sig, frame):
    """Handle graceful shutdown"""
    global is_shutting_down
    is_shutting_down = True
    logger.info("🛑 Shutdown signal received...")
    sys.exit(0)


async def main_loop():
    """Main bot loop dengan retry logic"""
    global is_shutting_down
    max_retries = 5
    retry_count = 0
    last_retry_time = 0
    
    while not is_shutting_down and retry_count < max_retries:
        try:
            logger.info("🚀 Starting Telegram client...")
            logger.info("📱 Connecting to Telegram...")
            
            # Start client
            await client.connect()
            if not await client.is_user_authorized():
                logger.error("❌ User not authorized - session invalid")
                logger.error("❌ Run 'python login.py' to re-authenticate")
                sys.exit(1)
            
            logger.info("✅ Connected to Telegram!")
            logger.info("👂 Listening for new messages...")
            logger.info(f"📨 Forwarding messages from chat {source_chat} to {target_group}")
            
            # Reset retry count on successful connection
            retry_count = 0
            
            # Keep alive task
            keep_alive_task = asyncio.create_task(keep_alive())
            
            # Wait for disconnection
            await client.run_until_disconnected()
            
            keep_alive_task.cancel()
            
        except ConnectionError as e:
            retry_count += 1
            wait_time = min(2 ** retry_count, 60)  # Exponential backoff, max 60s
            logger.error(f"❌ Connection error: {e}")
            logger.info(f"🔄 Retry {retry_count}/{max_retries} dalam {wait_time}s...")
            
            last_retry_time = time.time()
            await asyncio.sleep(wait_time)
            
        except asyncio.CancelledError:
            logger.info("🛑 Task cancelled - shutting down gracefully")
            break
            
        except Exception as e:
            retry_count += 1
            wait_time = min(2 ** retry_count, 60)
            logger.error(f"❌ Fatal error: {e}", exc_info=True)
            logger.info(f"🔄 Retry {retry_count}/{max_retries} dalam {wait_time}s...")
            
            last_retry_time = time.time()
            await asyncio.sleep(wait_time)
    
    if retry_count >= max_retries:
        logger.error(f"❌ Max retries ({max_retries}) exceeded - giving up")
        sys.exit(1)


if __name__ == "__main__":
    # Setup signal handlers untuk graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        logger.info("=" * 50)
        logger.info("🎯 TELETHON RESEND BOT - STARTING")
        logger.info("=" * 50)
        
        # Run main loop
        asyncio.run(main_loop())
        
    except KeyboardInterrupt:
        logger.info("🛑 Interrupted by user")
        sys.exit(0)
    finally:
        is_shutting_down = True
        logger.info("=" * 50)
        logger.info("🛑 Bot shutdown complete")
        logger.info("=" * 50)
        if client.is_connected():
            client.disconnect()