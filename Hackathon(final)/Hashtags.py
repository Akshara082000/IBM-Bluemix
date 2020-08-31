import tweepy
from tweepy import AppAuthHandler
import pandas as pd 
import re
import pickle
import emoji
import nltk


stopwords = nltk.corpus.stopwords.words('english')
    #spacy's stop words
newStopWords = ['im','oh','lol','whence','id', 'here', 'show', 'were', 'why'
    , 'n’t', 'the', 'whereupon', 'not', 'more', 'how', 'eight', 'indeed', 'i', 'only'
    , 'via', 'nine', 're', 'themselves', 'almost', 'to', 'already', 'front', 'least', 
    'becomes', 'thereby', 'doing', 'her', 'together', 'be', 'often', 'then', 'quite', 'less', 
    'many', 'they', 'ourselves', 'take', 'its', 'yours', 'each', 'would', 'may', 'namely', 'do'
    , 'whose', 'whether', 'side', 'both', 'what', 'between', 'toward', 'our', 'whereby', "'m", 'formerly'
    , 'myself', 'had', 'really', 'call', 'keep', "'re", 'hereupon', 'can', 'their', 'eleven', '’m', 'even',
     'around', 'twenty', 'mostly', 'did', 'at', 'an', 'seems', 'serious', 'against', "n't", 'except', 'has', 
     'five', 'he', 'last', '‘ve', 'because', 'we', 'himself', 'yet', 'something', 'somehow', '‘m', 'towards', 'his',
     'six', 'anywhere', 'us', '‘d', 'thru', 'thus', 'which', 'everything', 'become', 'herein',
     'one', 'in', 'although', 'sometime', 'give', 'cannot', 'besides', 'across', 'noone', 'ever',
        'that', 'over', 'among', 'during', 'however', 'when', 'sometimes', 'still', 'seemed', 'get',
         "'ve", 'him', 'with', 'part', 'beyond', 'everyone', 'same', 'this', 'latterly', 'no', 'regarding', 
         'elsewhere', 'others', 'moreover', 'else', 'back', 'alone', 'somewhere', 'are', 'will', 'beforehand', 
         'ten', 'very', 'most', 'three', 'former', '’re', 'otherwise', 'several', 'also', 'whatever', 'am', 
         'becoming', 'beside', '’s', 'nothing', 'some', 'since', 'thence', 'anyway', 'out', 'up', 'well', 'it', 
         'various', 'four', 'top', '‘s', 'than', 'under', 'might', 'could', 'by', 'too', 'and', 'whom', '‘ll',
          'say', 'therefore', "'s", 'other', 'throughout', 'became', 'your', 'put', 'per', "'ll", 'fifteen',
           'must', 'before', 'whenever', 'anyone', 'without', 'does', 'was', 'where', 'thereafter', "'d",
            'another', 'yourselves', 'n‘t', 'see', 'go', 'wherever', 'just', 'seeming', 'hence', 'full',
             'whereafter', 'bottom', 'whole', 'own', 'empty', 'due', 'behind', 'while', 'onto', 'wherein', 
             'off', 'again', 'a', 'two', 'above', 'therein', 'sixty', 'those', 'whereas', 'using', 'latter', 
             'used', 'my', 'herself', 'hers', 'or', 'neither', 'forty', 'thereupon', 'now', 'after', 'yourself', 
             'whither', 'rather', 'once', 'from', 'until', 'anything', 'few', 'into', 'such', 'being', 'make', 
             'mine', 'please', 'along', 'hundred', 'should', 'below', 'third', 'unless', 'upon', 'perhaps', 'ours', 
             'but', 'never', 'whoever', 'fifty', 'any', 'all', 'nobody', 'there', 'have', 'anyhow', 'of', 'seem', 
             'down', 'is', 'every', '’ll', 'much', 'none', 'further', 'me', 'who', 'nevertheless', 'about', 'everywhere', 
             'name', 'enough', '’d', 'next', 'meanwhile', 'though', 'through', 'on', 'first', 'been', 'hereby', 'if', 'move', 
             'so', 'either', 'amongst', 'for', 'twelve', 'nor', 'she', 'always', 'these', 'as', '’ve', 'amount', '‘re', 'someone',
              'afterwards', 'you', 'nowhere', 'itself', 'done', 'hereafter', 'within', 'made', 'ca', 'them']
stopwords.extend(newStopWords)

def stop_words(table):
    #We need to remove the stop words

    table = ' '.join([word for word in table.split() if word not in (stopwords)])
    return table


def cleanTxt(table):
    #put everythin in lowercase
    table=re.sub('[0-9]','',table)
    #table = re.sub('RT?\S+', '',table)
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



def hashtag_extract(i):
    hashtags =[]
    for x in i :
        temp = ([re.sub(r"(\W+)$", "", j) for j in set([i for i in x.split() if i.startswith("#")])])
        hashtags.append(temp)
    return hashtags

def hashtags():

    CONSUMER_KEY = "A0Ro0FdsNrVhnaf5HJ3lkB3yU"
    CONSUMER_SECRET = "MTBGPJ7urGnrwzJYRjNNyQCDskTFgbBXS83m9Z7tTOMRCTStuC"

    auth = AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    api=tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True,retry_count=3,timeout=30)

    search_word="lockdown OR corona OR COVID OR LOCKDOWN OR quarantine OR WHO OR stayhome OR StayHome OR socialdistancing OR pandemic OR virus OR selfisolation"
    date="2020-03-23"       #Tweets will be from this date
    tweets=tweepy.Cursor(api.search,q=search_word,since=date,tweet_mode='extended',result='mixed').items(700)

    df=pd.DataFrame([tweet._json['retweeted_status']['full_text'] if 'retweeted_status' in tweet._json else tweet.full_text for tweet in tweets],columns=["Tweets"])

    loaded_model = pickle.load(open('finalized_model123.sav','rb'))


    df['clean_tweets'] = df['Tweets']

    df['clean_tweets'] = df['clean_tweets'].apply(cleanTxt)
    df['clean_tweets'] = df['clean_tweets'].apply(stop_words)

    result=loaded_model.predict(df['clean_tweets'])
#print(result)

    list_conv=result.tolist()

    df['labels'] = pd.DataFrame(result)
#df.head()

    HT_positive = hashtag_extract(df['Tweets'][df['labels'] == 4])

# extracting hashtags from racist/sexist tweets
    HT_negative = hashtag_extract(df['Tweets'][df['labels'] == 0])

# unnesting list
    HT_positive = sum(HT_positive,[])
    HT_negative = sum(HT_negative,[])

    a_pos = nltk.FreqDist(HT_positive)
    df_pos = pd.DataFrame({'Hashtag': list(a_pos.keys()), 'Count': list(a_pos.values())})

# selecting top 20 most frequent hashtags     
    df_pos = df_pos.nlargest(columns="Count", n = 10)

    a_neg = nltk.FreqDist(HT_negative)
    df_neg = pd.DataFrame({'Hashtag': list(a_neg.keys()), 'Count': list(a_neg.values())})

# selecting top 20 most frequent hashtags     
    df_neg = df_neg.nlargest(columns="Count", n = 10)

    pos_hash=df_pos.Hashtag
    neg_hash=df_neg.Hashtag

    return pos_hash,neg_hash