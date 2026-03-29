import random

def make_catchy(title):
    hooks = [
        "🚀 Breaking:",
        "🔥 Trending:",
        "⚡ Just In:",
        "💡 Tech Alert:",
        "📢 Big Update:"
    ]
    return f"{random.choice(hooks)} {title}"


def format_message(title, link):
    return f"""
🚀 *Tech News of the Day*

📰 *{title}*

👉 [Read Full Article]({link})

#Tech #AI #Innovation
"""