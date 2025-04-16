from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream.input_file import AudioPiped
from pytgcalls.types.stream import StreamType

from telethon import TelegramClient
import yt_dlp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

class Assistant:
    def __init__(self, api_id, api_hash):
        self.client = TelegramClient('assistant', api_id, api_hash)
        self.pytgcalls = PyTgCalls(self.client)
        self.queue = []
        self.current_chat = None
        self.now_playing = None

        asyncio.create_task(self.start())

    async def start(self):
        await self.client.start()
        await self.pytgcalls.start()

    async def download_audio(self, query):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'temp/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
            return ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')

    async def play(self, query, chat_id):
        file_path = await self.download_audio(query)

        self.queue.append((file_path, chat_id))

        # Jika belum memutar apapun
        if not self.current_chat:
            await self._join_and_play()

    async def _join_and_play(self):
        if not self.queue:
            return

        file_path, chat_id = self.queue.pop(0)
        self.current_chat = chat_id
        self.now_playing = file_path

        await self.pytgcalls.join_group_call(
            chat_id,
            AudioPiped(file_path),
            stream_type=StreamType().pulse_stream,
        )

    async def pause(self):
        if self.current_chat:
            await self.pytgcalls.pause_stream(self.current_chat)

    async def resume(self):
        if self.current_chat:
            await self.pytgcalls.resume_stream(self.current_chat)

    async def skip(self):
        if self.queue:
            await self.stop()  # stop current
            await self._join_and_play()

    async def stop(self):
        if self.current_chat:
            await self.pytgcalls.leave_group_call(self.current_chat)
            self.current_chat = None
            self.now_playing = None

    async def get_queue(self):
        return "\n".join([os.path.basename(f) for f, _ in self.queue]) if self.queue else "Queue kosong."
