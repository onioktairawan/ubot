import asyncio
import yt_dlp
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types.stream import StreamAudioEnded
from pytgcalls.types.input_stream import AudioPiped
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

class Assistant:
    def __init__(self, api_id, api_hash):
        self.client = TelegramClient("userbot", api_id, api_hash)
        self.pytgcalls = PyTgCalls(self.client)
        self.queue = {}
        self.now_playing = {}

    async def start(self):
        await self.client.start()
        await self.pytgcalls.start()

    async def join_chat(self, chat_id):
        try:
            await self.client(JoinChannelRequest(chat_id))
        except:
            pass

    async def play(self, chat_id, query):
        audio_file = await self.download_audio(query)
        if chat_id not in self.queue:
            self.queue[chat_id] = []

        self.queue[chat_id].append(audio_file)

        if chat_id not in self.now_playing:
            await self._play_next(chat_id)

    async def _play_next(self, chat_id):
        if self.queue[chat_id]:
            audio = self.queue[chat_id].pop(0)
            await self.pytgcalls.join_group_call(
                chat_id,
                AudioPiped(audio),
            )
            self.now_playing[chat_id] = audio
        else:
            await self.stop(chat_id)

    async def pause(self, chat_id):
        await self.pytgcalls.pause_stream(chat_id)

    async def resume(self, chat_id):
        await self.pytgcalls.resume_stream(chat_id)

    async def skip(self, chat_id):
        await self.pytgcalls.leave_group_call(chat_id)
        self.now_playing.pop(chat_id, None)
        await self._play_next(chat_id)

    async def stop(self, chat_id):
        await self.pytgcalls.leave_group_call(chat_id)
        self.queue[chat_id] = []
        self.now_playing.pop(chat_id, None)

    async def get_queue(self, chat_id):
        return "\n".join(self.queue.get(chat_id, [])) or "Queue kosong."

    async def download_audio(self, query):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
            return ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
