from django.shortcuts import render
from django.shortcuts import render
import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
from datetime import datetime
import quandl
from . import plots, tables
import numpy as np
from data import views as data_views




def find_correlation(request):
    if request.method == 'POST':
        datatype_1 = request.POST['datatype1']
        datatype_2 = request.POST['datatype2']
        datatype_3 = request.POST['datatype3']
        datatype_4 = request.POST['datatype4']
        ticker1 = request.POST['symbol1'].upper()
        ticker2 = request.POST['symbol2'].upper()
        ticker3 = request.POST['symbol3'].upper()
        ticker4 = request.POST['symbol4'].upper()

        start = datetime.strptime(request.POST['start'][:10],'%Y-%m-%d')
        end = datetime.strptime(request.POST['end'][:10],'%Y-%m-%d')
        try:
            if datatype_1 == 'stock_data':
                corr_data_1 = data_views.get_stock_data(datatype_1, ticker1, start, end)
                corr_data_1 = corr_data_1['Adj. Close']
                corr_data_1.rename(ticker1, inplace = True)

            if datatype_1=='real_estate':
                corr_data_1 = data_views.get_stock_data(datatype_1,ticker1,start,end)
                corr_data_1.columns = ([ticker1])
            if datatype_1 =='economic':
                corr_data_1 = data_views.get_stock_data(datatype_1, ticker1, start, end)
                corr_data_1 = corr_data_1.iloc[:, 0]
                corr_data_1.rename(ticker1, inplace = True)

            if datatype_2 == 'stock_data':
                corr_data_2 = data_views.get_stock_data(datatype_2, ticker2, start, end)
                corr_data_2 = corr_data_2['Adj. Close']
                corr_data_2.rename(ticker2, inplace = True)

            if datatype_2 == 'real_estate':
                corr_data_2 = data_views.get_stock_data(datatype_2,ticker2,start,end)
                corr_data_2.columns = ([ticker2])

            if datatype_2 =='economic':
                corr_data_2 = data_views.get_stock_data(datatype_2, ticker2, start, end)
                corr_data_2 = corr_data_2.iloc[:, 0]
                corr_data_2.rename(ticker2, inplace = True)

            if datatype_3 == 'stock_data':

                corr_data_3 = data_views.get_stock_data(datatype_3, ticker3, start, end)
                corr_data_3 = corr_data_3['Adj. Close']
                corr_data_3.rename(ticker3, inplace = True)

            if datatype_3 == 'real_estate':

                corr_data_3 = data_views.get_stock_data(datatype_3,ticker3,start,end)
                corr_data_3.rename(columns = {'Adj. Close':ticker}, inplace = True)
            if datatype_3 =='economic':
                corr_data_3 = data_views.get_stock_data(datatype_3, ticker3, start, end)
                corr_data_3 = corr_data_3.iloc[:, 0]
                corr_data_3.rename(ticker3, inplace = True)

            if datatype_4 == 'stock_data':


                corr_data_4 = data_views.get_stock_data(datatype_4, ticker4, start, end)
                corr_data_4 = corr_data_4['Adj. Close']
                corr_data_4.rename(ticker4, inplace = True)

            if datatype_4 == 'real_estate':

                corr_data_4 = data_views.get_stock_data(datatype_4,ticker4,start,end)
                corr_data_4.rename(columns = {'Adj. Close':ticker4}, inplace = True)
            if datatype_4 =='economic':
                corr_data_4 = data_views.get_stock_data(datatype_4, ticker4, start, end)
                corr_data_4 = corr_data_4.iloc[:, 0]
                corr_data_4.rename(ticker4, inplace = True)





            if datatype_3 != 'none' and datatype_4 != 'none':
                corr_data_df = pd.concat([corr_data_1, corr_data_2, corr_data_3, corr_data_4], axis = 1)

            if datatype_3 != 'none' and datatype_4 == 'none':
                corr_data_df = pd.concat([corr_data_1, corr_data_2, corr_data_3], axis = 1)

            if datatype_3 == 'none' and datatype_4 == 'none':
                corr_data_df = pd.concat([corr_data_1, corr_data_2], axis = 1)


            corr_data_df.dropna(inplace = True)
            corr_df = corr_data_df.corr()
            corr_df.dropna(inplace = True)

            heatmap = plots.correlation_heatmap(corr_df)
            plot = plots.correlation_plot(corr_data_df)
            table = tables.make_corr_table(corr_data_df)
        except Exception as e:
            print(e)
            error = 'Please make sure you enter a valid date and symbol'
            return render(request, 'find_correlation/correlation_template.html', {'error':error})




        return render(request, 'find_correlation/correlation_charts.html', {
                                                                            'heatmap':heatmap,
                                                                            'plot':plot,
                                                                            'table':table,
                                                                            },
                                                                        )
    return render(request, 'find_correlation/correlation_template.html')
