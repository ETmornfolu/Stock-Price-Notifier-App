import requests


NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
API_KEY = "GX07FK8Q02082Q46"
NEWS_API_KEY = "86da72a39afa4b9cb0df3d5b48811d82"

news_feed_parameters = {
    "q": "premier league ",
    "from": "2025-01-14",
    "sortBy": "popularity",
    "apiKey": NEWS_API_KEY
}
response=requests.get(url=NEWS_ENDPOINT, params=news_feed_parameters)
news=response.json()
news_feed=news["articles"][0]
print(news_feed["publishedAt"])
