import feedparser
import requests
from bs4 import BeautifulSoup
import random
import html
import asyncio
import os

from telegram import Bot

# 🔑 Secrets
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

bot = Bot(token=BOT_TOKEN)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 🌐 Multi-source RSS
RSS_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://hnrss.org/frontpage"
]

# ❌ Block junk domains
BLOCKED_DOMAINS = [
    "github.com",
    "news.ycombinator.com",
    "reddit.com"
]


# 📰 Fetch all news
def get_news():
    news = []

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:
            news.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", "")
            })

    return news


def clean_summary(text):
    text = BeautifulSoup(text, "html.parser").get_text()

    words = text.split()
    summary = " ".join(words[:40])

    # ✅ Fix incomplete sentence
    if not summary.endswith("."):
        summary = summary.rsplit(" ", 1)[0] + "..."

    return summary 


# 🖼 Extract image
def get_image(link):
    try:
        res = requests.get(link, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")

        meta = soup.find("meta", property="og:image")
        if meta:
            return meta.get("content")
    except:
        return None


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
    t = title.lower()

    tags = []

    if "ai" in t:
        tags.append("#AI")
    if "startup" in t:
        tags.append("#Startup")
    if "crypto" in t:
        tags.append("#Crypto")
    if "google" in t or "meta" in t or "microsoft" in t:
        tags.append("#BigTech")

    tags.append("#Tech")

    return " ".join(tags)


# 🤖 Send news
async def send_news():
    news_list = get_news()

    print("🚀 Sending news...")

    random.shuffle(news_list)

    for news in news_list:
        link = news["link"]

        # ❌ Skip bad sources
        if any(domain in link for domain in BLOCKED_DOMAINS):
            continue

        try:
            title = html.escape(make_catchy(news["title"]))
            summary = clean_summary(news["summary"])

            # ❌ Skip weak content
            if len(summary.split()) < 8:
                continue

            tags = get_tags(news["title"])
            image = get_image(link)

            message = f"""
🚀 Tech Pulse

📰 {title}

🧠 {summary}

🔗 {link}

{tags}
"""

            # 🖼 Send with image if available
            if image:
                try:
                    await bot.send_photo(
                        chat_id=CHAT_ID,
                        photo=image,
                        caption=message
                    )
                except:
                    await bot.send_message(
                        chat_id=CHAT_ID,
                        text=message
                    )
            else:
                await bot.send_message(
                    chat_id=CHAT_ID,
                    text=message
                )

            print("✅ Sent:", title)

            break  # send only one per run

        except Exception as e:
            print("❌ Error:", e)


# 🚀 Run once (GitHub Actions)
if __name__ == "__main__":
    asyncio.run(send_news())
