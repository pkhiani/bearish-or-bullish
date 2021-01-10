from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from bs4 import BeautifulSoup
import requests

from csv import writer
#


def basic(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        # symbol = input("Enter a symbol you want to find the news for: ")
        if len(name) >= 1:
            url = 'https://finviz.com/quote.ashx?t='

            res = requests.get(url + name, headers={'User-Agent': 'Mozilla/5.0'})

            soup = BeautifulSoup(res.text, "html.parser")

            articles = soup.find_all("table", {"class": "fullview-news-outer"})

            for newsElement in articles:
                rows = newsElement.find_all('tr')
                # print(rows)
                lst = []

                for row in rows:

                    article_name = row.find("div", {"class": "news-link-left"}).get_text().strip()


                    content = article_name + " " 

                    lst.append('<br/>' + str(content) + '<br/>')
                    

                return HttpResponse(lst)
        else:
            return HttpResponse("please enter valid symbol")
    return render(request, 'basic.html')





