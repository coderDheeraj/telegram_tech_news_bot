import feedparser
import requests
from bs4 import BeautifulSoup
import random
import html
import asyncio
import os

from telegram import Bot

# 🔑 Secrets (GitHub)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
HF_API_KEY = os.getenv("HF_API_KEY")

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
        print("Image error:", e)

    return None


# 📰 Extract article text
def get_article_text(link):
    try:
        res = requests.get(link, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")

        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])

        return text[:1000]

    except Exception as e:
        print("Text error:", e)
        return ""


# 🧠 HuggingFace summary (≤ 60 words)
def summarize_text(text):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    prompt = f"""
Summarize this tech news in under 60 words.
Be direct and concise.
Do not use phrases like 'this article explains'.

{text[:800]}
"""

    payload = {"inputs": prompt}

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        result = response.json()

        if isinstance(result, list):
            summary = result[0]["summary_text"]

            # ✂️ Limit to 60 words
            words = summary.split()
            summary = " ".join(words[:60])

            # 🧹 Clean phrases
            summary = summary.replace("This article", "")
            summary = summary.replace("The article", "")

            return summary.strip()

    except Exception as e:
        print("HF error:", e)

    return "Summary not available."


# 🔥 Catchy title
def make_catchy(title):
    hooks = [
        "🚀 Breaking:",
        "🔥 Trending:",
        "⚡ Update:",
        "💡 Tech:"
    ]
    return f"{random.choice(hooks)} {title}"


# 🤖 Send news
async def send_news():
    feed = feedparser.parse("https://techcrunch.com/feed/")

    print("🚀 Sending news...")

    try:
        entry = random.choice(feed.entries)  # 🔥 only one news

        title = html.escape(make_catchy(entry.title))
        link = entry.link

        # 📄 Get content + summary
        article_text = get_article_text(link)
        summary = summarize_text(article_text)

        message = f"""
🚀 Tech News

📰 {title}

🧠 {summary}

🔗 {link}
"""

        await bot.send_message(
            chat_id=CHAT_ID,
            text=message
        )

        print("✅ Sent:", title)

    except Exception as e:
        print("❌ Error:", e)


# 🚀 Run once (for GitHub Actions)
if __name__ == "__main__":
    asyncio.run(send_news())
