from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import ipynb
import pickle
import nltk
import re
import emoji
import numpy as np
import sqlite3
import datetime
import time
import pandas as pd

x_count = 0
y_count = 0
del_count = 0
conn = sqlite3.connect('twitter.db')
c = conn.cursor()


def create_table():
    try:
        c.execute("CREATE TABLE IF NOT EXISTS sentiment(tweet TEXT, created_at REAL, sentiment REAL, var1 REAL, var2 REAL)")
        c.execute("CREATE INDEX fast_tweet ON sentiment(tweet)")
        c.execute("CREATE INDEX fast_created_at ON sentiment(created_at)")
        c.execute("CREATE INDEX fast_sentiment ON sentiment(sentiment)")
        c.execute("CREATE INDEX fast_var1 ON sentiment(var1)")
        c.execute("CREATE INDEX fast_var2 ON sentiment(var2)")
        conn.commit()
    except Exception as e:
        #pass
        print(str(e))
create_table()    
    
def delete1():
   c.execute('DELETE FROM sentiment;',)
   conn.commit()
delete1()
#sqlQuery    = "Select * from sentiment"
#c.execute(sqlQuery)
#recs = c.fetchall()
#print(recs)

#fil = open('C:\\Users\\Sudhakar T\\Desktop\\IBM\\twitter-out.txt','r+')
#fil.truncate(0)
#fil.close()
loaded_model = pickle.load(open('finalized_model123.sav','rb'))
stopwords = nltk.corpus.stopwords.words('english')
##    #spacy's stop words
newStopWords = ['im','oh','lol','whence','id', 'here', 'show', 'were', 'why', 'n’t', 'the', 'whereupon', 'not', 'more', 'how', 'eight', 'indeed', 'i', 'only', 'via', 'nine', 're', 'themselves', 'almost', 'to', 'already', 'front', 'least', 'becomes', 'thereby', 'doing', 'her', 'together', 'be', 'often', 'then', 'quite', 'less', 'many', 'they', 'ourselves', 'take', 'its', 'yours', 'each', 'would', 'may', 'namely', 'do', 'whose', 'whether', 'side', 'both', 'what', 'between', 'toward', 'our', 'whereby', "'m", 'formerly', 'myself', 'had', 'really', 'call', 'keep', "'re", 'hereupon', 'can', 'their', 'eleven', '’m', 'even', 'around', 'twenty', 'mostly', 'did', 'at', 'an', 'seems', 'serious', 'against', "n't", 'except', 'has', 'five', 'he', 'last', '‘ve', 'because', 'we', 'himself', 'yet', 'something', 'somehow', '‘m', 'towards', 'his', 'six', 'anywhere', 'us', '‘d', 'thru', 'thus', 'which', 'everything', 'become', 'herein', 'one', 'in', 'although', 'sometime', 'give', 'cannot', 'besides', 'across', 'noone', 'ever', 'that', 'over', 'among', 'during', 'however', 'when', 'sometimes', 'still', 'seemed', 'get', "'ve", 'him', 'with', 'part', 'beyond', 'everyone', 'same', 'this', 'latterly', 'no', 'regarding', 'elsewhere', 'others', 'moreover', 'else', 'back', 'alone', 'somewhere', 'are', 'will', 'beforehand', 'ten', 'very', 'most', 'three', 'former', '’re', 'otherwise', 'several', 'also', 'whatever', 'am', 'becoming', 'beside', '’s', 'nothing', 'some', 'since', 'thence', 'anyway', 'out', 'up', 'well', 'it', 'various', 'four', 'top', '‘s', 'than', 'under', 'might', 'could', 'by', 'too', 'and', 'whom', '‘ll', 'say', 'therefore', "'s", 'other', 'throughout', 'became', 'your', 'put', 'per', "'ll", 'fifteen', 'must', 'before', 'whenever', 'anyone', 'without', 'does', 'was', 'where', 'thereafter', "'d", 'another', 'yourselves', 'n‘t', 'see', 'go', 'wherever', 'just', 'seeming', 'hence', 'full', 'whereafter', 'bottom', 'whole', 'own', 'empty', 'due', 'behind', 'while', 'onto', 'wherein', 'off', 'again', 'a', 'two', 'above', 'therein', 'sixty', 'those', 'whereas', 'using', 'latter', 'used', 'my', 'herself', 'hers', 'or', 'neither', 'forty', 'thereupon', 'now', 'after', 'yourself', 'whither', 'rather', 'once', 'from', 'until', 'anything', 'few', 'into', 'such', 'being', 'make', 'mine', 'please', 'along', 'hundred', 'should', 'below', 'third', 'unless', 'upon', 'perhaps', 'ours', 'but', 'never', 'whoever', 'fifty', 'any', 'all', 'nobody', 'there', 'have', 'anyhow', 'of', 'seem', 'down', 'is', 'every', '’ll', 'much', 'none', 'further', 'me', 'who', 'nevertheless', 'about', 'everywhere', 'name', 'enough', '’d', 'next', 'meanwhile', 'though', 'through', 'on', 'first', 'been', 'hereby', 'if', 'move', 'so', 'either', 'amongst', 'for', 'twelve', 'nor', 'she', 'always', 'these', 'as', '’ve', 'amount', '‘re', 'someone', 'afterwards', 'you', 'nowhere', 'itself', 'done', 'hereafter', 'within', 'made', 'ca', 'them']
stopwords.extend(newStopWords)
##
def cleanTxt(tweet):
    #put everythin in lowercase
    tweet=re.sub('[0-9]','',tweet)
    tweet = re.sub('RT?\S+', '',tweet)
    tweet = re.sub('http?://\S+', '', tweet)
    tweet = re.sub('https?://\S+', '', tweet)
    tweet = re.sub('www.?\S+', '',tweet)
    tweet = tweet.lower()
    tweet = re.sub('@[A-Za-z0–9]+', '',tweet)
    #Replace rt indicating that was a retweet
    #table = table.replace('[!"#$%&()*+,-./:;<=>?@[\]^_`{|}~]', '')
    #Replace occurences of mentioning @UserNames
    tweet=re.sub(r"[^\w\d'\s]+",'',tweet)
    tweet=emoji.demojize(tweet)
    return tweet

