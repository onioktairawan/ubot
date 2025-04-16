from telethon import TelegramClient
from telethon import events
import json

# Load config
with open('data/config.json', 'r') as f:
    config = json.load(f)

api_id = config['api_id']
api_hash = config['api_hash']
bot_token = config['bot_token']

# Setup Telethon client
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Define some command handlers
@client.on(events.NewMessage(pattern=r'.kick'))
async def kick_user(event):
    # Example: Kick user command
    if event.reply_to_msg_id:
        message = await event.get_reply_message()
        user = message.sender_id
        await event.chat.kick_participant(user)
        await event.respond(f'User {user} kicked.')

@client.on(events.NewMessage(pattern=r'.gcast'))
async def broadcast_message(event):
    # Example: Send broadcast to all group chats
    if event.text:
        text = event.text.split(' ', 1)[1]  # Get message after .gcast
        for chat in await client.get_dialogs():
            if chat.is_group:
                await client.send_message(chat, text)
                await event.respond(f'Broadcast sent to {chat.title}')

# Run the bot
client.start()
client.run_until_disconnected()
