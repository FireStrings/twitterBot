#!/usr/bin/python3
# -*- coding:utf8 -*-

from Bot import Bot
import os
import datetime
from datetime import date
import pandas as pd
import time
import sys
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from scipy.misc import imread
import random

print("Criando instâncias...")
bot = Bot()

def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

def gernerateWordCloud():

    country = "Ireland"

    f = open("tweets", "w")
    tweets = bot.getTweetsByCountry(country)
    for status in tweets:
        f.write(bot.nlp.cleanText(bot.getTweetByID(status.id).text))
        
        # print(a[0]._json['text'])

    f.close()

    words= " "
    count =0
    f = open("tweets", "r")
    for line in f:
        words= words + line
    
    f.close
    
    stopwords = {"will"}

    logomask = imread("cloud.png")

    wordcloud = WordCloud(
        stopwords=STOPWORDS.union(stopwords),
        background_color="black",
        mask = logomask,
        max_words=500,
        width=1800,
        height=1400
        ).generate(words)

    plt.imshow(wordcloud.recolor(color_func=grey_color_func, random_state=3))
    plt.axis("off")
    plt.savefig("./tweetcloud2.png", dpi=300)

    bot.postImg("./tweetcloud2.png", "Here's a cloud words test, most speaked words in " + country)
    plt.show()

def postTemperature():
    print("Recueprando Temperatura...")
    temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read().split("=")[1]
    data = time.ctime()


    bot.post("XMechina Bot, on "+str(data)+". Current CPU temperature: " + temp)

def reply():
    tweets = bot.getTweets()
    _id = tweets[0]._json['id_str']
    user = tweets[0]._json['user']['screen_name']
    bot.reply("Texto de reply", _id, user)

def getTweetsByDate(user, startDate, endDate):
    tweets = bot.getTweetsByDate(user, startDate, endDate)
    # bot.writeCsv(tweets)
    # bot.showContentTweets(tweets)
    return tweets

def getTimeLineTweets():
    lFinal = [] 
    tweets = bot.getTweets()
    # bot.writeCsv(tweets)
    # bot.showContentTweets(tweets, classify=False)
    return tweets

def getTweetsByUser(user):
    bot.getTweetsByUser(user)

def getTweetById(id):
    tweets = bot.getTweetByID(id)


def download_tweets(id_file, sentiment):
    l = []
    with open(id_file) as infile:
        for tweet_id in infile:
            tweet_id = tweet_id.strip()

            # if l.exist_tweet(tweet_id):
            #     print("tweet com id: ", tweet_id, "já foi capturado")
            #     continue

            try:
                tweet = getTweetById(tweet_id)
                if tweet is None:
                    print("Sem id")
                else:
                    l.append([tweet, sentiment])
            except tweepy.error.TweepError:
                print("tweet com id: ", tweet_id, "não está disponível")

            print(l)
            time.sleep(0.1)

# print("Capturando tweets positivos ...")
# download_tweets("tpositivos.txt", 1)

# print("Capturando tweets negativos ...")
# download_tweets("tnegativos.txt", 0)
# postTemperature()
# getTweetsByUser("folha")
# bot.getTrendTopics()
# getTimeLineTweets()
# getTweetsByDate("folha", (2020, 3, 27, 0, 0, 0), (2020, 3, 28, 12, 0, 0))

# gernerateWordCloud()

tweetsUsers = []
tFinal = []
tbd = []
tweets = getTimeLineTweets()

for i in tweets:
    user = i._json["user"]["screen_name"]
    tweetsUsers.append(user)

tweetsUsers = list(set(tweetsUsers))
for i in tweetsUsers:
    print(i)
    tbd+=getTweetsByDate(i, (2020, 9, 11, 0, 0, 0), (2020, 10, 11, 18, 0, 0))
   
bot.writeCsv(tbd)

print("Fim")