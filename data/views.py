from django.shortcuts import render
import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
from datetime import datetime
import quandl
from . import plots, tables
import numpy as np

# Create your views here.





    #     return render(request, 'data/just_data.html', {'data':data.to_html()})
    # return render(request, 'data/just_data.html')
def get_stock_data(data_type, ticker, start, end):
    api_key = 'J84FuQJ6AzbBM8hWHviv'
    stock_columns = ['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']
    if data_type == 'stock_data':
        stock_data = quandl.get('WIKI/' + str(ticker), start_date=start,end_date= end, api_key = api_key)
        stock_data = stock_data[stock_columns]
        return stock_data
    elif data_type == 'real_estate':

        real_estate = quandl.get(ticker, start_date=start, end_date=end, api_key = api_key)
        return real_estate






def get_the_data(request):
    if request.method == 'POST':
        data_type = request.POST['datatype']
        try:
            if data_type == 'stock_data':

                ticker = request.POST['ticker'].upper()
                start = datetime.strptime(request.POST['start'][:10],'%Y-%m-%d')
                end = datetime.strptime(request.POST['end'][:10],'%Y-%m-%d')
                data = get_stock_data(data_type, ticker, start, end).round(4)

                plotly = plots.stock_plot(data, ticker)

                data.sort_index(ascending = False, inplace = True)
                data['pct_change'] = (data['Adj. Close'].pct_change().round(4))
                short_data = data[:50]

                data_plotly = tables.make_stock_table(data, ticker)


                return render(request, 'data/mean.html', {'mean':data.mean(),'data_html':data_plotly,'ticker':ticker,
                'plotly':plotly})


            elif data_type == 'real_estate':


                    ticker = request.POST['ticker'].upper()
                    start = datetime.strptime(request.POST['start'][:10],'%Y-%m-%d')
                    end = datetime.strptime(request.POST['end'][:10],'%Y-%m-%d')
                    data = get_stock_data(data_type,ticker,start,end)
                    plotly = plots.real_estate_plot(data, ticker)


        except:
            help = ('Make sure you have entered everything in correctly. Please Go to https://www.quandl.com/data/ZILLOW-Zillow-Real-Estate-Research' +
            ' and type in your area if you are unsure how to find the correct real estate code. Copy and paste the key into ticker.')
            return render(request,'data/get_the_data.html', {'help':help})

        return render(request, 'data/mean.html', {'mean':data.mean(),'data_html':data.to_html(),'ticker':ticker,
                        'plotly':plotly})
    return render(request, 'data/get_the_data.html')
