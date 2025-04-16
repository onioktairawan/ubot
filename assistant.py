import os
import yt_dlp
from telethon import TelegramClient
from pytgcalls import PyTgCalls
from pytgcalls import AudioPiped
from dotenv import load_dotenv

load_dotenv()

class Assistant:
    def __init__(self, api_id, api_hash):
        self.client = TelegramClient('assistant', api_id, api_hash)
        self.client.start()
        self.call = PyTgCalls(self.client)

    async def play(self, song_name):
        # Download audio using yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegAudioConvertor',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'music/%(id)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(song_name, download=True)
            file_path = f"music/{info['id']}.mp3"
        
        # Join the VC
        chat_id = 123456789  # Replace with the actual chat ID
        await self.call.join_group_call(chat_id, AudioPiped(file_path))

    async def pause(self):
        await self.call.pause_audio()

    async def resume(self):
        await self.call.resume_audio()

    async def skip(self):
        # Logic to skip the current track
        pass

    async def stop(self):
        await self.call.leave_group_call()

    async def get_queue(self):
        # Retrieve and return the current queue
        return "No songs in the queue"  # Example, implement queue logic as needed
