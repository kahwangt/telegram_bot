import logging
import os
import requests
import re
import json
import praw
from datetime import datetime, timedelta
from bottle import route, template, run
from twitter import *
from newsapi.newsapi_client import NewsApiClient
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = 'insert telegram token'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Welcome user!' + '\U0001F44B' + '\n\n' +
                    'For a little bit of motivation in life ' + '\U0001F973' + ', type /motivate\n' +
                    'For a random dog picture ' + '\U0001F436' + ', type /dog\n' +
                    'For a random reddit meme ' + '\U0001F92A' + ', type /memes\n' +
                    'For a random unsplash wallpaper ' + '\U0001F5BC' + ', type /wallpaper\n' +
                    'For current Singapore weather ' + '\U0001F324' + ', type /weather\n' +
                    'For latest tweets in Singapore ' + '\U0001F4AC' + ', type /tweets\n\n' +
                    'For SG latest news, choose from the following\n' +
                    'COVID19 ' + '\U0001F9A0' + ' ---> /covid \n' +
                    'Business ' + '\U0001F4BC' + ' ---> /business \n' +
                    'Entertainment ' + '\U0001F38A' + ' ---> /entertainment \n' +
                    'Technology ' + '\U0001F4F1' + ' ---> /technology \n' +
                    'Sports ' + '\U0001F93E' + ' ---> /sports \n\n' +
                    'Bot creation tutorial ' + '\U0001F9D0' + ' ---> /tutorial')
    sheet_db.append_row([update.message.from_user.username, (datetime.now()+ timedelta(hours=8)).strftime("%d/%m/%Y %H:%M:%S"), "start"])

# motivational quote
def motivate(update, context):
    quote = requests.request(url='https://api.quotable.io/random',method='get')
    update.message.reply_text(quote.json()['content'])

# dog pics
def dog(update, context):
    contents = requests.get('https://random.dog/woof.json').json()
    dog_pic = contents['url']
    update.message.reply_text(dog_pic)
    
# unsplash wallpaper
def wallpaper(update, context):
    url = 'insert unsplash token'
    response = requests.get(url)
    wall_pic = response.json()['urls']['regular']
    update.message.reply_text(wall_pic)

# news
newsapi = NewsApiClient(api_key='insert newsapi key')
business_news = newsapi.get_top_headlines(category='business', language='en', country='sg', page_size=3)
def business(update, context):
    business1 = list(business_news.values())[2][0]['title'] + '\n\n' + list(business_news.values())[2][0]['url']
    business2 = list(business_news.values())[2][1]['title'] + '\n\n' + list(business_news.values())[2][1]['url']
    business3 = list(business_news.values())[2][2]['title'] + '\n\n' + list(business_news.values())[2][2]['url']
    update.message.reply_text(business1)
    update.message.reply_text(business2)
    update.message.reply_text(business3)
    
enter_news = newsapi.get_top_headlines(category='entertainment', language='en', country='sg', page_size=3)
def entertainment(update, context):
    entertainment1 = list(enter_news.values())[2][0]['title'] + '\n\n' + list(enter_news.values())[2][0]['url']
    entertainment2 = list(enter_news.values())[2][1]['title'] + '\n\n' + list(enter_news.values())[2][1]['url']
    entertainment3 = list(enter_news.values())[2][2]['title'] + '\n\n' + list(enter_news.values())[2][2]['url']
    update.message.reply_text(entertainment1)
    update.message.reply_text(entertainment2)
    update.message.reply_text(entertainment3)
    
tech_news = newsapi.get_top_headlines(category='technology', language='en', country='sg', page_size=3)
def technology(update, context):
    tech1 = list(tech_news.values())[2][0]['title'] + '\n\n' + list(tech_news.values())[2][0]['url']
    tech2 = list(tech_news.values())[2][1]['title'] + '\n\n' + list(tech_news.values())[2][1]['url']
    tech3 = list(tech_news.values())[2][2]['title'] + '\n\n' + list(tech_news.values())[2][2]['url']
    update.message.reply_text(tech1)
    update.message.reply_text(tech2)
    update.message.reply_text(tech3)
    
