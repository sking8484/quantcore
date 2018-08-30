from django.shortcuts import render
import pandas as pd
import pandas_datareader as web
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
    elif data_type == 'economic':
        economic_data = quandl.get(ticker, start_date = start, end_date=end, api_key = api_key)

        return economic_data






def get_the_data(request):
    if request.method == 'POST':
        data_type = request.POST['datatype']
        ticker = request.POST['ticker'].upper()
        start = datetime.strptime(request.POST['start'],'%Y-%m-%d')
        end = datetime.strptime(request.POST['end'],'%Y-%m-%d')
        try:
            if data_type == 'stock_data':
                data = get_stock_data(data_type, ticker, start, end).round(4)
                first_column = pd.DataFrame(data['Adj. Close'])

            elif data_type == 'real_estate':
                data = get_stock_data(data_type,ticker,start,end)
                first_column = pd.DataFrame(data.iloc[:,0])
            elif data_type == 'economic':
                data=get_stock_data(data_type, ticker, start, end)
                first_column = pd.DataFrame(data.iloc[:,0])

        except:
            help = (
            ' If you are NOT using chrome, please enter your dates as follows: YYYY-MM-DD.\n Please Go to https://www.quandl.com/data/ZILLOW-Zillow-Real-Estate-Research' +
            'and type in your area if you are unsure how to find the correct real estate code. Copy and paste the key into ticker.')
            return render(request,'data/get_the_data.html', {'help':help})
        data.sort_index(ascending = False, inplace = True)
        plotly = plots.stock_plot(data, ticker)
        data_plotly = tables.make_stock_table(data, ticker)

        return render(request, 'data/mean.html', {'data_html':data_plotly,'ticker':ticker,
        'plotly':plotly})
    return render(request, 'data/get_the_data.html')
