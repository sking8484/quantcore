from django.shortcuts import render
import pandas as pd
import pandas_datareader as web
from datetime import datetime
import quandl
from . import plots, tables
import numpy as np
import datetime
from iexfinance.stocks import get_historical_data

# Create your views here.





    #     return render(request, 'data/just_data.html', {'data':data.to_html()})
    # return render(request, 'data/just_data.html')
def get_stock_data(data_type, ticker, start, end):
    api_key = 'J84FuQJ6AzbBM8hWHviv'
    stock_columns = ['Adj. Open', 'Adj. High', 'Adj. Low', 'AdjClose', 'Adj. Volume']
    if data_type == 'stock_data':
        # try:
        import datetime
        years = 5
        days_per_year = 365.30
        five_years_earlier = datetime.datetime.now() - datetime.timedelta(days=(years*days_per_year))

        if start > five_years_earlier:
            stock_data = get_historical_data(ticker,start = '2018-01-01', end = '2019-01-01',token ='sk_6d1c2037a984473895a42a17710cf794', output_format = 'pandas')
            stock_data = pd.DataFrame(stock_data['close'])
            #stock_data.rename(columns = {'close':stock}, inplace = True)
            #dataframe = pd.concat([dataframe, stock_data], axis = 1)

        else:
            stock_data = web.DataReader(str(ticker), 'quandl',five_years_earlier, end)
            stock_data.rename(columns = {'Close':'AdjClose'}, inplace = True)
            stock_data.index = pd.to_datetime(stock_data.index)


            return stock_data
        # except Exception as e:
        #
        #
        #     stock_data = quandl.get('WIKI/' + str(ticker), start_date=start,end_date= end, api_key = api_key)
        #     stock_data = stock_data[stock_columns]
        #     return stock_data






    elif data_type == 'real_estate':

        real_estate = quandl.get(ticker, start_date=start, end_date=end, api_key = api_key)
        real_estate.index = pd.to_datetime(real_estate.index)
        return real_estate
    elif data_type == 'economic':
        economic_data = quandl.get(ticker, start_date = start, end_date=end, api_key = api_key)
        economic_data.index = pd.to_datetime(economic_data.index)
        economic_data = economic_data.iloc[:,[0]]

        return economic_data






def get_the_data(request):
    if request.method == 'POST':
        data_type = request.POST['datatype']
        ticker = request.POST['ticker'].upper()
        start = pd.to_datetime(request.POST['start'])
        end = pd.to_datetime(request.POST['end'])
        try:
            if data_type == 'stock_data' or data_type == 'stock_data/candlestick':
                data = get_stock_data('stock_data', ticker, start, end)
                first_column = pd.DataFrame(data['AdjClose'])
                print(data)

            elif data_type == 'real_estate':
                data = get_stock_data(data_type,ticker,start,end)
                first_column = pd.DataFrame(data.iloc[:,0])
            elif data_type == 'economic':
                data=get_stock_data(data_type, ticker, start, end)
                first_column = pd.DataFrame(data.iloc[:,0])

        except Exception as e:
            error_message = e
            error = 'One or more of your inputs was not accepted: '
            return render(request,'data/get_the_data.html', {'error':error, 'error_message':error_message})
        data.sort_index(ascending = False, inplace = True)
        if data_type == 'stock_data/candlestick':
            plotly = plots.candle_stick_plot(data, ticker)
        else:
            plotly = plots.stock_plot(data, ticker)
        data_plotly = tables.make_stock_table(data, ticker)

        return render(request, 'data/mean.html', {'data_html':data_plotly,'ticker':ticker,
        'plotly':plotly})
    return render(request, 'data/get_the_data.html')