sports_news = newsapi.get_top_headlines(category='sports', language='en', country='sg', page_size=3)
def sports(update, context):
    sports1 = list(sports_news.values())[2][0]['title'] + '\n\n' + list(sports_news.values())[2][0]['url']
    sports2 = list(sports_news.values())[2][1]['title'] + '\n\n' + list(sports_news.values())[2][1]['url']
    sports3 = list(sports_news.values())[2][2]['title'] + '\n\n' + list(sports_news.values())[2][2]['url']
    update.message.reply_text(sports1)
    update.message.reply_text(sports2)
    update.message.reply_text(sports3)
    
covid_news = newsapi.get_top_headlines(q='covid', language='en', country='sg', page_size=3)
def covid(update, context):
    covid1 = list(covid_news.values())[2][0]['title'] + '\n\n' + list(covid_news.values())[2][0]['url']
    covid2 = list(covid_news.values())[2][1]['title'] + '\n\n' + list(covid_news.values())[2][1]['url']
    covid3 = list(covid_news.values())[2][2]['title'] + '\n\n' + list(covid_news.values())[2][2]['url']
    update.message.reply_text(covid1)
    update.message.reply_text(covid2)
    update.message.reply_text(covid3)

# weather
api_key = "insert weather api"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
complete_url = base_url + "appid=" + api_key + "&q=" + "singapore" 
response = requests.get(complete_url) 
x = response.json() 
current_temperature = x['main']['temp']-273.15
feels_like = x['main']['feels_like']-273.15
weather_description = x['weather'][0]['description']
def weather(update, context):
    weather_stats = "\U0001F324 Singapore Weather \U0001F327" + "\n\nWeather Description = " + str(weather_description) + \
      "\nCurrent Temperature (in degree celsius) = " + str(round(current_temperature,1)) + \
      "\nFeels like (in degree celsius) = " + str(round(feels_like,1))
    update.message.reply_text(weather_stats)  

# memes
def memes(update, context):
    reddit = praw.Reddit(client_id='insert reddit client id',
                     client_secret='insert reddit client secret key', 
                     password='insert reddit api password',
                     user_agent='insert reddit api user_agent',
                     username='insert reddit api username')
    subreddit = reddit.subreddit("memes")
    meme = subreddit.random()
    update.message.reply_text(meme.url)

# twitter    
def tweets(update, context):
    update.message.reply_text(text='What Twitter topics are you interested in?')
def tweets_reply(update, context):
    user_input = update.message.text
    consumer_key= 'insert twitter consumer key'
    consumer_secret= 'insert twitter consumer secret'
    access_token= 'insert twitter access token'
    access_token_secret= 'insert twitter access secret'
    twitter = Twitter(auth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret))
    latitude = 1.3521    
    longitude = 103.8198    
    max_range = 20
    query_search = user_input + "-filter:retweets"
    query = twitter.search.tweets(q = query_search, geocode = "%f,%f,%dkm" % (latitude, longitude, max_range), lang='en',count=3)
    answer = f'\U0001F4F1 Showing latest 3 tweets in SG for: {user_input}'
    update.message.reply_text(answer)
    update.message.reply_text(query['statuses'][0]['text'])
    update.message.reply_text(query['statuses'][1]['text'])
    update.message.reply_text(query['statuses'][2]['text'])
    
# bot creation tutorial
def tutorial(update, context):
    update.message.reply_text('https://kierantan.medium.com/building-a-one-stop-api-caller-on-telegram-with-python-f8ff845d5985')
    
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("motivate", motivate))
    dp.add_handler(CommandHandler("dog", dog))
    dp.add_handler(CommandHandler("business", business))
    dp.add_handler(CommandHandler("entertainment", entertainment))
    dp.add_handler(CommandHandler("technology", technology))
    dp.add_handler(CommandHandler("sports", sports))
    dp.add_handler(CommandHandler("covid", covid))
    dp.add_handler(CommandHandler("wallpaper", wallpaper))
    dp.add_handler(CommandHandler("weather", weather))
    dp.add_handler(CommandHandler("memes", memes))
    dp.add_handler(CommandHandler("tutorial", tutorial))
    dp.add_handler(CommandHandler("tweets", tweets))
    dp.add_handler(MessageHandler(Filters.text, tweets_reply))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook('insert heroku app name' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()