import feedparser
import requests
from bs4 import BeautifulSoup
import random
import html
import asyncio
import os
import json

from telegram import Bot

# 🔑 Secrets
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

bot = Bot(token=BOT_TOKEN)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 🗂 Multi-source RSS
RSS_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://hnrss.org/frontpage"
]

# 📁 File to store sent links
SEEN_FILE = "seen.json"


# 📂 Load seen links
def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()


# 💾 Save seen links
def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


# 📰 Get all news
def get_news():
    all_news = []

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:
            all_news.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", "")
            })

    return all_news


# 🧠 Clean summary (≤ 60 words)
def clean_summary(text):
    text = BeautifulSoup(text, "html.parser").get_text()

    words = text.split()
    return " ".join(words[:60])


# 🔥 Viral headline
def make_catchy(title):
    hooks = [
        "🚨 Breaking:",
        "🔥 Trending:",
        "⚡ Big Update:",
        "💡 Must Know:"
    ]
    return f"{random.choice(hooks)} {title}"


# 🏷 Smart hashtags
def get_tags(title):
    title_lower = title.lower()

    if "ai" in title_lower:
        return "#AI #Tech"
    elif "startup" in title_lower:
        return "#Startup #Tech"
    elif "google" in title_lower or "meta" in title_lower:
        return "#BigTech #Tech"
    else:
        return "#TechNews"


# 🤖 Send news
async def send_news():
    seen = load_seen()
    news_list = get_news()

    print("🚀 Sending news...")

    # Shuffle for randomness
    random.shuffle(news_list)

    for news in news_list:
        if news["link"] in seen:
            continue

        try:
            title = html.escape(make_catchy(news["title"]))
            link = news["link"]

            summary = clean_summary(news["summary"])
            tags = get_tags(news["title"])

            message = f"""
🚀 Tech Pulse

📰 {title}

🧠 {summary}

🔗 {link}

{tags}
"""

            await bot.send_message(
                chat_id=CHAT_ID,
                text=message
            )

            print("✅ Sent:", title)

            seen.add(link)
            save_seen(seen)

            break  # send only 1 per run

        except Exception as e:
            print("❌ Error:", e)


# 🚀 Run once
if __name__ == "__main__":
    asyncio.run(send_news())
