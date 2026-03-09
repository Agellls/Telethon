import os
import sys
import logging
from telethon import TelegramClient

# ===== LOGGING SETUP =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ===== ENV VALIDATION =====
logger.info("🔍 Validating environment variables...")
required_env = ["API_ID", "API_HASH"]
missing_env = [var for var in required_env if not os.getenv(var)]

if missing_env:
    logger.error("❌ Missing environment variables!")
    logger.error(f"❌ Missing: {', '.join(missing_env)}")
    sys.exit(1)

logger.info("✅ Environment variables valid!")

# ===== CONFIG =====
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# ===== LOGIN =====
if __name__ == "__main__":
    try:
        logger.info("🚀 Starting Telegram login...")
        logger.info("📱 Please complete authentication...")
        
        client = TelegramClient("session", api_id, api_hash)
        
        # This will prompt for authentication
        client.start()
        
        logger.info("✅ Login successful!")
        logger.info("📝 Session saved to 'session' file")
        logger.info("👉 Now you can run the bot with: python main.py")
        
        client.disconnect()
        
    except Exception as e:
        logger.error(f"❌ Login failed: {e}", exc_info=True)
        sys.exit(1)
