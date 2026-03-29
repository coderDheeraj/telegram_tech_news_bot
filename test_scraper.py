import feedparser
import requests
from bs4 import BeautifulSoup
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


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


def get_news():
    url = "https://techcrunch.com/feed/"
    feed = feedparser.parse(url)

    news_list = []

    for entry in feed.entries[:5]:
        image = get_full_image(entry.link)   # 🔥 main fix

        news_list.append({
            "title": entry.title,
            "link": entry.link,
            "image": image
        })

    return news_list


def make_catchy(title):
    hooks = [
        "🚀 Breaking:",
        "🔥 Trending:",
        "⚡ Just In:",
        "💡 Tech Alert:"
    ]
    return f"{random.choice(hooks)} {title}"


def test():
    news = get_news()

    if not news:
        print("⚠️ No news found")
        return

    print("\n✅ News Fetched Successfully!\n")

    for i, item in enumerate(news, 1):
        print(f"📰 News {i}")
        print("Title :", make_catchy(item["title"]))
        print("Link  :", item["link"])
        print("Image :", item["image"])
        print("-" * 50)


if __name__ == "__main__":
    test()