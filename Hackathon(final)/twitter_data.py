import tweepy
from textblob import TextBlob
import re
import twitter_credentials
from tweepy import OAuthHandler
from tweepy import AppAuthHandler
import pandas as pd 
import re
import emoji
import time
import nltk
from nltk.corpus import (
    wordnet,
    stopwords
)

##GetTweets will return fetched tweets from the user clicked location.

def getTweets(lat,lang):

   
    auth = AppAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
    api=tweepy.API(auth,wait_on_rate_limit=True,retry_count=3,timeout=60)

    search_word="lockdown OR corona OR COVID OR quarantine OR WHO OR stayhome OR socialdistancing OR pandemic OR virus OR selfisolation OR lockdownbirthday"
    date="2020-03-23"       #Tweets will be from this date


    km="150km"               #This km is for Geocoding 
    geo='"'+lat+','+lang+","+km+'"'
    t0=time.time()
    tweets=tweepy.Cursor(api.search,q=search_word,since=date,geocode=geo,lang="en",tweet_mode='extended').items(1000)

    ##creating dataframe for tweets data 

    df=pd.DataFrame([tweet._json['retweeted_status']['full_text'] if 'retweeted_status' in tweet._json else tweet.full_text for tweet in tweets],columns=["Tweets"])
    t1=time.time()
    print("time for fetching tweets:",(t1-t0))
    if len(df.index) == 0:

         km="300km"               #This km is for Geocoding 
         geo='"'+lat+','+lang+","+km+'"'
         tweets=tweepy.Cursor(api.search,q=search_word,since=date,geocode=geo,lang="en",tweet_mode='extended').items(1000)
         ##creating dataframe for tweets data 
         print("workingg")
         df=pd.DataFrame([tweet._json['retweeted_status']['full_text'] if 'retweeted_status' in tweet._json else tweet.full_text for tweet in tweets],columns=["Tweets"])

    ##calling cleanTxt function for preprocessing the data

    df['Tweets'] = df['Tweets'].apply(cleanTxt)
    df['Tweets'] = df['Tweets'].apply(stop_words)
    return df['Tweets']

###Tweets fetched from twitter will have emojies,link.cleanTxt will return cleaned tweets

def cleanTxt(table):
    #put everythin in lowercase
    table=re.sub('[0-9]','',table)
    table = re.sub('RT?\S+', '',table)
    table = re.sub('http?://\S+', '', table)
    table = re.sub('https?://\S+', '', table)
    table = re.sub('www.?\S+', '',table)
    table = table.lower()
    table = re.sub('@[A-Za-z0–9]+', '',table)
    #Replace rt indicating that was a retweet
    #table = table.replace('[!"#$%&()*+,-./:;<=>?@[\]^_`{|}~]', '')
    #Replace occurences of mentioning @UserNames
    table=re.sub(r"[^\w\d'\s]+",'',table)
    table=emoji.demojize(table)
    return table

def stop_words(table):
    #We need to remove the stop words
    stopwords = nltk.corpus.stopwords.words('english')
    #spacy's stop words
    newStopWords = ['im','oh','lol','whence','id', 'here', 'show', 'were', 'why', 'n’t', 'the', 'whereupon', 'not', 'more', 'how', 'eight', 'indeed', 'i', 'only', 'via', 'nine', 're', 'themselves', 'almost', 'to', 'already', 'front', 'least', 'becomes', 'thereby', 'doing', 'her', 'together', 'be', 'often', 'then', 'quite', 'less', 'many', 'they', 'ourselves', 'take', 'its', 'yours', 'each', 'would', 'may', 'namely', 'do', 'whose', 'whether', 'side', 'both', 'what', 'between', 'toward', 'our', 'whereby', "'m", 'formerly', 'myself', 'had', 'really', 'call', 'keep', "'re", 'hereupon', 'can', 'their', 'eleven', '’m', 'even', 'around', 'twenty', 'mostly', 'did', 'at', 'an', 'seems', 'serious', 'against', "n't", 'except', 'has', 'five', 'he', 'last', '‘ve', 'because', 'we', 'himself', 'yet', 'something', 'somehow', '‘m', 'towards', 'his', 'six', 'anywhere', 'us', '‘d', 'thru', 'thus', 'which', 'everything', 'become', 'herein', 'one', 'in', 'although', 'sometime', 'give', 'cannot', 'besides', 'across', 'noone', 'ever', 'that', 'over', 'among', 'during', 'however', 'when', 'sometimes', 'still', 'seemed', 'get', "'ve", 'him', 'with', 'part', 'beyond', 'everyone', 'same', 'this', 'latterly', 'no', 'regarding', 'elsewhere', 'others', 'moreover', 'else', 'back', 'alone', 'somewhere', 'are', 'will', 'beforehand', 'ten', 'very', 'most', 'three', 'former', '’re', 'otherwise', 'several', 'also', 'whatever', 'am', 'becoming', 'beside', '’s', 'nothing', 'some', 'since', 'thence', 'anyway', 'out', 'up', 'well', 'it', 'various', 'four', 'top', '‘s', 'than', 'under', 'might', 'could', 'by', 'too', 'and', 'whom', '‘ll', 'say', 'therefore', "'s", 'other', 'throughout', 'became', 'your', 'put', 'per', "'ll", 'fifteen', 'must', 'before', 'whenever', 'anyone', 'without', 'does', 'was', 'where', 'thereafter', "'d", 'another', 'yourselves', 'n‘t', 'see', 'go', 'wherever', 'just', 'seeming', 'hence', 'full', 'whereafter', 'bottom', 'whole', 'own', 'empty', 'due', 'behind', 'while', 'onto', 'wherein', 'off', 'again', 'a', 'two', 'above', 'therein', 'sixty', 'those', 'whereas', 'using', 'latter', 'used', 'my', 'herself', 'hers', 'or', 'neither', 'forty', 'thereupon', 'now', 'after', 'yourself', 'whither', 'rather', 'once', 'from', 'until', 'anything', 'few', 'into', 'such', 'being', 'make', 'mine', 'please', 'along', 'hundred', 'should', 'below', 'third', 'unless', 'upon', 'perhaps', 'ours', 'but', 'never', 'whoever', 'fifty', 'any', 'all', 'nobody', 'there', 'have', 'anyhow', 'of', 'seem', 'down', 'is', 'every', '’ll', 'much', 'none', 'further', 'me', 'who', 'nevertheless', 'about', 'everywhere', 'name', 'enough', '’d', 'next', 'meanwhile', 'though', 'through', 'on', 'first', 'been', 'hereby', 'if', 'move', 'so', 'either', 'amongst', 'for', 'twelve', 'nor', 'she', 'always', 'these', 'as', '’ve', 'amount', '‘re', 'someone', 'afterwards', 'you', 'nowhere', 'itself', 'done', 'hereafter', 'within', 'made', 'ca', 'them']
    stopwords.extend(newStopWords)
    table = ' '.join([word for word in table.split() if word not in (stopwords)])
    return table



	

