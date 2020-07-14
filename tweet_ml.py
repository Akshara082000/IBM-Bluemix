import pandas as pd
import twitter_data
import time
from sklearn import svm
from sklearn.metrics import classification_report

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import time
import pickle
loaded_model = pickle.load(open("finalized_model123.sav",'rb'))



def ML(lat,lang): 
    ##Training Dta using SVM classifier

    #Reading trainData and testData
    
    ##Calling the actual twitter data to apply our traing model
    #vectorizer = TfidfVectorizer(min_df = 5, max_df = 0.8, sublinear_tf = True,use_idf = True)
    t0=time.time()
    tweets=twitter_data.getTweets(lat,lang)##return preprocessed  twitter data fetched from the location 
    t1=time.time()
    print("time for fetching tweets with cleaning:",(t1-t0))
    #review = tweets# vectorizing

    positive_tweets=[] ##to store all the positive tweets
    negative_tweets=[] ## to store all the negative tweets
    
    ##Vectorizing the tweets and predicting its sentiment polarity.  
    
    #for i in review:
        #review_vector = vectorizer.transform([i])
    #x=loaded_model.predict(review).astype(str)
    t0=time.time()
    x=loaded_model.predict(tweets)
    t1=time.time()
    print("time for predicting:",(t1-t0))
    print(x)
    #print(type(x))
    list_conv=x.tolist()
 
    for i in list_conv:
        #x=x.astype(str)
        if i==4:
            positive_tweets.append(i) ##append positive tweets        
            
        else:
            negative_tweets.append(i) ##append negative tweets
                
            

  
  
    totaltweets=len(tweets)

    if totaltweets == 0:

        return totaltweets,positive_tweets,negative_tweets,"",0
    
    ##Count the popular words and its occarance

    cv = CountVectorizer(stop_words = 'english')
    words = cv.fit_transform(tweets)
    sum_words = words.sum(axis=0)
    words_freq = [(word, sum_words[0, i]) for word, i in cv.vocabulary_.items()]
    words_freq = sorted(words_freq, key = lambda x: x[1], reverse = True) ##Sorting to get the highest frequency First

    frequency = pd.DataFrame(words_freq, columns=['word', 'freq'])

    wordoffreq=[word for word in frequency.word] ##Creating List of words for data visulaization 
    print(wordoffreq)
    freq=frequency.freq ##Frequency of the words 
     
    ##Returning data to app.py(root file) to display in front end
    print(totaltweets)
    return totaltweets,positive_tweets,negative_tweets,wordoffreq,freq
    

