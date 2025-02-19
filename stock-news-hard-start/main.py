import requests
from smtplib import *
from math import floor
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
API_KEY = "GX07FK8Q02082Q46"
NEWS_API_KEY = "86da72a39afa4b9cb0df3d5b48811d82"

MY_EMAIL = "emmanuelmoronfolu6@gmail.com"
PASSWORD = "cuophgaoasoiabpz"

stock_market_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY,
    "outputsize": "compact"
}
news_feed_parameters = {
    "q": COMPANY_NAME,
    "from": "2024-12-12",
    "sortBy": "popularity",
    "apiKey": NEWS_API_KEY
}


def positive_difference(num1, num2):
    return abs(num1 - num2)


## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
# HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
# HINT 2: Work out the value of 5% of yerstday's closing stock price.
stock_market_response = requests.get(STOCK_ENDPOINT, params=stock_market_parameters)
stock_market_response.raise_for_status()
stock_market_data = stock_market_response.json()
yesterdays_closing_price = float(stock_market_data["Time Series (Daily)"]["2024-12-13"]["4. close"])
day_before_yesterday_closing_price = float(stock_market_data["Time Series (Daily)"]["2024-12-12"]["4. close"])

price_tuple = (yesterdays_closing_price, day_before_yesterday_closing_price)
print(price_tuple)
# Example usage

positive_diff = positive_difference(yesterdays_closing_price, day_before_yesterday_closing_price)
price_margin_percentage = floor(positive_diff / abs(day_before_yesterday_closing_price) * 100)

print(f"{price_margin_percentage} %")

## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME.
# HINT 1: Think about using the Python Slice Operator
news_response = requests.get(NEWS_ENDPOINT, params=news_feed_parameters)
news_response.raise_for_status()
news_feed = news_response.json()
news_article = news_feed["articles"]
news_article_list = news_article[:3]
articles = [f"Headline:{article['title']}\nNews brief:{article['description']}\n{article['url']}" for article in
            news_article_list]
subject = f"TSLA,{price_margin_percentage}%"


def send_email(logo):
    for message in articles:
        with SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs="emmanuelmoronfolu6@gmail.com",
                                msg=f"Subject:{logo},{subject}\n\n{message}".encode("utf-8")
                                )


## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number.
# HINT 1: Consider using a List Comprehension.
if price_margin_percentage > 3 and day_before_yesterday_closing_price > yesterdays_closing_price:
    send_email(logo="📈")
elif price_margin_percentage > 3 and yesterdays_closing_price > day_before_yesterday_closing_price:
    send_email(logo="📈")

# Optional: Format the SMS message like this:
"""
TSLA: 2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
