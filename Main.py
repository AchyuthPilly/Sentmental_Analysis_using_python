# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 16:01:37 2018

@author: Achyuth Pilly
"""

import tweepy,re
import matplotlib.pyplot as plt
from textblob import TextBlob

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'xxxxxxxxxxxxxxxxxxxx'
        consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        access_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        access_token_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
 
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
            print("Connection is Successful!!!")
        except:
            print("Error: Authentication Failed")
            
    def get_tweets(self, searchTerm, NoOfTerms):
        '''
        Main function to fetch tweets and parse them.
        '''
        self.searchTerm=searchTerm
        self.NoOfTerms=NoOfTerms
    
        # empty list to store parsed tweets
        tweets=[]
 
        try:
            # call twitter api to fetch tweets
           fetched_tweets = self.api.search(q = searchTerm, NoOfTerms = NoOfTerms)
          
            # parsing tweets one by one
           for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
 
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
 
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            # return parsed tweets
           return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
            
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," " ,tweet).split())
                               
                                    
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
        
    def percentage(self, part, whole):
        temp = round(100 * len(part) / len(whole),2)
        return format(temp, '.2f')
    
        
    def tweet_avg(self,tweets):
        #Picking positive tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        #Picking negetive tweets
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        #Picking neutral tweets
        ntrltweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
        
        #fetching the average of positive tweets
        positive=self.percentage(ptweets,tweets)
        print("Positive tweets percentage is: {} %".format(positive))
        #fetching the average of negetive tweets
        negative=self.percentage(ntweets,tweets)
        print("Negetive tweets percentege is: {} %".format(negative))
        #fetching the average of neutral tweets
        neutral=self.percentage(ntrltweets,tweets)
        print("Neutral tweets percentage is: {} %".format(neutral))
        
    # printing first 5 positive tweets    
        print("\n\nPositive tweets:\n")
        for tweet in ptweets[:10]:
            print(tweet['text'])
            
    # printing first 5 Neutral tweets    
        print("\n\nNeutral tweets:\n")
        for tweet in ntrltweets[:10]:
            print(tweet['text'])
 
    # printing first 5 negative tweets
        print("\n\nNegative tweets:\n")
        for tweet in ntweets[:10]:
            print(tweet['text'])
            
    #Plotting Pie chart
        labels = ['Positive [' + str(positive) + '%]','Neutral [' + str(neutral) + '%]', 'Negative [' + str(negative) + '%]']
        sizes = [positive, neutral, negative]
        colors = ['blue','green','red']
        explode = (0.1, 0, 0)
        text,patches=plt.pie(sizes,explode=explode, labels=labels,shadow=True, colors=colors, startangle=140)
        plt.title('Pie Chart depicting percentage of Sentiment of Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
        
def main():
        # creating object of TwitterClient Class
        api = TwitterClient()
        # calling function to get tweets
        tweets = api.get_tweets(searchTerm=input("Enter Keyword/Tag to search about: "),NoOfTerms=int(input("Enter how many tweets to search: ")))
        
        # Printing the percentage of sentiment of tweets
        api.tweet_avg(tweets)
        
         
 
if __name__ == "__main__":
    # calling main function
   main()