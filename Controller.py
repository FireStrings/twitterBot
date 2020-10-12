import tweepy
import configparser

class Controller():

    def __init__(self):
        pass
    
    def getCredentials(self):
        config = configparser.ConfigParser()
        config.sections()

        config.read('/home/pi/Bot/config/config.conf')

        return config['CRED']['consumer_key'], config['CRED']['consumer_secret'], config['CRED']['access_token'], config['CRED']['access_token_secret']

    def getAuth(self):
        consumer_key, consumer_secret,access_token, access_token_secret = self.getCredentials()

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        return auth

    def getApi(self):   
        return tweepy.API(self.getAuth(), wait_on_rate_limit=True) 