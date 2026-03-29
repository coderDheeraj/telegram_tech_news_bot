
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_news():
    url = "https://techcrunch.com/"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    news_list = []

    articles = soup.select("article")[:5]

    for article in articles:
        try:
            title = article.get_text(strip=True)
            link = article.find("a")["href"]

            img_tag = article.find("img")
            image = img_tag["src"] if img_tag else None

            news_list.append({
                "title": title,
                "link": link,
                "image": image
            })
        except:
            continue

    return news_list