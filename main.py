import os
import asyncio
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError

# ===== CONFIG =====
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")

# Prompt for chat IDs on startup
source_chat = int(input("Enter source chat ID: "))
target_group = int(input("Enter target group ID: "))

# ===== CLIENT =====
client = TelegramClient("session", api_id, api_hash)

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@client.on(events.NewMessage(chats=source_chat))
async def handler(event):

    msg = event.text or ""

    try:

        if event.media:

            print("⬇️ Downloading media...")

            file_path = await event.download_media(
                file=f"{DOWNLOAD_DIR}/"
            )

            if not file_path:
                print("❌ Failed to download media")
                return

            print(f"⬆️ Uploading {file_path}")

            await client.send_file(
                target_group,
                file_path,
                caption=msg
            )

            print("✅ Media resent")

            # delete local file
            os.remove(file_path)

        else:

            await client.send_message(
                target_group,
                msg
            )

            print("✅ Text resent")

    except FloodWaitError as e:

        print(f"🚫 FloodWait {e.seconds}s")
        await asyncio.sleep(e.seconds)

    except Exception as e:

        print(f"❌ Error: {e}")


# ===== START =====
client.start()
print("🚀 Listener started...")
client.run_until_disconnected()