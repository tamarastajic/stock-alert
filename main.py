import requests
from datetime import *
from twilio.rest import Client

# ~~~~~~~~~~~~~~~ GETTING DATA FROM alphavantage.co - TIME_SERIES_DAILY_ADJUSTED API ~~~~~~~~~~~~~~~

# Important Data
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_ENDPOINT = "https://www.alphavantage.co/query"
# Input your own data
ALPHA_API_KEY = YOUR ALPHAVANTAGE API KEY

alpha_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": ALPHA_API_KEY
}

# Getting Data
response = requests.get(ALPHA_ENDPOINT, params=alpha_params)
response.raise_for_status()

data = response.json()["Time Series (Daily)"]

# ~~~~~~~~~~~~~~~ Using datetime to Acquire Data from the Last Two Days ~~~~~~~~~~~~~~~
today = datetime.today()

# Making Sure to Get Data and Avoid Weekends
yesterday = today - timedelta(days=1)
yesterday_date = yesterday.date()
while True:
    try:
        y_data = data[str(yesterday_date)]["4. close"]
    except KeyError:
        yesterday = yesterday - timedelta(days=1)
        yesterday_date = yesterday.date()
    else:
        break

day_before_y = yesterday - timedelta(days=1)
day_before_y_date = day_before_y.date()
while True:
    try:
        day_before_y_data = data[str(day_before_y_date)]["4. close"]
    except KeyError:
        day_before_y_date = day_before_y_date - timedelta(days=1)
    else:
        break

y_data = float(y_data)
day_before_y_data = float(day_before_y_data)

# ~~~~~~~~~~~~~~~ Calculating the Difference and its Percentage ~~~~~~~~~~~~~~~
difference = y_data - day_before_y_data
difference = round(difference, 2)

difference_percent = round((difference / y_data) * 100)

# ~~~~~~~~~~~~~~~ GETTING DATA FROM newsapi.org - EVERYTHING API ~~~~~~~~~~~~~~~
# Necessary Info
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
# Input your own data
NEWS_API_KEY = YOUR NEWSAPI KEY

news_params = {
    "apiKey": NEWS_API_KEY,
    "q": COMPANY_NAME,
    "searchIn": "title,description",
    "from": str(yesterday_date),
    "sortBy": "popularity",
    "pageSize": 3,
    "language": "en"
}

# Acquiring Data
response = requests.get(NEWS_ENDPOINT, params=news_params)
news_data = response.json()["articles"]

# Making a List of Top 3 News
top_3_news = []

for i in range(3):
    news = {"headline": news_data[i]["title"], "summary": news_data[i]["description"]}
    top_3_news.append(news)

# ~~~~~~~~~~~~~~~ GETTING DATA FROM twilio.com - SEND SMS API ~~~~~~~~~~~~~~~

# Necessary Info
# Input your own data!
TWILIO_SID = YOUR TWILIO SID
TWILIO_AUTH = YOUR TWILIO AUTH
from_number = SENDER NUMBER
to_number = RECIPIENT NUMBER

# Creating the Body of the Text Message
if difference > 0:
    icon = f"⬆ {abs(difference_percent)}%"
elif difference < 0:
    icon = f"⬇ {abs(difference_percent)}%"
else:
    icon = f" Stock Price Same as Yesterday: ${y_data}"

text = f"{STOCK}: {icon}"

for i in range(3):
    headline = top_3_news[i]["headline"]
    brief = top_3_news[i]["summary"]
    text = text + "\n" + f"{i+1}: " + headline + "\n" + brief

print(text)

# Sending the Text Message
client = Client(TWILIO_SID, TWILIO_AUTH)
if difference_percent >= 5:
    message = client.messages \
        .create(
            body=text,
            from_=from_number,
            to=to_number"
                )
    print(message.status)