def stop_words(tweet):
    #We need to remove the stop words
    tweet = ' '.join([word for word in tweet.split() if word not in (stopwords)])
    return tweet

def clean(tweet):
    return(stop_words(cleanTxt(tweet)))

def sentiment1(tweet):
    global x_count
    global y_count
    
    #t0 = time.time()
    tweet = clean(tweet)
    #t1 = time.time()
    result,conf = loaded_model.predict([tweet]),loaded_model.predict_proba([tweet])
    #print(result,conf)
    ind  = np.argmax(conf[0])
    conf = round(max(conf[0]),2)

    x_count += 1
    #t2 = time.time()
    #print("cleaning time ;", t1 - t0)
    #print("loading time ;", t2 - t1)
    if ((result == 0) and (conf >= 0.70) and (ind == 0)):
      result = -1
      y_count -= 1
      
    
      # print(conf)
    elif ((result == 4) and (conf >= 0.70) and (ind == 1) ):
      result  = 1
      y_count += 1
    # print(conf)
    else :
      result  = 0
      y_count = y_count
    return (result ,x_count, y_count)


ACCESS_TOKEN = "1054958808789934081-cwkPzSd7DfYAY6YtKEJ0tILfWFcmxT"
ACCESS_TOKEN_SECRET = "EImrTHBtAaASADWVoXTwZzciAEnyftkeuB0ZrWIGWOptf"
CONSUMER_KEY = "A0Ro0FdsNrVhnaf5HJ3lkB3yU"
CONSUMER_SECRET = "MTBGPJ7urGnrwzJYRjNNyQCDskTFgbBXS83m9Z7tTOMRCTStuC"


class listener(StreamListener):

    def on_data(self, data):

        try :
            global del_count
            del_count += 1
            all_data = json.loads(data)
            tweet = all_data["text"]
            time1 = datetime.datetime.now().strftime('%D, %H:%M:%S')
            #df['created_at'] = pd.to_datetime(time)
            sentiment_value , var1 , var2  = sentiment1(tweet)
            print(var1)
            #print(tweet,sentiment_value)
            c.execute("INSERT INTO sentiment(tweet, created_at, sentiment, var1, var2) VALUES (?, ?, ?, ?, ?)",
                  (tweet, time1, sentiment_value, var1, var2))
            conn.commit()
            #if((del_count % 50) == 0):
            #    delete1()
            #    print("yes")
            

        #if confidence*100 >= 75:
        #output = open("C:/Users/Sudhakar T/Desktop/IBM/twitter-out.txt","a")
        #output.write(str(sentiment_value))
        #output.write('\n')
        #output.close()


            #sqlQuery    = "Select * from sentiment"
            #c.execute(sqlQuery)
            #recs = c.fetchall()
            #print(recs)

        except KeyError as e:
            #pass
            print(str(e))
        return (True)
     

    def on_error(self, status):
        #pass
        print(status)





while True:

    try:
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        twitterStream = Stream(auth, listener())
        twitterStream.filter(track=["lockdown"])
    except Exception as e:
        print(str(e))
        time.sleep(5)