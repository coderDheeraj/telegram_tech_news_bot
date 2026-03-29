import feedparser
import requests
from bs4 import BeautifulSoup
import random
import html
import asyncio
import os

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

# 🔑 Get from GitHub Secrets
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

bot = Bot(token=BOT_TOKEN)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# 🖼 Get image from article
def get_full_image(link):
    try:
        res = requests.get(link, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")

        meta = soup.find("meta", property="og:image")
        if meta:
            return meta.get("content")
    except Exception as e:
        print("Image fetch error:", e)

    return None


# 📰 Fetch news
def get_news():
    feed = feedparser.parse("https://techcrunch.com/feed/")
    news_list = []

    for entry in feed.entries[:5]:
        image = get_full_image(entry.link)

        news_list.append({
            "title": entry.title,
            "link": entry.link,
            "image": image
        })

    return news_list


# 🔥 Catchy titles
def make_catchy(title):
    hooks = [
        "🚀 Breaking:",
        "🔥 Trending:",
        "⚡ Just In:",
        "💡 Tech Alert:"
    ]
    return f"{random.choice(hooks)} {title}"


# 🤖 Send news
async def send_news():
    news_list = get_news()

    print("🚀 Sending news...")

    for news in news_list:
        try:
            title = html.escape(make_catchy(news["title"]))
            link = news["link"]
            image = news["image"]

            message = f"""
🚀 Tech News

📰 {title}
"""

            # 🔘 Button
            keyboard = [
                [InlineKeyboardButton("📖 Read Full Article", url=link)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # 🖼 Send with image if available
            if image:
                try:
                    await bot.send_photo(
                        chat_id=CHAT_ID,
                        photo=image,
                        caption=message,
                        reply_markup=reply_markup
                    )
                except Exception as img_error:
                    print("Image failed:", img_error)

                    await bot.send_message(
                        chat_id=CHAT_ID,
                        text=message,
                        reply_markup=reply_markup
                    )
            else:
                await bot.send_message(
                    chat_id=CHAT_ID,
                    text=message,
                    reply_markup=reply_markup
                )

            print("✅ Sent:", title)

        except Exception as e:
            print("❌ Error:", e)


# 🚀 Run once (GitHub Actions will handle schedule)
if __name__ == "__main__":
    asyncio.run(send_news())
