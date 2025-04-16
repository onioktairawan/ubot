import os
import logging
from telethon import TelegramClient, events
from dotenv import load_dotenv
from assistant import Assistant

# Load environment variables
load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the bot client
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Create the assistant userbot client
assistant = Assistant(API_ID, API_HASH)

@bot.on(events.NewMessage(pattern='/play (.*)'))
async def play_music(event):
    song_name = event.pattern_match.group(1)
    await event.reply(f"🔊 Playing: {song_name}")
    # Call the assistant to play the song
    await assistant.play(song_name)

@bot.on(events.NewMessage(pattern='/pause'))
async def pause_music(event):
    await event.reply("⏸️ Paused")
    await assistant.pause()

@bot.on(events.NewMessage(pattern='/resume'))
async def resume_music(event):
    await event.reply("▶️ Resumed")
    await assistant.resume()

@bot.on(events.NewMessage(pattern='/skip'))
async def skip_music(event):
    await event.reply("⏭️ Skipped")
    await assistant.skip()

@bot.on(events.NewMessage(pattern='/stop'))
async def stop_music(event):
    await event.reply("🛑 Stopped")
    await assistant.stop()

@bot.on(events.NewMessage(pattern='/queue'))
async def queue_music(event):
    queue = await assistant.get_queue()
    await event.reply(f"Current queue: {queue}")

@bot.on(events.NewMessage(pattern='/ping'))
async def ping(event):
    await event.reply("Pong!")

# Start the bot
async def main():
    await bot.start()
    await bot.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
