# src/scraper/telegram_scraper.py
import os, json, asyncio, datetime
from telethon import TelegramClient, events
from loguru import logger
from dotenv import load_dotenv

load_dotenv()
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION = os.getenv("TELEGRAM_SESSION", "ethio_med_session")

OUTPUT_DIR = "data/raw/telegram_messages"
IMAGE_DIR = "data/raw/images"

CHANNELS = [
    "lobelia4cosmetics",
    "tikvahpharma",
    # add more slugs
]

client = TelegramClient(SESSION, API_ID, API_HASH)

async def fetch_channel(channel):
    async for message in client.iter_messages(channel, limit=None):
        date_str = message.date.strftime("%Y-%m-%d")
        channel_name = channel if isinstance(channel, str) else channel.username
        outdir = os.path.join(OUTPUT_DIR, date_str)
        os.makedirs(outdir, exist_ok=True)
        fname = os.path.join(outdir, f"{channel_name}.jsonl")
        record = {
            "id": message.id,
            "date": message.date.isoformat(),
            "text": message.message,
            "media": None,
            "raw": str(message.to_dict()),
        }
        if message.photo or message.media:
            # save image
            img_dir = os.path.join(IMAGE_DIR, channel_name, date_str)
            os.makedirs(img_dir, exist_ok=True)
            path = await message.download_media(file=img_dir + f"/{message.id}")
            record["media"] = path
        with open(fname, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    logger.info(f"finished channel {channel}")

async def main():
    await client.start()
    for ch in CHANNELS:
        try:
            await fetch_channel(ch)
        except Exception as e:
            logger.exception(f"failed {ch}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
