from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt

import requests

fin_url = 'https://finviz.com/quote.ashx?t='
parsed_data = []

def basic(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        
        if len(name) >= 1:
            
            tickers = [name]

            news_tables = {}

            for ticker in tickers:
                url = fin_url + ticker

                req = Request(url=url, headers={'user-agent': 'my-app'})
                response = urlopen(req)

                html = BeautifulSoup(response, features='html.parser')
                news_table = html.find(id='news-table')
                news_tables[ticker] = news_table


            for ticker, news_table in news_tables.items():

                for row in news_table.findAll('tr'):

                    title = row.a.text
                    date_data = row.td.text.split(' ')

                    if len(date_data) == 1:
                        time = date_data[0]
                    else:
                        date = date_data[0]
                        time = date_data[1]

                    parsed_data.append([ticker, date, time, title])
                    

            df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])

            vader = SentimentIntensityAnalyzer()

            f = lambda title: vader.polarity_scores(title)['compound']
            df['compound'] = df['title'].apply(f)
            df['date'] = pd.to_datetime(df.date).dt.date

            plt.figure(figsize=(8,8))
            mean_df = df.groupby(['ticker', 'date']).mean().unstack()
            mean_df = mean_df.xs('compound', axis="columns")
            mean_df.plot(kind='bar')
            plt.savefig('graph.png')
            #plt.show()

            image_data = open("graph.png", "rb").read()
            return HttpResponse(image_data, content_type="image/png")
            
         
        else:
            return HttpResponse("please enter valid symbol")
    return render(request, 'basic.html')




