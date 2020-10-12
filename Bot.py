from Controller import Controller
import tweepy
import sys
import datetime
import time
import csv
import json
from NLP import NLP

class Bot():

    def __init__(self):
        self.api = Controller().getApi()
        self.nlp = NLP()
        self.clf, self.count_vect, self.tfidf_transformer = self.nlp.train() 
        
    def getTweetsByCountry(self, country=None):
        # api = tweepy.API(auth)
        places = self.api.geo_search(query=country,granularity="country", tweet_mode='extended')
        place_id = places[0].id
        tweets = self.api.search(q="place:%s" % place_id)

        return tweets

    def postImg(self, img, msg):
        self.api.update_with_media(img, status=msg)

    def getTweetsByUser(self, user):
        tweets = self.api.user_timeline(user, tweet_mode='extended')
        for i in tweets:
            print(i._json['full_text'])
            break

    def getTweetsByDate(self, user, startDate, endDate):
        print("Recuperando Tweets...")
        username = user
        startDate = datetime.datetime(*startDate)
        endDate =   datetime.datetime(*endDate)

        tweets = []
        tmpTweets = self.api.user_timeline(username, tweet_mode='extended')
        print("Tweets recuperados, fazendo for com as datas...")
        for tweet in tmpTweets:
            if tweet.created_at < endDate and tweet.created_at > startDate:
                tweets.append(tweet)
            
            while (tmpTweets[-1].created_at > startDate):
                tmpTweets = self.api.user_timeline(username, max_id = tmpTweets[-1].id, tweet_mode='extended')
                
                if len(tmpTweets) == 0:
                    print("Fim do for com as datas")
                    return tweets

                for tweet in tmpTweets:
                    if tweet.created_at < endDate and tweet.created_at > startDate:
                        tweets.append(tweet)
          return tweets
    def post(self, content):
        self.api.update_status(content)

    def reply(self, content, tweetId, user):
        self.api.update_status("@"+user+ " " + content, in_reply_to_status_id=tweetId)
        

    def getTweetByID(self, _id):
        try:
            return self.api.get_status(id=_id)
        except tweepy.error.TweepError:
            return None

    def getTweets(self):
        return self.api.home_timeline(tweet_mode='extended')

    def getLastTweet(self):
        return self.api.home_timeline()[0]
    
    def getReplies(self, user, _id):
        replies = tweepy.Cursor(self.api.search, q='to:{}'.format(user), since_id=_id, tweet_mode='extended').items()
        
        while True:
            try:
                time.sleep(0.5)
                reply = replies.next()

                if not hasattr(reply, 'in_reply_to_status_id_str'):                    
                    continue

                if reply.in_reply_to_status_id == _id:
                    print("User: " + reply.user.name)
                    print("reply of tweet:{}".format(reply.full_text))
                
            except StopIteration:
                break
    
    def showContentTweets(self, tweets, classify):        
        for a in tweets:
            _id = a._json['id_str']
            user = a._json['user']['screen_name']
            post = a._json['full_text'] 

            print("Ususario: "+user)
            print("ID: "+_id)
            print("text: "+post)
            if classify:
                print("Classificação: " + self.nlp.predict(self.clf, self.count_vect, self.tfidf_transformer, [post]))
            

            # self.getReplies(user, _id)
            
            print("----------------------------------")     

    def writeCsv(self, tweets):
        dataSet = []

        for a in tweets:
            _id = a._json['id']
            user = a._json['user']['screen_name']
            post = a._json['full_text']   
        

        with open('dataTweeter.csv', mode='w') as dataTweeter:
            writer = csv.writer(dataTweeter, delimiter=';')
            writer.writerow(["ID", "USER", "POST"])
            for a in tweets:
                writer.writerow([str(a._json['id']), a._json['user']['screen_name'], a._json['full_text']])
            
        
        print("CSV criado.")

    
    def getTrendTopics(self):
        BRAZIL_WOE_ID = 23424768
 
        brazil_trends = self.api.trends_place(BRAZIL_WOE_ID)
        
        trends = json.loads(json.dumps(brazil_trends, indent=1))
        
        for trend in trends[0]["trends"]:
            print (trend["name"].strip("#") )

