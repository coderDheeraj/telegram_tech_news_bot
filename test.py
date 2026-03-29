import asyncio
from telegram import Bot

BOT_TOKEN = "8671117308:AAHFpPaBYXWZLHqluF9VQlpgpGwN05aMxjY"
CHAT_ID = 7136143411

bot = Bot(token=BOT_TOKEN)

async def test():
    await bot.send_message(chat_id=CHAT_ID, text="✅ Working now")

asyncio.run(test())