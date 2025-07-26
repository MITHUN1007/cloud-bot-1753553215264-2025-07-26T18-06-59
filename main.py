import os
from telethon import TelegramClient, events
from groq import Groq

# Telegram API credentials
API_ID = int(os.environ.get("TELEGRAM_API_ID"))
API_HASH = os.environ.get("TELEGRAM_API_HASH")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Groq API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Initialize Telegram client
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

@client.on(events.NewMessage)
async def echo(event):
    try:
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": event.message.message}],
            model="mixtral-8x7b-32768",
        )
        await event.reply(response.choices[0].message.content)
    except Exception as e:
        await event.reply(f"Error processing message: {str(e)}")

if __name__ == '__main__':
    print("Bot started.  Please upload session.session file")
    client.run_until_disconnected()