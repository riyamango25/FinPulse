import yfinance as yf
from datetime import datetime


def get_market_news():

    try:

        ticker = yf.Ticker("RELIANCE.NS")

        news = ticker.news

        articles = []

        for article in news[:5]:

            content = article.get("content", {})

            published = content.get("pubDate")

            if published:
                try:
                    published = datetime.fromisoformat(
                        published.replace("Z", "+00:00")
                    ).strftime("%d %b %Y")
                except Exception:
                    pass

            provider = content.get("provider", {})

            canonical = content.get("clickThroughUrl")

            if canonical is None:
                canonical = content.get("canonicalUrl")

            link = None

            if canonical:
                link = canonical.get("url")

            articles.append({
                "title": content.get("title"),
                "publisher": provider.get("displayName"),
                "link": link,
                "published": published,
            })

        return articles

    except Exception as e:

        print(f"[market-news] fetch failed: {e}")  # shows up in your logs now
        return []