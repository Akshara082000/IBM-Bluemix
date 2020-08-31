#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
#from matplotlib import style
import time
#from backend import *
import sqlite3
import pandas as pd
import dash
from dash.dependencies import Output,Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import numpy as np
import os
import datetime

conn = sqlite3.connect('twitter.db')
c = conn.cursor()


#df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE '%olympic%' ORDER BY unix DESC LIMIT 1000",conn)
#df.sort_values('unix', inplace = True)
#df['smoothened_sentiment'] = df['sentiment']
#df.dropna(inplace = True)



app = dash.Dash(__name__)
app.layout = html.Div([
     html.Div([   html.H2('Live Twitter Sentiment'),
        dcc.Graph(id='graph5',animate = False),
        
        dcc.Interval(
            id='update',
            interval = int(500) ,
            n_intervals = 0
        )]),
    ]
)

@app.callback(Output('graph5', 'figure'),
              [Input('update', 'n_intervals')])
def update_graph_scatter(n):
    try:
        conn = sqlite3.connect('twitter.db')
        c = conn.cursor()
        df = pd.read_sql("SELECT tweet,created_at,sentiment FROM sentiment", conn)
        time = datetime.datetime.now().strftime('%D, %H:%M:%S')
        #df.sort_values('created_at', inplace=True)
        #df.set_index('created_at',inplace = True)
        #print(df.head())
        df.dropna(inplace=True)
        #df.resample('10s').mean()

        X = df.created_at.values[-100:]
        Y = df.sentiment.values[-100:]
    

        data = go.Scatter(
                x=X,
                y=Y,
                
                name='Scatter',
                mode= 'lines+markers'
                )
        layout = go.Layout(
             xaxis={
                'automargin': False,
                'range': [min(X),max(X)],
                'title': 'Current Time (GMT)',
                'nticks': 6
            },
            yaxis={
                'automargin': False,     
                'title': 'sentiment value',
                'range': [-2 , 2]
            },
        )

        return {'data': [data],'layout' : layout}

    except Exception as e:
        with open('errors.txt','a') as f:
            f.write(str(e))
            f.write('\n')

if __name__ == '__main__':
    app.run_server()

