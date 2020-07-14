from flask import Flask,render_template,url_for,request,send_file,Response
import tweet_ml 




app = Flask(__name__)


@app.route('/',methods=['POST','GET'])

def index():
     return render_template('index.html')

@app.route('/map',methods=['POST','GET'])



def map():
     
      if request.method == "POST": 
          ##fetches lang and lat from map via POST
          longitude=request.form['lang']
          latitude=request.form['lat'] 
         
          No_of_tweets,Positive_tweets,Negative_tweets,Popular_words,Word_frequency=tweet_ml.ML(latitude,longitude)##calling tweet_ml.ML()function to predict and return data
          
            ## Calculating percentage of positive and negative tweets
          try :
            
               positive_tweet_percent=100*len(Positive_tweets)/No_of_tweets ##positive percentage
               Negative_tweet_percent=100*len(Negative_tweets)/No_of_tweets ##negative percentage
    
          except:

               return  render_template('display.html',lang=longitude,lat=latitude,ERROR_MSG="No results found for this Location")
    
          
          dict_of_words={} ##converting from list to dictionary to read it as JSON in javascript for data visulaization
          dict_of_frequency={}  ##converting from list to dictionary to read it as JSON in javascript for data visulaization
      
          for i in  range(0,len(Popular_words)):
              dict_of_words[i]=Popular_words[i]
          for j in  range(0,len(Word_frequency)):
              dict_of_frequency[j]=Word_frequency[j]
          data={'Positive':positive_tweet_percent,'Negative':Negative_tweet_percent,'Tweets':No_of_tweets}
          return render_template('display.html',lang=longitude,lat=latitude,data=data,postweetslen=len(Positive_tweets),negtweetslen=len(Negative_tweets),words=dict_of_words,freq=dict_of_frequency,ERROR_MSG="Found")
      else:
          return render_template('map.html')




if __name__== "__main__":
    app.run(debug=True)
