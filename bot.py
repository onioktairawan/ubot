import json
from telethon import TelegramClient, events

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

API_ID = config['API_ID']
API_HASH = config['API_HASH']
BOT_TOKEN = config['BOT_TOKEN']
OWNER_ID = config['OWNER_ID']

client = TelegramClient('userbot', API_ID, API_HASH)

# Load users
with open('users.json', 'r') as f:
    users = json.load(f)

# Load broadcast database
with open('database/broadcast_db.json', 'r') as f:
    broadcast_db = json.load(f)

# Function to check if the user is the owner
def is_owner(user_id):
    return str(user_id) == OWNER_ID

# Command to add user
@client.on(events.NewMessage(pattern='/adduser'))
async def add_user(event):
    if not is_owner(event.sender_id):
        return await event.reply("You are not authorized to use this command.")
    
    # Prompt user to log in using API_ID, API_HASH, and phone number
    await event.reply("Please log in with your API_ID, API_HASH, and phone number.")
    # More logic to handle user login goes here
    
# Command to handle user login (simulate user data)
@client.on(events.NewMessage(pattern='/login'))
async def login_user(event):
    phone_number = event.text.split()[1]
    # Check if the number exists in users.json
    if phone_number not in users:
        await event.reply("User not found. Please register first.")
    else:
        users[phone_number]["status"] = "active"
        await event.reply(f"Welcome, {phone_number}!")
    
# Example command to broadcast to all groups
@client.on(events.NewMessage(pattern='/gcast'))
async def gcast(event):
    if not is_owner(event.sender_id):
        return await event.reply("You are not authorized to use this command.")
    
    text = event.text.split(" ", 1)[1]
    # Send broadcast to all groups
    for chat_id in broadcast_db['groups']:
        try:
            await client.send_message(chat_id, text)
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")

# Command to handle blacklist
@client.on(events.NewMessage(pattern='/addbl'))
async def add_blacklist(event):
    chat_id = event.text.split()[1]
    # Add chat to blacklist
    broadcast_db['blacklist'].append(chat_id)
    with open('database/broadcast_db.json', 'w') as f:
        json.dump(broadcast_db, f)
    await event.reply(f"Chat {chat_id} added to blacklist.")

# Command to handle remove from blacklist
@client.on(events.NewMessage(pattern='/delbl'))
async def remove_blacklist(event):
    chat_id = event.text.split()[1]
    if chat_id in broadcast_db['blacklist']:
        broadcast_db['blacklist'].remove(chat_id)
        with open('database/broadcast_db.json', 'w') as f:
            json.dump(broadcast_db, f)
        await event.reply(f"Chat {chat_id} removed from blacklist.")
    else:
        await event.reply(f"Chat {chat_id} not found in blacklist.")

# Start the bot
client.start(bot_token=BOT_TOKEN)
client.run_until_disconnected()
